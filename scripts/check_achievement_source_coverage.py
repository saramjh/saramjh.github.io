#!/usr/bin/env python3
"""Read-only source-URL coverage audit before drafting an achievement article.

An exact source match is a review flag: a link in an existing article can be
background rather than the main subject. No result grants publication rights.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import re
import sys
from pathlib import Path
from urllib.parse import parse_qsl, urlencode, urlsplit, urlunsplit

ROOT = Path(__file__).resolve().parents[1]
URL_RE = re.compile(r"https?://[^\s<>\]\\)\"']+", re.IGNORECASE)
FENCE_RE = re.compile(r"^\s*(`{3,}|~{3,})")
INLINE_CODE_RE = re.compile(r"`+[^`\n]*`+")
META_RE = re.compile(r"^([A-Za-z_][\w-]*):\s*(.*?)\s*$")
TRACKING = {"fbclid", "gclid", "mc_cid", "mc_eid", "igshid"}


def normalize_url(raw: str) -> str:
    raw = raw.strip().rstrip(".,;!?:")
    try:
        parsed = urlsplit(raw)
        if parsed.scheme.lower() not in {"https", "http"} or not parsed.hostname:
            raise ValueError("invalid scheme or host")
        if parsed.username or parsed.password:
            raise ValueError("credentials are not source identity")
        host = parsed.hostname.lower()
        if host.startswith("www."):
            host = host[4:]
        port = parsed.port
        if port and not ((parsed.scheme.lower() == "https" and port == 443) or
                         (parsed.scheme.lower() == "http" and port == 80)):
            host += f":{port}"
        query = urlencode(sorted(
            (key, value) for key, value in parse_qsl(parsed.query, keep_blank_values=True)
            if not key.lower().startswith("utm_") and key.lower() not in TRACKING
        ))
        path = parsed.path.rstrip("/") or "/"
        return urlunsplit(("https", host, path, query, ""))
    except (ValueError, AttributeError) as exc:
        raise ValueError(f"INVALID_SOURCE_URL: {exc}") from exc


def parse_post(raw: str) -> tuple[dict, str]:
    metadata = {}
    lines = raw.splitlines()
    start = 0
    if lines and lines[0].strip() == "---":
        try:
            end = next(i for i, line in enumerate(lines[1:], 1) if line.strip() == "---")
        except StopIteration:
            raise ValueError("UNTERMINATED_FRONTMATTER")
        for line in lines[1:end]:
            match = META_RE.match(line)
            if match:
                key, value = match.groups()
                metadata[key] = value.strip("\"'")
        start = end + 1
    return metadata, "\n".join(lines[start:])


def readable_prose(body: str) -> str:
    result = []
    inside = False
    active = ""
    for line in body.splitlines():
        match = FENCE_RE.match(line)
        if match:
            delimiter = match.group(1)
            if not inside:
                inside = True
                active = delimiter[0]
            elif delimiter[0] == active:
                inside = False
            continue
        if not inside:
            result.append(INLINE_CODE_RE.sub("", line))
    return "\n".join(result)


def find_links(text: str) -> set[str]:
    links = set()
    for match in URL_RE.finditer(text):
        url = match.group(0).rstrip(".,;!?:")
        try:
            links.add(normalize_url(url))
        except ValueError:
            continue
    return links


def scan(posts: Path, source_urls: list[str]) -> tuple[int, dict]:
    sources = []
    try:
        for value in source_urls:
            sources.append({"sourceUrl": value, "normalized": normalize_url(value), "matches": []})
    except ValueError:
        return 2, {"status": "INVALID_SOURCE_URL", "publicationAuthorized": False}

    if not posts.is_dir():
        return 2, {"status": "NO_POSTS_TO_REVIEW", "publicationAuthorized": False}

    count = 0
    for file in sorted(posts.rglob("*.md")):
        if file.is_symlink():
            continue
        try:
            raw_bytes = file.read_bytes()
            raw = raw_bytes.decode("utf-8", errors="strict")
            meta, body = parse_post(raw)
        except (UnicodeDecodeError, OSError, ValueError):
            return 2, {"status": "SOURCE_POST_READ_ERROR", "publicationAuthorized": False}
        count += 1
        links = find_links(readable_prose(body))
        for source in sources:
            if source["normalized"] not in links:
                continue
            source["matches"].append({
                "postPath": "_posts/" + file.relative_to(posts).as_posix(),
                "permalink": meta.get("permalink") or None,
                "lang": meta.get("lang") or None,
                "published": meta.get("published", "true").lower() != "false",
                "sha256": hashlib.sha256(raw_bytes).hexdigest(),
            })
    if count == 0:
        return 2, {"status": "NO_POSTS_TO_REVIEW", "publicationAuthorized": False}

    covered = any(source["matches"] for source in sources)
    return (3 if covered else 0), {
        "schema": "DEV_BLOG_SOURCE_COVERAGE_PRECREATE_V1",
        "status": "ALREADY_COVERED_REVIEW_REQUIRED" if covered else "NOT_IN_SCANNED_POSTS_UNVERIFIED",
        "scannedPosts": count,
        "sources": sources,
        "publicationAuthorized": False,
        "requiresSourceAndEditorialReview": True,
        "nativeProviderWrites": 0,
        "note": "A link match may be background context; review before creating a new story. "
                "No match does not prove originality, permission or delivery.",
    }


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--source-url", action="append", required=True,
                        help="Exact original external achievement URL; repeat for multiple sources.")
    parser.add_argument("--posts-root", type=Path, default=ROOT / "_posts",
                        help="Read-only existing local blog _posts root.")
    args = parser.parse_args(argv)
    code, report = scan(args.posts_root, args.source_url)
    print(json.dumps(report, ensure_ascii=False, sort_keys=True, indent=2))
    return code


if __name__ == "__main__":
    sys.exit(main())

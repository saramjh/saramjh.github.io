#!/usr/bin/env python3
import json
import os
import re
import sys
import subprocess
import urllib.request
import urllib.error

BING_API_KEY = os.environ.get("BING_API_KEY", "").strip()
INDEXNOW_KEY = "6c9119e1be3a49e2851073f16d11fee7"  # Public verification key; served at /<key>.txt.
HOST = "saramjh.github.io"
BASE_URL = f"https://{HOST}"

def get_urls():
    sitemap_path = os.path.join(os.path.dirname(__file__), "..", "_site", "sitemap.xml")
    urls = []
    if os.path.exists(sitemap_path):
        with open(sitemap_path, "r", encoding="utf-8") as f:
            content = f.read()
        urls = re.findall(r"<loc>(https://[^<]+)</loc>", content)
    else:
        try:
            req = urllib.request.Request(f"{BASE_URL}/sitemap.xml", headers={"User-Agent": "Mozilla/5.0"})
            with urllib.request.urlopen(req, timeout=10) as res:
                content = res.read().decode("utf-8")
                urls = re.findall(r"<loc>(https://[^<]+)</loc>", content)
        except Exception as e:
            print(f"[URLs] Warning: Failed to fetch live sitemap: {e}")
    
    if not urls:
        print("[URLs] No verifiable sitemap; skipping unsupported fallback URLs.")
        return []
    # Unique and remove anchors or unwanted assets
    cleaned = []
    seen = set()
    for u in urls:
        u = u.strip()
        if u not in seen and not u.endswith((".png", ".jpg", ".jpeg", ".css", ".js", ".txt")):
            seen.add(u)
            cleaned.append(u)
    return cleaned

def _permalink_from_source(path, revision):
    """Resolve a Jekyll page permalink from an exact current or prior source blob."""
    if path == "index.md":
        return f"{BASE_URL}/"
    content = subprocess.check_output(
        ["git", "show", f"{revision}:{path}"], text=True,
        stderr=subprocess.PIPE,
    )
    match = re.match(r"\A---\s*\n(.*?)\n---", content, re.S)
    if match is None:
        return None
    permalink = re.search(
        r"(?m)^permalink:\s*['\"]?(/[^'\"\s]+)", match.group(1)
    )
    if permalink is None:
        return None
    return f"{BASE_URL}{permalink.group(1)}"


def _skip_only_source(path):
    """Changes to these files do not update the served blog content."""
    return path.startswith((".github/", "scripts/", "tests/", ".context/", ".serena/")) or path in {
        "AGENTS.md", "CLAUDE.md", "README.md",
        ".gitignore", ".nojekyll",
    }


def changed_urls(before, after):
    """Return affected URLs, or None for a broad site change.

    An invalid commit comparison raises an exception and must never authorize
    a fallback full-site provider request.
    """
    if not all(re.fullmatch(r"[0-9a-f]{40}", x or "") for x in (before, after)):
        raise ValueError("Missing or invalid deploy before/after commit SHA")
    rows = subprocess.check_output(
        ["git", "diff", "--name-status", "--no-renames", before, after],
        text=True, stderr=subprocess.PIPE,
    )
    touched = set()
    for line in rows.splitlines():
        status, sep, file_path = line.partition("\t")
        if not sep or status not in ("M", "A", "D", "T"):
            raise ValueError("Unrecognized git diff record; no provider write")
        if _skip_only_source(file_path):
            continue
        # Any change to a shared template, global data, style or asset can
        # affect more than one generated page. Preserve complete coverage.
        if file_path.startswith(("_data/", "_includes/", "_layouts/", "_sass/", "assets/", "css/")) or file_path in ("_config.yml",):
            return None
        try:
            if file_path == "index.md" or file_path.endswith((".md", ".markdown", ".html")):
                if status != "A":
                    old = _permalink_from_source(file_path, before)
                    if old is None:
                        return None
                    touched.add(old)
                if status != "D":
                    current = _permalink_from_source(file_path, after)
                    if current is None:
                        return None
                    touched.add(current)
                if file_path.startswith("_posts/"):
                    touched.add(f"{BASE_URL}/")  # Recent Posts are on the home page.
            else:
                return None
        except (OSError, subprocess.CalledProcessError, UnicodeError):
            raise ValueError("Cannot resolve an exact changed page URL") from None
    return sorted(touched)


def get_deploy_urls():
    """Fail closed if the release's previous and current commit cannot be proven."""
    before = os.environ.get("INDEXNOW_BEFORE_SHA", "").strip().lower()
    after = os.environ.get("INDEXNOW_AFTER_SHA", "").strip().lower()
    try:
        selected = changed_urls(before, after)
    except (ValueError, subprocess.CalledProcessError) as exc:
        print(f"[URLs] Skipping notification: unverified release diff: {exc}")
        return []
    if selected is None:
        full = get_urls()
        print(f"[URLs] Shared layout/data/assets changed: {len(full)} sitemap URLs")
        return full
    print(f"[URLs] Changed page URLs: {len(selected)}")
    return selected


def submit_bing_api(urls):
    if not BING_API_KEY:
        print("[Bing API] No BING_API_KEY configured. Skipping.")
        return
    api_url = f"https://ssl.bing.com/webmaster/api.svc/json/SubmitUrlbatch?apikey={BING_API_KEY}"
    # Bing allows max 500 URLs per batch
    batch = urls[:100]
    payload = {
        "siteUrl": BASE_URL,
        "urlList": batch
    }
    data = json.dumps(payload).encode("utf-8")
    req = urllib.request.Request(api_url, data=data, headers={"Content-Type": "application/json; charset=utf-8"})
    try:
        with urllib.request.urlopen(req, timeout=15) as res:
            res_body = res.read().decode("utf-8")
            print(f"[Bing API] Submitted {len(batch)} URLs successfully: {res_body}")
    except urllib.error.HTTPError as e:
        print(f"[Bing API] HTTP Error {e.code}: {e.read().decode('utf-8')}")
    except Exception as e:
        print(f"[Bing API] Error: {e}")

def submit_indexnow(urls):
    """Send each sitemap URL once per batch through IndexNow's global endpoint.

    IndexNow permits up to 10,000 URLs in one POST. The old 100-URL cap
    silently omitted pages once the site grew beyond that limit.
    """
    if not urls:
        print("[IndexNow] No URLs to submit.")
        return

    endpoint = "https://api.indexnow.org/indexnow"
    batch_size = 10000
    total_batches = (len(urls) + batch_size - 1) // batch_size
    for offset in range(0, len(urls), batch_size):
        batch = urls[offset:offset + batch_size]
        batch_number = offset // batch_size + 1
        payload = {
            "host": HOST,
            "key": INDEXNOW_KEY,
            "keyLocation": f"{BASE_URL}/{INDEXNOW_KEY}.txt",
            "urlList": batch,
        }
        req = urllib.request.Request(
            endpoint,
            data=json.dumps(payload).encode("utf-8"),
            headers={"Content-Type": "application/json; charset=utf-8"},
        )
        label = f"[IndexNow] Batch {batch_number}/{total_batches} ({len(batch)} URLs)"
        try:
            with urllib.request.urlopen(req, timeout=15) as res:
                print(f"{label} Response {res.status}: Accepted")
        except urllib.error.HTTPError as e:
            print(f"{label} HTTP Error {e.code}: {e.read().decode('utf-8')}")
        except Exception as e:
            # Do not retry a request with an uncertain provider outcome.
            print(f"{label} Error: {e}")

if __name__ == "__main__":
    url_list = get_deploy_urls()
    if not url_list:
        print("[URLs] No qualified changed URLs; skipping Bing and IndexNow.")
        sys.exit(0)
    print(f"Total qualified URLs: {len(url_list)}")
    submit_bing_api(url_list)
    submit_indexnow(url_list)

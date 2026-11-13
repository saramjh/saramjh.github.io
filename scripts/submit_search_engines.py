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
    if permalink is None and path.startswith("_projects/"):
        # Jekyll collection projects use /portfolio/:name/ without a per-file
        # permalink. Resolve only the verified existing project source shape.
        project = re.fullmatch(r"_projects/([a-z0-9][a-z0-9-]*)\.(?:md|html)", path)
        if project is None:
            return None
        front = match.group(1)
        if not re.search(r"(?m)^layout: project\s*$", front):
            return None
        slug = re.search(r"(?m)^slug:\s*([a-z0-9-]+)\s*$", front)
        if slug is None or slug.group(1) != project.group(1):
            return None
        config = subprocess.check_output(
            ["git", "show", f"{revision}:_config.yml"],
            text=True, stderr=subprocess.PIPE,
        )
        if not re.search(
            r"(?m)^  projects:\n    output: true\n    permalink: /portfolio/:name/$",
            config,
        ):
            return None
        return f"{BASE_URL}/portfolio/{project.group(1)}/"
    if permalink is None:
        return None
    return f"{BASE_URL}{permalink.group(1)}"


def _skip_only_source(path):
    """Changes to these files do not update the served blog content."""
    return path.startswith((".github/", "scripts/", "tests/", ".context/", ".serena/")) or path in {
        "AGENTS.md", "CLAUDE.md", "README.md",
        ".gitignore", ".nojekyll",
    }



def _page_urls_for_asset(path, revision):
    """Resolve first-party site and post-local images to exact source pages.

    Shared/unknown references stay conservative. Jekyll publishes an image
    under _posts/<slug>/ at /<slug>/, without the _posts segment.
    """
    if not path.lower().endswith(
        (".png", ".jpg", ".jpeg", ".webp", ".gif", ".svg")
    ):
        return None
    if path.startswith("assets/"):
        public_asset_path = f"/{path}"
    elif path.startswith("_posts/") and path.count("/") >= 2:
        public_asset_path = f"/{path[len('_posts/'):]}"
    else:
        return None

    # Match the actual public image URL used in Markdown/HTML.
    # git grep -I skips binary blobs; a missing match is not proof of
    # non-use because a layout could construct the path dynamically.
    proc = subprocess.run(
        ["git", "grep", "-I", "-l", "-F", "-e", public_asset_path,
         revision, "--"],
        text=True, capture_output=True,
    )
    if proc.returncode not in (0, 1):
        raise ValueError("Cannot inspect image references for changed page URL")
    pages = set()
    for line in proc.stdout.splitlines():
        prefix, separator, source = line.partition(":")
        if not separator or prefix != revision or not source:
            raise ValueError("Unrecognized image reference record")
        if _skip_only_source(source):
            continue
        if not source.endswith((".md", ".markdown", ".html")):
            return None
        try:
            page = _permalink_from_source(source, revision)
        except (OSError, subprocess.CalledProcessError, UnicodeError):
            raise ValueError("Cannot resolve image reference page") from None
        if page is None:
            return None
        pages.add(page)
        if source.startswith("_posts/"):
            pages.add(f"{BASE_URL}/")  # Conservative home-preview coverage.
    return pages or None


def _page_urls_for_recognitions(revision):
    """Map the source-linked evidence ledger to its real page consumers.

    The two direct pages, project collection and milestone layout are checked
    against the committed dependency graph. Unknown new consumers use the
    existing broad fallback, never a guessed subset.
    """
    def tracked(needle, regex=False):
        proc = subprocess.run(
            ["git", "grep", "-I", "-l", "-E" if regex else "-F", "-e", needle,
             revision, "--"], text=True, capture_output=True,
        )
        if proc.returncode not in (0, 1):
            raise ValueError("Cannot inspect recognition dependencies")
        found = set()
        for line in proc.stdout.splitlines():
            prefix, sep, source = line.partition(":")
            if not sep or prefix != revision or not source:
                raise ValueError("Unrecognized recognition reference")
            if not _skip_only_source(source):
                found.add(source)
        return found

    data_users = {"_includes/portfolio-evidence.html", "_layouts/project.html"}
    include_users = {"_layouts/project.html", "_layouts/milestone.html",
                     "portfolio/index.html", "portfolio/recognition/index.html"}
    actual_data_users = tracked("site.data.recognitions")
    schema_source = "_includes/seo_schema.html"
    if actual_data_users == data_users:
        pass
    elif actual_data_users == data_users | {schema_source}:
        # The original project WebApplication schema uses recognition listings
        # only for project pages already represented in project_sources below.
        # Any additional recognition consumer or altered guard fails closed.
        try:
            schema = subprocess.check_output(
                ["git", "show", f"{revision}:{schema_source}"],
                text=True, stderr=subprocess.PIPE,
            )
        except subprocess.CalledProcessError:
            return None
        guard = "{%- if page.layout == 'project' and page.site_url and page.slug -%}"
        selector = ("{%- assign verified_listings = site.data.recognitions"
                    " | where: 'project', page.slug | where: 'type', 'listing'"
                    " | where: 'status', 'confirmed' -%}")
        next_branch = "{%- elsif page.date -%}"
        if (schema.count("site.data.recognitions") != 1
                or schema.count(guard) != 1
                or schema.count(selector) != 1
                or schema.count(next_branch) != 1
                or not schema.index(guard) < schema.index(selector) < schema.index(next_branch)):
            return None
    else:
        return None
    if tracked("portfolio-evidence.html") != include_users:
        return None

    config = subprocess.check_output(
        ["git", "show", f"{revision}:_config.yml"],
        text=True, stderr=subprocess.PIPE,
    )
    if not re.search(
        r"(?m)^  projects:\n    output: true\n    permalink: /portfolio/:name/$",
        config,
    ):
        return None

    layouts = tracked(r"^layout: (project|milestone)$", regex=True)
    project_sources = {source for source in layouts if source.startswith("_projects/")}
    milestone_sources = {source for source in layouts if source.startswith("_posts/")}
    if layouts != project_sources | milestone_sources:
        return None

    listed_projects = subprocess.check_output(
        ["git", "ls-tree", "-r", "--name-only", revision, "--", "_projects"],
        text=True, stderr=subprocess.PIPE,
    ).splitlines()
    if set(listed_projects) != project_sources or not listed_projects:
        return None

    urls = set()
    for source in {"portfolio/index.html", "portfolio/recognition/index.html"} | milestone_sources:
        page = _permalink_from_source(source, revision)
        if page is None:
            return None
        urls.add(page)
    for source in project_sources:
        stem = source.removeprefix("_projects/")
        if not re.fullmatch(r"[a-z0-9][a-z0-9-]*\.(md|html)", stem):
            return None
        urls.add(f"{BASE_URL}/portfolio/{stem.rsplit('.', 1)[0]}/")
    return urls


_VERIFICATION_SITEMAP_ONLY_ADDITIONS = [
    "  # Sitemap-only exclusions: keep verification files publicly reachable and byte-for-byte intact.",
    "  - scope:",
    '      path: "google5bb82d7c87a25782.html"',
    "    values:",
    "      sitemap: false",
    "  - scope:",
    '      path: "naver7c9f31d4d0aad1444db757e80b29f882.html"',
    "    values:",
    "      sitemap: false",
]


def _verification_sitemap_only_config_edit(before, after):
    """Recognize only the exact two static-file exclusions, not a general config change."""
    diff = subprocess.check_output(
        ["git", "diff", "--no-ext-diff", "--unified=0", before, after,
         "--", "_config.yml"],
        text=True, stderr=subprocess.PIPE,
    )
    added = [line[1:] for line in diff.splitlines()
             if line.startswith("+") and not line.startswith("+++")]
    removed = [line for line in diff.splitlines()
               if line.startswith("-") and not line.startswith("---")]
    return not removed and added == _VERIFICATION_SITEMAP_ONLY_ADDITIONS


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
        # Removing two static verification tokens from sitemap membership does
        # not change the content of a submitted URL. No mass replay.
        if file_path == "_config.yml" and _verification_sitemap_only_config_edit(before, after):
            continue
        # For referenced images only, resolve every affected source page.
        # A shared/unknown reference still conservatively uses the sitemap.
        if file_path.startswith("assets/") or (
            file_path.startswith("_posts/")
            and file_path.lower().endswith((".png", ".jpg", ".jpeg", ".webp", ".gif", ".svg"))
        ):
            try:
                pages = set()
                for revision in (before, after):
                    referenced = _page_urls_for_asset(file_path, revision)
                    if referenced is not None:
                        pages.update(referenced)
                if not pages:
                    return None
                touched.update(pages)
            except ValueError:
                raise
            continue
        # The recognition ledger renders through one checked include used by
        # two fixed pages. Unknown consumers retain the full-site fallback.
        if file_path == "_data/recognitions.yml":
            pages = set()
            for revision in (before, after):
                resolved = _page_urls_for_recognitions(revision)
                if resolved is None:
                    return None
                pages.update(resolved)
            touched.update(pages)
            continue
        # Other shared data and templates may affect every page.
        if file_path.startswith(("_data/", "_includes/", "_layouts/", "_sass/", "css/")) or file_path in ("_config.yml",):
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

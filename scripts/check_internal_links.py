"""Check generated first-party Jekyll navigation without visiting third-party sites.

This is intentionally limited to root-relative, relative, and fragment-only
links; separately hosted applications under the same GitHub Pages hostname
are not built by this repository and require independent deployment checks.
"""
from collections import Counter
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import unquote, urlsplit
import sys

INDEPENDENT_APP_ROUTES = frozenset({
    "/scratchLottery/", "/richChecker/", "/richChecker-us/",
})


class PageLinks(HTMLParser):
    def __init__(self):
        super().__init__()
        self.ids = set()
        self.links = []

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if attrs.get("id"):
            self.ids.add(attrs["id"])
        if tag == "a":
            if attrs.get("name"):
                self.ids.add(attrs["name"])
            if attrs.get("href"):
                self.links.append(attrs["href"])


def inspect(site_root):
    root = Path(site_root).resolve(strict=True)
    if not root.is_dir():
        raise ValueError("SITE_LINK_AUDIT_BUILD_DIRECTORY_REQUIRED")
    pages = {}
    for page in root.rglob("*.html"):
        doc = PageLinks()
        doc.feed(page.read_text(encoding="utf8"))
        pages[page.resolve()] = doc
    failures, checked, fragments, skipped = [], 0, 0, 0
    for page, doc in pages.items():
        for href in doc.links:
            url = urlsplit(href)
            if url.scheme or url.netloc:
                continue
            # Root-relative independent app roots are maintained in their
            # original repos; only those exact landing paths are excepted.
            if url.path in INDEPENDENT_APP_ROUTES:
                skipped += 1
                continue
            if url.path.startswith("//"):
                continue
            target_path = unquote(url.path)
            target = (root / target_path.lstrip("/") if target_path.startswith("/")
                      else page.parent / target_path).resolve()
            checked += 1
            name = str(page.relative_to(root))
            if not target.is_relative_to(root):
                failures.append(f"{name}: link leaves built site: {href}")
                continue
            if target.is_dir():
                target = target / "index.html"
            if not target.is_file():
                # Jekyll may emit a top-level .html page for extensionless
                # relative links; do not treat a missing file as success.
                html_target = Path(str(target) + ".html")
                if html_target.is_file():
                    target = html_target
                else:
                    failures.append(f"{name}: missing local destination: {href}")
                    continue
            if url.fragment and target.suffix.lower() == ".html":
                fragments += 1
                destination = pages.get(target.resolve())
                if destination is None:
                    failures.append(f"{name}: unindexed HTML target: {href}")
                elif unquote(url.fragment) not in destination.ids:
                    failures.append(f"{name}: missing target fragment: {href}")
    return {
        "pages": len(pages),
        "checked_links": checked,
        "checked_fragments": fragments,
        "separate_app_roots": skipped,
        "failures": failures,
    }


def main():
    root = Path(sys.argv[1]) if len(sys.argv) > 1 else Path("_site")
    result = inspect(root)
    print("Checked {pages} HTML pages, {checked_links} internal links, "
          "{checked_fragments} fragments; {separate_app_roots} separate app roots."
          .format(**result))
    if result["failures"]:
        for failure in result["failures"][:40]:
            print(f"ERROR: {failure}", file=sys.stderr)
        print(f"Internal link audit failed: {len(result['failures'])} issues",
              file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

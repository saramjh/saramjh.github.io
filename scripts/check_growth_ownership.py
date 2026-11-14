from pathlib import Path
from datetime import date
import re


def acquisition_metadata_current(post):
    front = post.split("---\n", 2)[1]
    modified = re.search(r"^modified: (\d{4}-\d{2}-\d{2})$", front, re.M)
    updated = re.search(r"^last_modified_at: (\d{4}-\d{2}-\d{2})$", front, re.M)
    if not modified or not updated or modified.group(1) != updated.group(1):
        return False
    try:
        return date.fromisoformat(modified.group(1)) >= date(2026, 9, 30)
    except ValueError:
        return False


root = Path(__file__).resolve().parents[1]
legacy = (root / "_posts/rich-tester/2024-09-04-rich-tester.md").read_text()
redirect = (root / "_layouts/redirect.html").read_text()
kr = (root / "_posts/rich-face-test/2026-09-12-rich-face-test.md").read_text()
en = (root / "_posts/billionaire-lookalike-test/2026-09-12-billionaire-lookalike-test.md").read_text()
llms = (root / "llms.txt").read_text()
home = (root / "_layouts/home.html").read_text()

checks = [
    ("layout: redirect" in legacy, "legacy page must use redirect layout"),
    ("sitemap: false" in legacy, "legacy page must be excluded from sitemap"),
    ("redirect_to: https://saramjh.github.io/richChecker/" in legacy, "legacy page target must be current Korean app"),
    ('name="robots" content="noindex, follow"' in redirect, "redirect must be noindex/follow"),
    ('rel="canonical" href="{{ page.redirect_to }}"' in redirect, "redirect canonical missing"),
    ('http-equiv="refresh"' in redirect, "static redirect refresh missing"),
    ("/rich-tester/" not in kr, "current Korean acquisition article must not link back to legacy competitor"),
    (acquisition_metadata_current(kr), "Korean acquisition freshness missing"),
    (acquisition_metadata_current(en), "English acquisition freshness missing"),
    ("https://saramjh.github.io/richChecker/" in llms, "current Korean app missing from llms.txt"),
    ("https://saramjh.github.io/richChecker-us/" in llms, "current global app missing from llms.txt"),
    ("https://saramjh.github.io/rich-tester/" not in llms, "legacy URL must not remain in llms.txt"),
    ('aria-label="Projects and services"' in home, "root homepage must expose an accessible project discovery group"),
    (all(f'href="{href}"' in home for href in ("/scratchLottery/", "https://spaceatlasedu.org/", "/richChecker/", "/richChecker-us/")), "root homepage must link to all four live interactive projects"),
]
errors = [message for ok, message in checks if not ok]
if errors:
    raise SystemExit("\n".join(errors))
print("PASS growth ownership: legacy search URL redirects out, current acquisition pages own discovery")

from pathlib import Path
import re

root = Path(__file__).resolve().parents[1]
legacy = (root / "_posts/rich-tester/2024-09-04-rich-tester.md").read_text()
redirect = (root / "_layouts/redirect.html").read_text()
kr = (root / "_posts/rich-face-test/2026-09-12-rich-face-test.md").read_text()
en = (root / "_posts/billionaire-lookalike-test/2026-09-12-billionaire-lookalike-test.md").read_text()
llms = (root / "llms.txt").read_text()

checks = [
    ("layout: redirect" in legacy, "legacy page must use redirect layout"),
    ("sitemap: false" in legacy, "legacy page must be excluded from sitemap"),
    ("redirect_to: https://saramjh.github.io/richChecker/" in legacy, "legacy page target must be current Korean app"),
    ('name="robots" content="noindex, follow"' in redirect, "redirect must be noindex/follow"),
    ('rel="canonical" href="{{ page.redirect_to }}"' in redirect, "redirect canonical missing"),
    ('http-equiv="refresh"' in redirect, "static redirect refresh missing"),
    ("/rich-tester/" not in kr, "current Korean acquisition article must not link back to legacy competitor"),
    ("modified: 2026-09-30" in kr and "last_modified_at: 2026-09-30" in kr, "Korean acquisition freshness missing"),
    ("modified: 2026-09-30" in en and "last_modified_at: 2026-09-30" in en, "English acquisition freshness missing"),
    ("https://saramjh.github.io/richChecker/" in llms, "current Korean app missing from llms.txt"),
    ("https://saramjh.github.io/richChecker-us/" in llms, "current global app missing from llms.txt"),
    ("https://saramjh.github.io/rich-tester/" not in llms, "legacy URL must not remain in llms.txt"),
]
errors = [message for ok, message in checks if not ok]
if errors:
    raise SystemExit("\n".join(errors))
print("PASS growth ownership: legacy search URL redirects out, current acquisition pages own discovery")

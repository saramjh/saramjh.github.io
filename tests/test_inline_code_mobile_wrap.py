"""Long first-party inline code must remain readable without changing fenced blocks."""
from pathlib import Path
import re
import unittest

ROOT = Path(__file__).resolve().parents[1]
SYNTAX = ROOT / "_sass/klise/_syntax.scss"
PAGES = {
    "analytic-en": ROOT / "_posts/gh-pages-analytics-notes-2-reasoning-en/2026-09-19-gh-pages-analytics-notes-2-reasoning-en.md",
    "analytic-ko": ROOT / "_posts/gh-pages-analytics-notes-2-reasoning-kr/2026-09-19-gh-pages-analytics-notes-2-reasoning-kr.md",
    "directory-en": ROOT / "_posts/homepage-project-directory-en/2026-11-10-homepage-project-directory-en.md",
    "directory-ko": ROOT / "_posts/homepage-project-directory-ko/2026-11-10-homepage-project-directory-ko.md",
}


class InlineCodeResponsivePolicy(unittest.TestCase):
    def test_scoped_inline_code_will_wrap(self):
        css = SYNTAX.read_text(encoding="utf8")
        self.assertRegex(css, r"(?s)main\s+:not\(pre\)\s*>\s*code\s*\{[^{}]*overflow-wrap:\s*anywhere\s*;[^{}]*\}")

    def test_fenced_code_retains_preformatting_and_scrolling(self):
        css = SYNTAX.read_text(encoding="utf8")
        self.assertRegex(css, r"(?s)pre\.highlight,\s*pre\s*\{[^{}]*overflow-x:\s*auto\s*;")
        self.assertRegex(css, r"(?s)>\s*code\s*\{[^{}]*white-space:\s*pre\s*;")

    def test_original_article_tokens_stay_localized_and_byte_intact(self):
        for key, path in PAGES.items():
            with self.subTest(key=key):
                text = path.read_text(encoding="utf8")
                needle = ("https://saramjh.github.io/scratchLottery/"
                          if key.startswith("analytic")
                          else "scripts/check_growth_ownership.py")
                self.assertIn(needle, text)
                self.assertNotIn("\ufffd", text)
                self.assertNotRegex(text, r"\?{5,}")
                self.assertIn("lang: " + ("en" if key.endswith("en") else "ko"), text)
                if key.endswith("ko"):
                    self.assertRegex(text, "[가-힣]")


if __name__ == "__main__":
    unittest.main()

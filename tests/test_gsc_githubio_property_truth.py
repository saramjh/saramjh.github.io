"""Bilingual Search Console Domain vs URL-prefix guidance regression."""
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]
SOURCES = {
    ("2", "en"): "_posts/gh-pages-analytics-notes-2-reasoning-en/2026-09-19-gh-pages-analytics-notes-2-reasoning-en.md",
    ("2", "ko"): "_posts/gh-pages-analytics-notes-2-reasoning-kr/2026-09-19-gh-pages-analytics-notes-2-reasoning-kr.md",
    ("3", "en"): "_posts/gh-pages-analytics-notes-3-decision-en/2026-09-20-gh-pages-analytics-notes-3-decision-en.md",
    ("3", "ko"): "_posts/gh-pages-analytics-notes-3-decision-kr/2026-09-20-gh-pages-analytics-notes-3-decision-kr.md",
    ("4", "en"): "_posts/gh-pages-analytics-notes-4-open-en/2026-09-21-gh-pages-analytics-notes-4-open-en.md",
    ("4", "ko"): "_posts/gh-pages-analytics-notes-4-open-kr/2026-09-21-gh-pages-analytics-notes-4-open-kr.md",
}
DOC_PROPERTY = "https://support.google.com/webmasters/answer/34592?hl=en"
DOC_VERIFY = "https://support.google.com/webmasters/answer/9008080?hl=en"
ROOT_PREFIX = "https://saramjh.github.io/"


class GSCPropertyAccuracy(unittest.TestCase):
    def test_source_bilingual_metadata_and_unicode_preserved(self):
        for (part, lang), rel in SOURCES.items():
            with self.subTest(part=part, lang=lang):
                text = (ROOT / rel).read_text(encoding="utf8")
                self.assertIn("lang: " + lang, text)
                self.assertIn("alternate_lang: " + ("ko" if lang == "en" else "en"), text)
                self.assertIn(f"permalink: /gh-pages-analytics-notes-{part}-", text)
                self.assertNotIn("\ufffd", text)
                self.assertNotRegex(text, r"\?{5,}")
                if lang == "ko":
                    self.assertRegex(text, r"[가-힣]")

    def test_parts_two_and_three_state_dns_condition_and_root_prefix(self):
        for part in ("2", "3"):
            for lang in ("en", "ko"):
                with self.subTest(part=part, lang=lang):
                    text = (ROOT / SOURCES[(part, lang)]).read_text(encoding="utf8")
                    self.assertIn(DOC_PROPERTY, text)
                    self.assertIn(DOC_VERIFY, text)
                    self.assertIn(ROOT_PREFIX, text)
                    self.assertIn("2026-11-20", text)
                    self.assertIn("DNS", text)
                    self.assertIn("URL-prefix", text)

    def test_unqualified_domain_property_migration_claim_removed(self):
        en3 = (ROOT / SOURCES[("3", "en")]).read_text(encoding="utf8")
        ko3 = (ROOT / SOURCES[("3", "ko")]).read_text(encoding="utf8")
        self.assertNotIn("is now unified under a single domain property", en3)
        self.assertNotIn("하나로 관리 단위를 통일했습니다", ko3)
        for text in (en3, ko3):
            self.assertIn("2026-11-20", text)
            self.assertIn("DNS", text)

    def test_open_questions_recommend_root_prefix(self):
        for lang in ("en", "ko"):
            with self.subTest(lang=lang):
                text = (ROOT / SOURCES[("4", lang)]).read_text(encoding="utf8")
                self.assertIn(ROOT_PREFIX, text)
                self.assertIn(DOC_PROPERTY, text)
                self.assertIn("DNS", text)
                self.assertNotIn("or per-project via URL-prefix", text)
                self.assertNotIn("URL 접두사로 프로젝트마다 따로 검증했는지", text)


if __name__ == "__main__":
    unittest.main()

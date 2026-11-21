"""Keep the September GA4 decision historically true while documenting the later ScratchLottery route."""
from pathlib import Path
import re
import unittest

ROOT = Path(__file__).resolve().parents[1]
SOURCE_COMMIT = "https://github.com/saramjh/scratchLottery/commit/fbbeb0b1e5b3fc7c439d4a219fd0cb4016339121"
CASES = {
    "en": "_posts/gh-pages-analytics-notes-3-decision-en/2026-09-20-gh-pages-analytics-notes-3-decision-en.md",
    "ko": "_posts/gh-pages-analytics-notes-3-decision-kr/2026-09-20-gh-pages-analytics-notes-3-decision-kr.md",
}


class DedicatedScratchLotteryGA4CorrectionTests(unittest.TestCase):
    def test_original_date_and_current_modification_are_separate(self):
        for lang, rel in CASES.items():
            with self.subTest(lang=lang):
                text = (ROOT / rel).read_text(encoding="utf-8")
                self.assertTrue(text.startswith("---\n"))
                frontmatter = text.split("---", 2)[1]
                fields = dict(re.findall(r"(?m)^(date|modified|last_modified_at):\s*(\S+)", frontmatter))
                self.assertEqual(fields["date"], "2026-09-18")
                self.assertEqual(fields["modified"], "2026-11-21")
                self.assertEqual(fields["last_modified_at"], "2026-11-21")
                self.assertIn("lang: " + lang, frontmatter)
                self.assertIn("alternate_lang: " + ("ko" if lang == "en" else "en"), frontmatter)

    def test_dated_correction_preserves_separate_tag_destinations(self):
        for lang, rel in CASES.items():
            with self.subTest(lang=lang):
                text = (ROOT / rel).read_text(encoding="utf-8")
                self.assertEqual(text.count(SOURCE_COMMIT), 1)
                for token in ("2026-11-21", "G-ERNG0LEKY9", "G-4DYFKSNFBG",
                              "scratch_completed", "run_fast_simulation", "554", "660"):
                    self.assertIn(token, text)
                self.assertIn("/scratchLottery/", text)
                self.assertIn("2026-11-20", text)  # Earlier dated account check retained.
                self.assertNotIn("\ufffd", text)
                self.assertNotRegex(text, r"\?{5,}")
                if lang == "ko":
                    self.assertRegex(text, r"[가-힣]")
                else:
                    self.assertIn("dedicated GA4 tag", text)

    def test_no_false_cross_property_growth_claim(self):
        for lang, rel in CASES.items():
            with self.subTest(lang=lang):
                text = (ROOT / rel).read_text(encoding="utf-8")
                if lang == "en":
                    self.assertIn("not verified distinct people or product adoption", text)
                else:
                    self.assertIn("서로 다른 실제 사람의 수나 제품 채택 실적이 아닙니다", text)


if __name__ == "__main__":
    unittest.main()

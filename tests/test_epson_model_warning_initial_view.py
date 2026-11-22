"""Existing L3100/L3156 limitations must precede procedural guidance.

Actual original blog GSC queries include model names, but the upstream
reinkpy-fix source confirms operation only for L3060 series/similar printers.
The source-first ordering requires no new claims or model compatibility.
"""
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
POSTS = {
    "ko": ROOT / "_posts/epson-waste-ink-pad-reset-without-key/2026-09-15-epson-waste-ink-pad-reset-without-key.md",
    "en": ROOT / "_posts/en-epson-waste-ink-pad-reset-without-key/2026-09-15-en-epson-waste-ink-pad-reset-without-key.md",
}


class EpsonModelWarningPlacementTest(unittest.TestCase):
    def test_model_specific_warning_precedes_language_banner_and_code(self):
        for lang, path in POSTS.items():
            with self.subTest(lang=lang):
                text = path.read_text(encoding="utf-8")
                heading = ("## L3100·L3156에서 리셋하려는 경우" if lang == "ko"
                           else "## If your printer is an L3100 or L3156")
                banner = "English Edition available:" if lang == "ko" else "한국어 안내:"
                source_check = ("2026-11-15 제조사 기준 재검증" if lang == "ko"
                                else "Manufacturer cross-check (15 Nov 2026)")
                self.assertEqual(text.count(heading), 1)
                self.assertLess(text.index(heading), text.index(banner))
                self.assertLess(text.index(banner), text.index(source_check))
                self.assertLess(text.index(heading), text.index("## 1. "))
                self.assertIn("L3106", text[text.index(heading):text.index(banner)])
                self.assertIn("L3156", text[text.index(heading):text.index(banner)])
                self.assertIn("https://epson.com/support/epson-ink-pad-reset-utility-faqs", text)
                self.assertNotIn("\ufffd", text)

    def test_existing_manufacturer_warnings_and_ko_en_relationship_survive(self):
        ko = POSTS["ko"].read_text(encoding="utf8")
        en = POSTS["en"].read_text(encoding="utf8")
        self.assertIn("기종별 호환성은 별도 확인이 필요", ko)
        self.assertIn("공식 서비스 안내", ko)
        self.assertIn("not an Epson-authorized repair procedure", en)
        self.assertIn("A software counter reset cannot replace servicing", en)
        self.assertIn("alternate_url: /en-epson-waste-ink-pad-reset-without-key/", ko)
        self.assertIn("alternate_url: /epson-waste-ink-pad-reset-without-key/", en)
        self.assertRegex(ko, r"(?m)^modified: \d{4}-\d{2}-\d{2}$")
        self.assertRegex(en, r"(?m)^modified: \d{4}-\d{2}-\d{2}$")


if __name__ == "__main__":
    unittest.main()

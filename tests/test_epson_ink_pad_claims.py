"""Regression checks for two original Epson ink-pad help articles.

This test checks the public reader-facing safety boundaries. It does not test
or invoke any printer, USB device, reset utility or external provider.
"""
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]
KO = ROOT / "_posts/epson-waste-ink-pad-reset-without-key/2026-09-15-epson-waste-ink-pad-reset-without-key.md"
EN = ROOT / "_posts/en-epson-waste-ink-pad-reset-without-key/2026-09-15-en-epson-waste-ink-pad-reset-without-key.md"


class EpsonInkPadSafetyCopyTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.ko = KO.read_text(encoding="utf-8")
        cls.en = EN.read_text(encoding="utf-8")

    def test_both_versions_name_physical_servicing_and_software_limits(self):
        self.assertIn("소프트웨어 카운터 초기화는 실제 잉크 흡수재 정비를 대신하지 않습니다", self.ko)
        self.assertIn("A software counter reset cannot replace servicing the physical ink pads", self.en)
        self.assertIn("https://epson.com/support/epson-ink-pad-reset-utility-faqs", self.ko)
        self.assertIn("https://epson.com/support/epson-ink-pad-reset-utility-faqs", self.en)

    def test_printed_success_is_not_printer_eeprom_verification(self):
        self.assertIn("출력 메시지만으로 프린터의 실제 카운터 변경이 확인되지는 않습니다", self.ko)
        self.assertIn("A printed success message alone does not prove the printer counter changed", self.en)

    def test_physical_steps_apply_to_documented_model_only(self):
        self.assertIn("아래 분해 단계는 작성자가 기록한 L3106 사례", self.ko)
        self.assertIn("The disassembly sequence below records the author's L3106 case", self.en)

    def test_frontmatter_faq_does_not_direct_retry_or_claim_universal_cheapest_repair(self):
        kofm = self.ko.split("---", 2)[1]
        enfm = self.en.split("---", 2)[1]
        self.assertIn("추가 리셋을 반복하지 말고", kofm)
        self.assertIn("do not run the reset again", enfm)
        self.assertNotIn("가장 안전합니다", kofm)
        self.assertNotIn("by far the safest", enfm)

    def test_articles_keep_original_localized_permalink_and_source_boundaries(self):
        self.assertIn("permalink: /epson-waste-ink-pad-reset-without-key/", self.ko)
        self.assertIn("permalink: /en-epson-waste-ink-pad-reset-without-key/", self.en)
        self.assertIn("L3060", self.ko)
        self.assertIn("L3060", self.en)
        self.assertIn("reinkpy-fix", self.ko)
        self.assertIn("reinkpy-fix", self.en)


if __name__ == "__main__":
    unittest.main()

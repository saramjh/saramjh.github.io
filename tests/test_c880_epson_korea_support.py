"""New source-bound Epson Korea reader actions: no unsupported reset claims."""
from pathlib import Path
import re
import unittest

ROOT = Path(__file__).resolve().parents[1]
PAGES = [
    ROOT / "_posts/epson-waste-ink-pad-reset-without-key/2026-09-15-epson-waste-ink-pad-reset-without-key.md",
    ROOT / "_posts/en-epson-waste-ink-pad-reset-without-key/2026-09-15-en-epson-waste-ink-pad-reset-without-key.md",
]
L3106 = "https://www.epson.co.kr/faq/SPT_C11CG88513~EKL_FAQ_0871"
SUPPORT = "https://www.epson.co.kr/cs"

class EpsonKoreaFirstPartyResource(unittest.TestCase):
    def test_both_articles_offer_identifiable_real_model_and_service_resources(self):
        for post in PAGES:
            with self.subTest(path=post.name):
                body = post.read_text(encoding="utf8")
                self.assertEqual(body.count(L3106),1)
                self.assertEqual(body.count(SUPPORT),1)
                self.assertIn("https://epson.com/support/epson-ink-pad-reset-utility-faqs",body)
                self.assertIn("https://epson.com/support/wa00369",body)
                self.assertEqual(body.count('<script src="/assets/js/epson-official-support-click.js" defer></script>'),1)
                self.assertNotIn("\ufffd",body)
                self.assertNotIn("????",body)
                self.assertEqual(body.count("modified: 2026-11-19"),1)
                self.assertEqual(body.count("last_modified_at: 2026-11-19"),1)
        ko, en = [p.read_text(encoding="utf8") for p in PAGES]
        self.assertIn("사용자가 직접 교체할 수 없",ko)
        self.assertIn("not a counter-reset",en)
        self.assertIn("L3106",ko)
        self.assertIn("L3106",en)

    def test_click_tracker_only_uses_exact_official_host_and_path_and_privacy_safe_payload(self):
        script = (ROOT / "assets/js/epson-official-support-click.js").read_text(encoding="utf8")
        self.assertIn("www.epson.co.kr",script)
        self.assertIn("/faq/SPT_C11CG88513~EKL_FAQ_0871",script)
        self.assertIn("kr_l3106_maintenance",script)
        self.assertIn("kr_customer_support",script)
        self.assertIn("epson_support_reference_select",script)
        for forbidden in ("fetch(", "sendBeacon", "preventDefault", "document.cookie"):
            self.assertNotIn(forbidden,script)
        # Original non-PII whitelist and DNT behavior remain necessary.
        for original in ("ink_pad_faq","waste_ink_service","navigator.doNotTrack","reference_id","article_lang"):
            self.assertIn(original,script)

if __name__ == "__main__":
    unittest.main()

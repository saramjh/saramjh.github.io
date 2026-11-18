"""Protect first-party Epson article analytics from unexpected scope expansion."""
from pathlib import Path
import unittest

ROOT=Path(__file__).resolve().parents[1]
PAGES=[
    ROOT / "_posts/epson-waste-ink-pad-reset-without-key/2026-09-15-epson-waste-ink-pad-reset-without-key.md",
    ROOT / "_posts/en-epson-waste-ink-pad-reset-without-key/2026-09-15-en-epson-waste-ink-pad-reset-without-key.md",
]
SCRIPT_TAG='<script src="/assets/js/epson-official-support-click.js" defer></script>'

class EpsonOfficialSelection(unittest.TestCase):
    def test_only_existing_two_first_party_articles_include_the_event_script(self):
        for page in PAGES:
            source=page.read_text(encoding="utf8")
            self.assertEqual(source.count(SCRIPT_TAG),1)
            self.assertIn("https://epson.com/support/epson-ink-pad-reset-utility-faqs",source)
            self.assertIn("https://epson.com/support/wa00369",source)
            self.assertNotIn("\ufffd",source)
            self.assertNotIn("????",source)
        self.assertIn("lang: ko", PAGES[0].read_text(encoding="utf8"))
        self.assertIn("lang: en", PAGES[1].read_text(encoding="utf8"))

    def test_no_shared_tracking_or_content_template_changes(self):
        footer=(ROOT/"_includes/footer.html").read_text(encoding="utf8")
        self.assertNotIn("epson-official-support-click.js",footer)
        script=(ROOT/"assets/js/epson-official-support-click.js").read_text(encoding="utf8")
        self.assertIn("epson_support_reference_select",script)
        self.assertNotIn("fetch(",script)
        self.assertNotIn("sendBeacon",script)
        self.assertNotIn("preventDefault",script)
        self.assertNotIn("document.cookie",script)

if __name__ == "__main__":
    unittest.main()

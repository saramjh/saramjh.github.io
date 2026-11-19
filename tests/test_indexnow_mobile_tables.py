"""Preserve bilingual IndexNow native-receipt evidence in accessible scrollable tables."""
from pathlib import Path
import re
import unittest

ROOT = Path(__file__).resolve().parents[1]
ARTICLES = {
    "ko": ROOT / "_posts/indexnow-image-page-scope-ko/2026-11-10-indexnow-image-page-scope-ko.md",
    "en": ROOT / "_posts/indexnow-image-page-scope-en/2026-11-10-indexnow-image-page-scope-en.md",
}
RECEIPTS = ("42760722178", "42761734284", "44317892057", "44321890015")
UNTOUCHED = ("120", "194", "195", "11")


class IndexNowResponsiveEvidenceTables(unittest.TestCase):
    def test_reuse_existing_site_scoped_table_overflow(self):
        css = (ROOT / "_sass/klise/_base.scss").read_text(encoding="utf8")
        self.assertRegex(css, r"(?s)\.overflow-table\s*\{\s*overflow-x:\s*auto")

    def test_both_tables_remain_kramdown_semantic_and_named(self):
        for lang, path in ARTICLES.items():
            with self.subTest(lang=lang):
                source = path.read_text(encoding="utf8")
                self.assertEqual(source.count('<div class="overflow-table" markdown="1"'), 2)
                self.assertEqual(source.count('role="region" tabindex="0" aria-label='), 2)
                self.assertEqual(source.count("</div>"), 2)
                tables = re.findall(
                    r'<div class="overflow-table" markdown="1"[^>]*>\s*'
                    r'((?:\|[^\n]*\|\n)+)\s*</div>',
                    source,
                    flags=re.M,
                )
                self.assertEqual(len(tables), 2)
                for table in tables:
                    lines = table.strip().splitlines()
                    self.assertEqual(len(lines), 5)
                    self.assertEqual(len([s for s in lines if s.startswith("|")]), 5)
                    self.assertEqual(lines[1].count("|"), 4)
                for receipt in RECEIPTS:
                    self.assertIn(receipt, source)
                for count in UNTOUCHED:
                    self.assertIn(count, source)
                self.assertNotIn("\ufffd", source)
                self.assertNotRegex(source, r"\?{4,}")
                if lang == "ko":
                    self.assertRegex(source, "[가-힣]")

    def test_original_locale_and_page_metadata(self):
        for lang, path in ARTICLES.items():
            with self.subTest(lang=lang):
                source = path.read_text(encoding="utf8")
                self.assertIn("lang: " + lang, source)
                self.assertIn("alternate_lang: " + ("en" if lang == "ko" else "ko"), source)
                self.assertIn("modified: 2026-11-19", source)
                self.assertIn("last_modified_at: 2026-11-19", source)


if __name__ == "__main__":
    unittest.main()

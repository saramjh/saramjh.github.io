"""The evidence archive's card headings belong to a navigable H2 section."""
from pathlib import Path
import re
import unittest

ROOT = Path(__file__).resolve().parents[1]
ARCHIVE = ROOT / 'portfolio/recognition/index.html'
CARD = ROOT / '_includes/portfolio-evidence.html'
STYLE = ROOT / 'assets/css/portfolio.css'


class RecognitionArchiveHeadingOutlineTests(unittest.TestCase):
    def test_archive_h1_h2_card_h3_outline(self):
        page = ARCHIVE.read_text(encoding='utf-8')
        card = CARD.read_text(encoding='utf-8')
        h1 = page.index('<h1>')
        h2 = page.index('<h2 class="folio-archive-outline-heading" id="folio-records-heading">External records</h2>')
        evidence_list = page.index('<ol class="folio-evidence-list" id="folio-records" aria-labelledby="folio-records-heading">')
        self.assertLess(h1, h2)
        self.assertLess(h2, evidence_list)
        self.assertIn('<h3><a href="{{ record.url | escape }}"', card)
        self.assertEqual(page.count('id="folio-records-heading"'), 1)
        self.assertEqual(page.count('aria-labelledby="folio-records-heading"'), 1)
        self.assertEqual(len(re.findall(r'<h2\b', page)), 1)

    def test_heading_is_screen_reader_accessible_without_visual_layout_change(self):
        css = STYLE.read_text(encoding='utf-8')
        rule = re.search(r'\.portfolio-body \.folio-archive-outline-heading\{([^}]*)\}', css)
        self.assertIsNotNone(rule)
        for required in ('position:absolute', 'width:1px', 'height:1px', 'overflow:hidden', 'white-space:nowrap'):
            self.assertIn(required, rule.group(1))
        self.assertNotIn('display:none', rule.group(1))
        self.assertNotIn('visibility:hidden', rule.group(1))

    def test_existing_archive_evidence_and_filter_structure_stays_unchanged(self):
        page = ARCHIVE.read_text(encoding='utf-8')
        for kind in ('publication', 'dataset_record', 'listing', 'collaboration'):
            self.assertEqual(page.count('{% include portfolio-evidence.html type="'+kind+'" %}'), 1)
            self.assertIn('data-filter="'+kind+'"', page)
        self.assertIn('id="folio-filter-count" aria-live="polite"', page)
        self.assertIn('id="folio-filter-empty" hidden', page)

if __name__ == '__main__':
    unittest.main()

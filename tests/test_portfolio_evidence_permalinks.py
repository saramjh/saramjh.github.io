"""Each external achievement has one accessible shareable original archive target."""
from pathlib import Path
import re
import unittest

ROOT = Path(__file__).resolve().parents[1]
INCLUDE = (ROOT / '_includes/portfolio-evidence.html').read_text('utf8')
ARCHIVE = (ROOT / 'portfolio/recognition/index.html').read_text('utf8')
STYLE = (ROOT / 'assets/css/portfolio.css').read_text('utf8')
LEDGER = (ROOT / '_data/recognitions.yml').read_text('utf8')
IDS = re.findall(r'^- id: ([^\n]+)', LEDGER, flags=re.M)

class ExternalEvidencePermalinks(unittest.TestCase):
    def test_confirmed_source_ids_are_unique_and_safe_fragments(self):
        self.assertEqual(len(IDS), 27)
        self.assertEqual(len(set(IDS)), len(IDS))
        self.assertTrue(all(re.fullmatch(r'[a-z0-9]+(?:-[a-z0-9]+)*', item) for item in IDS))

    def test_each_record_has_source_bound_anchor_and_an_accessible_share_link(self):
        self.assertIn('id="evidence-{{ record.id | escape }}"', INCLUDE)
        self.assertIn('href="{{ \'/portfolio/recognition/\' | relative_url }}#evidence-{{ record.id | escape }}"', INCLUDE)
        self.assertIn('class="folio-evidence-permalink"', INCLUDE)
        self.assertIn('aria-label="Direct link to record: {{ record.title | escape }}"', INCLUDE)
        self.assertIn('>Link to record</a>', INCLUDE)

    def test_original_external_proof_and_case_links_remain_authoritative(self):
        self.assertIn('href="{{ record.url | escape }}"', INCLUDE)
        self.assertIn('target="_blank" rel="noopener noreferrer"', INCLUDE)
        self.assertIn('data-case-lang="ko"', INCLUDE)
        self.assertIn('data-case-lang="en"', INCLUDE)
        self.assertIn('data-evidence-id="{{ record.id | escape }}"', INCLUDE)
        self.assertIn('id="folio-records"', ARCHIVE)

    def test_anchor_has_readable_scroll_target_and_keyboard_focus_treatment(self):
        self.assertIn('.folio-evidence-item[id^="evidence-"]{scroll-margin-top:', STYLE)
        self.assertIn('.folio-evidence-permalink', STYLE)
        self.assertIn('.folio-evidence-permalink:focus-visible', STYLE)

if __name__ == '__main__':
    unittest.main()

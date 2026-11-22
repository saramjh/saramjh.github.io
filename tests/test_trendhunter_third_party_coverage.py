"""A verified outside feature is not presented as the developer's byline."""
from pathlib import Path
import re
import unittest

ROOT = Path(__file__).resolve().parents[1]
LEDGER = (ROOT / '_data/recognitions.yml').read_text(encoding='utf8')
INCLUDE = (ROOT / '_includes/portfolio-evidence.html').read_text(encoding='utf8')
ARCHIVE = (ROOT / 'portfolio/recognition/index.html').read_text(encoding='utf8')
HOME = (ROOT / 'portfolio/index.html').read_text(encoding='utf8')
LINK = 'https://www.trendhunter.com/trends/scratch-lottery-simulation-program'
RECORD_ID = 'trendhunter-scratch-lottery-2025'


def fields_for_record():
    match = re.search(r'(?ms)^- id: trendhunter-scratch-lottery-2025\n(.*?)(?=^- id: |\Z)', LEDGER)
    assert match, 'original verified outside feature missing'
    return dict(re.findall(r'^  ([a-z_]+):\s*"?([^"\n]+)', match.group(1), re.M))


class TrendHunterCoverageTest(unittest.TestCase):
    def test_outside_author_and_original_2025_reference_are_distinct_from_our_bylines(self):
        item = fields_for_record()
        self.assertEqual(item['project'], 'scratch-lottery')
        self.assertEqual(item['type'], 'coverage')
        self.assertEqual(item['status'], 'confirmed')
        self.assertEqual(item['date'], '2025-03-27')
        self.assertEqual(item['source'], 'Trend Hunter')
        self.assertEqual(item['url'], LINK)
        self.assertIn('Ellen Smith', item['detail'])
        self.assertIn('measured visits', item['detail'])
        self.assertEqual(item['case_ko'], '/scratch-lottery-simulation-ko/')
        self.assertEqual(item['case_en'], '/scratch-lottery-simulation/')
        self.assertEqual(item['verified_at'], '2026-11-23')

    def test_original_bilingual_case_pages_cite_outside_author_without_republishing_media(self):
        paths = (
            ROOT / '_posts/scratch-lottery-simulation/2024-09-03-scratch-lottery-simulation.md',
            ROOT / '_posts/scratch-lottery-simulation-ko/2026-11-13-scratch-lottery-simulation-ko.md',
        )
        for path in paths:
            with self.subTest(path=path.name):
                source = path.read_text(encoding='utf8')
                self.assertIn(LINK, source)
                self.assertIn('Ellen Smith', source)
        self.assertNotIn('trendhunter.com/wp-content', LEDGER)
        self.assertNotIn('trendhunter.com/images', LEDGER)

    def test_distinct_archive_category_and_selected_first_party_preview(self):
        self.assertIn('data-filter="coverage"', ARCHIVE)
        self.assertIn('{% include portfolio-evidence.html type="coverage" %}', ARCHIVE)
        self.assertIn('{% include portfolio-evidence.html type="coverage" ids="trendhunter-scratch-lottery-2025" %}', HOME)
        self.assertIn("{% when 'coverage' %}Third-party feature", INCLUDE)
        self.assertIn("{% when 'coverage' %}External article", INCLUDE)
        self.assertIn('not a developer byline or evidence of adoption', ARCHIVE)
        self.assertEqual(len(re.findall(r'(?m)^- id: ', LEDGER)), 30)
        self.assertEqual(len(re.findall(r'(?m)^  type: publication$', LEDGER)), 7)
        self.assertEqual(len(re.findall(r'(?m)^  type: coverage$', LEDGER)), 1)


if __name__ == '__main__':
    unittest.main()

"""Owner-confirmed evidence must be discoverable in the existing on-site search."""
import re
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SEARCH = (ROOT / 'assets/search.json').read_text(encoding='utf-8')
ARCHIVE = (ROOT / 'archive.html').read_text(encoding='utf-8')
LEDGER = (ROOT / '_data/recognitions.yml').read_text(encoding='utf-8')


class EvidenceSearchIndex(unittest.TestCase):
    def test_exact_original_confirmed_inventory_is_source_bound(self):
        ids = re.findall(r'(?m)^- id: ([a-z0-9-]+)$', LEDGER)
        self.assertEqual(len(ids), 28)
        self.assertEqual(len(set(ids)), 28)
        self.assertEqual(len(re.findall(r'(?m)^  status: confirmed$', LEDGER)), 28)

    def test_existing_170_blog_posts_remain_indexed(self):
        self.assertIn('{% for post in site.posts %}', SEARCH)
        self.assertIn('{{ post.url }}', SEARCH)

    def test_source_owner_verified_records_only_and_exact_permalink_fragments(self):
        self.assertIn('{% for record in site.data.recognitions %}', SEARCH)
        self.assertIn("{% if record.status == 'confirmed' %}", SEARCH)
        self.assertIn('/portfolio/recognition/#evidence-{{ record.id | escape }}', SEARCH)
        self.assertIn('record.detail | escape | jsonify', SEARCH)
        self.assertIn('record.source', SEARCH)
        self.assertIn('record.title', SEARCH)
        self.assertIn('record.id', SEARCH)

    def test_search_page_describes_both_source_types_without_changing_post_archive(self):
        self.assertIn('Search articles and verified external records', ARCHIVE)
        self.assertIn('aria-label="Search articles and verified external records"', ARCHIVE)
        self.assertIn('{%- for post in site.posts -%}', ARCHIVE)
        self.assertIn('id="search-results"', ARCHIVE)


if __name__ == '__main__':
    unittest.main()

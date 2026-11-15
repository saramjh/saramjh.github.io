"""Search must surface source-verified achievements despite the 10-article cap."""
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ARCHIVE = (ROOT / 'archive.html').read_text('utf8')
FOOTER = (ROOT / '_includes/footer.html').read_text('utf8')
SCRIPT = ROOT / 'assets/js/archive-search.js'
INDEX = (ROOT / 'assets/search.json').read_text('utf8')

class BalancedSearch(unittest.TestCase):
    def test_confirmed_evidence_and_blog_source_share_one_index(self):
        self.assertIn('{% for post in site.posts %}', INDEX)
        self.assertIn('{% for record in site.data.recognitions %}', INDEX)
        self.assertIn("{% if record.status == 'confirmed' %}", INDEX)

    def test_archive_has_independent_accessible_result_groups(self):
        self.assertIn('id="evidence-search-results"', ARCHIVE)
        self.assertIn('id="search-results"', ARCHIVE)
        self.assertIn('id="search-result-status"', ARCHIVE)
        self.assertIn('aria-live="polite"', ARCHIVE)
        self.assertIn('id="search-evidence-section"', ARCHIVE)
        self.assertIn('id="search-article-section"', ARCHIVE)

    def test_single_archival_search_replaces_truncating_legacy_route(self):
        self.assertIn('src="/assets/js/archive-search.js"', FOOTER)
        self.assertNotIn('SimpleJekyllSearch({', FOOTER)
        self.assertTrue(SCRIPT.is_file())
        text = SCRIPT.read_text('utf8')
        self.assertIn("'/assets/search.json'", text)
        self.assertIn('MAX_ARTICLES = 10', text)
        self.assertIn("'/portfolio/recognition/#evidence-'", text)
        self.assertIn('evidenceMatches', text)
        self.assertIn('articleMatches', text)
        self.assertIn('document.createElement', text)
        self.assertIn('.textContent', text)
        self.assertNotIn('results.innerHTML', text)

    def test_legacy_date_archive_remains_accessible(self):
        self.assertIn('{%- for post in site.posts -%}', ARCHIVE)
        self.assertIn('href="{{ post.url }}"', ARCHIVE)

if __name__=='__main__':unittest.main()

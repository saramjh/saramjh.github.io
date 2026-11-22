"""Legacy redirect remains reachable, but is not a searchable article."""
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]
SEARCH = (ROOT / 'assets/search.json').read_text(encoding='utf8')
ARCHIVE = (ROOT / 'archive.html').read_text(encoding='utf8')
REDIRECT = (ROOT / '_posts/rich-tester/2024-09-04-rich-tester.md').read_text(encoding='utf8')


class ArchiveRedirectVisibilityTest(unittest.TestCase):
    def test_source_redirect_is_preserved(self):
        self.assertIn('layout: redirect', REDIRECT)
        self.assertIn('sitemap: false', REDIRECT)
        self.assertIn('redirect_to: https://saramjh.github.io/richChecker/', REDIRECT)

    def test_search_excludes_redirect_before_separator(self):
        self.assertIn("{% for post in site.posts %}", SEARCH)
        self.assertIn("{% unless post.layout == 'redirect' %}", SEARCH)
        start = SEARCH.index("{% unless post.layout == 'redirect' %}")
        end = SEARCH.index('{% endunless %}', start)
        self.assertIn("{{ post.url }}", SEARCH[start:end])
        self.assertIn("{% assign search_separator = ',' %}", SEARCH[start:end])
        self.assertNotIn('site.posts | where:', SEARCH)

    def test_browse_excludes_redirect_without_removing_posts(self):
        self.assertIn('{%- for post in site.posts -%}', ARCHIVE)
        self.assertIn("{%- unless post.layout == 'redirect' -%}", ARCHIVE)
        self.assertIn('href="{{ post.url }}"', ARCHIVE)
        self.assertLess(ARCHIVE.index("{%- unless post.layout == 'redirect' -%}"), ARCHIVE.index('href="{{ post.url }}"'))
        self.assertIn('{%- endunless -%}', ARCHIVE)

    def test_chrome_regression_checks_index_and_browse(self):
        src = (ROOT / 'tests/archive_search_browser.py').read_text(encoding='utf8')
        self.assertIn("legacy redirect must not appear as an archive article", src)
        self.assertIn("legacy redirect must not appear in article search", src)


if __name__ == '__main__':
    unittest.main()

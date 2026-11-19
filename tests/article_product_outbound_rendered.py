"""Check content-qualified Spoonie link measurement in the actual built Jekyll HTML."""
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = '/assets/js/article-product-outbound.js'

class RenderedArticleProductOutboundTest(unittest.TestCase):
    def test_posts_with_allowed_spoonie_links_receive_the_existing_script(self):
        for slug in (
            'recipe-calc-to-spoonie-origin-en',
            'chocolate-french-toast-guide',
            '20-minute-home-cooking-decision-guide',
            'spoonie-editorial-curators-en',
            'spoonie-search-discovery-en',
        ):
            with self.subTest(slug=slug):
                html = (ROOT / '_site' / slug / 'index.html').read_text(encoding='utf-8')
                self.assertIn('https://spoonie.kr/', html)
                self.assertEqual(html.count(SCRIPT), 1)

    def test_unrelated_article_does_not_load_the_extra_script(self):
        html = (ROOT / '_site' / 'space-atlas-eusci-diagrams-en' / 'index.html').read_text(encoding='utf-8')
        self.assertNotIn(SCRIPT, html)

if __name__ == '__main__':
    unittest.main()

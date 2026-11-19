"""The developer blog measures actual allowed Spoonie-link selections across article slugs."""
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]
FOOTER = ROOT / "_includes" / "footer.html"
SCRIPT = ROOT / "assets" / "js" / "article-product-outbound.js"
POSTS_WITH_SPOONIE_RECIPE_LINK = (
    "recipe-calc-to-spoonie-origin-en/2026-11-11-recipe-calc-to-spoonie-origin-en.md",
    "chocolate-french-toast-guide/2026-10-13-chocolate-french-toast-guide.md",
    "20-minute-home-cooking-decision-guide/2026-10-13-20-minute-home-cooking-decision-guide.md",
    "spoonie-editorial-curators-en/2026-11-11-spoonie-editorial-curators-en.md",
)

class ArticleProductOutboundLoaderTest(unittest.TestCase):
    def test_content_driven_loader_includes_unconventional_article_slugs(self):
        footer = FOOTER.read_text(encoding="utf-8")
        self.assertIn("page.content contains 'https://spoonie.kr'", footer)
        self.assertNotIn("page.url contains '/spoonie-'", footer)
        self.assertEqual(footer.count('src="/assets/js/article-product-outbound.js"'), 1)
        for post in POSTS_WITH_SPOONIE_RECIPE_LINK:
            with self.subTest(post=post):
                body = (ROOT / "_posts" / post).read_text(encoding="utf-8")
                self.assertIn('https://spoonie.kr/', body)

    def test_loader_and_event_scope_stay_private_and_click_only(self):
        footer = FOOTER.read_text(encoding="utf-8")
        script = SCRIPT.read_text(encoding="utf-8")
        self.assertIn("site.google_analytics", footer)
        self.assertIn("page.tracking != false", footer)
        self.assertIn("page.date", footer)
        self.assertIn("url.origin !== 'https://spoonie.kr'", script)
        self.assertIn("navigator.doNotTrack", script)
        self.assertIn("link.addEventListener('click'", script)
        self.assertNotIn("location.href", script)
        self.assertNotIn("page_location", script)
        self.assertNotIn("client_id", script)

if __name__ == "__main__":
    unittest.main()

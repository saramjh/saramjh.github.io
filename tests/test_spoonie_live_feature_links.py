"""Bilingual developer-case live-product entry points, no new tracking."""
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]
POSTS = {
    "spoonie-editorial-curators-ko": ("2026-11-11", "https://spoonie.kr/curators", "공개 큐레이터 목록"),
    "spoonie-editorial-curators-en": ("2026-11-11", "https://spoonie.kr/curators", "public curator directory"),
    "spoonie-search-discovery-ko": ("2026-11-12", "https://spoonie.kr/search", "레시피 검색"),
    "spoonie-search-discovery-en": ("2026-11-12", "https://spoonie.kr/search", "recipe search"),
}

class SourceBoundLiveLinkTest(unittest.TestCase):
    def test_each_article_has_one_clear_early_live_feature_entry_point(self):
        for slug, (date, url, label) in POSTS.items():
            with self.subTest(slug=slug):
                body = (ROOT / "_posts" / slug / f"{date}-{slug}.md").read_text(encoding="utf-8")
                start = body.index('class="article-live-demo"')
                self.assertGreater(start, body.index("\n---\n", 4))
                self.assertLess(start, body.index("\n## "))
                self.assertEqual(body.count('class="article-live-demo"'), 1)
                self.assertIn(f'<a class="article-live-demo-link" href="{url}">', body)
                self.assertIn(label, body[start:body.index("</p>",start)])
                self.assertIn('class="article-live-demo-note"', body[start:body.index("</p>",start)])
                self.assertNotIn("\ufffd", body)
                self.assertNotIn("????", body)

    def test_touch_keyboard_dark_and_existing_privacy_safe_click_measurement(self):
        light = (ROOT / "_sass/klise/_layout.scss").read_text(encoding="utf-8")
        dark = (ROOT / "_sass/klise/_dark.scss").read_text(encoding="utf-8")
        script = (ROOT / "assets/js/article-product-outbound.js").read_text(encoding="utf-8")
        self.assertIn(".article-live-demo-link {", light)
        self.assertIn("min-height: 44px", light.split(".article-live-demo-link {",1)[1])
        self.assertIn("&:focus-visible", light.split(".article-live-demo-link {",1)[1])
        self.assertIn(".article-live-demo-link {", dark)
        self.assertIn("select_content", script)
        self.assertIn("navigator.doNotTrack", script)
        self.assertIn("url.origin !== 'https://spoonie.kr'", script)

if __name__ == "__main__":
    unittest.main()

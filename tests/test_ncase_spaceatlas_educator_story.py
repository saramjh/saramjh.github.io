"""Regression: retain original educator article, avoid duplicate index entries.

The November 16 edition was a duplicate of the original November 11
NCASE/Share My Lesson case study. Its published URLs must still work.
"""
import struct
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DUPLICATE_SLUG = "space-atlas-educator-discovery"
CANONICAL_SLUG = "space-atlas-education-resource-paths"
MEDIA = ROOT / "assets/img/dev-ncase-spaceatlas-educator-20261116"


class SpaceAtlasEducatorDiscoveryStory(unittest.TestCase):
    def test_original_educator_case_is_the_only_indexable_article(self):
        for lang in ("ko", "en"):
            with self.subTest(lang=lang):
                original = ROOT / "_posts" / f"{CANONICAL_SLUG}-{lang}" / (
                    f"2026-11-11-{CANONICAL_SLUG}-{lang}.md"
                )
                self.assertTrue(original.is_file())
                text = original.read_text("utf8")
                self.assertIn(f"permalink: /{CANONICAL_SLUG}-{lang}/", text)
                self.assertIn("https://ncase.org/programs/", text)
                self.assertIn("https://sharemylesson.com/teaching-resource/", text)
                self.assertIn("published: true", text)
                self.assertFalse(
                    (ROOT / "_posts" / f"{DUPLICATE_SLUG}-{lang}"
                     / f"2026-11-16-{DUPLICATE_SLUG}-{lang}.md").exists(),
                    "Nov 16 duplicate post must not inflate site.posts/search/sitemap",
                )

    def test_november_16_public_urls_reuse_existing_redirect_layout(self):
        layout = (ROOT / "_layouts/redirect.html").read_text("utf8")
        self.assertIn("page.redirect_to", layout)
        self.assertIn('name="robots" content="noindex, follow"', layout)
        self.assertNotIn("현재 부자 관상 테스트 열기", layout)

        for lang in ("ko", "en"):
            with self.subTest(lang=lang):
                route = ROOT / f"{DUPLICATE_SLUG}-{lang}" / "index.html"
                self.assertTrue(route.is_file())
                data = route.read_text("utf8")
                self.assertIn("layout: redirect", data)
                self.assertIn(f"lang: {lang}", data)
                self.assertIn(f"permalink: /{DUPLICATE_SLUG}-{lang}/", data)
                self.assertIn(
                    f"redirect_to: https://saramjh.github.io/{CANONICAL_SLUG}-{lang}/",
                    data,
                )
                self.assertIn("sitemap: false", data)
                self.assertIn("ads: false", data)
                self.assertNotIn("site.posts", data)

    def test_firstparty_source_media_is_preserved_for_historical_receipts(self):
        source = ROOT / "_posts/space-atlas-student/space-atlas-moon-phases.png"
        self.assertTrue(source.is_file())
        for lang in ("ko", "en"):
            with self.subTest(lang=lang):
                p = MEDIA / f"space-atlas-ncase-{lang}.png"
                b = p.read_bytes()
                self.assertGreater(len(b), 16000)
                self.assertEqual(b[:8], bytes([137, 80, 78, 71, 13, 10, 26, 10]))
                self.assertEqual(struct.unpack(">II", b[16:24]), (1200, 630))


if __name__ == "__main__":
    unittest.main()

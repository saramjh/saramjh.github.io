"""Space Atlas educator-source routes remain reachable from its portfolio hub."""
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]
PAIRS = ("space-atlas-ncase-programs", "space-atlas-share-my-lesson")


class SpaceAtlasPortfolioEducatorLinks(unittest.TestCase):
    def test_existing_english_and_korean_source_notes_are_linked_once(self):
        hub = (ROOT / "_projects" / "space-atlas.md").read_text("utf8")
        for prefix in PAIRS:
            for lang in ("en", "ko"):
                slug = f"{prefix}-{lang}"
                with self.subTest(slug=slug):
                    self.assertEqual(hub.count(f"](/{slug}/)"), 1)
                    posts = list((ROOT / "_posts" / slug).glob("*.md"))
                    self.assertEqual(len(posts), 1)
                    article = posts[0].read_text("utf8")
                    self.assertIn(f"permalink: /{slug}/", article)
                    self.assertIn(f"lang: {lang}", article)
                    self.assertIn("published: true", article)

    def test_external_achievement_claims_remain_limited(self):
        hub = (ROOT / "_projects" / "space-atlas.md").read_text("utf8")
        self.assertIn("https://ncase.org/programs/", hub)
        self.assertIn("They do not establish school endorsement, classroom adoption or learning outcomes.", hub)
        self.assertIn("The [Korean activity note](/space-atlas-share-my-lesson-ko/)", hub)


if __name__ == "__main__":
    unittest.main()

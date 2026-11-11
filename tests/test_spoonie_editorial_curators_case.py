"""Source-bound bilingual release contract for Spoonie's public editorial directory."""

from pathlib import Path
import re
import unittest
import xml.etree.ElementTree as ET

ROOT = Path(__file__).resolve().parents[1]
BASE = "spoonie-editorial-curators"


class SpoonieEditorialDirectoryArticleTest(unittest.TestCase):
    def test_bilingual_localized_original_articles(self):
        texts = {}
        for language, counterpart in (("ko", "en"), ("en", "ko")):
            slug = f"{BASE}-{language}"
            post = ROOT / "_posts" / slug / f"2026-11-11-{slug}.md"
            text = post.read_text(encoding="utf-8")
            texts[language] = text

            self.assertTrue(text.startswith("---\n"))
            self.assertIn(f"permalink: /{slug}/", text)
            self.assertIn(f"image: /{slug}/spoonie-curator-flow.svg", text)
            self.assertIn(f"lang: {language}", text)
            self.assertIn(f"alternate_lang: {counterpart}", text)
            self.assertIn(f"alternate_url: /{BASE}-{counterpart}/", text)
            self.assertIn(f"](/{BASE}-{counterpart}/)", text)
            self.assertIn("published: true", text)
            self.assertIn("https://github.com/saramjh/spoonie/pull/16", text)
            self.assertIn("https://spoonie.kr/curators", text)
            self.assertIn("noindex", text)
            self.assertIn("18", text)
            self.assertNotIn("\ufffd", text)
            self.assertNotIn("????", text)
            self.assertGreater(len(text), 1800)
        self.assertRegex(texts["ko"], r"[가-힣]{3,}")
        self.assertNotEqual(texts["ko"], texts["en"])

    def test_two_distinct_first_party_diagrams_have_accessible_metadata(self):
        visuals = []
        for language in ("ko", "en"):
            image = (
                ROOT / "_posts" / f"{BASE}-{language}" / "spoonie-curator-flow.svg"
            )
            svg = image.read_text(encoding="utf-8")
            parsed = ET.fromstring(svg)
            self.assertEqual(parsed.attrib["width"], "1280")
            self.assertEqual(parsed.attrib["height"], "600")
            self.assertEqual(parsed.attrib["role"], "img")
            self.assertIn('aria-labelledby="title desc"', svg)
            self.assertIn("18", svg)
            self.assertIn("10", svg)
            self.assertIn("4", svg)
            self.assertNotIn("\ufffd", svg)
            visuals.append(svg)
        self.assertNotEqual(*visuals)

    def test_no_recycled_publisher_media_or_private_profile_ids(self):
        for language in ("ko", "en"):
            slug = f"{BASE}-{language}"
            text = (ROOT / "_posts" / slug / f"2026-11-11-{slug}.md").read_text(
                encoding="utf-8"
            )
            self.assertEqual(text.count("<figure>"), 1)
            self.assertEqual(text.count("<figcaption>"), 1)
            self.assertNotIn("<script", text)
            self.assertNotIn("followers: ", text.lower())
            self.assertFalse(re.search(r"/profile/[a-f0-9]{8}", text))
            self.assertIn("/portfolio/spoonie/", text)


if __name__ == "__main__":
    unittest.main()

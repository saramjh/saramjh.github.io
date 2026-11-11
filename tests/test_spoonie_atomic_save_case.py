"""Native regression contract: Spoonie PR25 first-party atomic save case."""

from pathlib import Path
import unittest
import xml.etree.ElementTree as ET

ROOT=Path(__file__).resolve().parents[1]

class SpoonieAtomicSaveCaseTest(unittest.TestCase):
    def test_two_bilingual_original_posts_have_source_and_boundaries(self):
        docs={}
        for lang,alt in (("ko","en"),("en","ko")):
            slug=f"spoonie-atomic-poll-data-{lang}"
            post=ROOT/"_posts"/slug/f"2026-11-11-{slug}.md"
            text=post.read_text(encoding="utf8")
            docs[lang]=text
            for token in (f"permalink: /{slug}/", f"lang: {lang}",
                          f"alternate_lang: {alt}",
                          f"alternate_url: /spoonie-atomic-poll-data-{alt}/",
                          "published: true",
                          "https://github.com/saramjh/spoonie/pull/25",
                          f"image: /{slug}/spoonie-atomic-flow.svg",
                          "save_item_with_poll_atomic", "media_cleanup_pending",
                          "363", "82", "SECURITY INVOKER"):
                self.assertIn(token,text)
            self.assertIn(f"](/spoonie-atomic-poll-data-{alt}/)",text)
            self.assertNotIn("\ufffd",text)
            self.assertNotIn("????",text)
            self.assertGreater(len(text),2100)
        self.assertNotEqual(docs["ko"],docs["en"])
        self.assertRegex(docs["ko"],r"[가-힣]{3,}")

    def test_distinct_accessible_original_svg_for_each_language(self):
        images=[]
        for lang in ("ko","en"):
            slug=f"spoonie-atomic-poll-data-{lang}"
            src=(ROOT/"_posts"/slug/"spoonie-atomic-flow.svg").read_text(encoding="utf8")
            tree=ET.fromstring(src)
            self.assertEqual(tree.attrib.get("width"),"1280")
            self.assertEqual(tree.attrib.get("height"),"650")
            self.assertEqual(tree.attrib.get("role"),"img")
            self.assertIn('aria-labelledby="title desc"',src)
            self.assertNotIn("\ufffd",src)
            self.assertNotIn("????",src)
            images.append(src)
        self.assertNotEqual(images[0],images[1])

    def test_no_false_usage_or_secrets_in_public_article(self):
        for lang in ("ko","en"):
            slug=f"spoonie-atomic-poll-data-{lang}"
            text=(ROOT/"_posts"/slug/f"2026-11-11-{slug}.md").read_text(encoding="utf8")
            self.assertIn("<figure>",text)
            self.assertIn("<figcaption>",text)
            self.assertNotIn("SUPABASE_SECRET_KEY=",text)
            self.assertNotIn("service_role=",text)
            self.assertNotIn("access_token=",text)
            self.assertNotIn("/profile/4e0370b9",text)
            self.assertIn("/portfolio/spoonie/",text)
            self.assertIn(f"/spoonie-live-polls-{lang}/",text)

if __name__=="__main__":
    unittest.main()

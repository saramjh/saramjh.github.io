"""Regression checks for the bilingual Spoonie PR #39 privacy case study."""
from pathlib import Path
import struct
import unittest
import xml.etree.ElementTree as ET

ROOT = Path(__file__).resolve().parents[1]
COMMIT = "https://github.com/saramjh/spoonie/commit/34603198d682a148e370c78c052ee139dd19b0a2"
PR = "https://github.com/saramjh/spoonie/pull/39"
NS = {"svg": "http://www.w3.org/2000/svg"}

class SpoonieBookmarkPrivacyCaseTest(unittest.TestCase):
    def test_bilingual_posts_keep_metadata_sources_and_owner_scope(self):
        docs = {}
        for lang, alt in (("ko", "en"), ("en", "ko")):
            slug = f"spoonie-bookmark-privacy-boundary-{lang}"
            post = ROOT / "_posts" / slug / f"2026-11-15-{slug}.md"
            body = post.read_text(encoding="utf-8")
            docs[lang] = body
            for token in (
                f"permalink: /{slug}/",
                f"lang: {lang}",
                f"alternate_lang: {alt}",
                f"alternate_url: /spoonie-bookmark-privacy-boundary-{alt}/",
                f"image: /{slug}/bookmark-privacy-boundary-og.png",
                "image_width: 1200",
                "image_height: 630",
                "published: true",
                PR,
                COMMIT,
                "public.bookmarks",
                "auth.uid()",
                "get_explore",
                "get_recipe_activity",
                "HTTP 401",
                "USING",
                "WITH CHECK",
            ):
                self.assertIn(token, body)
            self.assertIn(f"](/spoonie-bookmark-privacy-boundary-{alt}/)", body)
            self.assertIn("<figure>", body)
            self.assertIn("<figcaption>", body)
            self.assertEqual(body.count(chr(96) * 3), 2)
            self.assertNotIn(chr(92) + chr(96), body)
            self.assertNotIn(chr(0xfffd), body)
            self.assertNotIn("????", body)
            self.assertNotIn("service_role=", body)
            self.assertNotIn("access_token=", body)
            self.assertGreater(len(body), 2600)
        self.assertNotEqual(docs["ko"], docs["en"])
        self.assertRegex(docs["ko"], r"[가-힣]{3,}")

    def test_each_language_has_distinct_accessible_svg_and_og_png(self):
        svgs = []
        for lang in ("ko", "en"):
            slug = f"spoonie-bookmark-privacy-boundary-{lang}"
            folder = ROOT / "_posts" / slug
            svg = (folder / "bookmark-privacy-boundary.svg").read_text(encoding="utf-8")
            root = ET.fromstring(svg)
            self.assertEqual(root.attrib.get("width"), "1200")
            self.assertEqual(root.attrib.get("height"), "630")
            self.assertEqual(root.attrib.get("role"), "img")
            self.assertEqual(root.attrib.get("aria-labelledby"), "title desc")
            self.assertIsNotNone(root.find("svg:title", NS))
            self.assertIsNotNone(root.find("svg:desc", NS))
            for term in ("public.bookmarks", "auth.uid()", "get_explore", "get_recipe_activity"):
                self.assertIn(term, svg)
            self.assertNotIn(chr(0xfffd), svg)
            self.assertNotIn("????", svg)
            svgs.append(svg)

            png = (folder / "bookmark-privacy-boundary-og.png").read_bytes()
            self.assertTrue(png.startswith(bytes.fromhex("89504e470d0a1a0a")))
            self.assertGreater(len(png), 12000)
            self.assertEqual(struct.unpack(">II", png[16:24]), (1200, 630))
        self.assertNotEqual(svgs[0], svgs[1])

    def test_scope_and_limit_are_not_overstated(self):
        ko = (ROOT / "_posts/spoonie-bookmark-privacy-boundary-ko/2026-11-15-spoonie-bookmark-privacy-boundary-ko.md").read_text(encoding="utf-8")
        en = (ROOT / "_posts/spoonie-bookmark-privacy-boundary-en/2026-11-15-spoonie-bookmark-privacy-boundary-en.md").read_text(encoding="utf-8")
        self.assertIn("실제 회원 두 계정", ko)
        self.assertIn("two real member accounts", en)
        self.assertIn("내려받지는 않았다", ko)
        self.assertIn("transferred no bookmark rows", en)
        self.assertNotIn("user adoption", en.lower())
        self.assertNotIn("이용자 증가", ko)

    def test_project_case_study_links_to_the_database_boundary_note(self):
        case = (ROOT / "_projects/spoonie.md").read_text(encoding="utf-8")
        for token in (
            "PR #39",
            "writing_url: /spoonie-bookmark-privacy-boundary-en/",
            "20261113054444",
            "HTTP 401",
            "/spoonie-bookmark-privacy-boundary-en/",
            "/spoonie-bookmark-privacy-boundary-ko/",
        ):
            self.assertIn(token, case)

if __name__ == "__main__":
    unittest.main()

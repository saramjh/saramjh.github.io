"""Verify the actual bilingual developer case and its first-party diagram."""
import unittest
from pathlib import Path
from xml.etree import ElementTree
ROOT = Path(__file__).resolve().parents[1]
IMAGE = "/assets/img/dev-spoonie-sitemap-xml-20261111/xml-image-url-before-after.svg"
class SpoonieSitemapXmlCaseTest(unittest.TestCase):
    def test_diagram_xml_well_formed(self):
        diagram=ROOT/IMAGE.lstrip("/")
        root=ElementTree.parse(diagram).getroot()
        self.assertTrue(root.tag.endswith("svg"))
        self.assertIn("&amp;amp;",diagram.read_text(encoding="utf8"))
    def test_og_png_matches_illustration_size(self):
        file=ROOT/"assets/img/dev-spoonie-sitemap-xml-20261111/xml-image-url-before-after-og.png"
        data=file.read_bytes()
        self.assertEqual(data[:8],bytes.fromhex("89504e470d0a1a0a"))
        self.assertEqual(int.from_bytes(data[16:20],"big"),1200)
        self.assertEqual(int.from_bytes(data[20:24],"big"),620)

    def test_source_and_limits_in_bilingual_notes(self):
        for lang in ("ko","en"):
            with self.subTest(lang=lang):
                slug=f"spoonie-sitemap-xml-image-escaping-{lang}"
                text=(ROOT/"_posts"/slug/f"2026-11-11-{slug}.md").read_text(encoding="utf8")
                for part in ("published: true","https://github.com/saramjh/spoonie/pull/29","https://spoonie.kr/sitemap.xml","xml.etree.ElementTree","689","872","2026-11-11",IMAGE,"resolveSitemap","&amp;"):
                    self.assertIn(part,text)
                self.assertNotIn("???",text)
                self.assertNotIn("\ufffd",text)
                self.assertNotIn("my wife",text.lower())
                self.assertIn("색인 증가나 검색 유입 증가" if lang=="ko" else "does not establish indexing",text)
    def test_english_context_link_reaches_a_real_published_english_post(self):
        case = ROOT / "_posts/spoonie-sitemap-xml-image-escaping-en/2026-11-11-spoonie-sitemap-xml-image-escaping-en.md"
        text = case.read_text(encoding="utf8")
        target = "/spoonie-disquiet-first-record-en/"
        self.assertIn("[my English note on Spoonie's first-record problem](" + target + ")", text)
        self.assertNotIn("/spoonie-social-cooking-early-users-en/", text)
        target_file = ROOT / "_posts/spoonie-disquiet-first-record-en/2026-11-11-spoonie-disquiet-first-record-en.md"
        body = target_file.read_text(encoding="utf8")
        self.assertIn("permalink: " + target, body)
        self.assertIn("lang: en", body)
        self.assertIn("published: true", body)

if __name__=="__main__":
    unittest.main()

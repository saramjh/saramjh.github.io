import unittest
import xml.etree.ElementTree as ET
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SLUG = "ga4-deployment-report-window"
SOURCE_LINKS = (
    "https://developers.google.com/analytics/devguides/reporting/data/v1/basics",
    "https://support.google.com/analytics/answer/11198161",
    "https://support.google.com/analytics/answer/9216061",
)

def load_post(lang):
    slug = f"{SLUG}-{lang}"
    p = ROOT / "_posts" / slug / f"2026-11-10-{slug}.md"
    source = p.read_text(encoding="utf-8")
    assert source.startswith("---\n"), p
    raw, body = source.split("---", 2)[1:]
    meta = {}
    for line in raw.splitlines():
        if ":" in line:
            k, v = line.split(":", 1)
            meta[k.strip()] = v.strip().strip('"')
    return meta, body

class ReleaseContract(unittest.TestCase):
    def test_bilingual_frontmatter_and_reciprocal_urls(self):
        ko, kobody = load_post("ko")
        en, enbody = load_post("en")
        for lang, data, body, other in (("ko", ko, kobody, en), ("en", en, enbody, ko)):
            self.assertEqual(data["lang"], lang)
            self.assertEqual(data["date"], "2026-11-10")
            self.assertEqual(data["published"], "true")
            self.assertEqual(data["layout"], "default")
            self.assertEqual(data["permalink"], f"/{SLUG}-{lang}/")
            self.assertEqual(data["alternate_url"], other["permalink"])
            self.assertEqual(data["alternate_lang"], other["lang"])
            self.assertIn(other["permalink"], body)
            self.assertGreater(len(data["title"]), 14)
            self.assertGreater(len(data["description"]), 25)
            self.assertEqual(body.count("\n## "), 3)
            self.assertNotIn("\n# ", body)
            self.assertIn(f"/portfolio-evidence-release-qa-{lang}/", body)

    def test_source_accurate_numbers_and_uncertainty(self):
        for lang in ("ko", "en"):
            _, body = load_post(lang)
            for exact in ("21:20:55", "21:38:17", "23:45", "2026110919", "Asia/Seoul"):
                self.assertIn(exact, body)
            for url in SOURCE_LINKS:
                self.assertIn(url, body)
            self.assertNotIn("456806471", body)
            self.assertIn("https://www.threads.com/@devtestudinidae/post/DfgMbvdkni7", body)
            self.assertIn("runReport", body)
            if lang == "ko":
                self.assertIn("0행", body)
                self.assertIn("0명", body)
            else:
                self.assertIn("zero rows", body)
                self.assertIn("zero visitors", body)

    def test_original_accessible_localized_visual(self):
        namespace = "{http://www.w3.org/2000/svg}"
        for lang in ("ko", "en"):
            metadata, body = load_post(lang)
            svg_image = f"/assets/img/dev-ga4-report-window-20261110/timeline-{lang}.svg"
            social_image = f"/assets/img/dev-ga4-report-window-20261110/timeline-{lang}-og.png"
            self.assertEqual(metadata["image"], social_image)
            self.assertEqual(metadata["image_width"], "1200")
            self.assertEqual(metadata["image_height"], "630")
            self.assertIn(svg_image, body)
            self.assertIn('alt="', body)
            self.assertIn("<figcaption>", body)
            path = ROOT / svg_image.lstrip("/")
            xml = ET.parse(path).getroot()
            self.assertEqual(xml.attrib["viewBox"], "0 0 1200 620")
            self.assertIsNotNone(xml.find(f"{namespace}title"))
            self.assertIsNotNone(xml.find(f"{namespace}desc"))
            svg = path.read_text(encoding="utf-8")
            self.assertNotIn("<script", svg.lower())
            self.assertNotIn("<image", svg.lower())

            png = (ROOT / social_image.lstrip("/")).read_bytes()
            self.assertEqual(png[:8], b"\x89PNG\r\n\x1a\n")
            self.assertEqual(png[12:16], b"IHDR")
            self.assertEqual(
                tuple(int.from_bytes(png[i:i + 4], "big") for i in (16, 20)),
                (1200, 630),
            )
            self.assertEqual(png[24:26], b"\x08\x02")  # 8-bit RGB

if __name__ == "__main__":
    unittest.main()

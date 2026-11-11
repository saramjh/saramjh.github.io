"""Exact first-party EUSci card media source and bilingual article wiring."""
from pathlib import Path
import hashlib
import unittest

ROOT = Path(__file__).resolve().parents[1]
FOLDER = ROOT / "assets/images/dev/eusci-20261111"
FILES = {
    "card-01.jpg": "7edf2ec62ff630cabb350897c3dcffa9593b078a337a1cf71e16b4aca4a6a7ea",
    "card-02.jpg": "44dd00153ce6e7d2b819847e07bdcd30717646c340a91c99ac78bf5f73882632",
    "card-03.jpg": "594ca8f8949ead0392c71c4fe17970dcd5aa7720f4b3fadea63a5272c89fbc3a",
}

class OriginalIllustrationTests(unittest.TestCase):
    def test_source_media_exact_bytes(self):
        for name, digest in FILES.items():
            data = (FOLDER / name).read_bytes()
            self.assertEqual(hashlib.sha256(data).hexdigest(), digest)
            self.assertTrue(data.startswith(bytes.fromhex("ffd8ff")), name)
            self.assertTrue(data.endswith(bytes.fromhex("ffd9")), name)

    def test_two_existing_article_paths_reference_all_three_original_cards(self):
        for language in ("ko", "en"):
            post=ROOT / f"_posts/space-atlas-eusci-diagrams-{language}/2026-11-11-space-atlas-eusci-diagrams-{language}.md"
            body=post.read_text(encoding="utf8")
            self.assertIn("https://eusci.org.uk/2026/11/10/three-space-diagrams-three-missing-clues/",body)
            for name in FILES:
                url=f"/assets/images/dev/eusci-20261111/{name}"
                self.assertIn(f'<img src="{url}"',body)
                self.assertEqual(body.count(f'<img src="{url}"'),1)
            self.assertEqual(body.count('class="eusci-original-visuals"'),1)
            self.assertIn("loading=\"lazy\"",body)

if __name__=="__main__":
    unittest.main()

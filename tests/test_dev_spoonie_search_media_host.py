"""Source-bound hosting proof for original Dev media."""
from pathlib import Path
import hashlib
import re
import unittest

ROOT=Path(__file__).resolve().parents[1]
BASE=ROOT/"assets/img/dev-spoonie-search-pr31-instagram-20261112"
PAGE=ROOT/"media/dev-spoonie-search-pr31/index.md"
EXPECTED={
"card-01.jpg":"7adb2215d95c2f858b2aaf304b9c5a05ff81b6a88ae2c931460aead3f412f5e7",
"card-02.jpg":"1278808b9c95b264a9ab8871332c82c561ff1a8cd0cd5b614bf0368dffbab45e",
"card-03.jpg":"c91f38f73ea6e8d525b3279d8715c94f05f4be77324046353ac225986b4dac4e",
"card-04.jpg":"b5ddb1360b55a0107e59c0917e6787d9ca91de32651f41d7b31c27f04ac58bca",
}

class OriginalDevSearchMediaTest(unittest.TestCase):
    def test_exact_media_hashes(self):
        self.assertEqual({p.name for p in BASE.iterdir()},set(EXPECTED))
        for name,sha in EXPECTED.items():
            data=(BASE/name).read_bytes()
            self.assertTrue(data.startswith(bytes.fromhex("ffd8ff")))
            self.assertEqual(hashlib.sha256(data).hexdigest(),sha)
    def test_provenance_page_and_source_links(self):
        doc=PAGE.read_text("utf8")
        for source in (
            "permalink: /media/dev-spoonie-search-pr31/",
            'robots: "noindex, follow"',
            "sitemap: false",
            "https://github.com/saramjh/spoonie/pull/31",
            "/spoonie-search-discovery-en/",
            "/spoonie-search-discovery-ko/",
            "https://spoonie.kr/search",
            "not screenshots",
            "Real usage outcomes are not measured here",
        ):
            self.assertIn(source,doc)
        for name in EXPECTED:
            self.assertEqual(doc.count("/assets/img/dev-spoonie-search-pr31-instagram-20261112/"+name),1)
        self.assertEqual(len(re.findall(r"<img ",doc)),4)
        self.assertNotIn("\ufffd",doc)
        self.assertNotIn("????",doc)

if __name__=="__main__":
    unittest.main()

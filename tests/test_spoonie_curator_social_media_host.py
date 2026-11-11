"""First-party Dev media must remain linked and accurately labeled."""
import unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
PREFIX="/assets/img/dev-spoonie-curators-ig-20261111/"
class CuratorMediaHostTest(unittest.TestCase):
 def test_four_jpeg_assets_are_complete(self):
  for i in range(1,5):
   data=(ROOT/(PREFIX.lstrip("/")+f"card-{i:02}.jpg")).read_bytes()
   self.assertGreater(len(data),90000)
   self.assertEqual(data[:3],bytes.fromhex("ffd8ff"))
   self.assertEqual(data[-2:],bytes.fromhex("ffd9"))
 def test_bilingual_pages_link_all_four_and_disclose_original_diagrams(self):
  for lang in ("ko","en"):
   s=(ROOT/f"_posts/spoonie-editorial-curators-{lang}/2026-11-11-spoonie-editorial-curators-{lang}.md").read_text(encoding="utf8")
   for i in range(1,5):self.assertIn(PREFIX+f"card-{i:02}.jpg",s)
   self.assertIn("noindex",s)
   self.assertIn("복제한 이미지는 아니다" if lang=="ko" else "not the actual curators",s)
   self.assertNotIn("???",s)
   self.assertNotIn("\ufffd",s)

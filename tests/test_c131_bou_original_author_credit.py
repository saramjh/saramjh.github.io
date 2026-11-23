"""Original publisher author-credited BOU release: source-bound, bilingual, one event."""
from pathlib import Path
import re
import unittest

ROOT = Path(__file__).resolve().parents[1]
EN = ROOT / "_posts/koreaves-bou-when-records-become-maps-en/2026-11-23-koreaves-bou-when-records-become-maps-en.md"
KO = ROOT / "_posts/koreaves-bou-when-records-become-maps-ko/2026-11-23-koreaves-bou-when-records-become-maps-ko.md"
LEDGER = ROOT / "_data/recognitions.yml"
URL = "https://bou.org.uk/blog-oh-when-records-become-maps/"
SOURCE_ID = "bou-when-records-become-maps"
IMAGE = "/assets/images/portfolio/koreaves-gis.jpg"

class OriginalBOUBylineReleaseTests(unittest.TestCase):
    def test_exact_one_original_bou_publication_source(self):
        blocks = re.split(r"(?m)^- id: ", LEDGER.read_text("utf8"))[1:]
        self.assertEqual(len(blocks), 32)
        self.assertEqual(len({b.splitlines()[0] for b in blocks}), 32)
        single = [b for b in blocks if b.startswith(SOURCE_ID + "\n")]
        self.assertEqual(len(single),1)
        row=single[0]
        for phrase in [
           "  project: koreaves","  type: publication","  status: confirmed",
           "  date: 2026-11-23",
           "  source: \"British Ornithologists' Union\"",
           "  title: \"When Records Become Maps\"",
           "  url: \""+URL+"\"",
           "  case_en: \"/koreaves-bou-when-records-become-maps-en/\"",
           "  case_ko: \"/koreaves-bou-when-records-become-maps-ko/\"",
           "  verified_at: \"2026-11-23\""
        ]:self.assertIn(phrase,row)
        self.assertIn("Jihun Oh",row)
        self.assertIn("No peer review or partnership implied",row)
        self.assertNotIn("  image:",row)
    def test_fully_bilingual_unique_canonical_and_backlink(self):
        for lang,path,other in [
          ("en",EN,"/koreaves-bou-when-records-become-maps-ko/"),
          ("ko",KO,"/koreaves-bou-when-records-become-maps-en/")]:
            s=path.read_text("utf8")
            self.assertIn("lang: "+lang,s)
            self.assertIn("alternate_url: "+other,s)
            self.assertIn("permalink: /koreaves-bou-when-records-become-maps-"+lang+"/",s)
            self.assertIn("date: 2026-11-23",s)
            self.assertIn("last_modified_at: 2026-11-23",s)
            self.assertIn("seo:",s)
            self.assertIn(URL,s)
            self.assertIn(IMAGE,s)
            self.assertIn("https://koreaves.com/methodology/",s)
            self.assertIn("https://koreaves.com/sources/",s)
            self.assertIn("https://koreaves.com/gis/",s)
            self.assertIn("Jihun Oh",s)
            self.assertNotIn("\ufffd",s)
            self.assertNotIn("????",s)
            self.assertGreater(len(s),2500)
    def test_public_first_party_og_asset_not_publisher_media(self):
        self.assertTrue((ROOT / IMAGE.lstrip("/")).is_file())
        for p in [EN,KO]:
            s=p.read_text("utf8")
            self.assertEqual(s.count(IMAGE),2)
            self.assertNotIn("bou.org.uk/wp-content/uploads/",s)
            self.assertNotIn("Copyright British",s)
    def test_strict_original_no_invented_scientific_authority(self):
        en=EN.read_text("utf8"); ko=KO.read_text("utf8")
        self.assertIn("does not establish peer-reviewed scientific validation",en)
        self.assertIn("학술 동료심사",ko)
        self.assertIn("The article supplies the reasoning; the live application exposes what was implemented",en)
        self.assertIn("글과 서비스를 나란히 보여줄 수 있다",ko)
    def test_original_31_source_ids_preserved(self):
        rows=re.findall(r"(?m)^- id: ([a-z0-9-]+)$",LEDGER.read_text("utf8"))
        self.assertEqual(len(rows),32)
        self.assertIn("daily-korea-suncheon-koreaves-citation",rows)
        self.assertIn("one-earth-koreaves-feature",rows)
        self.assertIn("unsustainable-koreaves-bird-map",rows)
        self.assertEqual(rows.count(SOURCE_ID),1)

if __name__=="__main__":
 unittest.main()

"""Keep a pre-existing external resource mention precisely attributed, without adding a fictitious outcome."""
from pathlib import Path
import re
import unittest

ROOT=Path(__file__).resolve().parents[1]
EN=ROOT/"_posts/space-atlas-worldschooling-guide-en/2026-11-13-space-atlas-worldschooling-guide-en.md"
KO=ROOT/"_posts/space-atlas-worldschooling-guide-ko/2026-11-13-space-atlas-worldschooling-guide-ko.md"
LEDGER=ROOT/"_data/recognitions.yml"
SOURCE_URL="https://worldlytribe.com/the-complete-guide-to-online-programs-for-homeschoolers-worldschoolers/"

class WorldlyTribeAttributionTests(unittest.TestCase):
    def test_existing_public_case_only_and_bilingual_truth_boundary(self):
        en=EN.read_text("utf8")
        ko=KO.read_text("utf8")
        for text,language,alt in ((en,"en","ko"),(ko,"ko","en")):
            self.assertIn("lang: "+language,text)
            self.assertIn("alternate_lang: "+alt,text)
            self.assertIn("date: 2026-11-13",text)
            self.assertIn("modified: 2026-11-23",text)
            self.assertIn(SOURCE_URL,text)
            self.assertIn("/assets/images/portfolio/space-atlas-moon-phases.png",text)
            self.assertNotIn("????",text)
            self.assertNotIn("\ufffd",text)
        self.assertIn('"a brilliant habit to teach."',en)
        self.assertIn("editorial assessment",en)
        self.assertIn("not evidence",en)
        self.assertIn("NASA or ESA",en)
        self.assertIn("NASA·ESA",ko)
        self.assertIn("외부",ko)
        self.assertIn("근거는 아니다",ko)

    def test_original_public_record_count_and_type_unchanged(self):
        source=LEDGER.read_text("utf8")
        chunks=re.split(r"(?m)^- id: ",source)[1:]
        self.assertEqual(len(chunks),30)
        ids=[x.splitlines()[0].strip() for x in chunks]
        self.assertEqual(len(set(ids)),30)
        found=[x for x in chunks if x.startswith("worldlytribe-space-atlas-worldschooling\n")]
        self.assertEqual(len(found),1)
        block=found[0]
        self.assertIn("  project: space-atlas",block)
        self.assertIn("  type: listing",block)
        self.assertIn("  status: confirmed",block)
        self.assertIn("  url: \""+SOURCE_URL+"\"",block)
        self.assertIn("source links",block)
        self.assertIn("실제 사용을 입증하지 않습니다",block)
        self.assertNotIn("  date: ",block)
        self.assertEqual(source.count("  detail_ko: "),30)

if __name__=="__main__": unittest.main()

from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]
EN = ROOT / "_posts/en-impeccable-review-ai-ui-design/2026-10-05-en-impeccable-review-ai-ui-design.md"
KO = ROOT / "_posts/impeccable-review-ai-ui-design/2026-10-05-impeccable-review-ai-ui-design.md"

class CurrentImpeccableCliSource(unittest.TestCase):
    def test_dated_primary_source_and_run_mode_distinction(self):
        cases = [(EN, "### November 2026 CLI setup note"), (KO, "### 2026년 11월 CLI 설정 확인")]
        for file, section_header in cases:
            body = file.read_text(encoding="utf-8")
            self.assertEqual(body.count(section_header), 1)
            segment = body.split(section_header, 1)[1].split("\n## ",1)[0]
            for required in (
                "2026-11-16", "4.9.2", "https://github.com/pbakaus/impeccable/releases",
                "https://github.com/pbakaus/impeccable",
                "npx impeccable --version", "npx impeccable detect --list-rules",
                "npx impeccable detect", "/hooks", "4.1.0",
            ):
                with self.subTest(file=file.name, required=required):
                    self.assertIn(required, segment)
            self.assertNotIn("\ufffd", segment)
            self.assertNotIn("????", segment)

    def test_historical_trial_and_bilingual_metadata_preserved(self):
        en = EN.read_text(encoding="utf-8")
        ko = KO.read_text(encoding="utf-8")
        self.assertIn('"check:design": "npx --yes impeccable@4.1.0 detect app storefront extensions/profit-scratch-widget"', en)
        self.assertIn('alternate_url: /impeccable-review-ai-ui-design/', en)
        self.assertIn('alternate_url: /en-impeccable-review-ai-ui-design/', ko)
        self.assertNotIn("61 deterministic rules", en)
        self.assertNotIn("61개의 deterministic rule", ko)

if __name__=="__main__":
    unittest.main()

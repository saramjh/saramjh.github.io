"""Korean recognition archive presents the exact original ledger without extra claims."""
from pathlib import Path
import re
import subprocess
import unittest

ROOT=Path(__file__).resolve().parents[1]
LEDGER=ROOT/"_data/recognitions.yml"
EN=ROOT/"portfolio/recognition/index.html"
KO=ROOT/"portfolio/recognition/ko/index.html"
INCLUDE=ROOT/"_includes/portfolio-evidence.html"


class KoreanRecognitionArchiveTests(unittest.TestCase):
    def test_all_30_records_keep_source_field_contract(self):
        source=LEDGER.read_text("utf8")
        records=re.split(r"(?m)(?=^- id: )",source)
        found=[]
        for block in records:
            if not block.startswith("- id: "):
                continue
            record_id=block.splitlines()[0].removeprefix("- id: ").strip()
            found.append(record_id)
            original_detail=re.search(r"(?m)^  detail: (.+)$",block)
            localized_detail=re.search(r"(?m)^  detail_ko: (.+)$",block)
            original_url=re.search(r'(?m)^  url: "([^"]+)"$',block)
            original_title=re.search(r"(?m)^  title: (.+)$",block)
            self.assertIsNotNone(original_detail,record_id)
            self.assertIsNotNone(localized_detail,record_id)
            self.assertIsNotNone(original_url,record_id)
            self.assertIsNotNone(original_title,record_id)
            self.assertTrue(original_url.group(1).startswith("https://"),record_id)
            self.assertNotIn("\ufffd",localized_detail.group(1))
            self.assertRegex(localized_detail.group(1),r"[가-힣]")
            self.assertIn("  status: confirmed",block)
        self.assertEqual(len(found),31)
        self.assertEqual(len(set(found)),31)
        self.assertEqual(source.count("  detail_ko: "),31)
        self.assertNotIn("\ufffd",source)

    def test_bilingual_route_and_hreflang(self):
        en=EN.read_text("utf8")
        ko=KO.read_text("utf8")
        self.assertIn("lang: en",en)
        self.assertIn("lang: ko",ko)
        self.assertIn("alternate_url: /portfolio/recognition/ko/",en)
        self.assertIn("alternate_url: /portfolio/recognition/",ko)
        self.assertIn("alternate_lang: en",ko)
        self.assertIn("alternate_lang: ko",en)
        self.assertIn('href="/portfolio/recognition/ko/" hreflang="ko"',en)
        self.assertIn('href="/portfolio/recognition/" hreflang="en"',ko)
        for kind in ("publication","coverage","citation","dataset_record","listing","collaboration"):
            for page in (en,ko):
                self.assertEqual(page.count('include portfolio-evidence.html type="'+kind+'"'),1)

    def test_original_external_title_url_and_dedup_guards(self):
        source=INCLUDE.read_text("utf8")
        self.assertIn('href="{{ record.url | escape }}"',source)
        self.assertIn("{{ record.title | escape }}",source)
        self.assertIn('{{ record.detail_ko | default: record.detail | escape }}',source)
        self.assertIn('href="{{ \'/portfolio/recognition/ko/\' | relative_url }}#evidence-{{ record.id | escape }}"',source)
        self.assertIn('href="{{ \'/portfolio/recognition/\' | relative_url }}#evidence-{{ record.id | escape }}"',source)
        self.assertIn("record.status == 'confirmed'",source)
        self.assertIn("aria-label=\"기록 바로가기:",source)
        self.assertIn("개발 기록:",source)
        self.assertIn("record.date | date: '%Y년 %-m월 %-d일'",source)

    def test_history_korean_count_without_external_calls(self):
        result=subprocess.run(
            ["node","tests/portfolio_archive_filter_korean_runtime.cjs"],
            cwd=ROOT,capture_output=True,text=True,timeout=15
        )
        self.assertEqual(result.returncode,0,result.stderr)
        self.assertIn("PASS KO archive filters",result.stdout)


if __name__=="__main__":
    unittest.main()

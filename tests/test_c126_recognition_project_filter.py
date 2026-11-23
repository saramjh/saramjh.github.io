"""Keep original recognition projects browsable in both languages, without editing the evidence."""
import re
import subprocess
import unittest
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
PROJECTS=("all","koreaves","space-atlas","spoonie","scratch-lottery")
class ArchiveProjectFilterTests(unittest.TestCase):
    def test_bilingual_project_filters_and_no_js_fallback(self):
        for suffix in ("portfolio/recognition/index.html","portfolio/recognition/ko/index.html"):
            page=(ROOT/suffix).read_text("utf8")
            for project in PROJECTS:
                self.assertIn('data-project-filter="'+project+'"',page)
            self.assertEqual(page.count("portfolio-evidence.html type="),6)
            self.assertIn('<ol class="folio-evidence-list"',page)
            self.assertNotIn('hidden="hidden"',page)
        include=(ROOT/"_includes/portfolio-evidence.html").read_text("utf8")
        self.assertIn('data-evidence-project="{{ record.project | escape }}"',include)
    def test_original_id_and_project_counts_not_inflated(self):
        ledger=(ROOT/"_data/recognitions.yml").read_text("utf8")
        rows=re.split(r"(?m)^- id: ",ledger)[1:]
        self.assertEqual(len(rows),32)
        projects=[re.search(r"(?m)^  project: (.+)$",r).group(1) for r in rows]
        self.assertEqual({p:projects.count(p) for p in set(projects)},{
            "koreaves":17,"space-atlas":11,"spoonie":3,"scratch-lottery":1})
        self.assertEqual(len({r.splitlines()[0] for r in rows}),32)
    def test_runtime_navigation_and_no_network(self):
        run=subprocess.run(["node","tests/portfolio_archive_project_filter_runtime.cjs"],
                           cwd=ROOT,capture_output=True,text=True,timeout=20)
        self.assertEqual(run.returncode,0,run.stderr)
        self.assertIn("PASS combined source",run.stdout)
if __name__=="__main__":unittest.main()

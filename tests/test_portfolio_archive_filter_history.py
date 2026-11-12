"""Archive filter links stay shareable without replacing the evidence ledger."""
from pathlib import Path
import subprocess
import unittest

ROOT = Path(__file__).resolve().parents[1]
ARCHIVE = ROOT / "portfolio" / "recognition" / "index.html"
RUNTIME = ROOT / "tests" / "portfolio_archive_filter_history_runtime.cjs"


class PortfolioArchiveFilterHistoryTest(unittest.TestCase):
    def test_original_evidence_filters_remain_labels_not_new_records(self):
        source = ARCHIVE.read_text(encoding="utf-8")
        for category in ("all", "publication", "listing", "dataset_record", "collaboration"):
            self.assertIn(f'data-filter="{category}"', source)
        self.assertIn('{% include portfolio-evidence.html %}', source)
        self.assertIn('aria-live="polite"', source)
        self.assertIn('id="folio-filter-empty" hidden', source)

    def test_category_hash_links_and_back_forward_restore_original_filter(self):
        result = subprocess.run(
            ["node", str(RUNTIME)], cwd=ROOT,
            capture_output=True, text=True, timeout=12
        )
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("PASS archive deep link", result.stdout)


if __name__ == "__main__":
    unittest.main()

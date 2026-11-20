"""Keep the published Sigub developer commands aligned with its original public repository.

Verified 2026-11-20: saramjh/szwagecalc public GitHub repo, package.json
contains deploy:manual (not deploy), with gh-pages present in devDependencies.
"""
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]
POST = ROOT / "_posts/pay-calculator-for-part-time-job/2025-07-08-pay-calculator-for-part-time-job.md"
ORIGINAL_REPO = "https://github.com/saramjh/szwagecalc"


class SigubGuideCommands(unittest.TestCase):
    def test_developer_setup_clones_the_original_public_repository(self):
        content = POST.read_text(encoding="utf-8")
        self.assertIn(f"git clone {ORIGINAL_REPO}.git", content)
        self.assertIn("\n    cd szwagecalc", content)
        self.assertNotIn("github.com/your-username", content)

    def test_documented_deployment_script_matches_original_package_json(self):
        content = POST.read_text(encoding="utf-8")
        self.assertIn("npm run deploy:manual", content)
        self.assertNotIn("npm run deploy\n", content)
        self.assertIn("배포 권한", content)

    def test_source_text_keeps_its_korean_not_corrupt_question_marks(self):
        content = POST.read_text(encoding="utf-8")
        self.assertNotIn("\ufffd", content)
        self.assertNotIn("????", content)
        self.assertIn("시급이요", content)


if __name__ == "__main__":
    unittest.main()

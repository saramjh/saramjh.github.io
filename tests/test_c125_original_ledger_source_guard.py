"""Prevent repeat achievement posts when an original URL is in the evidence ledger."""
import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts/check_achievement_source_coverage.py"


class OriginalLedgerCoverageTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.posts = self.root / "_posts"
        self.posts.mkdir()
        self.article = self.posts / "already.md"
        self.article.write_text("---\npermalink: /already/\nlang: en\n---\n\nhttps://example.org/unrelated\n", "utf8")
        self.ledger = self.root / "recognitions.yml"
        self.ledger.write_text(
            "- id: existing-source\n"
            "  project: koreaves\n"
            "  type: listing\n"
            "  status: confirmed\n"
            '  url: "https://example.org/real-source/"\n', "utf8"
        )

    def check(self, source, *, ledger=True):
        cmd = [sys.executable, str(SCRIPT), "--posts-root", str(self.posts),
               "--source-url", source]
        if ledger:
            cmd += ["--recognitions-file", str(self.ledger)]
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=15)
        return result.returncode, json.loads(result.stdout)

    def test_existing_ledger_record_without_blog_is_protected(self):
        code, data = self.check("https://www.example.org/real-source/?utm_campaign=test")
        self.assertEqual(code, 3)
        self.assertEqual(data["status"], "ALREADY_COVERED_REVIEW_REQUIRED")
        self.assertEqual(data["scannedRecognitionRecords"], 1)
        self.assertEqual(data["sources"][0]["matches"], [])
        self.assertEqual(data["sources"][0]["ledgerMatches"][0]["recordId"], "existing-source")
        self.assertEqual(data["sources"][0]["ledgerMatches"][0]["recordType"], "listing")
        self.assertRegex(data["recognitionsLedgerSha256"], r"^[0-9a-f]{64}$")
        self.assertFalse(data["publicationAuthorized"])

    def test_original_31_ledger_records_are_read(self):
        self.ledger = ROOT / "_data/recognitions.yml"
        code, data = self.check("https://www.bearybirding.com/resources/")
        self.assertEqual(code, 3, data)
        self.assertEqual(data["scannedRecognitionRecords"], 31)
        self.assertEqual(data["sources"][0]["ledgerMatches"][0]["recordId"], "beary-resource")
        self.assertEqual(data["sources"][0]["matches"], [])

    def test_ledger_and_existing_post_matches_both_returned(self):
        self.article.write_text(
            "---\npermalink: /already/\nlang: en\n---\n\n"
            "Source: https://example.org/real-source/\n", "utf8"
        )
        code, data = self.check("https://example.org/real-source")
        self.assertEqual(code, 3)
        self.assertEqual(len(data["sources"][0]["matches"]), 1)
        self.assertEqual(len(data["sources"][0]["ledgerMatches"]), 1)

    def test_meaningful_query_is_not_collapsed(self):
        self.ledger.write_text(
            "- id: one\n  type: listing\n  status: confirmed\n"
            '  url: "https://example.org/resource?id=1"\n', "utf8"
        )
        code, data = self.check("https://example.org/resource?id=2")
        self.assertEqual(code, 0)
        self.assertEqual(data["status"], "NOT_IN_SCANNED_POSTS_OR_LEDGER_UNVERIFIED")
        self.assertFalse(data["publicationAuthorized"])

    def test_missing_malformed_and_duplicate_ledger_blocks(self):
        variants = [
            (None, "MISSING_OR_SYMLINK_RECOGNITIONS_LEDGER"),
            ("- id: broken\n  type: listing\n  status: confirmed\n",
             "DUPLICATE_OR_INCOMPLETE_RECOGNITIONS_LEDGER_RECORD"),
            ("- id: duplicate\n  type: listing\n  status: confirmed\n"
             '  url: "https://example.org/x"\n'
             "- id: duplicate\n  type: listing\n  status: confirmed\n"
             '  url: "https://example.org/y"\n',
             "DUPLICATE_OR_INCOMPLETE_RECOGNITIONS_LEDGER_RECORD"),
            ("- id: quote\n  type: listing\n  status: confirmed\n"
             '  url: "https://example.org/missing-close\n',
             "MALFORMED_RECOGNITIONS_LEDGER_URL"),
            ("- id: local\n  type: listing\n  status: confirmed\n"
             '  url: "file:///etc/passwd"\n',
             "INVALID_RECOGNITIONS_LEDGER_URL"),
            ("- ids: misspelled\n  type: listing\n  status: confirmed\n"
             '  url: "https://example.org/x"\n',
             "EMPTY_OR_MALFORMED_RECOGNITIONS_LEDGER"),
        ]
        for value, expected in variants:
            with self.subTest(expected=expected):
                if value is None:
                    self.ledger.unlink(missing_ok=True)
                else:
                    self.ledger.write_text(value, "utf8")
                code, data = self.check("https://example.org/new")
                self.assertEqual(code, 2, data)
                self.assertEqual(data["status"], expected)
                self.assertFalse(data["publicationAuthorized"])
                self.assertEqual(data["nativeProviderWrites"], 0)

    def test_custom_posts_scan_legacy_compatibility_without_ledger(self):
        code, data = self.check("https://example.org/new", ledger=False)
        self.assertEqual(code, 0)
        self.assertEqual(data["status"], "NOT_IN_SCANNED_POSTS_UNVERIFIED")
        self.assertEqual(data["scannedRecognitionRecords"], 0)
        self.assertFalse(data["recognitionsLedgerScanned"])
        self.assertFalse(data["publicationAuthorized"])


if __name__ == "__main__":
    unittest.main()

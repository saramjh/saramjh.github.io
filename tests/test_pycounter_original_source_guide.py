"""Verify the historical counter guide matches the original public source tree."""
from pathlib import Path
import re
import unittest

ROOT = Path(__file__).resolve().parents[1]
POST = ROOT / "_posts/outlier-dimension-rating-counter/2025-01-21-outlier-dimension-rating-counter.md"


class OriginalPycounterGuide(unittest.TestCase):
    def setUp(self):
        self.content = POST.read_text(encoding="utf-8")

    def test_clone_enters_actual_repository_before_running_script(self):
        self.assertRegex(
            self.content,
            r"git clone https://github[.]com/saramjh/pycounter[.]git\s+"
            r"cd pycounter\s+python3 pycounter[.]py",
        )

    def test_no_nonexistent_requirements_file(self):
        self.assertNotIn("requirements.txt", self.content)
        self.assertIn("Tkinter", self.content)

    def test_main_archive_not_called_a_latest_release(self):
        self.assertIn("https://github.com/saramjh/pycounter/archive/refs/heads/main.zip", self.content)
        self.assertNotRegex(self.content, r"latest release.*main[.]zip")
        self.assertIn("source archive", self.content)

    def test_preserves_original_reference_and_utf8(self):
        self.assertIn("https://github.com/saramjh/pycounter", self.content)
        self.assertNotIn("\ufffd", self.content)
        self.assertNotIn("????", self.content)


if __name__ == "__main__":
    unittest.main()

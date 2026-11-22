"""First-party code copy reports both success and clipboard permission failure."""
from pathlib import Path
import unittest
import re

ROOT = Path(__file__).resolve().parents[1]
FOOTER = (ROOT / "_includes/footer.html").read_text(encoding="utf8")
BROWSER = (ROOT / "tests/inline_code_mobile_browser.py").read_text(encoding="utf8")


class CopyFeedbackTest(unittest.TestCase):
    def test_success_is_reported_only_after_clipboard_write(self):
        self.assertLess(FOOTER.index('await navigator.clipboard.writeText(codeText);'),
                        FOOTER.index('showCopyStatus("Copied!", true);'))
        self.assertIn('class="copy-text" aria-live="polite"', FOOTER)

    def test_failure_selects_original_code_and_reports_a_visible_action(self):
        self.assertIn('range.selectNodeContents(codeEl || pre);', FOOTER)
        self.assertIn('selection.addRange(range);', FOOTER)
        self.assertIn('Selected: Ctrl+C / ⌘C', FOOTER)
        self.assertIn('showCopyStatus(selected ?', FOOTER)
        self.assertIn('Copy unavailable', FOOTER)
        self.assertIn('showCopyStatus("Copied!", true);', FOOTER)

    def test_copy_button_status_resets_and_updates_accessible_name(self):
        self.assertIn('clearTimeout(statusReset);', FOOTER)
        self.assertIn('copyBtn.classList.toggle("copied", success);', FOOTER)
        self.assertIn('copyBtn.setAttribute("aria-label"', FOOTER)
        self.assertIn('copyStatus.textContent = "Copy";', FOOTER)

    def test_inline_script_avoids_line_comments_during_jekyll_compaction(self):
        # The production Jekyll output compacts script newlines: a JavaScript
        # // comment would swallow the next statement and break every page.
        script = re.search(
            r'<script>\s*document.addEventListener\("DOMContentLoaded"[\s\S]*?</script>',
            FOOTER,
        )
        self.assertIsNotNone(script)
        self.assertIsNone(re.search(r"(?m)^\s*//", script.group()))

    def test_original_real_chrome_suite_covers_denial_and_absence(self):
        for state in ('allowed', 'denied', 'unavailable'):
            self.assertIn(state, BROWSER)
        self.assertIn('window.getSelection().toString()', BROWSER)
        self.assertIn('document.documentElement.scrollWidth', BROWSER)


if __name__ == "__main__":
    unittest.main()

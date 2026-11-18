"""Source-graph regression for the already-used Epson article event script.

No provider call or actual URL submission occurs in these tests.
"""
import os
import subprocess
import tempfile
import unittest
from pathlib import Path

from scripts import submit_search_engines as notifier

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = "assets/js/epson-official-support-click.js"
PUBLIC_SCRIPT = "/assets/js/epson-official-support-click.js"
TAG = '<script src="/assets/js/epson-official-support-click.js" defer></script>'
ORIGINAL_JS = (ROOT / SCRIPT).read_bytes()
POSTS = {
    "_posts/epson-waste-ink-pad-reset-without-key/2026-09-15-epson-waste-ink-pad-reset-without-key.md":
        ("/epson-waste-ink-pad-reset-without-key/", "ko"),
    "_posts/en-epson-waste-ink-pad-reset-without-key/2026-09-15-en-epson-waste-ink-pad-reset-without-key.md":
        ("/en-epson-waste-ink-pad-reset-without-key/", "en"),
}


class EpsonConsumerSourceProof(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory(prefix="c868-epson-indexnow-")
        self.prev = os.getcwd()
        os.chdir(self.tmp.name)
        self.git("init", "-q")
        self.git("config", "user.name", "Fixture")
        self.git("config", "user.email", "dev-test@example.invalid")
        for path, (url, lang) in POSTS.items():
            self.write(path, f"---\npermalink: {url}\nlayout: default\nlang: {lang}\n---\nExisting original article.\n")
        self.base = self.commit("two existing articles before event JS")

    def tearDown(self):
        os.chdir(self.prev)
        self.tmp.cleanup()

    def git(self, *args):
        return subprocess.check_output(["git", *args], text=True, stderr=subprocess.PIPE).strip()

    def write(self, path, content):
        f = Path(path)
        f.parent.mkdir(parents=True, exist_ok=True)
        f.write_bytes(content if isinstance(content, bytes) else content.encode("utf-8"))

    def commit(self, message):
        self.git("add", "-A")
        self.git("commit", "-qm", message)
        return self.git("rev-parse", "HEAD")

    def with_two_consumer_js(self):
        self.write(SCRIPT, ORIGINAL_JS)
        for path in POSTS:
            p = Path(path)
            p.write_text(p.read_text(encoding="utf-8") + TAG + "\n", encoding="utf-8")
        return self.commit("Epson JS used by exactly two original articles")

    def test_exact_asset_addition_notifies_only_ko_en_and_home(self):
        after = self.with_two_consumer_js()
        self.assertEqual(notifier.changed_urls(self.base, after), sorted({
            notifier.BASE_URL + "/",
            notifier.BASE_URL + "/epson-waste-ink-pad-reset-without-key/",
            notifier.BASE_URL + "/en-epson-waste-ink-pad-reset-without-key/",
        }))

    def test_unverified_new_template_consumer_remains_broad(self):
        after = self.with_two_consumer_js()
        self.write("_includes/shared.html", TAG + "\n")
        later = self.commit("new shared include consumer")
        self.assertIsNone(notifier.changed_urls(after, later))

    def test_modified_unsupported_script_sha_remains_broad(self):
        after = self.with_two_consumer_js()
        self.write(SCRIPT, ORIGINAL_JS + b"\n// Not source-approved\n")
        later = self.commit("changed content not in known bound hash")
        self.assertIsNone(notifier.changed_urls(after, later))

    def test_unverified_new_unreferenced_asset_stays_broad(self):
        self.write(SCRIPT, ORIGINAL_JS)
        after = self.commit("new asset without a verified page consumer")
        self.assertIsNone(notifier.changed_urls(self.base, after))


if __name__ == "__main__":
    unittest.main()

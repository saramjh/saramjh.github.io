"""The pinned local Jekyll runner changes no global Ruby configuration."""
import os
from pathlib import Path
import subprocess
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts/build-blog-local.sh"


class LocalJekyllBuildTests(unittest.TestCase):
    def run_stub(self, version, action, bundle_exit=0):
        with tempfile.TemporaryDirectory(prefix="dev-jekyll-test-") as temp:
            d = Path(temp)
            ruby = d / "ruby"
            ruby.write_text("#!/bin/sh\nprintf '%s' '" + version + "'\n", encoding="utf-8")
            ruby.chmod(0o755)
            bundle = d / "bundle"
            bundle.write_text("#!/bin/sh\nexit " + str(bundle_exit) + "\n", encoding="utf-8")
            bundle.chmod(0o755)
            env = os.environ.copy()
            env["BLOG_RUBY_BIN"] = str(ruby)
            env["BLOG_BUNDLE_PATH"] = str(d / "isolated-gems")
            return subprocess.run(
                ["bash", str(SCRIPT), action],
                cwd=ROOT, env=env, capture_output=True, text=True, timeout=15
            )

    def test_scoped_path(self):
        source = SCRIPT.read_text("utf-8")
        for text in ("$repo/.ruby-version", "BUNDLE_GEMFILE", "BUNDLE_PATH", "mktemp -d"):
            self.assertIn(text, source)
        for text in ("rvm install", "brew install", "sudo ", "git clean"):
            self.assertNotIn(text, source)

    def test_wrong_ruby_fails_without_install(self):
        result = self.run_stub("9.9.9", "doctor")
        self.assertEqual(result.returncode, 2, result.stderr)
        self.assertIn("no installation attempted", result.stderr)

    def test_unknown_action_rejected(self):
        result = self.run_stub("3.4.6", "unexpected")
        self.assertEqual(result.returncode, 64, result.stderr)

    def test_missing_scoped_gems_does_not_install(self):
        result = self.run_stub("3.4.6", "build", bundle_exit=1)
        self.assertEqual(result.returncode, 4, result.stderr)
        self.assertIn("Missing scoped gems", result.stderr)


if __name__ == "__main__":
    unittest.main()

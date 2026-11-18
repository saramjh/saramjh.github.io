"""Offline IndexNow dependency proof for the source-owned portfolio JS.

No GitHub writes, actual provider submissions, or browser requests.
"""
import contextlib
import os
from pathlib import Path
import subprocess
import tempfile
import unittest
from unittest.mock import patch

from scripts import submit_search_engines as sender


BASE = sender.BASE_URL
ROOT = Path(__file__).resolve().parents[1]
BEFORE_C849 = "22baa37488094d763a6fb9c2d30b90b4c55f4606"
AFTER_C849 = "1d5e7c0c80995270e8ab9c78156f4e172383bf68"


class ScopedPortfolioJS(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(prefix="indexnow-portfolio-js-proof-")
        self.root = Path(self.temp.name)
        self.original_cwd = Path.cwd()
        os.chdir(self.root)
        self.git("init", "-q")
        self.git("config", "user.email", "fixture@example.invalid")
        self.git("config", "user.name", "Fixture")
        self.write("_config.yml", "collections:\n  projects:\n    output: true\n    permalink: /portfolio/:name/\n")
        self.write("_layouts/portfolio.html",
                   "---\nlayout: compress\n---\n"
                   '<script src="/assets/js/portfolio.js" defer></script>\n')
        self.write("_layouts/project.html", "---\nlayout: portfolio\nportfolio_ui: true\n---\n")
        self.write("_layouts/milestone.html", "---\nlayout: portfolio\nportfolio_ui: true\n---\n")
        self.write("portfolio/index.html", "---\nlayout: portfolio\npermalink: /portfolio/\n---\n")
        self.write("portfolio/recognition/index.html",
                   "---\nlayout: portfolio\npermalink: /portfolio/recognition/\n---\n")
        for slug in ("space-atlas", "koreaves", "spoonie", "sigub", "ai-agent-systems"):
            self.write(f"_projects/{slug}.md",
                       f"---\nlayout: project\nslug: {slug}\n---\n")
        for slug in ("koreaves-published-contributions-en",
                     "koreaves-published-contributions-ko",
                     "koreaves-external-resources-en",
                     "koreaves-external-resources-ko"):
            self.write(f"_posts/{slug}/2026-11-02-{slug}.md",
                       f"---\nlayout: milestone\npermalink: /{slug}/\n---\n")
        self.write("_posts/unrelated/2026-11-03-unrelated.md",
                   "---\nlayout: post\npermalink: /unrelated/\n---\n")
        self.write("assets/js/portfolio.js", "console.log('original')\n")
        self.base = self.commit("source graph")

    def tearDown(self):
        os.chdir(self.original_cwd)
        self.temp.cleanup()

    def write(self, path, text):
        p = self.root / path
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_text(text, encoding="utf8")

    def git(self, *args):
        return subprocess.check_output(
            ["git", *args], text=True, stderr=subprocess.PIPE).strip()

    def commit(self, message):
        self.git("add", "-A")
        self.git("commit", "-qm", message)
        return self.git("rev-parse", "HEAD")

    @staticmethod
    def expected():
        return sorted([
            BASE + "/portfolio/",
            BASE + "/portfolio/recognition/",
            *[BASE + "/portfolio/" + n + "/" for n in
              ("space-atlas", "koreaves", "spoonie", "sigub", "ai-agent-systems")],
            *[BASE + "/" + n + "/" for n in
              ("koreaves-published-contributions-en",
               "koreaves-published-contributions-ko",
               "koreaves-external-resources-en",
               "koreaves-external-resources-ko")]
        ])

    def modify_script(self):
        self.write("assets/js/portfolio.js", "console.log('modified')\n")
        return self.commit("portfolio JS only")

    def test_real_native_c849_diff_is_11_and_not_194(self):
        # CI checks out a shallow PR commit; exact historical blobs may not be
        # available there. The local original repo contains both verified SHAs.
        for sha in (BEFORE_C849, AFTER_C849):
            has_blob = subprocess.run(
                ["git", "cat-file", "-e", f"{sha}^{{commit}}"],
                cwd=ROOT, stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
            )
            if has_blob.returncode:
                self.skipTest("Historical C849 commit not in shallow checkout")
        os.chdir(ROOT)
        self.assertEqual(sender.changed_urls(BEFORE_C849, AFTER_C849),
                         self.expected())

    def test_script_only_notifies_exact_11_not_194(self):
        after = self.modify_script()
        self.assertEqual(sender.changed_urls(self.base, after), self.expected())
        with patch.dict(os.environ, {
            "INDEXNOW_BEFORE_SHA": self.base, "INDEXNOW_AFTER_SHA": after
        }):
            with patch.object(sender, "get_urls",
                              side_effect=AssertionError("Full sitemap replay forbidden")):
                self.assertEqual(sender.get_deploy_urls(), self.expected())

    def test_source_scripts_tests_only_do_not_reissue(self):
        self.write("scripts/source.py", "print('changed')\n")
        self.write("tests/test_source.py", "# change\n")
        after = self.commit("source-only edits")
        self.assertEqual(sender.changed_urls(self.base, after), [])
        with patch.dict(os.environ, {
            "INDEXNOW_BEFORE_SHA": self.base, "INDEXNOW_AFTER_SHA": after
        }):
            with patch.object(sender, "get_urls",
                              side_effect=AssertionError("Full sitemap replay forbidden")):
                self.assertEqual(sender.get_deploy_urls(), [])

    def test_extra_unverified_js_consumer_falls_back(self):
        self.write("_includes/footer.html",
                   '<script src="/assets/js/portfolio.js"></script>\n')
        before = self.commit("new global JS consumer")
        after = self.modify_script()
        self.assertIsNone(sender.changed_urls(before, after))

    def test_unknown_layout_consumer_falls_back(self):
        self.write("_posts/new/2026-11-04-new.md",
                   "---\nlayout: portfolio\npermalink: /new/\n---\n")
        before = self.commit("new unverified portfolio layout")
        after = self.modify_script()
        self.assertIsNone(sender.changed_urls(before, after))

    def test_milestone_without_permalink_falls_back(self):
        self.write("_posts/unverified/2026-11-04-unverified.md",
                   "---\nlayout: milestone\n---\n")
        before = self.commit("milestone with nonexplicit route")
        after = self.modify_script()
        self.assertIsNone(sender.changed_urls(before, after))

    def test_project_slug_drift_falls_back(self):
        self.write("_projects/koreaves.md",
                   "---\nlayout: project\nslug: wrong-project\n---\n")
        before = self.commit("unknown new project route")
        after = self.modify_script()
        self.assertIsNone(sender.changed_urls(before, after))

    def test_unknown_page_js_include_falls_back(self):
        self.write("index.md",
                   "---\nlayout: default\n---\n"
                   '<script src="/assets/js/portfolio.js"></script>\n')
        before = self.commit("root page directly references JS")
        after = self.modify_script()
        self.assertIsNone(sender.changed_urls(before, after))

    def test_missing_layout_script_falls_back(self):
        self.write("_layouts/portfolio.html",
                   '---\nlayout: compress\n---\n<script src="/assets/js/other.js"></script>\n')
        before = self.commit("script no longer rendered")
        after = self.modify_script()
        self.assertIsNone(sender.changed_urls(before, after))

    def test_unknown_shared_asset_keeps_full_site(self):
        self.write("assets/js/global.js", "console.log('changed')\n")
        after = self.modify_script()
        self.assertIsNone(sender.changed_urls(self.base, after))

    def test_portfolio_js_plus_one_post_combines_exact_scope(self):
        self.write("_posts/unrelated/2026-11-03-unrelated.md",
                   "---\nlayout: post\npermalink: /unrelated/\n---\nChanged\n")
        after = self.modify_script()
        self.assertEqual(sender.changed_urls(self.base, after),
                         sorted(set(self.expected() + [BASE + "/", BASE + "/unrelated/"])))


if __name__ == "__main__":
    unittest.main()

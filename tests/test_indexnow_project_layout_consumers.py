"""Offline source-to-page coverage for the first-party project layout.

A prior IndexNow provider submission is not replayed by this test.
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
BEFORE_C856 = "96e4c2af8eeb890dcd575ef6efcc850a45498e11"
AFTER_C856 = "b1ecccc5d12be1185e6146cac5b6f431021db71f"
PROJECTS = ("ai-agent-systems", "koreaves", "sigub", "space-atlas", "spoonie")


class ProjectLayoutScope(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(prefix="indexnow-dev-project-layout-")
        self.root = Path(self.temp.name)
        self.prev = Path.cwd()
        os.chdir(self.root)
        self.git("init", "-q")
        self.git("config", "user.email", "fixture@example.invalid")
        self.git("config", "user.name", "Fixture")
        self.write("_config.yml", "collections:\n  projects:\n    output: true\n    permalink: /portfolio/:name/\n")
        self.write("_layouts/project.html", "---\nlayout: portfolio\nportfolio_ui: true\n---\n<main>original project layout</main>\n")
        self.write("_layouts/portfolio.html", "---\nlayout: compress\n---\n")
        self.write("portfolio/index.html", "---\nlayout: portfolio\npermalink: /portfolio/\n---\n<main>Projects</main>\n")
        for slug in PROJECTS:
            self.write(f"_projects/{slug}.md", f"---\nlayout: project\nslug: {slug}\n---\nProject content\n")
        self.write("_posts/unrelated/2026-11-19-unrelated.md", "---\nlayout: post\npermalink: /unrelated/\n---\nUnrelated post\n")
        self.before = self.commit("five original project consumers")

    def tearDown(self):
        os.chdir(self.prev)
        self.temp.cleanup()

    def write(self, path, content):
        p = self.root / path
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_text(content, encoding="utf8")

    def git(self, *args):
        return subprocess.check_output(["git", *args], text=True, stderr=subprocess.PIPE).strip()

    def commit(self, note):
        self.git("add", "-A")
        self.git("commit", "-qm", note)
        return self.git("rev-parse", "HEAD")

    @staticmethod
    def five():
        return sorted([f"{BASE}/portfolio/{slug}/" for slug in PROJECTS])

    def modify_project_layout(self):
        self.write("_layouts/project.html", "---\nlayout: portfolio\nportfolio_ui: true\n---\n<main>new source-owned project contact</main>\n")
        return self.commit("project layout affects five known pages")

    def test_original_native_c856_comparison_is_six_pages_without_replay(self):
        repo = Path(__file__).resolve().parents[1]
        for sha in (BEFORE_C856, AFTER_C856):
            has = subprocess.run(["git", "cat-file", "-e", sha+"^{commit}"], cwd=repo, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            if has.returncode:
                self.skipTest("Original history unavailable in shallow checkout")
        os.chdir(repo)
        self.assertEqual(sender.changed_urls(BEFORE_C856, AFTER_C856), sorted(self.five() + [BASE+"/portfolio/"]))

    def test_project_layout_only_targets_all_five_exact_live_pages(self):
        after = self.modify_project_layout()
        self.assertEqual(sender.changed_urls(self.before, after), self.five())
        with patch.dict(os.environ, {"INDEXNOW_BEFORE_SHA":self.before,"INDEXNOW_AFTER_SHA":after}):
            with patch.object(sender,"get_urls",side_effect=AssertionError("No full sitemap replay")):
                self.assertEqual(sender.get_deploy_urls(),self.five())

    def test_project_layout_plus_home_change_targets_exact_six(self):
        self.write("portfolio/index.html", "---\nlayout: portfolio\npermalink: /portfolio/\n---\nNew home contact\n")
        after = self.modify_project_layout()
        self.assertEqual(sender.changed_urls(self.before, after), sorted(self.five() + [BASE+"/portfolio/"]))

    def test_unknown_new_page_consumer_fails_conservative(self):
        self.write("pages/unverified.md","---\nlayout: project\npermalink: /unverified/\n---\n")
        prior = self.commit("new project-layout consumer")
        after = self.modify_project_layout()
        self.assertIsNone(sender.changed_urls(prior, after))

    def test_mismatched_project_slug_fails_conservative(self):
        self.write("_projects/koreaves.md","---\nlayout: project\nslug: different\n---\n")
        prior = self.commit("unverified source URL mapping")
        after = self.modify_project_layout()
        self.assertIsNone(sender.changed_urls(prior,after))

    def test_unknown_project_collection_config_fails_conservative(self):
        self.write("_config.yml","collections:\n  projects:\n    output: true\n    permalink: /another/:name/\n")
        prior = self.commit("collection route changed")
        after = self.modify_project_layout()
        self.assertIsNone(sender.changed_urls(prior,after))

    def test_unexpected_project_layout_parent_fails_conservative(self):
        self.write("_layouts/project.html","---\nlayout: default\n---\nOld\n")
        prior = self.commit("unverified parent layout")
        self.write("_layouts/project.html","---\nlayout: default\n---\nNew\n")
        after = self.commit("unverified page coverage")
        self.assertIsNone(sender.changed_urls(prior, after))

    def test_new_proven_project_source_is_included_dynamically(self):
        self.write("_projects/newly-added.md",
                   "---\nlayout: project\nslug: newly-added\n---\nNew verified project\n")
        prior = self.commit("new verified project page")
        after = self.modify_project_layout()
        self.assertEqual(sender.changed_urls(prior, after),
                         sorted(self.five() + [BASE + "/portfolio/newly-added/"]))

    def test_quoted_unknown_consumer_remains_conservative(self):
        self.write("pages/other.md",
                   '---\nlayout: "project"\npermalink: /other/\n---\n')
        prior = self.commit("quoted external layout consumer")
        after = self.modify_project_layout()
        self.assertIsNone(sender.changed_urls(prior, after))

    def test_config_default_project_consumer_remains_conservative(self):
        self.write("_config.yml",
                   "collections:\n  projects:\n    output: true\n    permalink: /portfolio/:name/\n"
                   "defaults:\n  - scope:\n      path: \"other\"\n    values:\n      layout: project\n")
        prior = self.commit("new unverified default project layout")
        after = self.modify_project_layout()
        self.assertIsNone(sender.changed_urls(prior, after))

    def test_unrelated_shared_portfolio_layout_is_not_scoped_by_this_rule(self):
        self.write("_layouts/portfolio.html","---\nlayout: compress\n---\nGlobal header changed\n")
        after = self.modify_project_layout()
        self.assertIsNone(sender.changed_urls(self.before, after))

    def test_source_only_edits_do_not_notify_any_page(self):
        self.write("tests/unrelated_test.py","# test file\n")
        self.write("scripts/new_helper.py","# source helper\n")
        after = self.commit("non-rendered source edits")
        self.assertEqual(sender.changed_urls(self.before,after),[])


if __name__ == "__main__":
    unittest.main()

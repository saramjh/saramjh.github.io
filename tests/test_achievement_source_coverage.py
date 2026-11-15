import json
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts" / "check_achievement_source_coverage.py"


class SourceCoverageTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.posts = Path(self.temp.name) / "_posts"
        self.posts.mkdir()

    def tearDown(self):
        self.temp.cleanup()

    def post(self, slug, body, *, published=True):
        folder = self.posts / slug
        folder.mkdir()
        file = folder / f"2026-11-15-{slug}.md"
        file.write_text(
            "---\n"
            f"title: \"{slug}\"\n"
            f"permalink: /{slug}/\n"
            f"published: {'true' if published else 'false'}\n"
            "---\n\n"
            + body,
            encoding="utf-8",
        )
        return file

    def check(self, *urls, extra=None):
        args = [sys.executable, str(SCRIPT), "--posts-root", str(self.posts)]
        for url in urls:
            args.extend(["--source-url", url])
        args.extend(extra or [])
        run = subprocess.run(args, capture_output=True, text=True, timeout=15)
        return run, json.loads(run.stdout)

    def test_existing_source_fails_closed_with_permalink_and_digest(self):
        self.post("koajs-attw-en", "[the patch](https://github.com/koajs/session/pull/240)")
        run, report = self.check("https://github.com/koajs/session/pull/240")
        self.assertEqual(run.returncode, 3)
        self.assertEqual(report["status"], "ALREADY_COVERED_REVIEW_REQUIRED")
        self.assertFalse(report["publicationAuthorized"])
        match = report["sources"][0]["matches"][0]
        self.assertEqual(match["permalink"], "/koajs-attw-en/")
        self.assertRegex(match["sha256"], r"^[0-9a-f]{64}$")

    def test_bilingual_articles_are_both_reported(self):
        self.post("ko", "<a href='https://ncase.org/programs/'>NCASE</a>")
        self.post("en", "See https://ncase.org/programs/ for details.")
        run, report = self.check("https://ncase.org/programs")
        self.assertEqual(run.returncode, 3)
        self.assertEqual([m["permalink"] for m in report["sources"][0]["matches"]], ["/en/", "/ko/"])

    def test_tracking_query_only_is_ignored(self):
        self.post("one-earth", "[source](https://www.oneearth.org/koreaves/?utm_campaign=example)")
        run, report = self.check("https://oneearth.org/koreaves")
        self.assertEqual(run.returncode, 3)
        self.assertEqual(len(report["sources"][0]["matches"]), 1)

    def test_meaningful_query_distinguishes_resources(self):
        self.post("resource-a", "https://example.org/resource?id=1")
        run, report = self.check("https://example.org/resource?id=2")
        self.assertEqual(run.returncode, 0)
        self.assertEqual(report["status"], "NOT_IN_SCANNED_POSTS_UNVERIFIED")
        self.assertFalse(report["publicationAuthorized"])

    def test_url_in_fenced_code_not_counted(self):
        self.post("example", "Example:\n\n~~~text\nhttps://github.com/koajs/session/pull/240\n~~~\n")
        run, report = self.check("https://github.com/koajs/session/pull/240")
        self.assertEqual(run.returncode, 0)
        self.assertEqual(report["sources"][0]["matches"], [])

    def test_url_in_inline_code_not_counted(self):
        self.post("example", "Literal `https://github.com/koajs/session/pull/240` here.")
        run, report = self.check("https://github.com/koajs/session/pull/240")
        self.assertEqual(run.returncode, 0)

    def test_source_in_unpublished_draft_still_requires_review(self):
        self.post("draft", "https://example.org/accepted", published=False)
        run, report = self.check("https://example.org/accepted")
        self.assertEqual(run.returncode, 3)
        self.assertEqual(report["sources"][0]["matches"][0]["published"], False)

    def test_multiple_sources_preserve_separate_matches(self):
        self.post("p1", "https://example.org/a")
        self.post("p2", "https://example.org/b")
        run, report = self.check("https://example.org/a", "https://example.org/b")
        self.assertEqual(run.returncode, 3)
        self.assertEqual([len(x["matches"]) for x in report["sources"]], [1, 1])
        self.assertEqual(report["scannedPosts"], 2)

    def test_rejects_non_http_source(self):
        self.post("p1", "https://example.org/a")
        run, report = self.check("file:///etc/passwd")
        self.assertEqual(run.returncode, 2)
        self.assertEqual(report["status"], "INVALID_SOURCE_URL")

    def test_empty_posts_root_fails_not_green(self):
        run, report = self.check("https://example.org/a")
        self.assertEqual(run.returncode, 2)
        self.assertEqual(report["status"], "NO_POSTS_TO_REVIEW")

    def test_foreign_post_path_not_exposed(self):
        self.post("ok", "https://example.org/a")
        run, report = self.check("https://example.org/a")
        self.assertEqual(run.returncode, 3)
        self.assertTrue(report["sources"][0]["matches"][0]["postPath"].startswith("_posts/"))
        self.assertNotIn(self.temp.name, json.dumps(report))


    @unittest.skipUnless(shutil.which("ruby"), "Ruby CLI unavailable")
    def test_new_post_achievement_source_aborts_before_creating_duplicate(self):
        self.post("old", "[original](https://github.com/koajs/session/pull/240)")
        scripts = Path(self.temp.name) / "scripts"
        scripts.mkdir()
        shutil.copyfile(SCRIPT, scripts / SCRIPT.name)
        shutil.copyfile(ROOT / "scripts" / "new_post.rb", scripts / "new_post.rb")
        run = subprocess.run([
            "ruby", str(scripts / "new_post.rb"), "--achievement-source",
            "https://github.com/koajs/session/pull/240", "same-evidence", "Another title",
        ], capture_output=True, text=True, timeout=15)
        self.assertNotEqual(run.returncode, 0)
        self.assertIn("existing", (run.stdout + run.stderr).lower())
        self.assertFalse((self.posts / "same-evidence").exists())

    @unittest.skipUnless(shutil.which("ruby"), "Ruby CLI unavailable")
    def test_new_post_new_achievement_source_creates_only_requested_slug(self):
        self.post("old", "https://example.org/other")
        scripts = Path(self.temp.name) / "scripts"
        scripts.mkdir()
        shutil.copyfile(SCRIPT, scripts / SCRIPT.name)
        shutil.copyfile(ROOT / "scripts" / "new_post.rb", scripts / "new_post.rb")
        run = subprocess.run([
            "ruby", str(scripts / "new_post.rb"), "--achievement-source",
            "https://example.org/new-achievement", "new-story", "Verified original",
        ], capture_output=True, text=True, timeout=15)
        self.assertEqual(run.returncode, 0, run.stderr)
        paths = list((self.posts / "new-story").glob("*.md"))
        self.assertEqual(len(paths), 1)
        self.assertIn("Verified original", paths[0].read_text(encoding="utf-8"))

    @unittest.skipUnless(shutil.which("ruby"), "Ruby CLI unavailable")
    def test_new_post_without_achievement_flag_keeps_existing_interface(self):
        self.post("old", "https://example.org/other")
        scripts = Path(self.temp.name) / "scripts"
        scripts.mkdir()
        shutil.copyfile(SCRIPT, scripts / SCRIPT.name)
        shutil.copyfile(ROOT / "scripts" / "new_post.rb", scripts / "new_post.rb")
        run = subprocess.run([
            "ruby", str(scripts / "new_post.rb"), "normal-article", "Normal title",
        ], capture_output=True, text=True, timeout=15)
        self.assertEqual(run.returncode, 0, run.stderr)
        self.assertEqual(len(list((self.posts / "normal-article").glob("*.md"))), 1)


if __name__ == "__main__":
    unittest.main()

"""Git-range-only IndexNow submission: no requests for unchanged pages."""
import contextlib
import io
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import patch

from scripts import submit_search_engines as sender


class ChangeScopeTest(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(prefix="indexnow-git-range-")
        self.root = Path(self.temp.name)
        self.cwd = Path.cwd()
        os.chdir(self.root)
        self.git("init", "-q")
        self.git("config", "user.email", "test@example.invalid")
        self.git("config", "user.name", "Fixture Test")
        self.write("portfolio/index.html", "---\npermalink: /portfolio/\n---\nBefore\n")
        self.write("index.md", "---\nlayout: home\n---\nHomepage\n")
        self.write("_posts/case-one/2026-11-10-case-one.md", "---\npermalink: /case-one/\n---\nCase one\n")
        self.write("scripts/example.py", "print('before')\n")
        self.git("add", ".")
        self.git("commit", "-qm", "baseline")
        self.base = self.sha()

    def tearDown(self):
        os.chdir(self.cwd)
        self.temp.cleanup()

    def git(self, *args):
        return subprocess.check_output(["git", *args], text=True, stderr=subprocess.PIPE).strip()

    def sha(self):
        return self.git("rev-parse", "HEAD")

    def write(self, name, content):
        p = self.root / name
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_text(content, encoding="utf-8")

    def commit(self, message):
        self.git("add", "-A")
        self.git("commit", "-qm", message)
        return self.sha()

    def test_exact_unlinked_firstparty_social_jpeg_no_page_resubmission(self):
        image_path = ("assets/img/dev-social-media-20261113/"
                      "portfolio-filter-contrast-c561.jpg")
        original = Path(sender.__file__).resolve().parents[1] / image_path
        raw = original.read_bytes()
        dest = self.root / image_path
        dest.parent.mkdir(parents=True, exist_ok=True)
        dest.write_bytes(raw)
        after = self.commit("original Dev JPG public hosting only")
        self.assertTrue(sender._is_exact_unlinked_firstparty_social_jpeg(
            image_path, after))
        self.assertEqual(sender.changed_urls(self.base, after), [])
        with patch.dict(os.environ, {"INDEXNOW_BEFORE_SHA": self.base,
                                     "INDEXNOW_AFTER_SHA": after}):
            with patch.object(sender, "get_urls",
                              side_effect=AssertionError("unexpected full sitemap")):
                self.assertEqual(sender.get_deploy_urls(), [])

        # A referenced image affects the changed page. No source-only skip.
        self.write("portfolio/index.html",
                   "---\npermalink: /portfolio/\n---\n"
                   '<img src="/' + image_path + '" alt="actual filter">\n')
        referenced = self.commit("public portfolio page now uses JPG")
        self.assertFalse(sender._is_exact_unlinked_firstparty_social_jpeg(
            image_path, referenced))
        self.assertEqual(sender.changed_urls(after, referenced),
                         ["https://saramjh.github.io/portfolio/"])

        # Any different media, even under the same folder, fails conservatively.
        other_path = "assets/img/dev-social-media-20261113/other.jpg"
        other = self.root / other_path
        other.write_bytes(raw)
        other_commit = self.commit("different standalone media")
        self.assertFalse(sender._is_exact_unlinked_firstparty_social_jpeg(
            other_path, other_commit))
        self.assertIsNone(sender.changed_urls(referenced, other_commit))

    def test_exact_two_original_api_carousel_cards_skip_page_notifications(self):
        paths = [
            f"assets/img/dev-social-media-20261113/c563-portfolio-filter-two-card/card-{i:02d}.jpg"
            for i in (1, 2)
        ]
        for image_path in paths:
            original = Path(sender.__file__).resolve().parents[1] / image_path
            data = original.read_bytes()
            output = self.root / image_path
            output.parent.mkdir(parents=True, exist_ok=True)
            output.write_bytes(data)
        after = self.commit("two exact source-owned non-page JPG cards")
        self.assertEqual(sender.changed_urls(self.base, after), [])
        for image_path in paths:
            self.assertTrue(sender._is_exact_unlinked_firstparty_social_jpeg(
                image_path, after))
        with patch.dict(os.environ, {"INDEXNOW_BEFORE_SHA": self.base,
                                     "INDEXNOW_AFTER_SHA": after}):
            with patch.object(sender, "get_urls",
                              side_effect=AssertionError("no all-site IndexNow replay")):
                self.assertEqual(sender.get_deploy_urls(), [])

        # A new page usage is not ignored. The changed HTML gets the exact URL.
        self.write("portfolio/index.html",
                   "---\npermalink: /portfolio/\n---\n"
                   '<img src="/' + paths[0] + '" alt="real before state">\n')
        uses_card = self.commit("source page now uses original first card")
        self.assertFalse(sender._is_exact_unlinked_firstparty_social_jpeg(
            paths[0], uses_card))
        self.assertEqual(sender.changed_urls(after, uses_card),
                         ["https://saramjh.github.io/portfolio/"])

        # Changed bytes for an existing protected card do not get a silent skip.
        original = self.root / paths[1]
        original.write_bytes(original.read_bytes() + b"not-original")
        changed = self.commit("original image digest drift")
        self.assertFalse(sender._is_exact_unlinked_firstparty_social_jpeg(
            paths[1], changed))
        self.assertIsNone(sender.changed_urls(uses_card, changed))

    def test_source_only_release_skips_all_notifications(self):
        self.write("scripts/example.py", "print('infra changed')\n")
        self.write(".github/workflows/pages.yml", "name: updated workflow\n")
        after = self.commit("infra only")
        self.assertEqual(sender.changed_urls(self.base, after), [])
        with patch.dict(os.environ, {"INDEXNOW_BEFORE_SHA": self.base,
                                     "INDEXNOW_AFTER_SHA": after}):
            with patch.object(sender, "get_urls", side_effect=AssertionError("unexpected sitemap request")):
                self.assertEqual(sender.get_deploy_urls(), [])
        script = Path(sender.__file__).resolve()
        p = subprocess.run(
            [sys.executable, str(script)], cwd=self.root, text=True, capture_output=True,
            env={**os.environ, "INDEXNOW_BEFORE_SHA": self.base, "INDEXNOW_AFTER_SHA": after},
            timeout=8
        )
        self.assertEqual(p.returncode, 0, p.stderr)
        self.assertIn("No qualified changed URLs; skipping Bing and IndexNow.", p.stdout)
        self.assertNotIn("Batch 1/", p.stdout)

    def test_only_existing_archive_filter_css_visual_state_skips_notifications(self):
        self.write("assets/js/portfolio.js",
                   "document.querySelectorAll('.folio-filter');\n")
        self.write("portfolio/recognition/index.html",
                   "---\npermalink: /portfolio/recognition/\n---\n"
                   '<button class="folio-filter" aria-pressed="false">Listings</button>\n')
        old = (
            ".portfolio-body .folio .folio-filter{background:transparent;color:#ddd}\n"
            ".portfolio-body .folio .folio-filter:hover,.portfolio-body .folio "
            ".folio-filter.is-active{background:blue;color:navy}\n"
        )
        self.write("assets/css/portfolio.css", old)
        before = self.commit("archive filter original CSS")
        new = (
            ".portfolio-body .folio .folio-filter{background:transparent!important;color:#ddd!important}\n"
            ".portfolio-body .folio .folio-filter[aria-pressed=\"false\"]:hover"
            "{background:#20242e!important;color:white!important}\n"
            ".portfolio-body .folio .folio-filter[aria-pressed=\"true\"]"
            "{background:blue!important;color:navy!important}\n"
        )
        self.write("assets/css/portfolio.css", new)
        after = self.commit("only archive filter appearance")
        self.assertEqual(sender.changed_urls(before, after), [])
        with patch.dict(os.environ, {
            "INDEXNOW_BEFORE_SHA": before, "INDEXNOW_AFTER_SHA": after,
        }):
            with patch.object(sender, "get_urls",
                              side_effect=AssertionError("full sitemap reissue forbidden")):
                self.assertEqual(sender.get_deploy_urls(), [])

        # A second unrelated CSS change cannot inherit the suppression.
        self.write("assets/css/portfolio.css", new + ".portfolio-body{font-size:18px}\n")
        after_global = self.commit("unrelated portfolio CSS change")
        self.assertIsNone(sender.changed_urls(after, after_global))

    def test_portfolio_content_change_submits_one_page(self):
        self.write("portfolio/index.html", "---\npermalink: /portfolio/\n---\nTwo new cards\n")
        self.write("tests/diff_check.py", "# new test\n")
        after = self.commit("portfolio change")
        self.assertEqual(sender.changed_urls(self.base, after),
                         ["https://saramjh.github.io/portfolio/"])

    def test_collection_project_edit_notifies_only_original_project_page(self):
        self.write("_config.yml",
                   "collections:\n  projects:\n    output: true\n    permalink: /portfolio/:name/\n")
        self.write("_projects/spoonie.md",
                   "---\nlayout: project\nslug: spoonie\n---\nOriginal case\n")
        before = self.commit("bounded project collection baseline")
        self.write("_projects/spoonie.md",
                   "---\nlayout: project\nslug: spoonie\n---\n"
                   "New source-bound links to KO and EN engineering articles.\n")
        after = self.commit("one original project case edit")
        expected = ["https://saramjh.github.io/portfolio/spoonie/"]
        self.assertEqual(sender.changed_urls(before, after), expected)
        with patch.dict(os.environ, {
            "INDEXNOW_BEFORE_SHA": before, "INDEXNOW_AFTER_SHA": after,
        }):
            with patch.object(sender, "get_urls",
                              side_effect=AssertionError("full sitemap replay is not needed")):
                self.assertEqual(sender.get_deploy_urls(), expected)

    def test_collection_project_slug_drift_is_not_guessed(self):
        self.write("_config.yml",
                   "collections:\n  projects:\n    output: true\n    permalink: /portfolio/:name/\n")
        self.write("_projects/spoonie.md",
                   "---\nlayout: project\nslug: spoonie\n---\nOriginal\n")
        before = self.commit("baseline collection route")
        self.write("_projects/spoonie.md",
                   "---\nlayout: project\nslug: unexpected\n---\nChanged\n")
        after = self.commit("unknown project path")
        self.assertIsNone(sender.changed_urls(before, after))

    def test_post_added_notifies_post_and_home_page(self):
        self.write("_posts/case-two/2026-11-10-case-two.md",
                   "---\npermalink: /case-two/\n---\nCase two\n")
        after = self.commit("post added")
        self.assertEqual(sender.changed_urls(self.base, after),
                         ["https://saramjh.github.io/",
                          "https://saramjh.github.io/case-two/"])

    def test_deleted_post_includes_original_url(self):
        (self.root / "_posts/case-one/2026-11-10-case-one.md").unlink()
        after = self.commit("post removed")
        self.assertEqual(sender.changed_urls(self.base, after),
                         ["https://saramjh.github.io/",
                          "https://saramjh.github.io/case-one/"])

    def test_permalink_changed_in_same_file_includes_old_and_new(self):
        self.write("_posts/case-one/2026-11-10-case-one.md",
                   "---\npermalink: /case-one-revised/\n---\nUpdated\n")
        after = self.commit("post permalink changed")
        self.assertEqual(sender.changed_urls(self.base, after),
                         ["https://saramjh.github.io/",
                          "https://saramjh.github.io/case-one-revised/",
                          "https://saramjh.github.io/case-one/"])

    def test_exact_static_verification_sitemap_exclusion_has_no_provider_urls(self):
        self.write("_config.yml", "defaults:\n  - scope:\n      path: \"\"\n    values:\n      layout: default\n")
        original = self.commit("baseline sitemap config")
        self.write("_config.yml", (
            "defaults:\n  - scope:\n      path: \"\"\n    values:\n      layout: default\n"
            + "\n".join(sender._VERIFICATION_SITEMAP_ONLY_ADDITIONS) + "\n"
        ))
        after = self.commit("exclude verification tokens from sitemap only")
        self.assertEqual(sender.changed_urls(original, after), [])
        with patch.dict(os.environ, {"INDEXNOW_BEFORE_SHA": original,
                                     "INDEXNOW_AFTER_SHA": after}):
            with patch.object(sender, "get_urls",
                              side_effect=AssertionError("full site replay is prohibited")):
                self.assertEqual(sender.get_deploy_urls(), [])

    def test_unrelated_config_change_remains_broad(self):
        self.write("_config.yml", "title: before\n")
        original = self.commit("baseline global config")
        self.write("_config.yml", "title: after\n")
        after = self.commit("global site update")
        self.assertIsNone(sender.changed_urls(original, after))

    def test_shared_layout_change_keeps_full_site_coverage(self):
        self.write("_includes/footer.html", "Shared footer modified\n")
        after = self.commit("sitewide change")
        self.assertIsNone(sender.changed_urls(self.base, after))
        with patch.dict(os.environ, {"INDEXNOW_BEFORE_SHA": self.base,
                                     "INDEXNOW_AFTER_SHA": after}):
            with patch.object(sender, "get_urls",
                              return_value=["https://saramjh.github.io/", "https://saramjh.github.io/portfolio/"]):
                self.assertEqual(len(sender.get_deploy_urls()), 2)

    def recognition_fixture(self):
        self.write("_config.yml",
                   "collections:\n  projects:\n    output: true\n    permalink: /portfolio/:name/\n")
        self.write("_includes/portfolio-evidence.html",
                   "{% for record in site.data.recognitions %}{{ record.title }}{% endfor %}\n")
        self.write("_layouts/project.html",
                   "{% assign matches = site.data.recognitions %}\n"
                   "{% include portfolio-evidence.html project=page.slug %}\n")
        self.write("_layouts/milestone.html",
                   "{% include portfolio-evidence.html project=page.project_id %}\n")
        self.write("portfolio/index.html",
                   "---\npermalink: /portfolio/\n---\n{% include portfolio-evidence.html %}\n")
        self.write("portfolio/recognition/index.html",
                   "---\npermalink: /portfolio/recognition/\n---\n{% include portfolio-evidence.html %}\n")
        self.write("_projects/koreaves.md",
                   "---\nlayout: project\nslug: koreaves\n---\n")
        self.write("_posts/folio-koreaves/2026-11-11-folio-koreaves.md",
                   "---\nlayout: milestone\npermalink: /koreaves-evidence/\n---\n")
        self.write("_data/recognitions.yml", "- id: before\n")
        return self.commit("original bounded recognition consumers")

    def test_recognition_data_change_only_notifies_verified_consumers(self):
        before = self.recognition_fixture()
        self.write("_data/recognitions.yml", "- id: after\n")
        after = self.commit("one new external achievement record")
        expected = ["https://saramjh.github.io/koreaves-evidence/",
                    "https://saramjh.github.io/portfolio/",
                    "https://saramjh.github.io/portfolio/koreaves/",
                    "https://saramjh.github.io/portfolio/recognition/"]
        self.assertEqual(sender.changed_urls(before, after), expected)
        with patch.dict(os.environ, {"INDEXNOW_BEFORE_SHA": before,
                                     "INDEXNOW_AFTER_SHA": after}):
            with patch.object(sender, "get_urls", side_effect=AssertionError("no sitemap replay")):
                self.assertEqual(sender.get_deploy_urls(), expected)

    def test_recognition_seo_schema_is_exact_project_only_consumer(self):
        self.recognition_fixture()
        guarded = (
            "{%- if page.layout == 'project' and page.site_url and page.slug -%}\\n"
            "{%- assign verified_listings = site.data.recognitions"
            " | where: 'project', page.slug | where: 'type', 'listing'"
            " | where: 'status', 'confirmed' -%}\\n"
            "{%- elsif page.date -%}\\n"
            "<script type=\\\"application/ld+json\\\">{}<\\/script>\\n"
            "{%- endif -%}\\n"
        )
        self.write("_includes/seo_schema.html", guarded)
        before = self.commit("project-scoped recognition JSON-LD")
        self.write("_data/recognitions.yml", "- id: after\\n")
        after = self.commit("one confirmed listing")
        expected = [
            "https://saramjh.github.io/koreaves-evidence/",
            "https://saramjh.github.io/portfolio/",
            "https://saramjh.github.io/portfolio/koreaves/",
            "https://saramjh.github.io/portfolio/recognition/",
        ]
        self.assertEqual(sender.changed_urls(before, after), expected)

        # An unguarded JSON-LD consumer could affect every post. Keep
        # the original conservative fallback rather than inventing scope.
        self.write("_includes/seo_schema.html",
                   "{{ site.data.recognitions }}\\n")
        new_base = self.commit("unscoped new template consumer")
        self.write("_data/recognitions.yml", "- id: another\\n")
        after_unscoped = self.commit("subsequent listing")
        self.assertIsNone(sender.changed_urls(new_base, after_unscoped))

    def test_recognition_data_unknown_new_template_keeps_conservative_scope(self):
        before = self.recognition_fixture()
        self.write("_includes/footer.html", "{{ site.data.recognitions.size }}\n")
        self.write("_data/recognitions.yml", "- id: after\n")
        after = self.commit("new footer consumer requires full coverage")
        self.assertIsNone(sender.changed_urls(before, after))

    def test_empty_or_unknown_commit_never_requests_sitemap(self):
        after = self.base
        for before in ("", "a" * 40):
            with self.subTest(before=before):
                with patch.dict(os.environ, {"INDEXNOW_BEFORE_SHA": before,
                                             "INDEXNOW_AFTER_SHA": after}):
                    with patch.object(sender, "get_urls", side_effect=AssertionError("must fail closed")):
                        with contextlib.redirect_stdout(io.StringIO()):
                            self.assertEqual(sender.get_deploy_urls(), [])

    def test_referenced_image_and_portfolio_edit_only_notify_portfolio(self):
        self.write("portfolio/index.html",
                   '---\npermalink: /portfolio/\n---\n'
                   '<img src="/assets/img/ci-preview.png" alt="Measured CI time">\n')
        self.write("assets/img/ci-preview.png", "PNG fixture, no image sent")
        self.write("scripts/render_preview.swift", "// only generator changed")
        self.write("tests/preview_test.py", "# same preview check")
        after = self.commit("one page with owned preview")
        self.assertEqual(sender.changed_urls(self.base, after),
                         ["https://saramjh.github.io/portfolio/"])
        with patch.dict(os.environ, {"INDEXNOW_BEFORE_SHA": self.base,
                                     "INDEXNOW_AFTER_SHA": after}):
            with patch.object(sender, "get_urls",
                              side_effect=AssertionError("must not resubmit entire sitemap")):
                self.assertEqual(sender.get_deploy_urls(),
                                 ["https://saramjh.github.io/portfolio/"])

    def test_image_referenced_in_two_pages_maps_both_urls(self):
        self.write("portfolio/index.html",
                   '---\npermalink: /portfolio/\n---\n'
                   '<img src="/assets/img/shared-card.png">\n')
        self.write("_posts/case-one/2026-11-10-case-one.md",
                   '---\npermalink: /case-one/\n---\n'
                   '![First-party illustration](/assets/img/shared-card.png)\n')
        self.write("assets/img/shared-card.png", "PNG fixture")
        after = self.commit("same image on two specific pages")
        self.assertEqual(sender.changed_urls(self.base, after),
                         ["https://saramjh.github.io/",
                          "https://saramjh.github.io/case-one/",
                          "https://saramjh.github.io/portfolio/"])

    def test_global_template_reference_retains_full_site_fallback(self):
        self.write("_includes/header.html",
                   '<img src="/assets/img/site-logo.svg">\n')
        self.write("assets/img/site-logo.svg", "<svg></svg>")
        after = self.commit("global image")
        self.assertIsNone(sender.changed_urls(self.base, after))

    def test_unknown_asset_does_not_silently_drop_notifications(self):
        self.write("assets/img/new-diagram.svg", "<svg></svg>")
        after = self.commit("unreferenced graphic")
        self.assertIsNone(sender.changed_urls(self.base, after))

    def test_unmapped_page_content_changes_use_conservative_full_site_scope(self):
        self.write("assets/img/new-diagram.svg", '<svg xmlns="http://www.w3.org/2000/svg"></svg>\n')
        after = self.commit("shared asset changed")
        self.assertIsNone(sender.changed_urls(self.base, after))

    def test_post_local_svg_added_with_own_post_limits_notification_to_two_urls(self):
        self.write(
            "_posts/atomic-ko/2026-11-11-atomic-ko.md",
            '---\npermalink: /atomic-ko/\n---\n'
            '<img src="/atomic-ko/atomic-flow.svg" alt="Own source diagram">\n',
        )
        self.write("_posts/atomic-ko/atomic-flow.svg", "<svg></svg>\n")
        after = self.commit("new original bilingual article and local image")
        expected = ["https://saramjh.github.io/", "https://saramjh.github.io/atomic-ko/"]
        self.assertEqual(sender.changed_urls(self.base, after), expected)
        with patch.dict(os.environ, {
            "INDEXNOW_BEFORE_SHA": self.base, "INDEXNOW_AFTER_SHA": after,
        }):
            with patch.object(sender, "get_urls", side_effect=AssertionError("no sitemap replay")):
                self.assertEqual(sender.get_deploy_urls(), expected)

    def test_post_local_svg_only_change_limits_notification_to_its_page(self):
        self.write(
            "_posts/case-one/2026-11-10-case-one.md",
            '---\npermalink: /case-one/\n---\n'
            '<img src="/case-one/case-flow.svg">\n',
        )
        self.write("_posts/case-one/case-flow.svg", "<svg>original</svg>\n")
        old = self.commit("original post owns image")
        self.write("_posts/case-one/case-flow.svg", "<svg>edited</svg>\n")
        after = self.commit("update one local image")
        self.assertEqual(sender.changed_urls(old, after), [
            "https://saramjh.github.io/", "https://saramjh.github.io/case-one/"
        ])

    def test_unreferenced_post_local_asset_uses_conservative_full_site_scope(self):
        self.write("_posts/case-one/unreferenced.svg", "<svg></svg>\n")
        after = self.commit("unreferenced post-local asset")
        self.assertIsNone(sender.changed_urls(self.base, after))

    def test_post_local_asset_used_in_shared_template_is_not_narrowed(self):
        self.write(
            "_includes/header.html",
            '<img src="/case-one/local-asset.svg">\n',
        )
        self.write("_posts/case-one/local-asset.svg", "<svg></svg>\n")
        after = self.commit("shared template uses local asset")
        self.assertIsNone(sender.changed_urls(self.base, after))


if __name__ == "__main__":
    unittest.main()

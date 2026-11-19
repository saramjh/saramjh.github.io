"""Regression checks for the Jekyll build's internal link QA."""
from pathlib import Path
from tempfile import TemporaryDirectory
import unittest

from scripts.check_internal_links import inspect


class InternalLinksTests(unittest.TestCase):
    def fixture(self, files):
        self.temp = TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        root = Path(self.temp.name)
        for name, html in files.items():
            file = root / name
            file.parent.mkdir(parents=True, exist_ok=True)
            file.write_text(html, encoding="utf8")
        return root

    def test_valid_page_links_fragments_assets_and_independent_app_mounts(self):
        root = self.fixture({
            "index.html": (
                '<a href="/posts/#why">Case</a>'
                '<a href="#home">Top</a>'
                '<a id="home"></a>'
                '<a href="/richChecker/">KR app</a>'
                '<a href="/richChecker-us/">US app</a>'
                '<a href="/scratchLottery/">Scratch app</a>'
            ),
            "posts/index.html": (
                '<h2 id="why">Why</h2><a href="../index.html#home">Home</a>'
                '<a href="figure.svg">Image source</a>'
            ),
            "posts/figure.svg": "<svg></svg>",
        })
        outcome = inspect(root)
        self.assertEqual(outcome["failures"], [])
        self.assertEqual(outcome["pages"], 2)
        self.assertEqual(outcome["checked_fragments"], 3)
        self.assertEqual(outcome["separate_app_roots"], 3)

    def test_missing_local_page_and_hash_fail_even_when_other_routes_exist(self):
        root = self.fixture({
            "index.html": '<a href="/missing/">Missing</a><a href="#absent">Anchor</a>'
        })
        failures = inspect(root)["failures"]
        self.assertEqual(len(failures), 2)
        self.assertTrue(any("missing local destination" in f for f in failures))
        self.assertTrue(any("missing target fragment" in f for f in failures))

    def test_independent_app_exceptions_are_exact_not_arbitrary_subpaths(self):
        root = self.fixture({
            "index.html": (
                '<a href="/richChecker/">Real owned app root</a>'
                '<a href="/richChecker/not-a-real-page/">Broken nested page</a>'
            )
        })
        out = inspect(root)
        self.assertEqual(out["separate_app_roots"], 1)
        self.assertEqual(len(out["failures"]), 1)
        self.assertIn("/richChecker/not-a-real-page/", out["failures"][0])

    def test_disallows_escape_outside_generated_site(self):
        root = self.fixture({"index.html": '<a href="../../outside.txt">Invalid</a>'})
        self.assertIn("link leaves built site", inspect(root)["failures"][0])

    def test_resolves_percent_encoded_links_and_legacy_named_anchors(self):
        root = self.fixture({
            "index.html": '<a href="/docs/page%20one.html#legacy-name">Read</a>',
            "docs/page one.html": '<a name="legacy-name"></a>',
        })
        self.assertEqual(inspect(root)["failures"], [])


if __name__ == "__main__":
    unittest.main()

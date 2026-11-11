"""Portfolio editorial navigation for existing, independently verified case studies."""

from html.parser import HTMLParser
from pathlib import Path
import unittest


ROOT = Path(__file__).resolve().parents[1]
PORTFOLIO = ROOT / "portfolio" / "index.html"
EXPECTED = [
    (
        "/koreaves-published-contributions-en/",
        "/assets/images/portfolio/koreaves-gis.jpg",
    ),
    (
        "/koreaves-external-resources-en/",
        "/assets/images/portfolio/koreaves-desktop.jpg",
    ),
    (
        "/spoonie-live-polls-en/",
        "/spoonie-live-polls-en/spoonie-poll-flow.svg",
    ),
    (
        "/utf8-caption-hash-is-not-text-quality-en/",
        "/assets/img/dev-utf8-caption-integrity-20261110/audit-en-og.png",
    ),
    (
        "/jekyll-dnt-analytics-compress-regression-en/",
        "/assets/img/dev-dnt-analytics-20261110/loader-gate-en.png",
    ),
    (
        "/playwright-github-actions-runner-chrome-en/",
        "/assets/img/dev-playwright-ci-runner-chrome-20261110/setup-comparison-en.png",
    ),
    (
        "/jekyll-svg-to-png-og-ci-regression-en/",
        "/assets/img/dev-ga4-report-window-20261110/timeline-en-og.png",
    ),
]


class NotesParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.in_notes = False
        self.note_depth = 0
        self.cards = []
        self.current_card = None

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if tag == "div" and "folio-writing-grid" in attrs.get("class", "").split():
            assert not self.in_notes
            self.in_notes = True
            self.note_depth = 1
            return
        if not self.in_notes:
            return
        if tag == "div":
            self.note_depth += 1
        if tag == "a" and "folio-writing-card" in attrs.get("class", "").split():
            self.current_card = {"href": attrs.get("href"), "id": attrs.get("data-case-id"), "img": None, "alt": None}
            self.cards.append(self.current_card)
        if tag == "img" and self.current_card is not None:
            self.current_card["img"] = attrs.get("src")
            self.current_card["alt"] = attrs.get("alt")
            self.current_card["loading"] = attrs.get("loading")

    def handle_endtag(self, tag):
        if not self.in_notes:
            return
        if tag == "a":
            self.current_card = None
        if tag == "div":
            self.note_depth -= 1
            if self.note_depth == 0:
                self.in_notes = False


class PortfolioEngineeringNotesTest(unittest.TestCase):
    def test_seven_distinct_source_linked_notes(self):
        parser = NotesParser()
        parser.feed(PORTFOLIO.read_text(encoding="utf-8"))
        self.assertEqual(len(parser.cards), 7)
        self.assertEqual(
            [(card["href"], card["img"]) for card in parser.cards], EXPECTED
        )
        self.assertEqual(len(set(card["href"] for card in parser.cards)), 7)
        self.assertEqual(
            [card["id"] for card in parser.cards],
            [
                "koreaves_published_contributions",
                "koreaves_resource_lists",
                "spoonie_public_recipe_poll",
                "utf8_caption_integrity",
                "jekyll_dnt_analytics_loader",
                "playwright_runner_chrome_ci",
                "jekyll_og_png_ci_regression",
            ],
        )
        self.assertEqual(len(set(card["id"] for card in parser.cards)), 7)
        for card in parser.cards:
            self.assertTrue(card["alt"])
            self.assertEqual(card["loading"], "lazy")

    def test_new_preview_assets_and_story_pages_exist(self):
        external_cases = {
            "/koreaves-published-contributions-en/",
            "/koreaves-external-resources-en/",
        }
        for href, image in EXPECTED:
            if href in external_cases:
                continue
            slug = href.strip("/")
            post = ROOT / "_posts" / slug / (("2026-11-11-" if slug == "spoonie-live-polls-en" else "2026-11-10-") + slug + ".md")
            self.assertTrue(post.is_file(), post)
            content = post.read_text(encoding="utf-8")
            self.assertIn("permalink: " + href, content)
            asset = (
                ROOT / "_posts" / image.lstrip("/")
                if image.startswith("/spoonie-live-polls-")
                else ROOT / image.lstrip("/")
            )
            self.assertTrue(asset.is_file(), asset)
            data = asset.read_bytes()
            if slug == "spoonie-live-polls-en":
                self.assertTrue(data.startswith(b"<svg"), "Original SVG diagram expected")
                self.assertIn(b'width="1280" height="560"', data)
                self.assertIn(b'PR #19', data)
                self.assertIn(b'PR #20', data)
                self.assertIn("/spoonie-live-polls-ko/", content)
                self.assertIn("https://spoonie.kr/recipes/", content)
            else:
                self.assertEqual(data[:8], b"\x89PNG\r\n\x1a\n")
                self.assertEqual(
                    (int.from_bytes(data[16:20], "big"), int.from_bytes(data[20:24], "big")),
                    (1200, 630),
                )


if __name__ == "__main__":
    unittest.main()

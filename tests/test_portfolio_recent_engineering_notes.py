"""Portfolio editorial navigation for existing, independently verified case studies."""

from html.parser import HTMLParser
from pathlib import Path
import unittest


ROOT = Path(__file__).resolve().parents[1]
PORTFOLIO = ROOT / "portfolio" / "index.html"
EXPECTED = [
    (
        "/jekyll-svg-to-png-og-ci-regression-en/",
        "/assets/img/dev-ga4-report-window-20261110/timeline-en-og.png",
    ),
    (
        "/spoonie-author-header-consistency-en/",
        "/spoonie-author-header-consistency-en/author-header-en-og.png",
    ),
    (
        "/koreaves-external-resources-en/",
        "/assets/images/portfolio/koreaves-desktop.jpg",
    ),
    (
        "/koreaves-published-contributions-en/",
        "/assets/images/portfolio/koreaves-gis.jpg",
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
    def test_four_distinct_source_linked_notes(self):
        parser = NotesParser()
        parser.feed(PORTFOLIO.read_text(encoding="utf-8"))
        self.assertEqual(len(parser.cards), 4)
        self.assertEqual(
            [(card["href"], card["img"]) for card in parser.cards], EXPECTED
        )
        self.assertEqual(len(set(card["href"] for card in parser.cards)), 4)
        self.assertEqual(
            [card["id"] for card in parser.cards],
            [
                "jekyll_og_png_ci_regression",
                "spoonie_author_header",
                "koreaves_resource_lists",
                "koreaves_published_contributions",
            ],
        )
        self.assertEqual(len(set(card["id"] for card in parser.cards)), 4)
        for card in parser.cards:
            self.assertTrue(card["alt"])
            self.assertEqual(card["loading"], "lazy")

    def test_new_preview_assets_and_story_pages_exist(self):
        for href, image in EXPECTED[:2]:
            slug = href.strip("/")
            post = ROOT / "_posts" / slug / ("2026-11-10-" + slug + ".md")
            self.assertTrue(post.is_file(), post)
            content = post.read_text(encoding="utf-8")
            self.assertIn("permalink: " + href, content)
            asset = (
                ROOT / "_posts" / image.lstrip("/")
                if image.startswith("/spoonie-author-header-consistency-")
                else ROOT / image.lstrip("/")
            )
            self.assertTrue(asset.is_file(), asset)
            png = asset.read_bytes()
            self.assertEqual(png[:8], b"\x89PNG\r\n\x1a\n")
            self.assertEqual(
                (int.from_bytes(png[16:20], "big"), int.from_bytes(png[20:24], "big")),
                (1200, 630),
            )


if __name__ == "__main__":
    unittest.main()

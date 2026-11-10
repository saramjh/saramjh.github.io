"""Portfolio cross-link to a verified recent privacy implementation."""
from pathlib import Path
from html.parser import HTMLParser
import re
import unittest

ROOT=Path(__file__).resolve().parents[1]
PORTFOLIO=ROOT / "portfolio" / "index.html"
TARGET="/jekyll-eu-consent-revocation-en/"

class LinkParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.targets=[]
        self.cards=[]
    def handle_starttag(self,tag,attrs):
        attrs=dict(attrs)
        if tag=="a" and attrs.get("href")==TARGET:
            self.targets.append(attrs)
        if tag=="a" and "folio-writing-card" in attrs.get("class","").split():
            self.cards.append(attrs)

class PortfolioConsentLinkTest(unittest.TestCase):
    def test_contextual_link_is_native_and_not_an_eighth_card(self):
        src=PORTFOLIO.read_text(encoding="utf-8")
        parsed=LinkParser()
        parsed.feed(src)
        self.assertEqual(len(parsed.targets),1)
        self.assertEqual(len(parsed.cards),7)
        self.assertTrue(all(card.get("href")!=TARGET for card in parsed.cards))
        self.assertRegex(src,re.compile(r'folio-section-end[^>]*><a href="'+re.escape(TARGET)))
    def test_actual_source_article_exists(self):
        path=ROOT / "_posts" / "jekyll-eu-consent-revocation-en" / "2026-11-10-jekyll-eu-consent-revocation-en.md"
        self.assertTrue(path.is_file())
        s=path.read_text(encoding="utf-8")
        self.assertIn("permalink: "+TARGET,s)
        self.assertIn("d3ce5a1be67c3e014db547521bd333f849d1fb53",s)

if __name__=="__main__":
    unittest.main()

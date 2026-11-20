"""Keep the homepage evidence preview aligned with source-verified listings."""
from pathlib import Path
import re
import unittest

ROOT = Path(__file__).resolve().parents[1]
HOME = ROOT / "portfolio/index.html"
RECORDS = ROOT / "_data/recognitions.yml"
INCLUDE = ROOT / "_includes/portfolio-evidence.html"

FEATURED = ("ncase-space-atlas-programs", "webapps-spoonie-listing")


class FeaturedVerifiedListings(unittest.TestCase):
    def test_exact_two_eligible_listings_are_in_home_preview(self):
        home = HOME.read_text("utf-8")
        self.assertIn('{% include portfolio-evidence.html type="publication" %}', home)
        self.assertIn(
            '{% include portfolio-evidence.html type="listing" ids="ncase-space-atlas-programs,webapps-spoonie-listing" %}',
            home,
        )

    def test_original_records_are_publicly_confirmed_listings(self):
        records = RECORDS.read_text("utf-8")
        for rid in FEATURED:
            entry = re.search(
                r"(?ms)^- id: " + re.escape(rid) + r"\n(.*?)(?=^- id: |\Z)",
                records,
            )
            self.assertIsNotNone(entry, rid)
            for field in ("type: listing", "status: confirmed", "case_ko:", "case_en:", "url:"):
                self.assertIn(field, entry.group(1), (rid, field))

    def test_reuses_existing_source_link_and_evidence_tracking(self):
        component = INCLUDE.read_text("utf-8")
        self.assertIn("include.ids contains record.id", component)
        self.assertIn('data-evidence-id="{{ record.id | escape }}"', component)
        self.assertIn('href="{{ record.url | escape }}"', component)
        self.assertNotIn("\ufffd", HOME.read_text("utf-8"))


if __name__ == "__main__":
    unittest.main()

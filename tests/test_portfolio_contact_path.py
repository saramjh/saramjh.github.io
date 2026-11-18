"""A direct, non-sending path to the already-public developer contact."""
import re
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
HOME = ROOT / "portfolio/index.html"
PROJECT = ROOT / "_layouts/project.html"
CONFIG = ROOT / "_config.yml"


class PortfolioContactJourney(unittest.TestCase):
    def test_public_owner_contact_matches_the_existing_site_config(self):
        config = CONFIG.read_text(encoding="utf8")
        self.assertRegex(config, r"(?m)^  email: devtestudinidae@gmail\.com\b")
        self.assertIn("# public contact email", config)

    def test_landing_page_has_one_direct_non_sending_contact_cta(self):
        home = HOME.read_text(encoding="utf8")
        self.assertEqual(home.count('class="folio-text-cta folio-contact-cta"'), 1)
        self.assertEqual(home.count('href="mailto:{{ site.author.email | escape }}"'), 1)
        self.assertIn("Email the developer", home)
        self.assertIn('href="#selected-work"', home)
        self.assertIn('href="#external-records"', home)

    def test_every_project_case_uses_same_contact_source_and_keeps_its_other_links(self):
        project = PROJECT.read_text(encoding="utf8")
        self.assertEqual(project.count('class="folio-contact-cta"'), 1)
        self.assertEqual(project.count('href="mailto:{{ site.author.email | escape }}"'), 1)
        self.assertIn('href="/portfolio/"', project)
        self.assertIn('href="/portfolio/recognition/"', project)
        self.assertIn('Email the developer', project)

    def test_no_new_form_tracking_or_auto_send_service(self):
        for f in (HOME, PROJECT):
            s = f.read_text(encoding="utf8")
            self.assertNotIn("mailto:someone@", s)
            self.assertNotIn("fetch('https://", s)
            self.assertNotIn('onsubmit=', s)
            self.assertNotIn("gtag('event', 'contact'", s)
            self.assertNotIn("formspree.io", s)


if __name__ == "__main__":
    unittest.main()

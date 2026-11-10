"""Original Jekyll privacy-choice source, bilingual editorial and image contracts."""
from pathlib import Path
import re
import subprocess
import unittest

ROOT = Path(__file__).resolve().parents[1]
STEM = "jekyll-eu-consent-revocation"
IMG = ROOT / "assets" / "img" / "dev-eu-consent-choices-20261110"
COMMIT = "https://github.com/saramjh/saramjh.github.io/commit/d3ce5a1be67c3e014db547521bd333f849d1fb53"
GOOGLE = "https://developers.google.com/funding-choices/fc-api-docs"


def page(lang):
    path = ROOT / "_posts" / (STEM + "-" + lang) / (
        "2026-11-10-" + STEM + "-" + lang + ".md"
    )
    source = path.read_text(encoding="utf-8")
    match = re.match(r"\A---\n(.*?)\n---\n(.*)\Z", source, re.S)
    if not match:
        raise AssertionError(f"Missing or malformed frontmatter: {path}")
    return match.groups()


class ConsentChoicePublicationTests(unittest.TestCase):
    def test_first_party_source_and_clear_test_boundary(self):
        for lang in ("ko", "en"):
            with self.subTest(lang=lang):
                front, body = page(lang)
                self.assertIn(COMMIT, body)
                self.assertIn(GOOGLE, body)
                self.assertIn("CONSENT_API_READY", body)
                self.assertIn("gdprApplies", body)
                self.assertIn("showRevocationMessage", body)
                self.assertIn("~~~javascript", body)
                self.assertIn("/privacy/", body)
                self.assertIn("/jekyll-dnt-analytics-compress-regression-" + lang + "/", body)
                self.assertNotIn("GDPR compliant", body)
                self.assertNotIn("100% compliant", body)
                self.assertGreaterEqual(body.count("\n## "), 4)
                self.assertIn("date: 2026-11-10", front)

    def test_native_localization_and_metadata(self):
        for lang, other in (("ko", "en"), ("en", "ko")):
            with self.subTest(lang=lang):
                front, body = page(lang)
                self.assertIn("permalink: /" + STEM + "-" + lang + "/", front)
                self.assertIn("lang: " + lang, front)
                self.assertIn("alternate_lang: " + other, front)
                self.assertIn("alternate_url: /" + STEM + "-" + other + "/", front)
                self.assertIn("published: true", front)
                self.assertIn("image_width: 1200", front)
                self.assertIn("image_height: 630", front)
                self.assertIn("seo:\n  title:", front)
                self.assertIn("/" + STEM + "-" + other + "/", body)
                self.assertIn('<figure>', body)
                self.assertIn('<figcaption>', body)
                self.assertIn('loading="lazy"', body)

    def test_distinct_original_images_and_renderer(self):
        data = {}
        for lang in ("ko", "en"):
            png = IMG / f"consent-choices-{lang}.png"
            raw = png.read_bytes()
            self.assertEqual(raw[:8], b"\x89PNG\r\n\x1a\n")
            self.assertEqual((int.from_bytes(raw[16:20], "big"),
                              int.from_bytes(raw[20:24], "big")), (1200, 630))
            self.assertGreater(len(raw), 40000)
            data[lang] = raw
        self.assertNotEqual(data["en"], data["ko"])
        renderer = (ROOT / "scripts" / "render_eu_consent_choices.swift").read_text()
        self.assertIn("gdprApplies", renderer)
        self.assertIn("NSBitmapImageRep", renderer)
        self.assertIn("does not depict any real visitor", renderer)

    def test_public_root_page_scope_is_narrow(self):
        footer = (ROOT / "_includes" / "footer.html").read_text(encoding="utf-8")
        privacy = (ROOT / "privacy.md").read_text(encoding="utf-8")
        self.assertIn("page.ads != false", footer)
        self.assertIn("page.date", footer)
        self.assertIn("jekyll.environment == 'production'", footer)
        self.assertIn('id="privacy-choices" hidden', footer)
        self.assertIn("CONSENT_API_READY", footer)
        self.assertIn('window.__tcfapi("addEventListener", 0', footer)
        self.assertIn("showRevocationMessage", footer)
        self.assertIn("ads: false", privacy)
        self.assertIn("tracking: false", privacy)

    def test_mocked_runtime_has_no_provider_side_effects(self):
        test_file = ROOT / "tests" / "eu_privacy_choices_runtime.cjs"
        run = subprocess.run(["node", str(test_file)], cwd=ROOT,
                             capture_output=True, text=True, timeout=15)
        self.assertEqual(run.returncode, 0, run.stderr)
        self.assertIn("PASS 6 mocked footer cases", run.stdout)
        self.assertIn("provider side effects: 0", run.stdout)


if __name__ == "__main__":
    unittest.main()

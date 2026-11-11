"""Source-bound bilingual navigation for public achievement records."""
from pathlib import Path
import re
import unittest


ROOT = Path(__file__).resolve().parents[1]
LEDGER = ROOT / "_data" / "recognitions.yml"
INCLUDE = ROOT / "_includes" / "portfolio-evidence.html"
CSS = ROOT / "assets" / "css" / "portfolio.css"

EXPECTED = {
    "birds-photo-10000": "koreaves-published-contributions",
    "suncheon-10000": "koreaves-published-contributions",
    "one-earth-koreaves-feature": "koreaves-oneearth-author-achievement",
    "unsustainable-koreaves-bird-map": "koreaves-unsustainable-bird-map",
    "webapps-spoonie-listing": "spoonie-webapps-directory",
    "eusci-space-atlas-diagrams": "space-atlas-eusci-diagrams",
    "disquiet-spoonie-first-record": "spoonie-disquiet-first-record",
}


def parse_records():
    source = LEDGER.read_text(encoding="utf8")
    chunks = re.split(r"(?m)^- id: ", source)[1:]
    records = {}
    for chunk in chunks:
        lines = chunk.splitlines()
        record_id = lines[0].strip()
        record = {}
        for line in lines[1:]:
            match = re.fullmatch(r"  ([a-z_]+):\s*(.*)", line)
            if match:
                record[match.group(1)] = match.group(2).strip('"\'')

        if record_id in records:
            raise AssertionError("Duplicate public record: " + record_id)
        records[record_id] = record
    return records


class EvidenceContextLinksTest(unittest.TestCase):
    def test_canonical_records_only_and_original_source_retained(self):
        records = parse_records()
        self.assertEqual(len(records), 11)
        for record_id, slug in EXPECTED.items():
            item = records[record_id]
            self.assertEqual(item["status"], "confirmed")
            self.assertTrue(item["url"].startswith("https://"))
            self.assertEqual(item["case_ko"], f"/{slug}-ko/")
            self.assertEqual(item["case_en"], f"/{slug}-en/")
        self.assertEqual(
            records["eusci-space-atlas-diagrams"]["url"],
            "https://eusci.org.uk/2026/11/10/three-space-diagrams-three-missing-clues/",
        )
        self.assertEqual(records["eusci-space-atlas-diagrams"]["date"], "2026-11-10")
        self.assertEqual(records["eusci-space-atlas-diagrams"]["type"], "publication")
        self.assertIn("not university endorsement", records["eusci-space-atlas-diagrams"]["detail"])
        self.assertEqual(
            records["disquiet-spoonie-first-record"]["url"],
            "https://disquiet.io/articles/MVsxQv",
        )
        self.assertEqual(
            records["disquiet-spoonie-first-record"]["date"], "2026-10-13"
        )
        self.assertIn("Self-authored", records["disquiet-spoonie-first-record"]["detail"])
        self.assertEqual(records["disquiet-spoonie-first-record"]["project"], "spoonie")
        self.assertIn("Not independent press", records["disquiet-spoonie-first-record"]["detail"])
        self.assertTrue(
            all(("case_ko" in r) == ("case_en" in r) for r in records.values())
        )

    def test_each_target_has_a_real_published_bilingual_jekyll_page(self):
        records = parse_records()
        for record_id, slug in EXPECTED.items():
            for lang, opposite in (("ko", "en"), ("en", "ko")):
                target = records[record_id][f"case_{lang}"]
                source_files = [p for p in (ROOT / "_posts").rglob("*.md") if "permalink: " + target in p.read_text(encoding="utf8")]
                self.assertEqual(len(source_files), 1, (record_id, target, source_files))
                post = source_files[0].read_text(encoding="utf8")
                self.assertIn("permalink: " + target, post)
                self.assertIn("lang: " + lang, post)
                self.assertIn("published: true", post)
                if "alternate_url:" in post:
                    self.assertIn("alternate_url: " + records[record_id][f"case_{opposite}"], post)

    def test_eusci_byline_has_one_attributed_source_and_uses_owned_visual(self):
        original = "https://eusci.org.uk/2026/11/10/three-space-diagrams-three-missing-clues/"
        owned_image = "/space-atlas-student/space-atlas-hero.png"
        self.assertTrue((ROOT / "_posts/space-atlas-student/space-atlas-hero.png").is_file())
        for language in ("ko", "en"):
            p = ROOT / f"_posts/space-atlas-eusci-diagrams-{language}" / f"2026-11-11-space-atlas-eusci-diagrams-{language}.md"
            post = p.read_text(encoding="utf-8")
            self.assertIn(original, post)
            self.assertIn(f"image: {owned_image}", post)
            self.assertIn(f'<img src="{owned_image}"', post)
            self.assertNotIn("i0.wp.com", post)
            self.assertNotIn("commons.wikimedia.org/wiki/File:Solar", post)
            self.assertIn("Jihun Oh", post)
            self.assertIn("Priscilla Wong", post)
            self.assertIn("published: true", post)

    def test_shared_evidence_component_preserves_external_and_internal_destinations(self):
        include = INCLUDE.read_text(encoding="utf8")
        css = CSS.read_text(encoding="utf8")
        self.assertEqual(include.count('href="{{ record.url | escape }}"'), 1)
        self.assertIn("{% if record.case_ko or record.case_en %}", include)
        self.assertIn('data-case-lang="ko"', include)
        self.assertIn('data-case-lang="en"', include)
        self.assertIn('href="{{ record.case_ko | relative_url | escape }}"', include)
        self.assertIn('href="{{ record.case_en | relative_url | escape }}"', include)
        tracker = (ROOT / "assets" / "js" / "portfolio.js").read_text(encoding="utf8")
        self.assertIn("portfolio_evidence_case", tracker)
        self.assertIn("id+':'+lang", tracker)
        self.assertIn("navigator.msDoNotTrack==='1'", tracker)
        privacy = (ROOT / "privacy.md").read_text(encoding="utf8")
        self.assertIn("Korean or English developer note", privacy)
        self.assertIn("Developer notes:", include)
        self.assertIn("한국어", include)
        self.assertIn("English", include)
        self.assertIn(".folio-evidence-context a:focus-visible", css)
        for page in ("portfolio/index.html", "portfolio/recognition/index.html"):
            self.assertIn("portfolio-evidence.html", (ROOT / page).read_text(encoding="utf8"))


if __name__ == "__main__":
    unittest.main()

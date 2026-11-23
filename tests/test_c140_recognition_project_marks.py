"""First-party project marks in the public evidence archive; no third-party brand media."""
from pathlib import Path
import re
import unittest

ROOT = Path(__file__).resolve().parents[1]
INCLUDE = ROOT / "_includes" / "portfolio-evidence.html"
CSS = ROOT / "assets/css/portfolio.css"
LEDGER = ROOT / "_data" / "recognitions.yml"
EXPECTED = {
    "koreaves": ("koreaves.png", "KoreAves"),
    "space-atlas": ("space-atlas.svg", "Space Atlas"),
    "spoonie": ("spoonie.png", "Spoonie"),
    "scratch-lottery": ("scratch-lottery.svg", "Scratch Lottery"),
}


class ProjectMarkTests(unittest.TestCase):
    def setUp(self):
        self.include = INCLUDE.read_text(encoding="utf-8")
        self.css = CSS.read_text(encoding="utf-8")
        self.ledger = LEDGER.read_text(encoding="utf-8")

    def test_exact_project_icons_from_first_party_assets_only(self):
        projects = set(re.findall(r"(?m)^  project: ([a-z-]+)$", self.ledger))
        self.assertEqual(projects, set(EXPECTED))
        for project, (basename, label) in EXPECTED.items():
            icon = f"/assets/images/project-icons/{basename}"
            self.assertTrue((ROOT / icon.lstrip("/")).is_file(), icon)
            self.assertIn(f"{{% when '{project}' %}}", self.include)
            self.assertIn(f"record_project_icon = '{icon}'", self.include)
            self.assertIn(f"record_project_name = '{label}'", self.include)
        self.assertEqual(self.include.count("record_project_icon = '/assets/"), 4)
        self.assertNotIn("record_project_icon = 'https://", self.include)

    def test_same_include_is_used_by_both_locales_and_milestones(self):
        for path in [
            ROOT / "portfolio/recognition/index.html",
            ROOT / "portfolio/recognition/ko/index.html",
            ROOT / "_layouts/milestone.html",
            ROOT / "_layouts/project.html",
        ]:
            self.assertIn("include portfolio-evidence.html", path.read_text(encoding="utf-8"), str(path))
        self.assertIn("record.status == 'confirmed'", self.include)
        self.assertIn('href="{{ record.url | escape }}"', self.include)
        self.assertIn("{{ record.title | escape }}", self.include)

    def test_project_mark_is_an_image_with_accessible_localized_alt(self):
        self.assertIn('class="folio-evidence-project-mark"', self.include)
        self.assertIn('src="{{ record_project_icon | relative_url }}"', self.include)
        self.assertIn("{{ record_project_name | escape }}", self.include)
        self.assertIn("프로젝트 아이콘", self.include)
        self.assertIn("project icon", self.include)
        self.assertIn('width="22" height="22"', self.include)
        self.assertIn('loading="lazy" decoding="async"', self.include)
        self.assertIn("{% if record_project_icon != '' %}", self.include)

    def test_style_is_small_and_does_not_change_archive_grid(self):
        self.assertIn(".folio-evidence-source .folio-evidence-project-mark", self.css)
        self.assertIn("width:22px;height:22px", self.css)
        self.assertIn("object-fit:contain", self.css)
        self.assertIn("vertical-align:middle", self.css)
        self.assertIn("grid-template-columns:170px minmax(0,1fr) 118px", self.css)
        self.assertIn("@media(max-width:680px)", self.css)

    def test_copy_and_proof_contract_remains_exact(self):
        self.assertIn('{{ record.detail_ko | default: record.detail | escape }}', self.include)
        self.assertIn('{{ record.case_ko | relative_url | escape }}', self.include)
        self.assertIn('{{ record.case_en | relative_url | escape }}', self.include)
        self.assertIn("record.date | date:", self.include)
        self.assertNotIn("\ufffd", self.include)
        self.assertNotIn("????", self.include)
        for file in (INCLUDE, CSS):
            self.assertNotIn("\ufffd", file.read_text("utf-8"))


if __name__ == "__main__":
    unittest.main()

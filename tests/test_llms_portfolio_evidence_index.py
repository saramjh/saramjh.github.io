"""Offline source-bound checks for the existing first-party llms.txt index."""

from pathlib import Path
import re
import unittest

ROOT = Path(__file__).resolve().parents[1]
LLMS = (ROOT / "llms.txt").read_text(encoding="utf-8")
SECTION = LLMS.split("## Developer projects and public evidence\n", 1)[1].split("\n## ", 1)[0]
EXPECTED = {
    "/portfolio/": ROOT / "portfolio/index.html",
    "/portfolio/recognition/": ROOT / "portfolio/recognition/index.html",
    "/portfolio/space-atlas/": ROOT / "_projects/space-atlas.md",
    "/portfolio/koreaves/": ROOT / "_projects/koreaves.md",
    "/portfolio/spoonie/": ROOT / "_projects/spoonie.md",
    "/space-atlas-eusci-diagrams-en/": ROOT / "_posts/space-atlas-eusci-diagrams-en/2026-11-11-space-atlas-eusci-diagrams-en.md",
    "/space-atlas-eusci-diagrams-ko/": ROOT / "_posts/space-atlas-eusci-diagrams-ko/2026-11-11-space-atlas-eusci-diagrams-ko.md",
    "/space-atlas-ncase-programs-en/": ROOT / "_posts/space-atlas-ncase-programs-en/2026-11-10-space-atlas-ncase-programs-en.md",
    "/space-atlas-ncase-programs-ko/": ROOT / "_posts/space-atlas-ncase-programs-ko/2026-11-10-space-atlas-ncase-programs-ko.md",
    "/space-atlas-share-my-lesson-en/": ROOT / "_posts/space-atlas-share-my-lesson-en/2026-11-10-space-atlas-share-my-lesson-en.md",
    "/space-atlas-share-my-lesson-ko/": ROOT / "_posts/space-atlas-share-my-lesson-ko/2026-11-10-space-atlas-share-my-lesson-ko.md",
    "/earth-seasons-no-tilt-experiment-en/": ROOT / "_posts/earth-seasons-no-tilt-experiment-en/2026-11-15-earth-seasons-no-tilt-experiment-en.md",
    "/earth-seasons-no-tilt-experiment-ko/": ROOT / "_posts/earth-seasons-no-tilt-experiment-ko/2026-11-15-earth-seasons-no-tilt-experiment-ko.md",
    "/koreaves-english-display-labels-en/": ROOT / "_posts/koreaves-english-display-labels-en/2026-11-28-koreaves-english-display-labels-en.md",
    "/koreaves-english-display-labels-ko/": ROOT / "_posts/koreaves-english-display-labels-ko/2026-11-28-koreaves-english-display-labels-ko.md",
    "/koreaves-published-contributions-en/": ROOT / "_posts/folio-koreaves-publications-en/2026-11-02-folio-koreaves-publications-en.md",
    "/koreaves-bou-when-records-become-maps-en/": ROOT / "_posts/koreaves-bou-when-records-become-maps-en/2026-11-23-koreaves-bou-when-records-become-maps-en.md",
    "/koreaves-bou-when-records-become-maps-ko/": ROOT / "_posts/koreaves-bou-when-records-become-maps-ko/2026-11-23-koreaves-bou-when-records-become-maps-ko.md",
    "/spoonie-pwa-search-state-recovery-en/": ROOT / "_posts/spoonie-pwa-search-state-recovery-en/2026-11-16-spoonie-pwa-search-state-recovery-en.md",
    "/spoonie-pwa-search-state-recovery-ko/": ROOT / "_posts/spoonie-pwa-search-state-recovery-ko/2026-11-16-spoonie-pwa-search-state-recovery-ko.md",
    "/spoonie-rsc-prefetch-20261119-en/": ROOT / "_posts/spoonie-rsc-prefetch-20261119-en/2026-11-19-spoonie-rsc-prefetch-20261119-en.md",
    "/spoonie-rsc-prefetch-20261119-ko/": ROOT / "_posts/spoonie-rsc-prefetch-20261119-ko/2026-11-19-spoonie-rsc-prefetch-20261119-ko.md",
}


class LLMsPortfolioEvidenceIndexTest(unittest.TestCase):
    def test_all_curated_links_have_exact_existing_local_sources(self):
        links = re.findall(r"(?m)^- \[[^\]]+\]\(https://saramjh\.github\.io(/[^)]+)\): ", SECTION)
        paths = list(links)
        self.assertEqual(len(paths), len(EXPECTED))
        self.assertCountEqual(paths, list(EXPECTED))
        self.assertEqual(len(paths), len(set(paths)))
        for path, source in EXPECTED.items():
            self.assertTrue(source.is_file(), (path, source))
            body = source.read_text(encoding="utf-8")
            if path.startswith("/portfolio/") and path not in ("/portfolio/", "/portfolio/recognition/"):
                self.assertIn("slug: " + path.strip("/").split("/")[-1], body, (path, source))
                self.assertIn("layout: project", body)
            else:
                self.assertIn("permalink: " + path, body, (path, source))

    def test_bou_pair_has_reciprocal_locales_and_original_publication(self):
        for lang, alternate in (("en", "ko"), ("ko", "en")):
            path = f"/koreaves-bou-when-records-become-maps-{lang}/"
            other = f"/koreaves-bou-when-records-become-maps-{alternate}/"
            body = EXPECTED[path].read_text(encoding="utf-8")
            self.assertIn(f"lang: {lang}\n", body)
            self.assertIn(f"alternate_url: {other}\n", body)
            self.assertIn("https://bou.org.uk/blog-oh-when-records-become-maps/", body)
            self.assertIn(f"https://saramjh.github.io{path}", SECTION)

    def test_index_describes_source_categories_without_claiming_adoption(self):
        self.assertIn("External writing, resource listings and catalogue records", SECTION)
        self.assertIn("A public programs-directory entry", SECTION)
        self.assertIn("An author-contributed teaching resource", SECTION)
        self.assertNotRegex(SECTION.lower(), r"university endorsed|measured adoption|guaranteed traffic")
        self.assertIn("Monthly Functions savings were not measured.", SECTION)
        self.assertIn("월간 Functions 절감 효과는 확인되지 않았다.", SECTION)
        self.assertIn("## Hardware & macOS Troubleshooting Guides", LLMS)
        self.assertIn("## Web Utilities & Interactive Tools", LLMS)


if __name__ == "__main__":
    unittest.main()

"""Evidence-bound bilingual technical case study of the original author PR #240."""
from pathlib import Path
import re
import unittest

ROOT = Path(__file__).resolve().parents[1]
POSTS = {
    "ko": ROOT / "_posts/koajs-attw-security-repair-ko/2026-11-15-koajs-attw-security-repair-ko.md",
    "en": ROOT / "_posts/koajs-attw-security-repair-en/2026-11-15-koajs-attw-security-repair-en.md",
}

PR = "https://github.com/koajs/session/pull/240"
RUN = "https://github.com/koajs/session/actions/runs/43637614241"
COMMIT = "57e88bac2663135c1d8fb5da243d4c6173f84924"
ADVISORY = "https://github.com/advisories/GHSA-px8p-9vwx-vf98"

class OriginalKoaContributorCase(unittest.TestCase):
    def test_language_pairs_frontmatter_and_permalinks(self):
        for lang, path in POSTS.items():
            with self.subTest(lang=lang):
                t = path.read_text(encoding="utf-8")
                other = "en" if lang == "ko" else "ko"
                self.assertIn("date: 2026-11-15", t)
                self.assertIn("layout: default", t)
                self.assertIn(f"lang: {lang}", t)
                self.assertIn(f"alternate_lang: {other}", t)
                self.assertIn(f"permalink: /koajs-attw-security-repair-{lang}/", t)
                self.assertIn(f"alternate_url: /koajs-attw-security-repair-{other}/", t)
                self.assertIn("published: true", t)
                self.assertIn("seo:", t)
                self.assertIn(f"/koajs-attw-security-repair-{other}/", t)
                self.assertNotIn("\ufffd", t)
                self.assertFalse(re.search(r"\?{4,}", t))
                self.assertFalse(any(0xd800 <= ord(c) <= 0xdfff for c in t))

    def test_real_first_party_pr_ci_and_security_sources(self):
        for lang, path in POSTS.items():
            with self.subTest(lang=lang):
                t = path.read_text("utf-8")
                for term in (PR, RUN, COMMIT, ADVISORY,
                             "fflate", "0.8.2", "0.7.5", "0.8.3",
                             "Node 18", "13", "attw --pack"):
                    self.assertIn(term, t)

    def test_truth_boundary_and_independent_zod_pr(self):
        ko = POSTS["ko"].read_text("utf-8")
        en = POSTS["en"].read_text("utf-8")
        self.assertIn("병합되지", ko)
        self.assertIn("not merged", en)
        self.assertIn("https://github.com/koajs/session/pull/238", ko)
        self.assertIn("https://github.com/koajs/session/pull/238", en)
        self.assertIn("CVE-2026-45820", ko)
        self.assertIn("CVE-2026-45820", en)
        self.assertNotIn("유지관리자가 승인", ko)
        self.assertNotIn("maintainers approved", en)

    def test_explanation_not_a_triumphal_ci_status_stub(self):
        for lang, path in POSTS.items():
            with self.subTest(lang=lang):
                t = path.read_text("utf-8")
                self.assertGreater(len(t), 2400)
                self.assertIn("@arethetypeswrong/core", t)
                self.assertIn("package.json", t)
                self.assertIn("npm run ci", t)
                self.assertIn("https://github.com/101arrowz/fflate/issues/258", t)

if __name__ == "__main__":
    unittest.main()

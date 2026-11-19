"""Keep a single source-backed bilingual note about the One Earth homepage card.

Source observation: original One Earth homepage returned HTTP 200 on
2026-11-20 KST and linked an existing Oct 28 KoreAves article. These tests
do not claim continuing placement or publisher analytics.
"""
import re
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
CASES = {
    "ko": ROOT / "_posts/koreaves-oneearth-author-achievement-ko"
    / "2026-11-10-koreaves-oneearth-author-achievement-ko.md",
    "en": ROOT / "_posts/koreaves-oneearth-author-achievement-en"
    / "2026-11-10-koreaves-oneearth-author-achievement-en.md",
}


class OneEarthHomepageVisibilityTest(unittest.TestCase):
    def test_source_is_an_existing_author_publication_not_a_new_one(self):
        for lang, path in CASES.items():
            with self.subTest(lang=lang):
                source = path.read_text(encoding="utf-8")
                self.assertEqual(source.split("---", 2)[1].count("date: 2026-11-10"), 1)
                self.assertIn("https://www.oneearth.org/koreaves/", source)
                self.assertIn("[One Earth 홈페이지](https://www.oneearth.org/)" if lang == "ko"
                              else "[One Earth homepage](https://www.oneearth.org/)", source)
                self.assertEqual(source.count("https://www.oneearth.org/"), 4)
                self.assertNotIn("\ufffd", source)
                self.assertGreaterEqual(len(re.findall(r"[\\uac00-\\ud7a3]", source)), 100
                                        if lang == "ko" else 0)

    def test_placement_observation_is_dated_and_not_equated_to_adoption(self):
        ko = CASES["ko"].read_text(encoding="utf-8")
        en = CASES["en"].read_text(encoding="utf-8")
        self.assertIn("2026년 11월 20일", ko)
        self.assertIn("November 20, 2026", en)
        self.assertIn("새로운 글이 한 편 더 실린 것은 아니며", ko)
        self.assertIn("not a second publication", en)
        self.assertIn("실제 조회·방문 증가량은 확인되지 않았다", ko)
        self.assertIn("whether it brought more readers", en)
        self.assertIn("원문에는 Jihun Oh가 작성자로", ko)
        self.assertIn("credits Jihun Oh as a contributor", en)
        # An original developer image is reused. No publisher photograph imported.
        self.assertIn("/assets/images/portfolio/koreaves-gis.jpg", ko)
        self.assertIn("/assets/images/portfolio/koreaves-gis.jpg", en)


if __name__ == "__main__":
    unittest.main()

from pathlib import Path
import re
import unittest

ROOT = Path(__file__).resolve().parents[1]
EN = ROOT / "_posts/recipe-scaling-application/2024-09-03-recipe-scaling-application.md"
KO = ROOT / "_posts/ko-recipe-scaling-application/2026-11-19-ko-recipe-scaling-application.md"

class RecipeScalingBilingual(unittest.TestCase):
    def test_existing_english_route_and_reciprocal_korean_edition(self):
        en = EN.read_text(encoding="utf-8")
        ko = KO.read_text(encoding="utf-8")
        fields = [
            (en, "permalink: /recipe-scaling-application/", "lang: en",
             "alternate_lang: ko", "alternate_url: /ko-recipe-scaling-application/"),
            (ko, "permalink: /ko-recipe-scaling-application/", "lang: ko",
             "alternate_lang: en", "alternate_url: /recipe-scaling-application/"),
        ]
        for body, *needed in fields:
            for item in needed:
                self.assertIn(item, body)
            self.assertIn("recipescalingapplication.jpg", body)
            self.assertIn("https://saramjh.github.io/recipeCalc/", body)
            self.assertIn("https://github.com/saramjh/recipeCalc", body)
            self.assertNotIn("\ufffd", body)
            self.assertNotIn("????", body)

    def test_actual_calculation_example_and_honest_limits(self):
        for page in (EN, KO):
            body = page.read_text(encoding="utf-8")
            self.assertIn("100g flour", body)
            self.assertIn("200ml water", body)
            self.assertIn("20g sugar", body)
            self.assertIn("150g", body)
            self.assertIn("300ml", body)
            self.assertIn("30g", body)
            self.assertIn("1.5", body)
            self.assertIn("1/2", body)
            self.assertIn("0.5", body)
        self.assertIn("unit conversion", EN.read_text(encoding="utf-8").lower())
        self.assertIn("단위 변환", KO.read_text(encoding="utf-8"))

    def test_original_english_url_is_not_removed(self):
        en = EN.read_text(encoding="utf-8")
        self.assertEqual(len(re.findall(r"^permalink: /recipe-scaling-application/$", en, re.M)), 1)
        self.assertIn("legacy_asset_url: /posts/recipe-scaling-application/", en)

if __name__ == "__main__":
    unittest.main()

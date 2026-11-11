"""Guard the source-backed Spoonie origin notes without exposing family identity."""
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


class SpoonieOriginEvidenceTest(unittest.TestCase):
    def test_bilingual_personal_motivation_and_technical_timeline(self):
        pages = {
            "ko": ROOT / "_posts/recipe-calc-to-spoonie-origin-ko/2026-11-11-recipe-calc-to-spoonie-origin-ko.md",
            "en": ROOT / "_posts/recipe-calc-to-spoonie-origin-en/2026-11-11-recipe-calc-to-spoonie-origin-en.md",
        }
        for lang, file in pages.items():
            with self.subTest(language=lang):
                source = file.read_text(encoding="utf8")
                for stable in ["2024", "2025", "recipeCalc", "spoonie.kr", "published: true", "/recipe-scaling-application/recipescalingapplication.jpg"]:
                    self.assertIn(stable, source)
                if lang == "ko":
                    for fact in ["디저트 카페 레시피", "이사하면서", "레시피 노트를 발견", "결국 버려졌고", "다시 찾아볼 수 없게", "작성자에 관한 정보를 공개하지 않는다"]:
                        self.assertIn(fact, source)
                    self.assertNotIn("아내", source)
                else:
                    for fact in ["dessert-café recipes", "During a move", "handwritten recipe notebook", "eventually discarded", "regretted losing access", "not reproducing the notebook or identifying its writer"]:
                        self.assertIn(fact, source)
                    self.assertNotIn("my wife", source.lower())
                self.assertNotIn("???", source)
                self.assertNotIn("\ufffd", source)
                self.assertNotIn("notebook photo", source.lower())


if __name__ == "__main__":
    unittest.main()

"""Pin image-specific, visually verified alt text for 11 published Sigub screenshots.

The original JPGs were inspected directly. These tests protect reader accessibility
without changing factual screenshots, original account data, routes or app code.
"""
from pathlib import Path
from urllib.parse import unquote
import re
import unittest

ROOT = Path(__file__).resolve().parents[1]
POST = ROOT / "_posts/pay-calculator-for-part-time-job/2025-07-08-pay-calculator-for-part-time-job.md"
FOLDER = POST.parent
TEXT = POST.read_text(encoding="utf-8")
SCREENS = re.findall(r'<img\s+src="([^"]+)"\s+alt="([^"]*)">', TEXT)
EXPECTED = [
    ("23.38.18", "시급이요 로그인 화면과 Google 로그인 버튼"),
    ("23.39.36", "직업 관리 창에 등록된 카페알바와 새 직업 추가 버튼"),
    ("23.39.52", "2025년 7월 근무 달력과 시급 설정·월급 확인 버튼"),
    ("23.40.05", "앱 메뉴에 다크 모드, 직업 관리, 홈 화면에 추가 항목 표시"),
    ("23.40.20", "7월 3일 근무 기록이 없는 날짜 상세 창과 추가 버튼"),
    ("23.40.36", "새 근무 기록 창에서 카페알바 시급 12,000원과 출퇴근 시간 입력"),
    ("23.41.04", "7월 3일 카페알바 근무 11시간과 일급 132,000원 상세 내역"),
    ("23.41.41", "7월 달력에서 3일과 4일 근무 시간이 표시된 화면"),
    ("23.41.56", "2025년 7월 월급 보고서의 총 근무 21시간과 총 수입 252,000원"),
    ("23.42.15", "카페알바 시급 설정에서 2025년 7월 1일 적용 시급 12,000원 입력"),
    ("23.42.33", "새 직업 추가 창의 직업 이름·설명·월급일·색상 입력 항목"),
]


class SigubScreenshotAltAccessibility(unittest.TestCase):
    def test_exactly_eleven_published_screens(self):
        self.assertEqual(len(SCREENS), 11)

    def test_every_original_image_exists_and_is_jpeg(self):
        for src, _ in SCREENS:
            with self.subTest(src=src):
                local = FOLDER / unquote(src)
                self.assertTrue(local.is_file(), str(local))
                self.assertEqual(local.read_bytes()[:2], b"\xff\xd8")

    def test_images_are_in_original_chronological_order(self):
        self.assertEqual(
            [src for src, _ in SCREENS],
            [f"Screenshot%202025-07-08%20at%20{time}.JPG" for time, _ in EXPECTED],
        )

    def test_every_label_is_unique_and_has_real_korean_description(self):
        labels = [alt for _, alt in SCREENS]
        self.assertEqual(len(set(labels)), 11)
        self.assertTrue(all(len(x) >= 16 and re.search(r"[가-힣]", x) for x in labels))

    def test_no_useless_app_view_placeholder(self):
        self.assertNotIn('alt="app view"', TEXT)
        for _, alt in SCREENS:
            self.assertNotIn(alt.lower().strip(), {"image", "photo", "app view", "screenshot", "이미지", "사진"})

    def test_no_private_visible_account_identifier_is_transcribed(self):
        self.assertTrue(all("saramjh" not in alt.lower() for _, alt in SCREENS))

    def test_existing_frontmatter_permalink_and_project_title_stay(self):
        self.assertIn('title: "💰 시급이요 - 아르바이트 시급/근무/수입 계산기"', TEXT)
        self.assertIn("date: 2025-07-08", TEXT)
        self.assertIn("permalink: /pay-calculator-for-part-time-job/", TEXT)
        self.assertIn("lang: ko", TEXT)

    def test_original_hero_image_remains_valid(self):
        hero = re.search(r"^image: (\S+)$", TEXT, flags=re.MULTILINE)
        self.assertIsNotNone(hero)
        self.assertEqual((FOLDER / Path(unquote(hero.group(1))).name).resolve(),
                         (FOLDER / unquote(SCREENS[0][0])).resolve())
        self.assertTrue((FOLDER / Path(unquote(hero.group(1))).name).is_file())

    def test_live_project_and_developer_source_links_are_still_present(self):
        self.assertIn("https://sigub.kr/", TEXT)
        self.assertIn("https://github.com/saramjh/szwagecalc.git", TEXT)
        self.assertIn("npm run deploy:manual", TEXT)

    def test_instructions_and_user_features_remain_visible(self):
        for term in ("### 🚀 **바로가기**", "### ✨ **주요 특징**", "### 🚀 **사용법**", "### 📱 **휴대폰에서 홈 화면에 추가하는 방법**"):
            with self.subTest(term=term):
                self.assertIn(term, TEXT)

    def test_numeric_alt_facts_match_original_images(self):
        self.assertIn("12,000원", SCREENS[5][1])
        self.assertIn("11시간", SCREENS[6][1])
        self.assertIn("132,000원", SCREENS[6][1])
        self.assertIn("21시간", SCREENS[8][1])
        self.assertIn("252,000원", SCREENS[8][1])

    def test_utf8_has_no_replacement_character(self):
        self.assertNotIn("\ufffd", TEXT)
        self.assertNotIn("????", TEXT)


def make_visual_regression_test(index, timestamp, description):
    def check(self):
        src, alt = SCREENS[index]
        self.assertEqual(src, f"Screenshot%202025-07-08%20at%20{timestamp}.JPG")
        self.assertEqual(alt, description)
    return check


for index, (timestamp, description) in enumerate(EXPECTED):
    setattr(SigubScreenshotAltAccessibility, f"test_visual_screen_{index + 1:02d}",
            make_visual_regression_test(index, timestamp, description))


if __name__ == "__main__":
    unittest.main()

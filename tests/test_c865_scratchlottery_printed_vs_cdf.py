from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]
EN = ROOT / "_posts/scratch-lottery-simulation/2024-09-03-scratch-lottery-simulation.md"
KO = ROOT / "_posts/scratch-lottery-simulation-ko/2026-11-13-scratch-lottery-simulation-ko.md"
OPERATOR_SOURCE = "https://www.texaslottery.com/export/sites/lottery/Games/Scratch_Offs/details.html"

class PhysicalScratchTicketDistinction(unittest.TestCase):
    def test_english_simulated_draw_not_printing_mechanism(self):
        body=EN.read_text(encoding="utf-8")
        self.assertNotIn("the same mechanism a real printed ticket relies on",body)
        self.assertIn("physical scratch tickets have printed outcomes",body)
        self.assertIn("CDF",body)
        self.assertIn(OPERATOR_SOURCE,body)
        for old in ("4,773","2,576","95 Google search clicks","994 impressions","permalink: /scratch-lottery-simulation/"):
            self.assertIn(old,body)

    def test_korean_equivalent_and_original_links(self):
        body=KO.read_text(encoding="utf-8")
        self.assertIn("실물 스크래치 복권은 인쇄된 결과",body)
        self.assertIn(OPERATOR_SOURCE,body)
        self.assertIn("누적확률표(CDF)",body)
        for old in ("4,773","2,576","검색 클릭 95회","검색 노출 994회","permalink: /scratch-lottery-simulation-ko/"):
            self.assertIn(old,body)
        self.assertNotIn("\ufffd",body)

if __name__=="__main__":
    unittest.main()

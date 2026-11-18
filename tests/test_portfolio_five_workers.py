"""Guard the first-party portfolio diagram against stale specialist count and roles."""
import re
import unittest
import xml.etree.ElementTree as ET
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SVG = ROOT / "assets/images/portfolio/agent-architecture.svg"
PROJECT = ROOT / "_projects/ai-agent-systems.md"
HOME = ROOT / "portfolio/index.html"
NS = "{http://www.w3.org/2000/svg}"
EXPECTED = {
    "ave": "KoreAves",
    "orion": "Space Atlas",
    "soy": "Spoonie",
    "riff": "Social Relations Lab",
    "dev": "Maker Log",
}


class FiveWorkerPortfolioDiagramTests(unittest.TestCase):
    def test_svg_has_exact_five_identified_workers_with_accessible_caption(self):
        root = ET.parse(SVG).getroot()
        self.assertEqual(root.tag, NS + "svg")
        self.assertEqual(root.attrib["viewBox"], "0 0 1200 750")
        title = root.find(NS + "title")
        desc = root.find(NS + "desc")
        self.assertIsNotNone(title)
        self.assertIsNotNone(desc)
        self.assertIn("five", "".join(desc.itertext()).lower())
        groups = [g for g in root.iter(NS + "g") if "data-worker" in g.attrib]
        ids = [g.attrib["data-worker"] for g in groups]
        self.assertCountEqual(ids, EXPECTED)
        self.assertEqual(len(ids), len(set(ids)))
        for group in groups:
            worker = group.attrib["data-worker"]
            self.assertIsNotNone(group.find(NS + "rect"), worker)
            labels = " ".join("".join(t.itertext()) for t in group.iter(NS + "text"))
            self.assertIn(worker.capitalize() if worker != "soy" else "Soy", labels)
            self.assertIn(EXPECTED[worker], labels)
        all_words = " ".join(root.itertext()).lower()
        self.assertIn("session supervisor", all_words)
        self.assertIn("persistent execution ledger", all_words)
        self.assertNotIn("tents", all_words)
        self.assertNotIn("product research", all_words)

    def test_hero_and_project_alt_match_current_five_worker_diagram(self):
        project = PROJECT.read_text(encoding="utf8")
        home = HOME.read_text(encoding="utf8")
        self.assertIn("image: /assets/images/portfolio/agent-architecture.svg", project)
        self.assertRegex(project, r"(?m)^image_alt: .*five.*")
        self.assertRegex(home, r'alt="[^"]*five[^"]*project[^"]*worker[^"]*"')
        for content in (project, home):
            self.assertNotIn("four independent project agents", content.lower())
            self.assertNotIn("four independently supervised local project agents", content.lower())


if __name__ == "__main__":
    unittest.main()

"""Original first-party Search Console evidence must not become unsupported adoption."""
import json
import re
import subprocess
import unittest
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
DATA=ROOT/"assets/data/dev-c127-gsc-search-performance-20261123.json"
PORTFOLIO=ROOT/"portfolio/index.html"
ARTICLES={
 "en":ROOT/"_posts/dev-search-evidence-20261123-en/2026-11-23-dev-search-evidence-20261123-en.md",
 "ko":ROOT/"_posts/dev-search-evidence-20261123-ko/2026-11-23-dev-search-evidence-20261123-ko.md",
}
SITES={"koreaves.com","spoonie.kr","spaceatlasedu.org"}
class SearchDiscoveryTruthTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.data=json.loads(DATA.read_text("utf8"))

    def test_original_gsc_property_aggregation_and_exact_date(self):
        d=self.data
        self.assertEqual(d["property"],"https://saramjh.github.io/")
        self.assertEqual(d["search_type"],"web")
        self.assertEqual(d["data_state"],"final")
        self.assertEqual((d["start_date"],d["end_date"]),("2026-10-15","2026-11-20"))
        self.assertEqual(d["site_aggregation"]["aggregation_type"],"byProperty")
        self.assertEqual(d["site_aggregation"]["clicks"],300)
        self.assertEqual(d["site_aggregation"]["impressions"],3601)
        self.assertAlmostEqual(d["site_aggregation"]["ctr"],300/3601,places=12)
        self.assertTrue(d["no_synthetic_events"])
        self.assertIn("private",d["data_access"])
        self.assertEqual(d["page_breakdown"]["aggregation_type"],"byPage")
        self.assertEqual(
            [(r["url"],r["clicks"],r["impressions"]) for r in d["page_breakdown"]["rows"]],
            [("https://saramjh.github.io/scratchLottery/",120,1416),
             ("https://saramjh.github.io/epson-waste-ink-pad-reset-without-key/",88,485),
             ("https://saramjh.github.io/richChecker/",73,236)]
        )
        self.assertTrue(all(not any(s in r["url"] for s in SITES) for r in d["page_breakdown"]["rows"]))

    def test_original_portfolio_separates_search_metrics_from_independent_recognition(self):
        html=PORTFOLIO.read_text("utf8")
        self.assertIn('id="measured-search"',html)
        self.assertIn('aria-labelledby="measured-search-heading"',html)
        self.assertEqual(html.count('<strong>300</strong>'),1)
        self.assertIn("3,601 impressions",html)
        self.assertIn("8.33% search CTR",html)
        self.assertIn("property-level",html)
        self.assertIn("page counts use separate aggregation",html)
        for name,clicks in [("Scratch Lottery simulator",120),("Epson printer guide",88),("RichChecker experiment",73)]:
            self.assertIn(name,html)
            self.assertIn(f">{clicks} <small>clicks</small>",html)
        self.assertIn('/independent-tools-google-search-results-en/',html)
        self.assertIn('/independent-tools-google-search-results-ko/',html)
        self.assertEqual(html.count('id="external-records"'),1)
        self.assertNotIn("data-evidence-project",html)
        self.assertNotIn("gtag('event','search",html)

    def test_original_pair_locale_seo_source_limits_and_real_og_dimensions(self):
        pages={lang:p.read_text("utf8") for lang,p in ARTICLES.items()}
        self.assertTrue(all(s.startswith("---\n") for s in pages.values()))
        for lang,s in pages.items():
            expected="/independent-tools-google-search-results-"+lang+"/"
            other="/independent-tools-google-search-results-"+("ko" if lang=="en" else "en")+"/"
            self.assertIn(f"permalink: {expected}",s)
            self.assertIn(f"alternate_url: {other}",s)
            self.assertIn(f"lang: {lang}",s)
            self.assertIn("2026-11-23",s)
            self.assertIn("image_width: 1200\nimage_height: 681",s)
            self.assertIn("scratchlottery-2026-fast-simulation.png",s)
            self.assertTrue((ROOT/"_posts/scratch-lottery-simulation/scratchlottery-2026-fast-simulation.png").exists())
            for value in ["300","3,601","120","88","73","2026"]:
                self.assertIn(value,s)
            self.assertIn("/assets/data/dev-c127-gsc-search-performance-20261123.json",s)
            self.assertIn(other,s)
            self.assertNotIn("\\ufffd",s)
            self.assertNotIn("????",s)
        self.assertIn("Search Console",pages["en"])
        self.assertIn("구글 검색",pages["ko"])
        self.assertIn("byProperty",json.dumps(self.data))
        self.assertFalse((ROOT/"_data/recognitions.yml").read_text("utf8").find("300 web search clicks")!=-1)

    def test_schema_and_new_source_are_valid_json_and_unicode(self):
        run=subprocess.run(["python3","-m","json.tool",str(DATA)],capture_output=True,text=True,timeout=12)
        self.assertEqual(run.returncode,0,run.stderr)
        self.assertTrue(DATA.read_text("utf8").endswith("\n"))

if __name__=="__main__":unittest.main()

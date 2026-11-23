"""Original BOU source click event: only two author-owned blog articles."""
from pathlib import Path
import unittest
import subprocess

ROOT=Path(__file__).resolve().parents[1]
POSTS=[
 ROOT/"_posts/koreaves-bou-when-records-become-maps-ko/2026-11-23-koreaves-bou-when-records-become-maps-ko.md",
 ROOT/"_posts/koreaves-bou-when-records-become-maps-en/2026-11-23-koreaves-bou-when-records-become-maps-en.md"
]
TAG='<script src="/assets/js/bou-original-source-select.js" defer></script>'
JS=ROOT/"assets/js/bou-original-source-select.js"
ORIGINAL="https://bou.org.uk/blog-oh-when-records-become-maps/"
class BOUOriginalSelect(unittest.TestCase):
 def test_only_original_bilingual_posts_load_once(self):
  for lang,p in [('ko',POSTS[0]),('en',POSTS[1])]:
   s=p.read_text('utf8')
   self.assertEqual(s.count(TAG),1)
   self.assertEqual(s.count(ORIGINAL),2)
   self.assertIn("lang: "+lang,s)
   self.assertNotIn("\ufffd",s)
   self.assertNotIn("????",s)
 def test_shared_analytics_template_unchanged(self):
  footer=(ROOT/"_includes/footer.html").read_text('utf8')
  self.assertNotIn('bou-original-source-select',footer)
  self.assertIn("site.google_analytics and page.tracking != false",footer)
 def test_no_tracking_other_posts_or_expanded_scope(self):
  matches=[]
  for p in (ROOT/"_posts").rglob("*.md"):
   if TAG in p.read_text('utf8'):matches.append(p)
  self.assertEqual({x.resolve() for x in matches},{x.resolve() for x in POSTS})
  s=JS.read_text('utf8')
  self.assertIn("bou_original_source_select",s)
  self.assertIn("bou_when_records_become_maps",s)
  self.assertIn("article_lang: pageLang",s)
  self.assertIn("navigator.doNotTrack",s)
  self.assertIn("window.gtag",s)
  for bad in ["sendBeacon","fetch(","XMLHttpRequest","document.cookie","localStorage","sessionStorage","preventDefault("]:
   self.assertNotIn(bad,s)
 def test_original_exact_browser_runtime(self):
  subprocess.run(["node","tests/bou_original_source_select_runtime.cjs"],cwd=ROOT,check=True,stdout=subprocess.PIPE,stderr=subprocess.PIPE,timeout=10)
if __name__=="__main__":
 unittest.main()

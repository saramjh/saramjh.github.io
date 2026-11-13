"""Source-bound bilingual navigation for public achievement records."""
from pathlib import Path
import re
import unittest


ROOT = Path(__file__).resolve().parents[1]
LEDGER = ROOT / "_data" / "recognitions.yml"
INCLUDE = ROOT / "_includes" / "portfolio-evidence.html"
CSS = ROOT / "assets" / "css" / "portfolio.css"

EXPECTED = {
    "worldlytribe-space-atlas-worldschooling": "space-atlas-worldschooling-guide",
    "nav-ai-koreaves-directory": "koreaves-external-resources",
    "birdalbum-koreaves-further-reading": "koreaves-external-resources",
    "kantorilode-koreaves-legacy-links": "koreaves-external-resources",
    "kartoza-awesome-geodata-koreaves": "koreaves-external-resources",
    "birds-photo-10000": "koreaves-published-contributions",
    "suncheon-10000": "koreaves-published-contributions",
    "one-earth-koreaves-feature": "koreaves-oneearth-author-achievement",
    "unsustainable-koreaves-bird-map": "koreaves-unsustainable-bird-map",
    "webapps-spoonie-listing": "spoonie-webapps-directory",
    "eusci-space-atlas-diagrams": "space-atlas-eusci-diagrams",
    "ncase-space-atlas-programs": "space-atlas-ncase-programs",
    "sharemylesson-space-atlas-moon-phases": "space-atlas-share-my-lesson",
    "disquiet-spoonie-first-record": "spoonie-disquiet-first-record",
}


def parse_records():
    source = LEDGER.read_text(encoding="utf8")
    chunks = re.split(r"(?m)^- id: ", source)[1:]
    records = {}
    for chunk in chunks:
        lines = chunk.splitlines()
        record_id = lines[0].strip()
        record = {}
        for line in lines[1:]:
            match = re.fullmatch(r"  ([a-z_]+):\s*(.*)", line)
            if match:
                record[match.group(1)] = match.group(2).strip('"\'')

        if record_id in records:
            raise AssertionError("Duplicate public record: " + record_id)
        records[record_id] = record
    return records


class EvidenceContextLinksTest(unittest.TestCase):
    def test_canonical_records_only_and_original_source_retained(self):
        records = parse_records()
        self.assertEqual(len(records), 20)
        for record_id, slug in EXPECTED.items():
            item = records[record_id]
            self.assertEqual(item["status"], "confirmed")
            self.assertTrue(item["url"].startswith("https://"))
            self.assertEqual(item["case_ko"], f"/{slug}-ko/")
            self.assertEqual(item["case_en"], f"/{slug}-en/")
        greenus = records["greenus-koreaves-community-tool"]
        self.assertEqual(greenus["status"], "confirmed")
        self.assertEqual(greenus["type"], "listing")
        self.assertEqual(greenus["project"], "koreaves")
        self.assertEqual(greenus["url"], "https://greenus.upb.ro/resources.php?rp=2")
        self.assertIn("Community-submitted", greenus["detail"])
        self.assertIn("Jihun Oh", greenus["detail"])
        self.assertIn("does not establish editorial endorsement", greenus["detail"])
        self.assertNotIn("date", greenus)
        self.assertNotIn("case_ko", greenus)
        self.assertNotIn("case_en", greenus)
        self.assertEqual(
            records["eusci-space-atlas-diagrams"]["url"],
            "https://eusci.org.uk/2026/11/10/three-space-diagrams-three-missing-clues/",
        )
        self.assertEqual(records["eusci-space-atlas-diagrams"]["date"], "2026-11-10")
        self.assertEqual(records["eusci-space-atlas-diagrams"]["type"], "publication")
        self.assertIn("not university endorsement", records["eusci-space-atlas-diagrams"]["detail"])
        self.assertEqual(
            records["disquiet-spoonie-first-record"]["url"],
            "https://disquiet.io/articles/MVsxQv",
        )
        self.assertEqual(
            records["disquiet-spoonie-first-record"]["date"], "2026-10-13"
        )
        self.assertIn("Self-authored", records["disquiet-spoonie-first-record"]["detail"])
        self.assertEqual(records["disquiet-spoonie-first-record"]["project"], "spoonie")
        self.assertIn("Not independent press", records["disquiet-spoonie-first-record"]["detail"])
        self.assertTrue(
            all(("case_ko" in r) == ("case_en" in r) for r in records.values())
        )

    def test_launchfree_spoonie_listing_is_a_precise_directory_record(self):
        records = parse_records()
        listing = records["launchfree-spoonie-beta-listing"]
        self.assertEqual(listing["project"], "spoonie")
        self.assertEqual(listing["type"], "listing")
        self.assertEqual(listing["status"], "confirmed")
        self.assertEqual(listing["date"], "2026-10-12")
        self.assertEqual(listing["source"], "LaunchFree.io")
        self.assertEqual(listing["url"], "https://launchfree.io/listings/spoonie.html")
        self.assertIn("Community / Beta", listing["detail"])
        self.assertIn("does not establish independent endorsement or product adoption", listing["detail"])
        self.assertNotIn("case_ko", listing)
        self.assertNotIn("case_en", listing)
        self.assertEqual(
            sum(record["url"] == listing["url"] for record in records.values()),
            1,
        )

    def test_birdalbum_and_kantorilode_links_keep_exact_public_provenance(self):
        records = parse_records()
        checks = {
            "birdalbum-koreaves-further-reading": (
                "https://birdalbum.com/countries/kr/", "Bird Album"
            ),
            "kantorilode-koreaves-legacy-links": (
                "https://kantorilode.weebly.com/links.html", "Kantorilode"
            ),
        }
        for record_id, (url, owner) in checks.items():
            item = records[record_id]
            self.assertEqual(item["project"], "koreaves")
            self.assertEqual(item["type"], "listing")
            self.assertEqual(item["status"], "confirmed")
            self.assertEqual(item["source"], owner)
            self.assertEqual(item["url"], url)
            self.assertNotIn("date", item)
            self.assertEqual(item["case_en"], "/koreaves-external-resources-en/")
            self.assertEqual(item["case_ko"], "/koreaves-external-resources-ko/")
            self.assertEqual(sum(r["url"] == url for r in records.values()), 1)
            for language in ("en", "ko"):
                post = (ROOT / f"_posts/folio-koreaves-resources-{language}" /
                        f"2026-11-02-folio-koreaves-resources-{language}.md").read_text("utf8")
                self.assertIn(record_id, post)
                self.assertIn(url, post)
                self.assertNotIn("\ufffd", post)
                self.assertNotIn("????", post)
                self.assertIn("modified: 2026-11-13", post)
        self.assertIn("legacy", records["kantorilode-koreaves-legacy-links"]["detail"].lower())
        en = (ROOT / "_posts/folio-koreaves-resources-en" /
              "2026-11-02-folio-koreaves-resources-en.md").read_text("utf8")
        ko = (ROOT / "_posts/folio-koreaves-resources-ko" /
              "2026-11-02-folio-koreaves-resources-ko.md").read_text("utf8")
        self.assertIn("four", en.lower())
        self.assertIn("네", ko)
        self.assertIn("https://kantorilode.com/links.html", en)
        self.assertIn("https://kantorilode.com/links.html", ko)
        self.assertNotIn("15 language editions verified", en.lower())

    def test_awesome_geodata_koreaves_entry_is_a_directory_link(self):
        records = parse_records()
        entry = records["kartoza-awesome-geodata-koreaves"]
        self.assertEqual(entry["project"], "koreaves")
        self.assertEqual(entry["type"], "listing")
        self.assertEqual(entry["status"], "confirmed")
        self.assertEqual(entry["source"], "Kartoza Awesome Geodata")
        self.assertEqual(entry["url"], "https://github.com/kartoza/awesome-geodata/blob/main/README.md#kr")
        self.assertIn("South Korea section", entry["detail"])
        self.assertIn("does not establish endorsement or measured use", entry["detail"])
        self.assertNotIn("date", entry)
        self.assertEqual(entry["case_ko"], "/koreaves-external-resources-ko/")
        self.assertEqual(entry["case_en"], "/koreaves-external-resources-en/")
        self.assertEqual(
            sum(r["url"] == entry["url"] for r in records.values()), 1
        )

    def test_worldlytribe_verified_science_directory_not_classroom_adoption(self):
        records = parse_records()
        item = records["worldlytribe-space-atlas-worldschooling"]
        self.assertEqual(item["project"], "space-atlas")
        self.assertEqual(item["type"], "listing")
        self.assertEqual(item["status"], "confirmed")
        self.assertEqual(item["source"], "WorldlyTribe")
        self.assertEqual(item["url"], "https://worldlytribe.com/the-complete-guide-to-online-programs-for-homeschoolers-worldschoolers/")
        self.assertNotIn("date", item)
        self.assertNotIn("endorsement", item["detail"])
        for lang in ("en", "ko"):
            self.assertEqual(item[f"case_{lang}"], f"/space-atlas-worldschooling-guide-{lang}/")
            src = ROOT / "_posts" / f"space-atlas-worldschooling-guide-{lang}" / f"2026-11-13-space-atlas-worldschooling-guide-{lang}.md"
            body = src.read_text("utf8")
            self.assertIn(item["url"], body)
            self.assertIn("https://spaceatlasedu.org/moon/phases/", body)
            self.assertIn("https://spaceatlasedu.org/earth/seasons/", body)
            self.assertNotIn("\ufffd", body)
            self.assertNotIn("????", body)
            self.assertIn(f"/space-atlas-worldschooling-guide-{'ko' if lang=='en' else 'en'}/", body)
        self.assertEqual(sum(r["url"] == item["url"] for r in records.values()), 1)

    def test_nav_ai_source_bound_listing_and_bilingual_context(self):
        records = parse_records()
        item = records["nav-ai-koreaves-directory"]
        self.assertEqual(item["project"], "koreaves")
        self.assertEqual(item["type"], "listing")
        self.assertEqual(item["status"], "confirmed")
        self.assertEqual(item["source"], "Nav-AI")
        self.assertEqual(item["url"], "https://nav-ai.net/ai/koreaves")
        self.assertNotIn("date", item)
        self.assertIn("no independent testing or measured adoption", item["detail"])
        for lang in ("en", "ko"):
            self.assertEqual(item[f"case_{lang}"], f"/koreaves-external-resources-{lang}/")
            body = (ROOT / "_posts" / f"folio-koreaves-resources-{lang}" /
                    f"2026-11-02-folio-koreaves-resources-{lang}.md").read_text(encoding="utf8")
            self.assertIn(item["url"], body)
            self.assertIn("nav-ai-koreaves-directory", body)
            self.assertNotIn("�", body)
            self.assertNotIn("????", body)
        self.assertEqual(sum(item["url"] == entry["url"] for entry in records.values()), 1)

    def test_kartoza_article_context_is_bilingual_and_distinct_from_publication(self):
        entry = parse_records()["kartoza-awesome-geodata-koreaves"]
        self.assertEqual(entry["type"], "listing")
        self.assertNotIn("date", entry)
        for lang in ("ko", "en"):
            article = (ROOT / f"_posts/folio-koreaves-resources-{lang}"
                       / f"2026-11-02-folio-koreaves-resources-{lang}.md").read_text(encoding="utf8")
            self.assertIn("kartoza-awesome-geodata-koreaves", article)
            self.assertIn(entry["url"], article)
            self.assertIn("modified: 2026-11-13", article)
            self.assertNotIn("\ufffd", article)
            self.assertNotIn("????", article)
            self.assertIn("koreaves.com", article)
        self.assertGreaterEqual(sum("가" <= c <= "힣" for c in (
            ROOT / "_posts/folio-koreaves-resources-ko/2026-11-02-folio-koreaves-resources-ko.md"
        ).read_text(encoding="utf8")), 300)

    def test_each_target_has_a_real_published_bilingual_jekyll_page(self):
        records = parse_records()
        for record_id, slug in EXPECTED.items():
            for lang, opposite in (("ko", "en"), ("en", "ko")):
                target = records[record_id][f"case_{lang}"]
                source_files = [p for p in (ROOT / "_posts").rglob("*.md") if "permalink: " + target in p.read_text(encoding="utf8")]
                self.assertEqual(len(source_files), 1, (record_id, target, source_files))
                post = source_files[0].read_text(encoding="utf8")
                self.assertIn("permalink: " + target, post)
                self.assertIn("lang: " + lang, post)
                self.assertIn("published: true", post)
                if "alternate_url:" in post:
                    self.assertIn("alternate_url: " + records[record_id][f"case_{opposite}"], post)

    def test_ncase_listing_and_share_my_lesson_are_distinct_proof_kinds(self):
        records = parse_records()
        ncase = records["ncase-space-atlas-programs"]
        lesson = records["sharemylesson-space-atlas-moon-phases"]
        self.assertEqual(ncase["type"], "listing")
        self.assertEqual(lesson["type"], "publication")
        self.assertEqual(ncase["project"], lesson["project"])
        self.assertEqual(ncase["project"], "space-atlas")
        self.assertEqual(ncase["source"], "NCASE Programs")
        self.assertEqual(lesson["source"], "Share My Lesson")
        self.assertEqual(ncase["url"], "https://ncase.org/programs/")
        self.assertTrue(lesson["url"].startswith("https://sharemylesson.com/teaching-resource/moon-phases"))
        self.assertNotIn("date", ncase)
        self.assertNotIn("date", lesson)
        self.assertIn("not accreditation", ncase["detail"])
        self.assertIn("Creator-contributed", lesson["detail"])
        for lang in ("ko", "en"):
            self.assertEqual(ncase[f"case_{lang}"], f"/space-atlas-ncase-programs-{lang}/")
            self.assertEqual(lesson[f"case_{lang}"], f"/space-atlas-share-my-lesson-{lang}/")

        for lang in ("ko", "en"):
            path = ROOT / "_posts" / f"space-atlas-education-resource-paths-{lang}" / f"2026-11-11-space-atlas-education-resource-paths-{lang}.md"
            body = path.read_text(encoding="utf8")
            self.assertIn("published: true", body)
            self.assertIn("https://ncase.org/programs/", body)
            self.assertIn(lesson["url"], body)
            self.assertIn("Jihun Oh", body)
            self.assertIn("CC BY-NC-ND", body)
            self.assertIn("Google AdSense", body)
            self.assertIn("GA4", body)
            self.assertIn("/space-atlas-student/space-atlas-hero.png", body)
            self.assertNotIn("sharemylesson.com/sites/default/files", body)
            self.assertNotIn("ncase.org/wp-content/uploads", body)
            self.assertNotIn("???", body)
            self.assertNotIn("\\ufffd", body)
            if lang == "ko":
                self.assertIn("처음 등재된 날짜는 알 수 없다", body)
                self.assertIn("교육기관 인증이나 실제 수업 효과의 증거는 아니다", body)
            else:
                self.assertIn("original listing date is not established", body)
                self.assertIn("Neither record establishes classroom uptake", body)

    def test_10000birds_approved_public_response_is_context_not_audience(self):
        link = ("https://www.10000birds.com/"
                "the-bird-photo-i-could-use-was-not-the-bird-photo-i-wanted.htm"
                "#comment-7017451")
        posts = {
            "ko": ROOT / "_posts/folio-koreaves-publications-ko/2026-11-02-folio-koreaves-publications-ko.md",
            "en": ROOT / "_posts/folio-koreaves-publications-en/2026-11-02-folio-koreaves-publications-en.md",
        }
        for lang, file in posts.items():
            text = file.read_text(encoding="utf8")
            self.assertEqual(text.count(link), 1)
            self.assertIn("David Tomlinson", text)
            if lang == "ko":
                self.assertIn("10월 9일", text)
                self.assertIn("11월 11일", text)
                self.assertIn("조회수나 KoreAves 사용을 측정한 결과는 아니다", text)
            else:
                self.assertIn("October 9", text)
                self.assertIn("November 11", text)
                self.assertIn("nothing reliable about total readership or KoreAves adoption", text)
        # A comment is not an additional externally published author contribution.
        records = parse_records()
        self.assertEqual(len(records), 20)
        self.assertEqual(records["birds-photo-10000"]["type"], "publication")

    def test_eusci_byline_has_one_attributed_source_and_uses_owned_visual(self):
        original = "https://eusci.org.uk/2026/11/10/three-space-diagrams-three-missing-clues/"
        owned_image = "/space-atlas-student/space-atlas-hero.png"
        self.assertTrue((ROOT / "_posts/space-atlas-student/space-atlas-hero.png").is_file())
        for language in ("ko", "en"):
            p = ROOT / f"_posts/space-atlas-eusci-diagrams-{language}" / f"2026-11-11-space-atlas-eusci-diagrams-{language}.md"
            post = p.read_text(encoding="utf-8")
            self.assertIn(original, post)
            self.assertIn(f"image: {owned_image}", post)
            self.assertIn(f'<img src="{owned_image}"', post)
            self.assertNotIn("i0.wp.com", post)
            self.assertNotIn("commons.wikimedia.org/wiki/File:Solar", post)
            self.assertIn("Jihun Oh", post)
            self.assertIn("Priscilla Wong", post)
            self.assertIn("published: true", post)

    def test_unsustainable_publisher_editor_credit_without_peer_review_claim(self):
        original = "https://www.unsustainablemagazine.com/why-a-bird-map-is-not-a-bird-count/"
        for language in ("ko", "en"):
            page = ROOT / f"_posts/koreaves-unsustainable-bird-map-{language}" / f"2026-11-10-koreaves-unsustainable-bird-map-{language}.md"
            source = page.read_text(encoding="utf8")
            self.assertIn(original, source)
            self.assertIn("Jihun Oh", source)
            self.assertEqual(source.count("Brett Stadelmann"), 1)
            self.assertIn("Edited and reviewed by Brett Stadelmann", source)
            self.assertIn("/assets/images/portfolio/koreaves-gis.jpg", source)
            self.assertNotIn("wp-content/uploads", source)
            if language == "ko":
                self.assertIn("학술 동료심사를 받은 연구라는 뜻은 아니다", source)
            else:
                self.assertIn("not evidence of scientific peer review", source)
        records = parse_records()
        self.assertEqual(len(records), 20)
        self.assertEqual(records["unsustainable-koreaves-bird-map"]["date"], "2026-11-06")
        self.assertEqual(records["unsustainable-koreaves-bird-map"]["type"], "publication")

    def test_eusci_original_published_figure_credit_is_evidence_bounded(self):
        # The original article credits its Figure 1 drawing to Jihun Oh.
        # We cite the credit only; article images are not imported.
        for language in ("ko", "en"):
            p = ROOT / f"_posts/space-atlas-eusci-diagrams-{language}" / f"2026-11-11-space-atlas-eusci-diagrams-{language}.md"
            post = p.read_text(encoding="utf8")
            self.assertEqual(post.count("Original illustration by Jihun Oh"), 1)
            self.assertIn("Priscilla Wong", post)
            self.assertIn("https://eusci.org.uk/2026/11/10/three-space-diagrams-three-missing-clues/", post)
            self.assertNotIn("i0.wp.com", post)
            self.assertNotIn("wp-content/uploads", post)
            self.assertIn("/assets/images/dev/eusci-20261111/card-02.jpg", post)
            if language == "ko":
                self.assertIn("원문 Figure 1의 천문학 설명 도해", post)
            else:
                self.assertIn("Figure 1 caption reads", post)
        # This is one article, not a new external publication or directory record.
        records = parse_records()
        self.assertEqual(len(records), 20)

    def test_homepage_shows_published_work_before_full_evidence_archive(self):
        records = parse_records()
        published = [r for r in records.values() if r["status"] == "confirmed" and r["type"] == "publication"]
        self.assertEqual(len(published), 7)
        self.assertEqual(len(records), 20)
        self.assertEqual(len([r for r in records.values() if r["type"] == "listing"]), 12)
        self.assertEqual(len([r for r in records.values() if r["type"] == "dataset_record"]), 1)
        homepage = (ROOT / "portfolio/index.html").read_text(encoding="utf8")
        archive = (ROOT / "portfolio/recognition/index.html").read_text(encoding="utf8")
        include = INCLUDE.read_text(encoding="utf8")
        self.assertEqual(homepage.count('{% include portfolio-evidence.html type="publication" %}'), 1)
        self.assertEqual(archive.count('{% include portfolio-evidence.html type="publication" %}'), 1)
        self.assertIn('include.type and record.type != include.type', include)
        self.assertIn('Resource listings and catalogue entries are in the full archive.', homepage)
        self.assertIn('/portfolio/recognition/', homepage)
        self.assertNotIn('{% include portfolio-evidence.html %}', archive)
        for record_id in ("eusci-space-atlas-diagrams", "one-earth-koreaves-feature",
                          "unsustainable-koreaves-bird-map", "suncheon-10000",
                          "sharemylesson-space-atlas-moon-phases"):
            self.assertEqual(records[record_id]["type"], "publication")

    def test_shared_evidence_component_preserves_external_and_internal_destinations(self):
        include = INCLUDE.read_text(encoding="utf8")
        css = CSS.read_text(encoding="utf8")
        self.assertEqual(include.count('href="{{ record.url | escape }}"'), 1)
        self.assertIn("{% if record.case_ko or record.case_en %}", include)
        self.assertIn('data-case-lang="ko"', include)
        self.assertIn('data-case-lang="en"', include)
        self.assertIn('href="{{ record.case_ko | relative_url | escape }}"', include)
        self.assertIn('href="{{ record.case_en | relative_url | escape }}"', include)
        tracker = (ROOT / "assets" / "js" / "portfolio.js").read_text(encoding="utf8")
        self.assertIn("portfolio_evidence_case", tracker)
        self.assertIn("id+':'+lang", tracker)
        self.assertIn("navigator.msDoNotTrack==='1'", tracker)
        privacy = (ROOT / "privacy.md").read_text(encoding="utf8")
        self.assertIn("Korean or English developer note", privacy)
        self.assertIn("Developer notes:", include)
        self.assertIn("한국어", include)
        self.assertIn("English", include)
        self.assertIn(".folio-evidence-context a:focus-visible", css)
        for page in ("portfolio/index.html", "portfolio/recognition/index.html"):
            self.assertIn("portfolio-evidence.html", (ROOT / page).read_text(encoding="utf8"))


if __name__ == "__main__":
    unittest.main()

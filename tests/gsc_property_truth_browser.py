"""Render six original bilingual Search Console corrections in real Chrome."""
import os
import sys
from playwright.sync_api import sync_playwright

BASE = sys.argv[1].rstrip("/") if len(sys.argv) > 1 else "http://127.0.0.1:4317"
DOC_PROPERTY = "https://support.google.com/webmasters/answer/34592?hl=en"
DOC_VERIFY = "https://support.google.com/webmasters/answer/9008080?hl=en"
PREFIX = "https://saramjh.github.io/"
WIDTHS = (240, 280, 390, 768)
PAGES = [
    (part, lang, f"/gh-pages-analytics-notes-{part}-{('reasoning' if part == '2' else 'decision' if part == '3' else 'open')}-{'kr' if lang == 'ko' else 'en'}/")
    for part in ("2", "3", "4") for lang in ("ko", "en")
]

with sync_playwright() as pw:
    channel = os.environ.get("BLOG_TEST_BROWSER_CHANNEL") or None
    browser = pw.chromium.launch(headless=True, channel=channel)
    for part, lang, path in PAGES:
        for width in WIDTHS:
            page = browser.new_page(viewport={"width": width, "height": 900})
            errors = []
            page.on("pageerror", lambda e: errors.append(str(e)))
            page.route("**/*", lambda route: route.continue_()
                       if route.request.url.startswith(BASE + "/") else route.abort())
            response = page.goto(BASE + path, wait_until="domcontentloaded", timeout=20000)
            assert response is not None and response.status == 200, (part, lang, width, "HTTP")
            assert page.locator("html").get_attribute("lang") == lang, (part, lang, "lang")
            assert page.locator("main h1").count() == 1, (part, lang, "heading")
            assert page.locator("link[rel=canonical]").get_attribute("href").endswith(path), (
                part, lang, "canonical")
            main = page.locator("main")
            text = main.inner_text()
            assert PREFIX in text, (part, lang, "root URL-prefix absent")
            assert "DNS" in text, (part, lang, "DNS prerequisite absent")
            links = main.locator(f'a[href="{DOC_PROPERTY}"]')
            assert links.count() >= 1, (part, lang, "official property source")
            if part in ("2", "3"):
                assert "2026-11-20" in text, (part, lang, "correction date")
                assert main.locator(f'a[href="{DOC_VERIFY}"]').count() >= 1, (
                    part, lang, "verification source")
                assert "URL-prefix" in text, (part, lang, "property type")
            if part == "3":
                assert ("remains unverified" in text if lang == "en"
                        else "확실하지 않습니다" in text), (part, lang, "unknown provenance")
            style = page.evaluate("""() => {
              const source=document.querySelector('main');
              const firstSource=source.querySelector('a[href*="support.google.com/webmasters/answer/34592"]');
              const r=firstSource?.getBoundingClientRect();
              return {docWidth:document.documentElement.scrollWidth,
                      sourceLinkRight:r?.right,sourceLinkLeft:r?.left};
            }""")
            assert style["docWidth"] <= width + 2, (part, lang, width, "page overflow", style)
            assert not errors, (part, lang, width, "page JS errors", errors)
            print("PASS original GSC correction", part, lang, width)
            page.close()
    browser.close()
print("PASS 24 bilingual Search Console property correction Chrome cases")

"""Check original bilingual IndexNow evidence tables on a compiled Jekyll site."""
import os
import sys
from playwright.sync_api import sync_playwright

BASE = sys.argv[1].rstrip("/") if len(sys.argv) > 1 else "http://127.0.0.1:4317"
PAGES = {"ko": "/indexnow-image-page-scope-ko/", "en": "/indexnow-image-page-scope-en/"}
LABEL = {"ko": ("IndexNow 최초 전송", "IndexNow JavaScript"), "en": ("IndexNow original submission", "IndexNow JavaScript")}
RECEIPTS = (
    "42760722178",
    "42761734284",
    "44317892057",
    "44321890015",
)

with sync_playwright() as playwright:
    channel = os.environ.get("BLOG_TEST_BROWSER_CHANNEL") or None
    browser = playwright.chromium.launch(headless=True, channel=channel)
    for lang, path in PAGES.items():
        for viewport in (240, 280, 320, 390, 768):
            page = browser.new_page(viewport={"width": viewport, "height": 900})
            errors = []
            page.on("pageerror", lambda error: errors.append(str(error)))
            page.route("**/*", lambda route: route.continue_()
                       if route.request.url.startswith(BASE + "/") else route.abort())
            response = page.goto(BASE + path, wait_until="domcontentloaded", timeout=20000)
            assert response is not None and response.status == 200, (lang, viewport, "article")
            assert page.locator("html").get_attribute("lang") == lang, (lang, viewport, "lang")
            regions = page.locator('main .overflow-table[role="region"][tabindex="0"]')
            assert regions.count() == 2, (lang, viewport, "missing scroll containers")
            assert page.locator("main h1").count() == 1, (lang, viewport, "heading")
            for i in range(2):
                region = regions.nth(i)
                name = region.get_attribute("aria-label")
                assert name and name.startswith(LABEL[lang][i]), (lang, viewport, i, name)
                table = region.locator("table")
                assert table.count() == 1, (lang, viewport, i, "table not rendered")
                assert table.locator("thead th").count() == 3, (lang, viewport, i, "table columns")
                assert table.locator("tbody tr").count() == 3, (lang, viewport, i, "table rows")
                geom = region.evaluate("""el => {
                  const b=el.getBoundingClientRect(),tbl=el.querySelector('table');
                  const last=tbl.querySelector('tbody tr:last-child td:last-child');
                  el.scrollLeft=el.scrollWidth;
                  const end=last.getBoundingClientRect();
                  return {left:b.left,right:b.right,scrollWidth:el.scrollWidth,
                          clientWidth:el.clientWidth,scrollLeft:el.scrollLeft,
                          overflow:getComputedStyle(el).overflowX,lastRight:end.right,
                          docWidth:document.documentElement.scrollWidth};
                }""")
                assert geom["overflow"] == "auto", (lang, viewport, i, geom)
                assert geom["left"] >= -1 and geom["right"] <= viewport + 1, (
                    lang, viewport, i, "container out of viewport", geom)
                assert geom["docWidth"] <= viewport + 2, (
                    lang, viewport, i, "page overflow", geom)
                assert geom["lastRight"] <= geom["right"] + 1, (
                    lang, viewport, i, "last evidence column unreachable", geom)
                if lang == "en" and viewport <= 280:
                    assert geom["scrollWidth"] > geom["clientWidth"] and geom["scrollLeft"] > 0, (
                        lang, viewport, i, "english table needs working scroll", geom)
                region.focus()
                assert region.evaluate("el => document.activeElement === el"), (
                    lang, viewport, i, "keyboard focus")
            for receipt in RECEIPTS:
                assert page.locator(f'main a[href*="/actions/runs/{receipt}"]').count() == 1, (
                    lang, viewport, receipt, "original native receipt changed")
            assert not errors, (lang, viewport, "JS errors", errors)
            print("PASS original IndexNow evidence table and native receipts", lang, viewport)
            page.close()
    browser.close()

print("PASS bilingual IndexNow scroll-region browser QA")

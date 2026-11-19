"""Check first-party long inline paths remain readable without changing code blocks."""
import os
import sys
from playwright.sync_api import sync_playwright

BASE = sys.argv[1].rstrip("/") if len(sys.argv) > 1 else "http://127.0.0.1:4317"
PAGES = {
    "/gh-pages-analytics-notes-2-reasoning-en/": ("en", "https://saramjh.github.io/scratchLottery/"),
    "/gh-pages-analytics-notes-2-reasoning-kr/": ("ko", "https://saramjh.github.io/scratchLottery/"),
    "/homepage-project-directory-en/": ("en", "scripts/check_growth_ownership.py"),
    "/homepage-project-directory-ko/": ("ko", "scripts/check_growth_ownership.py"),
}
WIDTHS = (240, 280, 320, 390, 768)

with sync_playwright() as playwright:
    channel = os.environ.get("BLOG_TEST_BROWSER_CHANNEL") or None
    browser = playwright.chromium.launch(headless=True, channel=channel)
    for path, (lang, original_code_text) in PAGES.items():
        for width in WIDTHS:
            page = browser.new_page(viewport={"width": width, "height": 844})
            errors = []
            page.on("pageerror", lambda error: errors.append(str(error)))
            page.route("**/*", lambda route: route.continue_()
                       if route.request.url.startswith(BASE + "/") else route.abort())
            response = page.goto(BASE + path, wait_until="domcontentloaded", timeout=20000)
            assert response is not None and response.status == 200, (path, width, "HTTP")
            assert page.locator("html").get_attribute("lang") == lang, (path, width, "lang")
            assert page.locator("main h1").count() == 1, (path, width, "h1")
            assert page.locator("link[rel=canonical]").get_attribute("href").endswith(path), (
                path, width, "canonical")
            code = page.locator("main :not(pre) > code").filter(
                has_text=original_code_text).first
            assert code.count() == 1, (path, width, "original inline code absent")
            assert code.inner_text().strip() == original_code_text, (
                path, width, "original first-party source text changed")
            dimensions = code.evaluate("""el => {
              const r=el.getBoundingClientRect(),style=getComputedStyle(el);
              return {left:r.left,right:r.right,overflowWrap:style.overflowWrap,
                      docWidth:document.documentElement.scrollWidth,
                      text:el.textContent.trim()};
            }""")
            assert dimensions["overflowWrap"] == "anywhere", (
                path, width, "inline code wrap not in compiled CSS", dimensions)
            assert dimensions["left"] >= -1 and dimensions["right"] <= width + 1, (
                path, width, "inline code clipped", dimensions)
            assert dimensions["docWidth"] <= width + 2, (
                path, width, "page-wide horizontal overflow", dimensions)
            assert not errors, (path, width, "JavaScript errors", errors)
            print("PASS source-bound inline code", lang, width, path)
            page.close()

    # The new rule must not replace the existing fenced-block scrolling contract.
    page = browser.new_page(viewport={"width": 240, "height": 844})
    page.route("**/*", lambda route: route.continue_()
               if route.request.url.startswith(BASE + "/") else route.abort())
    response = page.goto(BASE + "/indexnow-image-page-scope-en/",
                         wait_until="domcontentloaded", timeout=20000)
    assert response is not None and response.status == 200
    code_blocks = page.locator("main pre")
    assert code_blocks.count() >= 1, "reference fenced code block missing"
    sample = code_blocks.first.evaluate("""el => ({
      overflowX:getComputedStyle(el).overflowX,
      codeWhitespace:getComputedStyle(el.querySelector('code')).whiteSpace
    })""")
    assert sample["overflowX"] == "auto" and sample["codeWhitespace"] == "pre", (
        "fenced code block style regressed", sample)
    page.close()
    browser.close()

print("PASS 20 bilingual original long-inline-code viewports and fenced-block preservation")

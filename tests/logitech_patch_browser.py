"""Real compiled Jekyll Chrome QA for original bilingual Logitech patch guidance."""
import os
import sys
from playwright.sync_api import sync_playwright

BASE = sys.argv[1].rstrip("/") if len(sys.argv) > 1 else "http://127.0.0.1:4317"
INSTALLER = "https://download01.logi.com/web/ftp/pub/techsupport/optionsplus/logioptionsplus_installer.zip"
OFFICIAL = "https://www.logitech.com/blog/2026/01/07/restoring-access-to-options-and-g-hub-on-macos/"
PAGES = {
    "en": "/en-logi-option-infinite-loading-solution/",
    "ko": "/kr-logi-option-infinite-loading-solution/",
}

with sync_playwright() as playwright:
    channel = os.environ.get("BLOG_TEST_BROWSER_CHANNEL") or None
    browser = playwright.chromium.launch(headless=True, channel=channel)
    for lang, path in PAGES.items():
        for viewport in (240, 280, 320, 390, 768):
            page = browser.new_page(viewport={"width": viewport, "height": 900})
            errors = []
            page.on("pageerror", lambda error: errors.append(str(error)))
            page.route("**/*", lambda route: route.continue_()
                       if route.request.url.startswith(BASE + "/")
                       else route.abort())
            response = page.goto(BASE + path, wait_until="domcontentloaded", timeout=20000)
            assert response and response.status == 200, (lang, viewport, "article response")
            assert page.locator("html").get_attribute("lang") == lang, (lang, viewport, "language")
            assert page.locator("main h1").count() == 1, (lang, viewport, "article heading")
            download = page.locator(f'main a[href="{INSTALLER}"]')
            official = page.locator(f'main a[href="{OFFICIAL}"]')
            assert download.count() == 1 and official.count() == 1, (
                lang, viewport, "official installer and source links")
            assert download.is_visible() and official.is_visible(), (lang, viewport, "links hidden")
            assert "logioptionsplus_installer.zip" not in download.inner_text(), (
                lang, viewport, "long raw address displayed")
            assert (
                "Do not uninstall" in page.locator("main").inner_text()
                if lang == "en"
                else "삭제하지 마세요" in page.locator("main").inner_text()
            ), (lang, viewport, "loss-prevention warning")
            rect = download.bounding_box()
            assert rect and rect["x"] >= -1 and rect["x"] + rect["width"] <= viewport + 1, (
                lang, viewport, "long URL link clips outside viewport", rect)
            assert page.evaluate("document.documentElement.scrollWidth") <= viewport + 2, (
                lang, viewport, "horizontal page overflow")
            download.focus()
            assert download.evaluate("node => document.activeElement === node"), (
                lang, viewport, "download link keyboard focus")
            assert not errors, (lang, viewport, "JavaScript errors", errors)
            print("PASS Logitech official patch source, warning and visible download", lang, viewport)
            page.close()
    browser.close()

print("PASS bilingual Logitech compiled article browser checks")

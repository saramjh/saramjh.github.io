"""Verify only original developer mailto link selections in Jekyll-rendered pages.

Browser dispatches synthetic, navigation-blocked clicks and forbids external requests.
No email client, Google Analytics request, or provider submission is performed.
"""
import os
import sys
from playwright.sync_api import sync_playwright

BASE = sys.argv[1].rstrip("/") if len(sys.argv) > 1 else "http://127.0.0.1:4317"
SURFACES = {
    "/portfolio/": (".folio-hero .folio-contact-cta", "portfolio_home"),
    "/portfolio/space-atlas/": (".folio-next .folio-contact-cta", "project_case"),
}

with sync_playwright() as playwright:
    channel = os.environ.get("BLOG_TEST_BROWSER_CHANNEL") or None
    browser = playwright.chromium.launch(headless=True, channel=channel)
    for path, (selector, surface) in SURFACES.items():
        for viewport in (390, 1440):
            page = browser.new_page(viewport={"width": viewport, "height": 900})
            page.route(
                "**/*",
                lambda route: route.continue_()
                if route.request.url.startswith(BASE + "/") else route.abort()
            )
            page.add_init_script(
                "Object.defineProperty(navigator, 'doNotTrack', {value:'0', configurable:true});"
            )
            errors = []
            page.on("pageerror", lambda exc: errors.append(str(exc)))
            response = page.goto(BASE + path, wait_until="load", timeout=20000)
            assert response and response.status == 200, (path, viewport)
            assert page.locator("script[src='/assets/js/portfolio.js']").count() == 1
            assert page.locator(selector).count() == 1, (path, viewport, "original CTA")
            data = page.evaluate("""selector => {
              const link = document.querySelector(selector);
              const original = link.getAttribute('href');
              const originalGtag = window.gtag;
              const originalDnt = window.doNotTrack;
              const values = [];
              window.gtag = (...args) => values.push(args);
              window.doNotTrack = '0';
              link.addEventListener('click', event => event.preventDefault());
              link.dispatchEvent(new MouseEvent('click',{bubbles:true,cancelable:true}));
              const allowed = values.length;
              window.doNotTrack = '1';
              link.dispatchEvent(new MouseEvent('click',{bubbles:true,cancelable:true}));
              const suppressed = values.length;
              window.gtag = undefined;
              window.doNotTrack = '0';
              link.dispatchEvent(new MouseEvent('click',{bubbles:true,cancelable:true}));
              const withoutGtag = values.length;
              window.gtag = originalGtag;
              window.doNotTrack = originalDnt;
              return {original, allowed, suppressed, withoutGtag, values,
                remainingPath: location.pathname};
            }""", selector)
            assert data["original"] == "mailto:devtestudinidae@gmail.com", (path,viewport,data)
            assert data["values"] == [
                ["event", "developer_contact_link_select", {"contact_surface":surface}]
            ], (path,viewport,data)
            assert (data["allowed"],data["suppressed"],data["withoutGtag"]) == (1,1,1), data
            assert data["remainingPath"] == path, (path,viewport,data)
            assert not errors, (path,viewport,errors)
            page.close()
    browser.close()
print("portfolio-contact-selection-browser: PASS actual KO/EN-neutral owner CTA DOM, mobile/desktop, DNT, no network or mail send")

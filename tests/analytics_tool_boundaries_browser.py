"""Verify bilingual analytics guidance on real Chrome at narrow mobile widths."""
import os
from playwright.sync_api import sync_playwright

BASE = os.environ.get("BLOG_TEST_BASE", "http://127.0.0.1:4317").rstrip("/")
GA4 = "https://support.google.com/analytics/answer/9679158?hl=en"
GA4_CROSS = "https://support.google.com/analytics/answer/10071811?hl=en"
GSC = "https://support.google.com/webmasters/answer/34592?hl=en"
VERIFY = "https://support.google.com/webmasters/answer/9008080?hl=en"
CLARITY = "https://learn.microsoft.com/en-us/clarity/faq/"
CLARITY_SETUP = "https://learn.microsoft.com/en-us/clarity/setup-and-installation/clarity-setup"
SUBDOMAIN_FAQ = "https://developers.google.com/search/help/crawling-index-faq?hl=en"
CRAWL_BUDGET = "https://developers.google.com/crawling/docs/crawl-budget?hl=en"
CRAWL_MYTHS = "https://developers.google.com/crawling/docs/myths-about-crawling"
LINKS = "https://developers.google.com/search/docs/crawling-indexing/links-crawlable"
RANKING = "https://developers.google.com/search/docs/appearance/ranking-systems-guide"
DOMAIN_AGE = "https://www.youtube.com/watch?v=-pnpg00FWJY"
PAGES = [
    ("1", "en", "/gh-pages-analytics-notes-1-problem-en/"),
    ("1", "ko", "/gh-pages-analytics-notes-1-problem-kr/"),
    ("2", "en", "/gh-pages-analytics-notes-2-reasoning-en/"),
    ("2", "ko", "/gh-pages-analytics-notes-2-reasoning-kr/"),
    ("3", "en", "/gh-pages-analytics-notes-3-decision-en/"),
    ("3", "ko", "/gh-pages-analytics-notes-3-decision-kr/"),
    ("4", "en", "/gh-pages-analytics-notes-4-open-en/"),
    ("4", "ko", "/gh-pages-analytics-notes-4-open-kr/"),
]
NEXT = {
    ("1", "en"): "/gh-pages-analytics-notes-2-reasoning-en/",
    ("1", "ko"): "/gh-pages-analytics-notes-2-reasoning-kr/",
    ("2", "en"): "/gh-pages-analytics-notes-3-decision-en/",
    ("2", "ko"): "/gh-pages-analytics-notes-3-decision-kr/",
    ("3", "en"): "/gh-pages-analytics-notes-4-open-en/",
    ("3", "ko"): "/gh-pages-analytics-notes-4-open-kr/",
    ("4", "en"): "/gh-pages-analytics-notes-5-followup-en/",
    ("4", "ko"): "/gh-pages-analytics-notes-5-followup-kr/",
}
WIDTHS = (240, 280, 390, 768)

with sync_playwright() as pw:
    channel = os.environ.get("BLOG_TEST_BROWSER_CHANNEL") or None
    browser = pw.chromium.launch(headless=True, channel=channel)
    passed = 0
    for part, lang, path in PAGES:
        for width in WIDTHS:
            page = browser.new_page(viewport={"width": width, "height": 900})
            errors = []
            page.on("pageerror", lambda error: errors.append(str(error)))
            page.route("**/*", lambda route: route.continue_()
                       if route.request.url.startswith(BASE + "/") else route.abort())
            response = page.goto(BASE + path, wait_until="domcontentloaded", timeout=20000)
            assert response is not None and response.status == 200, (part, lang, width, "HTTP")
            assert page.locator("html").get_attribute("lang") == lang, (part, lang, width, "lang")
            assert page.locator("main h1").count() == 1, (part, lang, width, "h1")
            canonical = page.locator("link[rel=canonical]").get_attribute("href") or ""
            assert canonical.endswith(path), (part, lang, width, "canonical", canonical)
            main = page.locator("main")
            text = main.inner_text()
            assert "\ufffd" not in text, (part, lang, width, "replacement character")
            assert main.locator(f'a[href="{NEXT[(part, lang)]}"]').count() >= 1, (
                part, lang, width, "next article link")
            if part == "1":
                assert "URL-prefix" in text and "Domain" in text, (part, lang, width, "teaser")
            elif part == "2":
                required = (
                    ("one web stream per property", "same tag ID from the same web stream",
                     "logical user base", "Domain property", "URL-prefix property",
                     "different domains", "2026-11-20", "remains unknown",
                     "no indexing or ranking preference", "unique hostname",
                     "crawling itself is not a ranking signal",
                     "does not establish a blanket trust score", "not proof of shared ranking trust")
                    if lang == "en" else
                    ("속성당 웹 스트림 하나", "같은 웹 스트림의 같은 태그 ID",
                     "논리적 사용자 집단", "도메인 속성", "URL 접두사 속성",
                     "도메인이 다른 사이트", "2026-11-20", "확실하지 않습니다",
                     "어느 쪽도 선호하지 않는다고", "고유 호스트 이름",
                     "크롤링 자체는 순위 신호가 아니며",
                     "순위 신뢰를 자동으로 공유한다는 증거는 아닙니다")
                )
                for phrase in required:
                    assert phrase in text, (part, lang, width, "missing text", phrase)
                for url in (GA4, GA4_CROSS, GSC, VERIFY, CLARITY, CLARITY_SETUP,
                            SUBDOMAIN_FAQ, CRAWL_BUDGET, CRAWL_MYTHS, LINKS, RANKING, DOMAIN_AGE):
                    assert main.locator(f'a[href="{url}"]').count() >= 1, (
                        part, lang, width, "official source link", url)
            elif part == "3":
                required = (
                    ("reporting choice", "not a general GA4 recommendation",
                     "does not automatically join users across streams",
                     "one web stream per property", "same tag ID",
                     "G-4DYFKSNFBG", "streamName=blog", "remains unverified")
                    if lang == "en" else
                    ("보고 목적에 따른 제 설정", "일반 권장안은 아닙니다",
                     "자동으로 연결되지는 않습니다", "속성당 웹 스트림 하나",
                     "같은 웹 스트림의 같은 태그 ID", "G-4DYFKSNFBG",
                     "streamName=blog", "확실하지 않습니다")
                )
                for phrase in required:
                    assert phrase in text, (part, lang, width, "missing text", phrase)
                for url in (GA4, GA4_CROSS, GSC, VERIFY):
                    assert main.locator(f'a[href="{url}"]').count() >= 1, (
                        part, lang, width, "official source link", url)
            else:
                required = (
                    ("one current web stream", "siteOwner", "siteUnverifiedUser",
                     "2026-11-20", "672", "651")
                    if lang == "en" else
                    ("현재 웹 스트림은 1개", "siteOwner", "siteUnverifiedUser",
                     "2026-11-20", "672", "651")
                )
                for phrase in required:
                    assert phrase in text, (part, lang, width, "missing text", phrase)
                assert main.locator(f'a[href="{GSC}"]').count() >= 1, (
                    part, lang, width, "official source link", GSC)
            if part in ("2", "3", "4"):
                for phrase in ("G-4DYFKSNFBG", "sc-domain:saramjh.github.io",
                               "siteOwner", "siteUnverifiedUser"):
                    assert phrase in text, (part, lang, width, "current native source", phrase)
            layout = page.evaluate("""() => ({
              width: document.documentElement.scrollWidth,
              viewport: window.innerWidth
            })""")
            assert layout["width"] <= layout["viewport"] + 2, (
                part, lang, width, "horizontal overflow", layout)
            assert not errors, (part, lang, width, "page errors", errors)
            passed += 1
            print("PASS", part, lang, width)
            page.close()
    browser.close()

print(f"PASS {passed} analytics article Chrome cases")
assert passed == 32, passed

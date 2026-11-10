---
title: "Playwright installed Chromium for 66 seconds. The browser test took seven."
description: "A GitHub Actions case study: replacing the Chromium download with runner-installed Chrome, with measured build times and preserved responsive tests."
date: 2026-11-10
tags: ["Playwright", "GitHub Actions", "Chrome", "CI", "Developer Notes"]
permalink: /playwright-github-actions-runner-chrome-en/
layout: default
lang: en
alternate_lang: ko
alternate_url: /playwright-github-actions-runner-chrome-ko/
published: true
seo:
  title: "Use preinstalled Chrome to avoid Playwright CI browser downloads"
  description: "Measured CI bottleneck: Chromium setup 66 seconds versus seven seconds of browser checks. A later runner-Chrome build took 40 instead of 90 seconds."
---

> 한국어판: [Playwright 테스트는 7초, Chromium 설치는 66초였다](/playwright-github-actions-runner-chrome-ko/)

**Before making Playwright assertions faster, measure how much CI time goes into installing the browser.** In one GitHub Pages job, Chromium setup took **66 seconds**, while the responsive test itself took **seven**. That was the problem behind [PR #36](https://github.com/saramjh/saramjh.github.io/pull/36).

This is a first-party record from the Jekyll developer blog. Its test still opens real routes at **390, 768 and 1440 pixels**, checking layout geometry, JavaScript errors, privacy conditions and mocked event wiring. No assertion was deleted to improve the result.

## Separate setup time from test time

I checked the original GitHub Actions step durations across four deployments.

| Existing build | Chromium installation | Responsive browser test |
|---|---:|---:|
| [#42740449886](https://github.com/saramjh/saramjh.github.io/actions/runs/42740449886) | 21 s | 3 s |
| [#42745558937](https://github.com/saramjh/saramjh.github.io/actions/runs/42745558937) | 42 s | 4 s |
| [#42747929262](https://github.com/saramjh/saramjh.github.io/actions/runs/42747929262) | 66 s | 7 s |
| [#42742948303](https://github.com/saramjh/saramjh.github.io/actions/runs/42742948303) | 328 s | 6 s |

These are workflow observations, not a controlled benchmark. They do show a recurring cost outside the browser assertions. Previously the workflow ran:

~~~sh
python -m pip install playwright==1.56.0
python -m playwright install --with-deps chromium
~~~

The site uses GitHub-hosted **Ubuntu 24.04**. Its [runner software inventory](https://github.com/actions/runner-images/blob/main/images/ubuntu/Ubuntu2404-Readme.md) includes Google Chrome. Playwright can [launch installed Chrome using its branded channel](https://playwright.dev/python/docs/browsers).

## Change the CI browser without removing tests

[The PR #36 diff](https://github.com/saramjh/saramjh.github.io/pull/36/files) keeps the pinned Playwright Python package and checks for the browser already present:

~~~yaml
- name: Install Playwright for preinstalled Chrome checks
  run: |
    python -m pip install playwright==1.56.0
    command -v google-chrome
    google-chrome --version

- name: Verify portfolio layout in real browser
  env:
    BLOG_TEST_BROWSER_CHANNEL: chrome
  run: |
    python tests/portfolio_layout_smoke.py
~~~

The existing Python test only needs one configurable channel:

~~~python
import os
from playwright.sync_api import sync_playwright

with sync_playwright() as playwright:
    channel = os.environ.get("BLOG_TEST_BROWSER_CHANNEL") or None
    browser = playwright.chromium.launch(headless=True, channel=channel)
    # Existing page, viewport and privacy assertions follow.
    browser.close()
~~~

The environment variable selects Chrome on CI. Local development without that variable continues to use Playwright's default Chromium installation, which must already be available locally. If Chrome disappears from the hosted runner, the binary check will fail instead of silently skipping browser tests.

## What the deployment actually measured

| Step | Earlier main run [#42747929262](https://github.com/saramjh/saramjh.github.io/actions/runs/42747929262) | Later main run [#42752895730](https://github.com/saramjh/saramjh.github.io/actions/runs/42752895730) |
|---|---:|---:|
| Browser preparation | 66 s | 6 s |
| Browser checks | 7 s | 17 s |
| Entire build job | 90 s | 40 s |

The later job took **50 seconds less**. Importantly, the browser checks were **10 seconds slower**. Runner load, network conditions and browser versions vary. This single comparison does not prove that every future CI run will be 55.6% faster or that every saved second came from the browser change.

The [PR checks](https://github.com/saramjh/saramjh.github.io/pull/36/checks) and [main GitHub Pages build and deployment](https://github.com/saramjh/saramjh.github.io/actions/runs/42752895730) passed. The main log identified **Google Chrome 156.0.8078.79** and confirmed the real browser geometry checks passed. The public site endpoints subsequently returned HTTP 200. The IndexNow notification step skipped correctly because no published content URL changed in that code release.

## What remains uncertain

The runner's Chrome version can change even though the Playwright Python package is pinned. Keep the real browser checks as a compatibility gate. [Playwright's CI guidance](https://playwright.dev/python/docs/ci) also notes that Linux browser-cache restoration is often not worth the cost.

This release improved one **developer feedback loop**, not search visibility or human readership. There are no verified visitor or conversion outcomes from the change. Another CI case, [the SVG-to-PNG Open Graph regression](/jekyll-svg-to-png-og-ci-regression-en/), shows a different failure. More first-party work is linked from the [developer portfolio](/portfolio/).

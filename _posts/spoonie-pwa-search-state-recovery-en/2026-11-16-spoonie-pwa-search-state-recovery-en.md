---
title: "Spoonie: restoring iPhone PWA updates and search state"
description: "How Spoonie PR #47 improved service-worker update checks, URL-backed search state, result counts and browser regression coverage."
date: 2026-11-16
tags: ["Spoonie", "PWA", "Frontend", "Search"]
permalink: /spoonie-pwa-search-state-recovery-en/
layout: default
lang: en
alternate_lang: ko
alternate_url: /spoonie-pwa-search-state-recovery-ko/
image: /assets/img/dev/spoonie-pr47-pwa-og-20261118/spoonie-pr47-en.png
image_width: 1200
image_height: 630
published: true
seo:
  title: "Spoonie iPhone PWA and search-state recovery"
  description: "A case study of Spoonie PR #47, covering Home Screen update checks and search state restored after opening a recipe and pressing Back."
---

> 한국어: [Spoonie iPhone 홈 화면 앱과 검색 상태 복원](/spoonie-pwa-search-state-recovery-ko/)

Two Spoonie workflows were breaking. An iPhone Home Screen installation could continue showing an older version after a deployment. On the search page, opening a recipe and pressing the browser's Back button could clear the query, selected tab and results. The result count also remained hidden until every matching page had loaded.

[Spoonie PR #47](https://github.com/saramjh/spoonie/pull/47), merged on November 16, 2026, addressed these three behaviors.

## Keep the search when returning from a recipe

The reproduction recorded in the pull request used the live search page: entering \`김치\` returned 19 recipe links. After opening one result and going Back, the query was blank and the URL no longer carried the search state.

The updated search client writes a committed query to the current route as \`?q=...\`. When a reader selects a result tab, it can also store \`?tab=...\`. Other URL parameters are preserved. When the page mounts again or the browser fires \`popstate\`, the client restores the query and selected tab from the URL.

SWR page data is reused when the search component remounts. Changing the query starts with one page instead of requesting extra pages speculatively.

The result count now appears as soon as the first page arrives. If more pages remain, the interface shows \`N+\`; it shows an exact count after the final page loads. The pull request's deterministic RPC fixture checks a first page with 20 or more results and a final total of 22. That 22 is test data, not a measurement of live search traffic.

## Check for updates in iPhone Home Screen installations

The change keeps the existing service-worker registration and generated Workbox worker. It asks the current registration to check for updates after registration, when the browser comes online, on \`pageshow\`, and when the app returns to the foreground. Checks are throttled to once per minute. The registration uses \`updateViaCache: "none"\` so stale imported worker scripts do not interfere with update checks.

When a new worker takes control, a standalone Home Screen app reloads if it is safe to do so. The app avoids automatic reloads on recipe or post editing routes and while an input or editable element has focus. Regular browser sessions keep the existing manual update prompt.

The fix does not clear local storage or discard an in-progress draft.

## Browser tests and production-code readback

[PR #47](https://github.com/saramjh/spoonie/pull/47) was merged on November 16, 2026, as \`e563ab228642d4262cbca95a6c2c0d96468c185f\`. [GitHub Actions run 43877018376](https://github.com/saramjh/spoonie/actions/runs/43877018376) completed successfully. The job waited for the Netlify preview for that commit, then ran real Chromium browser regressions against it.

The tests cover query, tab, results and scroll restoration after detail navigation and Back; incremental and final result counts; reuse of previously loaded pages; first-page-only fetching for a new query; standalone service-worker update checks; and avoiding refresh while a user is editing.

The live [Spoonie search page](https://spoonie.kr/search?q=%EA%B9%80%EC%B9%98) and [service-worker file](https://spoonie.kr/sw.js) returned HTTP 200. The served production JavaScript also contained \`updateViaCache\` and \`controllerchange\` in the \`app/layout\` bundle, and \`popstate\` and \`URLSearchParams\` in the search-page bundle.

The remote Chromium regression passed. A physical iPhone Home Screen installation was not tested. Update success rates, repeat visits and changes in the number of users have not been measured.

## Related Spoonie work

- [Search discovery and the server-rendered explorer](/spoonie-search-discovery-en/)
- [Handling blocked service-worker registration in Spoonie](/spoonie-service-worker-registration-en/)
- [Spoonie's bookmark privacy boundary](/spoonie-bookmark-privacy-boundary-en/)

[Read PR #47](https://github.com/saramjh/spoonie/pull/47) · [View the merge commit](https://github.com/saramjh/spoonie/commit/e563ab228642d4262cbca95a6c2c0d96468c185f) · [Open Spoonie](https://spoonie.kr/)

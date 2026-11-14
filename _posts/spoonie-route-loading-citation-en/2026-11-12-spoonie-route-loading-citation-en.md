---
title: "Route loading and recipe citation search in Spoonie"
description: "How Spoonie handles destination loading, canceled navigation and stalled routes, alongside recipe citation search."
date: 2026-11-12
tags: ["Spoonie", "Frontend", "User Experience"]
permalink: /spoonie-route-loading-citation-en/
layout: default
lang: en
alternate_lang: ko
alternate_url: /spoonie-route-loading-citation-ko/
published: true
modified: 2026-11-14
seo:
  title: "Spoonie route loading and recipe citation search"
  description: "Spoonie destination skeletons, safe input handling, canceled links and 10-second navigation recovery, with source and deployment evidence."
---

> 한국어: [Spoonie 화면 전환 로딩과 레시피 인용 검색 정비](/spoonie-route-loading-citation-ko/)

Spoonie updated its route-loading behavior and recipe citation search interface. [Pull request #34](https://github.com/saramjh/spoonie/pull/34) merged on November 12, 2026. The changed code was also found in JavaScript served by the public site.

## Two moments in the recipe workflow

Moving between recipe pages should make the transition state understandable. When citing another recipe, the search and selection flow should be clear enough to follow. The changes in this pull request address those two interactions.

## Implementation and verification

The merged change covers route-loading behavior and the citation-search UI. Comparing the source change with publicly served JavaScript confirmed that the relevant code reached production.

That check establishes deployment of the code. It does not measure perceived loading speed, citation usage, or user retention. Those outcomes have not been independently measured.

For a separate account-specific UI issue, see [Spoonie's viewer-scoped likes and saves cache fix](/spoonie-viewer-cache-isolation-en/).

## November 14 follow-up: show the destination while navigation waits

The progress bar from the earlier fix still left the old homepage in place when the server was slow. In the reproduction for [PR #42](https://github.com/saramjh/spoonie/pull/42), delaying the `/search` response kept that old view visible for more than 700 ms. The follow-up displays a skeleton shaped like the destination as soon as internal navigation starts.

A move to search shows placeholders for the search field and filters; a move to a recipe or post shows a detail-page layout. The top progress indicator remains, and the bottom navigation can interrupt a pending transition. A filter change that only updates query parameters keeps the current screen visible.

In an isolated Chromium test with a delayed route, the destination skeleton was visible at 90, 200, 500 and 950 ms, then disappeared when the route completed. The PR reports 405 passing regression tests and six separate media-cleanup tests. On November 14, the `app/layout` JavaScript served by [Spoonie](https://spoonie.kr/) was byte-identical to the PR #42 Netlify preview and included `data-route-feedback`. That confirms the deployed code, while real visitors' perceived wait times and abandonment have not been measured.

### November 14 follow-ups: prevent hidden input and false navigation

A skeleton can cover the old screen while leaving its search input reachable by keyboard. [PR #43](https://github.com/saramjh/spoonie/pull/43) marks the outgoing `main` as `inert` until the new route commits. It also removes the duplicate `needsHeader` state and keeps photo-press feedback through the existing 300 ms single-versus-double-tap interval.

A separate bug remained: the global click listener treated some canceled links as navigation, showing a full-screen skeleton even though the app had stopped the move. [PR #44](https://github.com/saramjh/spoonie/pull/44) removed that click listener. Links now report a real Next.js `onNavigate` event after the caller can cancel it. Programmatic routing and browser history keep their existing signals.

If a destination is still pending after 10 seconds, the loading UI now explains the delay and offers **Keep previous screen** or **Try again**, rather than silently dismissing progress. Query-only updates retain their existing behavior. PR #44 reports 407 passing Vitest cases, six media safety checks and an isolated Chromium run covering canceled links, history, keyboard focus, retry and cancellation. The [November 14 production layout bundle](https://spoonie.kr/_next/static/chunks/app/layout-ef63d2df452ac6a9.js) includes the recovery text and navigation feedback; that verifies deployed code, not measured reductions in user frustration or abandonment.

[Review the merged change](https://github.com/saramjh/spoonie/pull/34) · [Visit Spoonie](https://spoonie.kr/)

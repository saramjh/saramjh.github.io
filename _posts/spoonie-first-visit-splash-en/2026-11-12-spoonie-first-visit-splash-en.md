---
title: "Why Spoonie restored its first-visit introduction"
description: "How Spoonie PR #35 brought back the home splash without bringing back overlays during navigation."
date: 2026-11-12
tags: ["Spoonie", "Frontend", "User Experience"]
permalink: /spoonie-first-visit-splash-en/
layout: default
lang: en
alternate_lang: ko
alternate_url: /spoonie-first-visit-splash-ko/
published: true
seo:
  title: "Restoring Spoonie's first-visit splash | PR #35"
  description: "The first-home splash regression fix in Spoonie PR #35, with source and deployment checks."
---

> 한국어: [Spoonie 첫 화면의 브랜드 인트로를 다시 살린 이유](/spoonie-first-visit-splash-ko/)

Spoonie restored its branded introduction on the first visit to the home page. [Pull request #35](https://github.com/saramjh/spoonie/pull/35) merged on November 12, 2026, correcting a regression introduced during an earlier loading-performance change.

## An introduction should not interrupt navigation

A first-visit logo can establish where someone has landed. Replaying it whenever they open a recipe or switch pages would slow down the experience. The fix separates the initial home visit from ordinary route transitions.

## What changed

- A static server-rendered logo introduction returns on the first home visit.
- `sessionStorage` remembers whether it has appeared in the current tab.
- The roughly 1.6-second introduction has a CSS fallback so a delayed React hydration does not leave an invisible overlay blocking the page.
- Internal navigation and directly opened recipe-detail links skip the introduction.

The pull request reports 377 passing Vitest tests, TypeScript and ESLint checks, a production build, and local viewport checks. Those are the PR author's reported results, not a separate rerun by Dev.

## What was checked on the public site

The [Spoonie home page](https://spoonie.kr/) returned HTTP 200. Its served HTML contained the `spoonie-splash` session key and `splash-seen` class logic, evidence that the initial-entry handling reached the public deployment. I have not independently reproduced the timed transition in a browser or measured how visitors respond to it.

[Read the merged PR](https://github.com/saramjh/spoonie/pull/35) · [Open Spoonie](https://spoonie.kr/) · [Earlier loading work](/spoonie-route-loading-citation-en/)

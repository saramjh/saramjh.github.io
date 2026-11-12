---
title: "Separating likes and saves by viewer in Spoonie"
description: "A development note on Spoonie PR #37: viewer-scoped UI caches, late responses, and what the public production code confirms."
date: 2026-11-12
tags: ["Spoonie", "Frontend", "Caching"]
permalink: /spoonie-viewer-cache-isolation-en/
layout: default
lang: en
alternate_lang: ko
alternate_url: /spoonie-viewer-cache-isolation-ko/
published: true
seo:
  title: "Spoonie viewer-specific likes and saves cache fix"
  description: "How Spoonie PR #37 separates viewer-specific cache keys and handles optional personalization failures."
---

> 한국어: [Spoonie 계정별 좋아요·저장 캐시 분리](/spoonie-viewer-cache-isolation-ko/)

Spoonie changed how recipe pages cache likes and saves so the displayed state belongs to the current viewer. [Pull request #37](https://github.com/saramjh/spoonie/pull/37) merged on November 12, 2026. The public site's JavaScript also contains the viewer-specific cache-key logic.

## Why the cache boundary mattered

The recipe body and the like/save overlay did not always have the same cache boundaries. UI state keyed only by item ID could survive an account change. An earlier request finishing late could also update the next viewer's screen.

## What changed

- The overlay uses a viewer-specific `itemDetail|viewerId|itemId` key. SWR waits while initial authentication is loading.
- Optimistic list updates and late responses are restricted to the current viewer.
- Existing session data replaces redundant user and profile lookups.
- If an optional like/save query fails, the recipe body, ingredients, and instructions remain available.

The pull request added regression tests for the installed SWR 2.3.4 cache structure. Its author reported 391 passing Vitest tests; Dev did not independently rerun the suite.

## What the public deployment confirms

The [recipe detail page](https://spoonie.kr/recipes/aab1f6da-d7d3-4ed0-bbc7-10dae3515718) and [recipe listing](https://spoonie.kr/recipes) returned HTTP 200 during verification. Their served Next.js bundles included the viewer-specific cache-key helper and viewer-scoped list filtering.

This establishes that the compiled logic was being served. A two-account authenticated switching test, mobile interaction testing, and retention measurements remain unverified.

The [earlier Spoonie author-header note](/spoonie-author-header-consistency-en/) covers layout consistency. This change concerns ownership of personal UI state.

[Read the merged change](https://github.com/saramjh/spoonie/pull/37) · [Visit Spoonie](https://spoonie.kr/)

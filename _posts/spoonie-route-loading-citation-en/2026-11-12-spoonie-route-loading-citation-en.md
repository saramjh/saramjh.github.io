---
title: "Route loading and recipe citation search in Spoonie"
description: "An engineering note on Spoonie PR #34, covering route loading and the recipe citation search interface."
date: 2026-11-12
tags: ["Spoonie", "Frontend", "User Experience"]
permalink: /spoonie-route-loading-citation-en/
layout: default
lang: en
alternate_lang: ko
alternate_url: /spoonie-route-loading-citation-ko/
published: true
seo:
  title: "Spoonie route loading and recipe citation search"
  description: "What Spoonie PR #34 changed in route loading and recipe citation search, with deployment evidence and limits."
---

> 한국어: [Spoonie 화면 전환 로딩과 레시피 인용 검색 정비](/spoonie-route-loading-citation-ko/)

Spoonie updated its route-loading behavior and recipe citation search interface. [Pull request #34](https://github.com/saramjh/spoonie/pull/34) merged on November 12, 2026. The changed code was also found in JavaScript served by the public site.

## Two moments in the recipe workflow

Moving between recipe pages should make the transition state understandable. When citing another recipe, the search and selection flow should be clear enough to follow. The changes in this pull request address those two interactions.

## Implementation and verification

The merged change covers route-loading behavior and the citation-search UI. Comparing the source change with publicly served JavaScript confirmed that the relevant code reached production.

That check establishes deployment of the code. It does not measure perceived loading speed, citation usage, or user retention. Those outcomes have not been independently measured.

For a separate account-specific UI issue, see [Spoonie's viewer-scoped likes and saves cache fix](/spoonie-viewer-cache-isolation-en/).

[Review the merged change](https://github.com/saramjh/spoonie/pull/34) · [Visit Spoonie](https://spoonie.kr/)

---
title: "How I made Spoonie's recipe search work past its first twenty results"
description: "A source-backed account of Spoonie PR #31: separate server-paged Recipe and Recipeed results, predictable ordering, and a reference picker that preserves author identity."
date: 2026-11-12
tags: ["Spoonie", "Product Engineering", "Recipe Discovery", "Supabase", "Search"]
permalink: /spoonie-search-discovery-en/
layout: default
lang: en
alternate_lang: ko
alternate_url: /spoonie-search-discovery-ko/
image: /spoonie-search-discovery-en/spoonie-search-flow.svg
image_width: 1280
image_height: 530
published: true
seo:
  title: "Fixing Spoonie's recipe search, pagination and reference picker"
  description: "I replaced a single 20-item search batch with separate paged results and made same-title recipes easier to distinguish. The implementation and production evidence behind PR #31."
---

> 한국어: [Spoonie 검색에서 20개 이후의 레시피도 찾도록 고친 과정](/spoonie-search-discovery-ko/)

**I changed Spoonie's recipe search so its results no longer have to stop at the first batch.** [PR #31](https://github.com/saramjh/spoonie/pull/31) merged on November 11, 2026 at 15:33 UTC. The [live search page](https://spoonie.kr/search) serves JavaScript with the new server pagination parameters and separate “show more” controls for Recipes and Recipeed posts.

<p class="article-live-demo"><a class="article-live-demo-link" href="https://spoonie.kr/search">Try Spoonie's public recipe search</a><span class="article-live-demo-note">Search Recipe and Recipeed results in their separate tabs.</span></p>

## Where the old search stopped

The previous client requested up to twenty matching items, then split that batch into Recipe and Recipeed tabs. When more items matched the term, the interface had no path to the next set. This is an awkward limit for a recipe product: different authors may publish dishes with identical names, and the reader needs to see which version belongs to whom.

Each tab now makes its own server request. The client asks for 21 rows, displays the first twenty, and uses the extra row to determine whether another page exists. A later request carries the result offset. The corresponding button appears only while more matches remain.

<figure>
  <img src="/spoonie-search-discovery-en/spoonie-search-flow.svg" alt="Developer-authored diagram of a search query feeding server-side ranking and separate twenty-item Recipe and Recipeed pages with conditional show-more controls" width="1280" height="530" loading="lazy" style="display:block;width:100%;height:auto;">
  <figcaption>A diagram of the implementation in PR #31. It is not a screenshot or a measure of search activity.</figcaption>
</figure>

## Preserve distinct recipes with the same title

The server ranks exact title matches ahead of weaker ones and uses relevance, creation time, and an item ID to make ordering predictable across pages. A recipe is not discarded just because another author used the same title. Its unique ID remains part of the result, and the existing cards still show the author and thumbnail.

The [merged SQL change](https://github.com/saramjh/spoonie/pull/31/files) extends search_items_optimized with an item-type filter and offset. Defaults maintain compatibility with older calls. It retains SECURITY INVOKER, so database row-level security still governs which records each requester can see. The PR documents checks for the old call form, private-record visibility under anonymous access, and overlapping pages.

## Selecting a referenced recipe

When a Spoonie author wants to attach a recipe as a reference, title alone may not identify the right post. The editor previously searched author profiles and recipe items in two client requests. PR #31 replaces those requests with a single server function, search_citable_recipes, that matches titles and authors. It returns ten items per page, waits 300 ms after input, and cancels stale requests. The existing author and image presentation stays in place.

Finding a referenced recipe does not grant permission to copy its prose or photographs. Search and content reuse remain separate decisions.

## What reached production

On November 12, [Spoonie's search page](https://spoonie.kr/search) returned HTTP 200. The deployed search bundle includes result_offset and item_type_filter in the server call and both Recipe and Recipeed “show more” controls.

I did not run a production end-to-end test with more than twenty real matching results or measure a change in search success, referrals, or active readers. The verifiable result is a merged search implementation delivered to the public client, with a way to request further results.

Related first-party work: the [Spoonie editorial directory](/spoonie-editorial-curators-en/), the [recipe poll feature](/spoonie-live-polls-en/), and the [Spoonie project overview](/portfolio/spoonie/).

Original evidence: [Spoonie PR #31](https://github.com/saramjh/spoonie/pull/31) and the [live search page](https://spoonie.kr/search).

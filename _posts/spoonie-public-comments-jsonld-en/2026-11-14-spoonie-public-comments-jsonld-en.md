---
title: "Spoonie: fixing missing comments in SocialMediaPosting JSON-LD"
description: "A Spoonie PR #41 case study on real public comment data and readback of 13 deployed post pages."
date: 2026-11-14
tags: ["Spoonie", "SEO", "Structured Data", "Next.js"]
permalink: /spoonie-public-comments-jsonld-en/
layout: default
lang: en
alternate_lang: ko
alternate_url: /spoonie-public-comments-jsonld-ko/
published: true
seo:
  title: "Fixing real post comments in Spoonie JSON-LD"
  description: "Why Spoonie post schema could report zero comments, how PR #41 fixed the data path, and what 13 live pages show."
---

> 한국어: [Spoonie 레시피드 댓글 구조화 데이터 수정](/spoonie-public-comments-jsonld-ko/)

A Spoonie post could have replies while its structured data described none. The detail query returned a comment count, but did not always include the `comments_data` array used by `PostSchema`. The component previously derived `commentCount` from that optional array.

[Spoonie PR #41](https://github.com/saramjh/spoonie/pull/41) connected the JSON-LD to public reply records. I checked the rendered output of all 13 post URLs listed in the [public sitemap](https://spoonie.kr/sitemap.xml) after the change.

## Where the count went missing

The page-level count and the schema were reading different shapes of data. `initialItem.comments_count` held the total, while the earlier schema relied on `item.comments_data || []`. When the array was absent, the generated count could become zero.

The server now fetches comments only for **public posts that already report at least one reply**. It excludes deleted comments, sorts by creation time, and limits the list to 50. `PostSchema` keeps the original total in `commentCount` and emits `Comment` objects only for replies with nonempty text. A post with no replies does not get a fabricated comment object.

The total count can exceed the number of embedded `Comment` objects when a post has more than 50 replies. The limit keeps the rendered markup bounded.

## Reading the deployed HTML

On November 14, 2026 (KST), the public sitemap listed 13 Spoonie post URLs. All 13 returned HTTP 200 and contained `SocialMediaPosting` JSON-LD.

| Observed output | Result |
| --- | ---: |
| Public pages with comments | 3 |
| Public pages without comments | 10 |
| Embedded `Comment` objects | 4 (1, 1, and 2) |
| Mismatches between declared count and embedded list | 0 |

For example, the [public post with two comments](https://spoonie.kr/posts/577808ef-555f-40cb-a71c-dcad1a1b6058) has `commentCount: 2` and two actual `Comment` objects in its JSON-LD. The zero-comment pages have `commentCount: 0` and no embedded comment. The audit did not retain the comment text or author details.

This is a readback of **13 publicly listed pages at one point in time**. It does not establish whether Google crawled the new markup, displayed a special result, or sent more visitors.

## A regression check worth adding

A component unit test alone may not reveal a missing field in the live data fetch. PR #41 added three regression cases covering real replies, empty lists, and a bounded embedded list. I also parsed the `application/ld+json` blocks from the served HTML.

[Schema.org SocialMediaPosting](https://schema.org/SocialMediaPosting) and [Comment](https://schema.org/Comment) define the vocabulary. Using it correctly does not guarantee a search feature or ranking outcome. The earlier [Spoonie sitemap XML fix](/spoonie-sitemap-xml-image-escaping-en/) followed the same source-versus-rendered-output verification approach.

[Read PR #41](https://github.com/saramjh/spoonie/pull/41) · [Open Spoonie](https://spoonie.kr/)

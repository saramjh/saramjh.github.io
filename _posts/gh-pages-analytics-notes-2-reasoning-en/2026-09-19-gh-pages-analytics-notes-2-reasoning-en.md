---
title: "Running Several GitHub Pages Sites Solo: An Analytics Dilemma (Part 2 — The Reasoning)"
description: "Merge or split GA4 properties? Is Search Console verified per domain or per project? Reconstructing the reasoning behind that decision from GA4/Search Console/Clarity's general principles, not a verbatim transcript."
date: 2026-09-18
tags: GA4, Google Analytics, Search Console, Microsoft Clarity, GitHub Pages, SEO
permalink: /gh-pages-analytics-notes-2-reasoning-en/
layout: default
lang: en
alternate_lang: ko
alternate_url: /gh-pages-analytics-notes-2-reasoning-kr/
---

<p style="background: rgba(0, 120, 212, 0.08); border-left: 4px solid #0078d4; padding: 10px 14px; margin-bottom: 16px; border-radius: 4px; font-size: 0.95rem;">
  🌐 <strong>한국어 버전:</strong> Read the Korean version at <a href="/gh-pages-analytics-notes-2-reasoning-kr/"><strong>애널리틱스 고민 노트 (한국어)</strong></a>.
</p>

<p style="background: rgba(120, 90, 0, 0.08); border-left: 4px solid #b8860b; padding: 10px 14px; margin-bottom: 24px; border-radius: 4px; font-size: 0.9rem;">
  📚 <strong>Series</strong> — <a href="/gh-pages-analytics-notes-1-problem-en/">Part 1: The Problem</a> · Part 2 <strong>Reasoning</strong> (this post) · <a href="/gh-pages-analytics-notes-3-decision-en/">Part 3: The Decision</a> · <a href="/gh-pages-analytics-notes-4-open-en/">Part 4: Current State &amp; Open Questions</a>
</p>

## A disclosure first

The reasoning below is not a verbatim quote from the AI conversation I actually had. I don't have that session's log anymore, so what follows is a **reconstruction from GA4/Search Console/Clarity's documented behavior and the general principles the SEO community treats as settled**, not "the AI said this." Read it as "here's why that advice seemed sound," not as a transcript.

## GA4: properties and data streams are different layers

The most confusing part of GA4's structure, for me, was realizing that "property" and "data stream" are not the same thing.

- **Property**: the top-level unit where data is aggregated. Reports, data retention, free-tier data thresholds, and the BigQuery link are all independent per property.
- **Data stream**: an individual source feeding data into a property — one website, one app. A single property can hold multiple web data streams.

In other words, my habit of "a new property for every tool" was splitting things one layer higher than necessary — a case where **a new data stream per tool might have been enough**.

Google's own recommendation for organizations that want several sites or apps tracked as one brand is exactly this: one property, multiple data streams. With that structure:

- A user who reads a blog post and then moves to a tool can be followed as a single journey within the same property (assuming cross-domain measurement is configured).
- Hostname or stream name can be used as a dimension, and exploration/comparison features let you filter down to "just this tool" or "just the blog" when needed — the same principle behind querying sessions by `hostName`, as I did earlier in this series' data pull.
- Splitting into separate properties, by contrast, means each one burns through its own free-tier thresholds and retention window separately, and the user journey is cut off at the property boundary by design.

## Search Console: domain-level vs. URL-prefix verification is the crux

Search Console supports two verification methods:

- **Domain property**: verifies all of `saramjh.github.io` at once — every subdomain, every protocol (http/https), and every subpath like `/scratchLottery/` or `/richChecker/` falls under this one property automatically.
- **URL-prefix property**: verifies one exact path, e.g. `https://saramjh.github.io/scratchLottery/`.

Registering a sitemap per project, as I'd been doing, is closer to the URL-prefix pattern. If everything sits on the same domain anyway, consolidating into a single domain property removes the redundancy in verification and reporting. Sitemaps themselves can still be submitted per project (each tool's sitemap path listed separately in `robots.txt`), but the property overseeing them only needs to be the one domain-level property.

## What "a shared root domain shares trust" actually means — and its limits

This is the part that calls for the most caution. The claim that "sites under the same root domain share trust/authority" gets repeated often in SEO circles, but Google hasn't published exactly how — or whether — this is reflected algorithmically. What's comparatively well-supported:

- Subdirectories (path-based structures like `/scratchLottery/`) are more easily read by search engines as part of the same site than subdomains or entirely separate domains would be — and this already applied to my project pages by default, since none of them had a custom domain attached.
- Site-wide signals like crawl budget, backlinks, and domain age accumulate at the domain level. But "Google factors this into ranking" and "exactly how much it factors in" are two separate claims, and the second one is hard to verify externally.
- Conversely, sharing trust doesn't mean rankings improve for unrelated search intents — each tool still has to earn relevance for its own content and query space.

Net takeaway: "one root domain means shared trust" isn't wrong, exactly, but it's better described as **a reasonable, industry-accepted explanation, not something with a proven causal chain behind it**.

## Clarity: really a question of what you want to see together, not a principle

Unlike GA4 or Search Console, Clarity has no concept of domain-level verification. Technically, one Clarity project code works fine embedded across multiple domains or paths. So this wasn't really a matter of principle — it was closer to **an operating decision**.

- One shared project: every tool's session replays and heatmaps land in a single dashboard, but a low-traffic tool's sessions can get lost in the noise of a higher-traffic one.
- Separate projects per tool: cleaner per-tool analysis, at the cost of a dashboard to check for every tool you ship.

## Putting it together

Across all three tools, the same shape kept recurring:

1. **Verify / create at the broadest reasonable unit (the whole domain)**
2. **Narrow down only when needed, using filters like subpath or hostname within that unit**

That's the direction I actually ended up taking. Next: how I applied this in practice — what got merged, and when.

→ [Continue to Part 3: The Decision](/gh-pages-analytics-notes-3-decision-en/)

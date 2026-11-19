---
title: "Running Several GitHub Pages Sites Solo: An Analytics Dilemma (Part 2 — The Reasoning)"
description: "Merge or split GA4 properties? Is Search Console verified per domain or per project? Reconstructing the reasoning behind that decision from GA4/Search Console/Clarity's general principles, not a verbatim transcript."
date: 2026-09-18
tags: ["GA4", "Google Analytics", "Search Console", "Microsoft Clarity", "GitHub Pages", "SEO"]
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
  📚 <strong>Series</strong> — <a href="/gh-pages-analytics-notes-1-problem-en/">Part 1: The Problem</a> · Part 2 <strong>Reasoning</strong> (this post) · <a href="/gh-pages-analytics-notes-3-decision-en/">Part 3: The Decision</a> · <a href="/gh-pages-analytics-notes-4-open-en/">Part 4: Current State &amp; Open Questions</a> · <a href="/gh-pages-analytics-notes-5-followup-en/">Part 5: After a Naver #2 Placement and a Traffic Spike</a>
</p>

## A disclosure first

The reasoning below is not a verbatim quote from the AI conversation I actually had. I don't have that session's log anymore, so what follows is a **reconstruction from GA4/Search Console/Clarity's documented behavior and the general principles the SEO community treats as settled**, not "the AI said this." Read it as "here's why that advice seemed sound," not as a transcript.

## GA4: properties and data streams are different layers

The most confusing part of GA4's structure, for me, was realizing that "property" and "data stream" are not the same thing.

- **Property**: the top-level unit where data is aggregated. Reports, data retention, free-tier data thresholds, and the BigQuery link are all independent per property.
- **Data stream**: a source sending data to a property from a website or app. A property can contain multiple streams, although Google's general best practice is one web data stream per property in most cases.

At the time, I assumed a separate property per tool was more granular than necessary. Whether that was true depends on whether the tools share a logical user base and should be analyzed together; a separate stream is not always a substitute for a separate property.

**Account verification (2026-11-20).** Google's recommendation above is distinct from what this account contains today. The original `blog` GA4 property currently lists **one current web stream**, named `blog` (measurement ID `G-4DYFKSNFBG`). Part 3 preserves my September notes about separate streams for each tool, but a present-day inventory cannot reconstruct which streams existed then. It does not confirm that separate per-tool streams remain in place ([Google's account-structure guidance](https://support.google.com/analytics/answer/9679158?hl=en)).

Several streams can be reported under one property, but that does not itself join users across streams. Google's cross-domain setup requires the same tag ID from the same web stream on each domain ([Google's cross-domain setup](https://support.google.com/analytics/answer/10071811?hl=en)). Today's one-stream inventory should be checked against actual page tags and event reports before claiming any blog-to-tool journey. The old September registration history remains unknown from this read.
- Hostname or stream name can be used as a dimension, and exploration/comparison features let you filter down to "just this tool" or "just the blog" when needed — the same principle behind querying sessions by `hostName`, as I did earlier in this series' data pull.
- Splitting into separate properties, by contrast, means each one burns through its own free-tier thresholds and retention window separately, and the user journey is cut off at the property boundary by design.

## Search Console: Domain and URL-prefix properties differ in coverage and verification

Search Console has two property types, with different coverage and verification requirements:

- **Domain property**: includes subdomains, protocols and paths, but **requires DNS verification**. A GitHub Pages repository doesn't let me edit the DNS records for GitHub's default `saramjh.github.io` hostname.
- **URL-prefix property**: `https://saramjh.github.io/` includes the HTTPS pages for every project below that host. A narrower prefix such as `https://saramjh.github.io/scratchLottery/` includes only that path and its descendants. An HTML file or tag can be used to verify a URL-prefix property.

**Native Search Console check (2026-11-20).** The original connected account currently lists `https://saramjh.github.io/` as `siteOwner` and `sc-domain:saramjh.github.io` as `siteUnverifiedUser`. The site-root URL-prefix property is therefore currently verified for this HTTPS host; the Domain property is not verified in this account. My earlier conclusion that a single verified Domain property covered everything omitted the DNS requirement. Submitting per-project sitemaps does not prove verification. Exactly which method was used in September remains unknown without the historical receipt ([property coverage](https://support.google.com/webmasters/answer/34592?hl=en); [verification instructions](https://support.google.com/webmasters/answer/9008080?hl=en)).

## What a shared root domain does — and doesn't — establish

Google's public guidance supports several narrower facts, not a general rule that every path under one domain inherits the same ranking authority:

- **Subdirectories and subdomains:** Google says it has no indexing or ranking preference between them. Choose the structure that's easier to organize and manage. Its crawl-budget documentation defines a site by a unique hostname, so subdomains have separate crawl budgets. This is a crawling boundary, not a ranking advantage.
- **Crawl budget:** It is the set of URLs Google can and wants to crawl. Google says crawling itself is not a ranking signal, and the guidance is mainly intended for very large or frequently updated sites.
- **Links and ranking:** Google uses links to discover pages and as relevance signals. Its ranking systems primarily evaluate pages, while also using some site-wide signals. This does not establish a blanket trust score that transfers to every path under a root domain.
- **Domain age:** I removed it from the list of supported ranking signals; the evidence here does not establish registration age as a ranking advantage.

For `https://saramjh.github.io/`, the tools share one hostname and use different paths. They therefore share a host-level crawl-budget boundary, but that does not prove that Google combines their relevance or rankings into one score ([subfolder vs. subdomain FAQ](https://developers.google.com/search/help/crawling-index-faq?hl=en); [crawl-budget guide](https://developers.google.com/crawling/docs/crawl-budget?hl=en); [crawling myths](https://developers.google.com/crawling/docs/myths-about-crawling); [link best practices](https://developers.google.com/search/docs/crawling-indexing/links-crawlable); [ranking systems guide](https://developers.google.com/search/docs/appearance/ranking-systems-guide); [Google Search Central's domain-age video](https://www.youtube.com/watch?v=-pnpg00FWJY)).

Net takeaway: a shared hostname is a fact about URL and crawl structure, not proof of shared ranking trust. Each page still has to earn relevance for its own content and search intent.

## Clarity: really a question of what you want to see together, not a principle

Clarity does not use Search Console's Domain/URL-prefix verification model. A project can collect data from multiple sites when its tracking code is installed on each, and the same script can be installed on multiple subdomains. Microsoft recommends a separate project for each different domain. For tools under one host, the choice is whether their recordings and heatmaps should be grouped together ([Clarity FAQ](https://learn.microsoft.com/en-us/clarity/faq/); [setup guide](https://learn.microsoft.com/en-us/clarity/setup-and-installation/clarity-setup)).

- One shared project: every tool's session replays and heatmaps land in a single dashboard, but a low-traffic tool's sessions can get lost in the noise of a higher-traffic one.
- Separate projects per tool: cleaner per-tool analysis, at the cost of a dashboard to check for every tool you ship.

## Putting it together

**Clarification (2026-11-20):** GA4, Search Console and Clarity each use different boundaries for grouping data.

- **GA4:** Choose a property according to whether the data belongs to a logical user base that should be analyzed together. Google generally recommends one web stream per property. Multiple streams in one property share reporting, but do not automatically stitch users across streams; cross-domain measurement requires the same tag ID from the same web stream on each domain ([account-structure guidance](https://support.google.com/analytics/answer/9679158?hl=en); [cross-domain setup](https://support.google.com/analytics/answer/10071811?hl=en)).
- **Search Console:** A Domain property includes subdomains, protocols and paths but requires DNS verification. A URL-prefix property covers only its exact prefix, so `https://saramjh.github.io/` includes HTTPS project paths on this host ([property types](https://support.google.com/webmasters/answer/34592?hl=en); [verification methods](https://support.google.com/webmasters/answer/9008080?hl=en)).
- **Clarity:** A project can collect data from multiple sites when its tracking code is installed on each. Microsoft recommends separate projects for different domains. For paths under this same host, the choice is whether to group their recordings and heatmaps together ([Clarity FAQ](https://learn.microsoft.com/en-us/clarity/faq/); [setup guide](https://learn.microsoft.com/en-us/clarity/setup-and-installation/clarity-setup)).

Part 3 records which settings I changed and which I left alone.

→ [Continue to Part 3: The Decision](/gh-pages-analytics-notes-3-decision-en/)

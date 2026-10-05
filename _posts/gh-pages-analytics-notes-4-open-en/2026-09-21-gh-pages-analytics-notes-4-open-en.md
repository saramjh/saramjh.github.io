---
title: "Running Several GitHub Pages Sites Solo: An Analytics Dilemma (Part 4 — Current State & Open Questions)"
description: "The merge happened too recently to claim it 'worked.' Closing the series with the current data snapshot and the questions I still don't have answers to."
date: 2026-09-18
tags: ["GA4", "Google Analytics", "Search Console", "Microsoft Clarity", "GitHub Pages", "SEO"]
permalink: /gh-pages-analytics-notes-4-open-en/
layout: default
lang: en
alternate_lang: ko
alternate_url: /gh-pages-analytics-notes-4-open-kr/
---

<p style="background: rgba(0, 120, 212, 0.08); border-left: 4px solid #0078d4; padding: 10px 14px; margin-bottom: 16px; border-radius: 4px; font-size: 0.95rem;">
  🌐 <strong>한국어 버전:</strong> Read the Korean version at <a href="/gh-pages-analytics-notes-4-open-kr/"><strong>애널리틱스 고민 노트 (한국어)</strong></a>.
</p>

<p style="background: rgba(120, 90, 0, 0.08); border-left: 4px solid #b8860b; padding: 10px 14px; margin-bottom: 24px; border-radius: 4px; font-size: 0.9rem;">
  📚 <strong>Series</strong> — <a href="/gh-pages-analytics-notes-1-problem-en/">Part 1: The Problem</a> · <a href="/gh-pages-analytics-notes-2-reasoning-en/">Part 2: Reasoning</a> · <a href="/gh-pages-analytics-notes-3-decision-en/">Part 3: The Decision</a> · Part 4 <strong>Current State &amp; Open Questions</strong> (this post)
</p>

## To be clear upfront: this is not a validation

The merge is too recent, and there's no long enough before/after window or control group to compare against. So this post is not proof that "consolidating GA4 improved traffic or rankings." It's a snapshot of what's visible right now, plus a set of criteria I can use to check my own judgment later.

## The current snapshot

Splitting sessions by `hostName` in the merged GA4 property over the trailing 90 days looks roughly like this:

| Host | Sessions | Active users |
| :--- | :--- | :--- |
| saramjh.github.io | 672 | 651 |
| 127.0.0.1 (local testing) | 16 | 16 |
| localhost (local testing) | 1 | 1 |

This confirms exactly one thing: **the hostname filter works as intended.** Local development traffic is cleanly separated from real user traffic, so the "narrow down only when needed" design from [Part 2](/gh-pages-analytics-notes-2-reasoning-en/) at least holds up functionally. These numbers don't represent the merge's "effect" — there's no comparable pre-merge period measured the same way to compare them against.

## What I still don't know

- **Whether this actually affected SEO.** As noted in [Part 2](/gh-pages-analytics-notes-2-reasoning-en/), shared root-domain trust has never had a proven causal chain behind it. I'd need to watch Search Console's indexing and impression trends over months before I could say anything — and right now there's no basis to judge.
- **When to consolidate Clarity.** I deferred it because traffic is low right now, but I haven't set a concrete threshold for when to revisit that call.
- **Whether this structure holds up if the number of tools grows a lot more.** If data streams go from around ten to several dozen, whether managing them all under one property is still the right call is worth re-examining — along with the free-tier data thresholds at that point.
- **Whether this problem is even specific to "solo developer, many small projects, one root domain."** A team running multiple products is a different situation, so I'd be cautious about generalizing this series' conclusions beyond that specific setup.

## For anyone in the same situation

If you're running several GitHub Pages project pages without custom domains, at minimum it's worth checking these three things on your own account:

1. Whether your custom-domain-free projects really do all sit under the same root domain (`https://<account>.github.io/<repo>/`)
2. Whether you're actually distinguishing "property" from "data stream" in GA4, or repeating my old habit of spinning up a new property every time
3. Whether Search Console is verified as a domain property, or per-project via URL-prefix

This series doesn't hand you a definitive answer, but I think those three questions are worth checking for yourself regardless. If traffic grows or I learn something that changes the picture, I'll keep adding to this record.

← [Back to Part 1](/gh-pages-analytics-notes-1-problem-en/)

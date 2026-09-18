---
title: "Running Several GitHub Pages Sites Solo: An Analytics Dilemma (Part 3 — The Decision)"
description: "In September 2026 I merged separate per-project GA4 properties into one. What actually changed, why I stopped short of changing more, and what I'm still not confident about."
date: 2026-09-18
tags: GA4, Google Analytics, Search Console, Microsoft Clarity, GitHub Pages, SEO
permalink: /gh-pages-analytics-notes-3-decision-en/
layout: default
lang: en
alternate_lang: ko
alternate_url: /gh-pages-analytics-notes-3-decision-kr/
---

<p style="background: rgba(0, 120, 212, 0.08); border-left: 4px solid #0078d4; padding: 10px 14px; margin-bottom: 16px; border-radius: 4px; font-size: 0.95rem;">
  🌐 <strong>한국어 버전:</strong> Read the Korean version at <a href="/gh-pages-analytics-notes-3-decision-kr/"><strong>애널리틱스 고민 노트 (한국어)</strong></a>.
</p>

<p style="background: rgba(120, 90, 0, 0.08); border-left: 4px solid #b8860b; padding: 10px 14px; margin-bottom: 24px; border-radius: 4px; font-size: 0.9rem;">
  📚 <strong>Series</strong> — <a href="/gh-pages-analytics-notes-1-problem-en/">Part 1: The Problem</a> · <a href="/gh-pages-analytics-notes-2-reasoning-en/">Part 2: Reasoning</a> · Part 3 <strong>The Decision</strong> (this post) · <a href="/gh-pages-analytics-notes-4-open-en/">Part 4: Current State &amp; Open Questions</a>
</p>

## What actually changed

In mid-September 2026, I merged the GA4 properties that had been split one-per-tool into a single property representing the `saramjh.github.io` domain. Concretely:

- I retired the separate GA4 properties each tool had been using and consolidated everything into the property the blog was already using (measurement ID `G-4DYFKSNFBG`).
- Each tool was re-registered as its own web data stream under that one property — richChecker, scratchLottery, SquircleSimulator, pomodorotimerKR/EN, resizeIMG, space_atlas_student, and the rest listed in [Part 1](/gh-pages-analytics-notes-1-problem-en/).
- When I need per-tool traffic in reports, I filter by `hostName`. While preparing this series I actually queried GA4's Data API by the `hostName` dimension and confirmed `saramjh.github.io` (the blog and most project pages) is cleanly separated from local test traffic (`localhost`, `127.0.0.1`).

Search Console, which had been managed per-project sitemap, is now unified under a single domain property (verifying all of `saramjh.github.io`). Sitemaps themselves are still submitted per tool, each with its own path.

## What I left alone

I didn't touch Microsoft Clarity this round. As covered in [Part 2](/gh-pages-analytics-notes-2-reasoning-en/), this was more an operating decision than a structural one, and I judged that traffic across tools isn't yet high enough for one tool's sessions to drown out another's inside a shared project. Unlike the GA4/Search Console changes, this isn't "I'm confident this is structurally correct" — it's closer to "this doesn't feel urgent yet, so I deferred it." It's something I'll need to revisit if traffic grows.

## Why I went along with the reasoning

Honestly, the "GA4 property vs. data stream" part of [Part 2](/gh-pages-analytics-notes-2-reasoning-en/)'s reasoning was easy to accept because it's clearly confirmed in official documentation. The "shared root domain shares trust" part, I'm still not fully sold on. But the merge decision itself didn't hinge on that uncertain premise being true — the downside either way looked small.

- What merging GA4 properties costs: a little extra friction — one more filter step — whenever I want a fully isolated per-tool dashboard.
- What merging gains: less management overhead scaling with the number of properties, and the ability to see a blog-post-to-tool-usage flow within one property.

So the bigger factor in the actual decision wasn't the unproven "this probably helps SEO" expectation — it was the much more solid "this is easier to manage and doesn't cost much."

## Practical pitfalls during the migration

- **Merging a property doesn't bring historical data with it.** Whatever history had accumulated in each old per-tool property stays there; the new consolidated property only starts accumulating data from the point of the merge. If you need the old history, leave the old properties in place read-only rather than deleting them.
- **It's easy to forget to swap the measurement ID in code.** Since each tool lives in its own repo, I had to repeat the ID swap once per repo, and missing even one meant that tool kept silently sending data to the old property.
- **Free-tier data thresholds reset around the consolidated property.** This hasn't been an issue at my current traffic level, but it's something to revisit if the tool count keeps growing.

Next: what the data actually looks like under this new structure, and the questions I still don't have answers to.

→ [Continue to Part 4: Current State & Open Questions](/gh-pages-analytics-notes-4-open-en/)

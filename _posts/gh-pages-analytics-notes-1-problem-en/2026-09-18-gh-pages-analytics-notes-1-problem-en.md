---
title: "Running Several GitHub Pages Sites Solo: An Analytics Dilemma (Part 1 — The Problem)"
description: "Run several GitHub Pages project pages without custom domains, and every one of them is already sharing the same root domain. Should GA4 properties stay split or merge? Where should Search Console and Clarity live? Notes from a solo developer working through the question."
date: 2026-09-18
tags: ["GA4", "Google Analytics", "Search Console", "Microsoft Clarity", "GitHub Pages", "SEO"]
permalink: /gh-pages-analytics-notes-1-problem-en/
layout: default
lang: en
alternate_lang: ko
alternate_url: /gh-pages-analytics-notes-1-problem-kr/
---

<p style="background: rgba(0, 120, 212, 0.08); border-left: 4px solid #0078d4; padding: 10px 14px; margin-bottom: 16px; border-radius: 4px; font-size: 0.95rem;">
  🌐 <strong>한국어 버전:</strong> Read the Korean version at <a href="/gh-pages-analytics-notes-1-problem-kr/"><strong>애널리틱스 고민 노트 (한국어)</strong></a>.
</p>

<p style="background: rgba(120, 90, 0, 0.08); border-left: 4px solid #b8860b; padding: 10px 14px; margin-bottom: 24px; border-radius: 4px; font-size: 0.9rem;">
  📚 <strong>Series</strong> — Part 1 <strong>The Problem</strong> (this post) · <a href="/gh-pages-analytics-notes-2-reasoning-en/">Part 2: Reasoning</a> · <a href="/gh-pages-analytics-notes-3-decision-en/">Part 3: The Decision</a> · <a href="/gh-pages-analytics-notes-4-open-en/">Part 4: Current State &amp; Open Questions</a>
</p>

## This is a record of the deliberation, not a proven playbook

Up front: this series is not a "we did X and traffic went up" case study. I don't actually know whether what I ended up doing helps. I discussed the GA4/SEO structure with an AI, the reasoning it laid out seemed sound, and I applied it — what I want to record here is the deliberation itself and the uncertainty that's still left over. I suspect other solo developers running multiple GitHub Pages projects hit the exact same fork in the road.

## The setup: many repos, one domain

I deploy everything from a single GitHub account, `github.com/saramjh`. Alongside this blog (`saramjh.github.io`), I've shipped a handful of small tools as GitHub Pages project pages whenever I needed one, for example:

- [scratchLottery](https://saramjh.github.io/scratchLottery) — a scratch-lottery simulator
- [richChecker](https://saramjh.github.io/richChecker/) / [richChecker-us](https://saramjh.github.io/richChecker-us/) — a billionaire face-match tool
- [SquircleSimulator](https://saramjh.github.io/SquircleSimulator) — a squircle shape simulator
- [pomodorotimerKR](https://saramjh.github.io/pomodorotimerKR/) / [pomodorotimerEN](https://saramjh.github.io/pomodorotimerEN/) — a pomodoro timer
- [resizeIMG](https://saramjh.github.io/resizeIMG) — an image resizer
- [space_atlas_student](https://saramjh.github.io/space_atlas_student/) — a 3D astronomy learning tool

Each one is a separate repository, shares no code with the others, and was built for a different reason. But because none of them has a custom domain attached, GitHub Pages' default behavior puts every single one at `saramjh.github.io/<repo-name>/` — **already under one root domain**. I didn't design that; it's just what happens when you don't bother attaching a custom domain.

Once that clicked, a bunch of settings I'd been repeating on autopilot every time I shipped a new tool suddenly looked worth questioning.

## Three concrete forks in the road

### 1. GA4 — a new property for every project?

Every time I shipped a new tool, I'd reflexively spin up a new GA4 property and paste in a new measurement ID. With close to ten tools, the property list in my GA4 account grew just as long, and answering something like "how much did that blog post actually drive usage of the tool" meant juggling tabs across properties and lining up date ranges by hand. A recent example: to see how traffic from my [Space Atlas blog post](/space-atlas-student-en/) fed into the tool itself, I had to open the blog's property and the tool's property side by side.

### 2. Search Console — register per project too?

Same pattern with Search Console — a new sitemap registered for every new tool. (The commit adding a `space_atlas_student` sitemap to `robots.txt` is one trace of that habit.) But if everything already sits on the same root domain, is splitting management by project actually the right unit here?

### 3. Microsoft Clarity — a new project per tool, or one shared project?

Microsoft Clarity, installed for session replay and heatmaps, raised the identical question. The blog already has one Clarity project installed. It wasn't clear whether each new tool needed its own Clarity project, or whether — since it's the same root domain — the existing project could simply be reused.

## Why this doesn't have an obvious answer

Most GA4 and SEO guides I found assume one of two setups:

- "One large product split into sections" (e.g., a storefront with product pages, a blog, and support)
- "Genuinely separate businesses on genuinely separate domains"

My situation sat in between: **one person, one root domain, a growing pile of small tools with no shared audience or purpose, that happen to share URL space.** I couldn't find guidance written for that middle case, and that gap is why I'm writing this series.

Next up: the reasoning I worked through with an AI — how GA4 properties and data streams actually relate to each other, how Search Console verification works at the domain level, and what root-domain trust signals do and don't share.

→ [Continue to Part 2: Reasoning](/gh-pages-analytics-notes-2-reasoning-en/)

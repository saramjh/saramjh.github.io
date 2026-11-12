---
layout: project
portfolio_ui: true
title: "Spoonie | Project case study"
description: "A cooking-oriented web product exploring useful recipe discovery, personal recipe records, and community participation."
slug: spoonie
order: 4
name: Spoonie
subtitle: A social cooking and recipe project
field: Consumer product / content design
summary: A cooking-oriented web product exploring useful recipe discovery, personal recipe records, and community participation.
image: /assets/images/portfolio/spoonie-desktop.jpg
image_alt: Screenshot of the Spoonie cooking and recipes homepage
site_url: https://spoonie.kr/
writing_url: /spoonie-privacy-cache-transition-en/
status: Product in development
stack:
  - Next.js 16
  - React 19
  - TypeScript
  - Supabase
  - Vitest
---
## The problem

A community is difficult to build before users can consistently find something worth returning for. For a cooking product, useful recipes must precede some social features.

## What I am exploring

Spoonie combines recipe discovery, recipe books, and community-oriented cooking records. Recent product decisions have focused on recipe usefulness and responsible curation rather than growth claims.

## An outside directory listing

On October 25, 2026, [Web Apps Directory catalogued Spoonie](https://webapps.directory/directory/spooniespoonie). The entry links to the live Korean-language service and describes recipe search, serving adjustments and cooking records. I built those features around the Recipe and Recipeed workflow so a visitor can find a dish and keep a record of cooking it. Referral traffic and repeat use from the directory have not been measured.

The development case and original source are available in [English](/spoonie-webapps-directory-en/) and [Korean](/spoonie-webapps-directory-ko/).

## Engineering and editorial decisions

- Keep source credit for curated recipes visible.
- Produce original explanatory text rather than copying creators' directions.
- Reuse imagery only with appropriate permissions.
- Separate product hypotheses from validated user behaviour.

## Keeping private recipes out of other accounts

A recipe can become private while another viewer still has a cached copy of its public details. In [PR #38](https://github.com/saramjh/spoonie/pull/38), I updated those caches when visibility changes. The author's private recipe book keeps the post while public and other-viewer caches drop it. Save responses that arrive after an account switch stay tied to the account that started the request.

The earlier [PR #37](https://github.com/saramjh/spoonie/pull/37) separated viewer-specific likes and bookmarks. The cache changes in PR #38 cover a different point in the flow: privacy changes and delayed account responses. Both fixes are merged, and the production recipe route was checked against PR #38's deployed browser assets. Authenticated cross-account use in production and audience retention have not been measured.

Read the implementation note in [English](/spoonie-privacy-cache-transition-en/) or [Korean](/spoonie-privacy-cache-transition-ko/). The [viewer-cache follow-up](/spoonie-viewer-cache-isolation-en/) has the earlier source and tests.

## Finding recipes beyond the first page

The earlier search returned up to twenty combined Recipe and Recipeed matches. In [PR #31](https://github.com/saramjh/spoonie/pull/31), I changed the two result types to request separate pages from the server. Each shows up to twenty items at a time and offers a way to request more when additional matches exist. The ordering preserves different authors’ recipes even when they share a title. The reference picker now uses a separate ten-item paged search.

The [public search page](https://spoonie.kr/search) serves the updated controls. This verifies the shipped interface, not a measured change in recipe discovery or reader retention. See the implementation notes in [English](/spoonie-search-discovery-en/) or [Korean](/spoonie-search-discovery-ko/).

## A public recipe with a real poll

I added a structured poll to a published Spoonie Recipe. The [public example](https://spoonie.kr/recipes/6eaa37a1-6c0f-4841-aadd-7a2d980fbdbf) returns the question, available choices and recorded totals as server-rendered data. [PR #19](https://github.com/saramjh/spoonie/pull/19) documents the initial curator Recipe implementation and its access controls.

I then extended the same data model and poll interface to optional member-authored Recipe and Recipeed posts in [PR #20](https://github.com/saramjh/spoonie/pull/20). The original repository documents **Next.js 16, React 19, TypeScript, Supabase and Vitest**. This is a verifiable implementation record; an authenticated member's complete production create-and-vote journey has not been independently tested here.

Read the developer's notes in [English](/spoonie-live-polls-en/) or [Korean](/spoonie-live-polls-ko/), with original code links and a diagram of the aggregate-only public response.

The earlier [author-header case study](/spoonie-author-header-consistency-en/) ([Korean](/spoonie-author-header-consistency-ko/)) covers a separate Recipe and Recipeed detail-page change.

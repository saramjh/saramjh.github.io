---
title: "KoreAves: Explore South Korean Bird Records with Sources and Regional Evidence"
description: "A free bird evidence atlas for South Korea's 597 species and 20 subspecies. Explore qualifying source-linked occurrence evidence across 17 regions without confusing records with population or biological range."
date: 2026-10-12
modified: 2026-11-16
last_modified_at: 2026-11-16
tags: ["KoreAves", "South Korea birds", "Korean bird checklist", "GBIF", "birding", "biodiversity data", "GIS", "citizen science", "provenance"]
permalink: /koreaves-bird-evidence-atlas-en/
layout: default
lang: en
alternate_lang: ko
alternate_url: /koreaves-bird-evidence-atlas/
published: true
---

Looking up a South Korean bird is one thing. Finding out **which public sources support a regional record**, and what those records can actually tell you, is another. Taxonomy references, occurrence datasets and mapping tools answer different questions.

I built [KoreAves](https://koreaves.com/?utm_source=devtestudinidae_blog&utm_medium=owned_editorial&utm_campaign=koreaves_evidence_atlas_20261012&utm_content=en_intro), a free, non-commercial evidence reference for South Korean birds, to connect those questions without pretending that a record map is a complete biological distribution map.

**한국어:** [한국 조류 지도와 기록 출처를 함께 확인하는 법](/koreaves-bird-evidence-atlas/)

## 617 taxa, not 617 species

The canonical starting point is South Korea's 2025 national bird reference: **597 species plus 20 subspecies, or 617 taxa in all**. A subspecies is not counted as an additional species. KoreAves keeps that distinction explicit and does not silently equate a name match with evidence of a taxonomic synonym.

The atlas offers taxon pages, comparisons, regional views, source documentation and provenance links. It primarily uses English with Korean names and navigation available alongside them.

## Explore documented evidence across 17 regions

The [interactive GIS explorer](https://koreaves.com/gis/?utm_source=devtestudinidae_blog&utm_medium=owned_editorial&utm_campaign=koreaves_evidence_atlas_20261012&utm_content=en_gis) lets you select a bird taxon and examine where qualifying source evidence is documented within South Korea's 17 first-level administrative divisions.

The map carries explicit limitations:

- **A shaded region is not a biological range polygon.** It indicates eligible documented evidence within that administrative unit.
- **No eligible record is not evidence of biological absence.** The analyzed and filtered public sources may simply contain no qualifying observation.
- **Record counts are not bird counts or population estimates.** They can be affected by observation effort, reporting and source coverage.
- **Regional overlap is not co-occurrence.** Two taxa documented within one large division may have been recorded at unrelated places and times.

These distinctions matter when maps are read by visitors, educators, birders and researchers. The interface tries to keep those caveats close to the claims rather than hiding them exclusively in a methodology document.

## November 16 update: Region searches now show only matching birds

In the [Seoul regional bird catalog](https://koreaves.com/regions/seoul/), a search could reduce the result count while leaving unrelated bird cards visible. The filter was marking nonmatches with `hidden`, but the cards' `display: grid` rule overrode the browser's default hiding behavior. I corrected that CSS rule and tightened the regional summary and card spacing on small screens.

I checked the published page in Chrome at 390px and 1440px. Searching for `Accipiter gularis` now leaves **one matching bird** out of Seoul's 280 listed taxa; clearing the search restores all 280. The same visibility rule also covers the [full species catalog](https://koreaves.com/species/browse/). This was a repair to the way filtered results appear, not a change to the underlying source records or eligibility rules. Any change in actual reader use has not been measured.

## Trace the sources rather than accepting a map on trust

The public [dataset page](https://koreaves.com/dataset/) describes **1,970,745 normalized source rows**, a versioned evidence projection, and the different roles played by GBIF occurrence evidence, Korea's EcoBank survey material, a canonical national checklist and administrative boundary geometry.

The atlas does not treat every source as supporting every possible biological claim. Identity, eligible occurrence evidence, spatial assignment and publication rights remain separate layers. A record can be retained for provenance without being eligible to support a particular displayed regional claim.

The [methodology](https://koreaves.com/methodology/) outlines the derivation and evidence boundaries. The [source register](https://koreaves.com/sources/) describes the providers and permissions without claiming that any institution endorses KoreAves.

## A short walkthrough

1. Open [KoreAves](https://koreaves.com/?utm_source=devtestudinidae_blog&utm_medium=owned_editorial&utm_campaign=koreaves_evidence_atlas_20261012&utm_content=en_try) and search for a bird in Korean, English or by scientific name.
2. Use the species page to orient yourself and inspect the evidence summary.
3. Open GIS to select a region and review the supporting source types.
4. Use Compare for overlapping **regional evidence**, not an inference that two birds share a habitat or were observed together.
5. Read Dataset and Methodology when you need to cite or question the versioned analysis.

KoreAves is **not** an observation-submission platform, an official government distribution map, or a bird abundance estimator. It is an independent, free reference designed to make existing bird evidence easier to inspect critically.

I am looking for practical corrections to taxon identities, regional evidence, translations and provenance attribution. If you find something that looks wrong, the site's [written contact and corrections route](https://koreaves.com/contact/) is the best way to report the precise page and supporting source.

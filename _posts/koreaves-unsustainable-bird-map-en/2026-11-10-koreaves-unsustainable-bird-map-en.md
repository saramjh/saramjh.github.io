---
title: "My KoreAves bird-map essay was published in Unsustainable Magazine"
description: "Unsustainable Magazine published my article about why a bird observation map cannot count a population. It grew from the evidence and provenance decisions behind KoreAves."
date: 2026-11-10
tags: ["KoreAves", "Unsustainable Magazine", "Biodiversity", "Data Provenance", "GIS", "Developer Writing"]
permalink: /koreaves-unsustainable-bird-map-en/
layout: default
lang: en
alternate_lang: ko
alternate_url: /koreaves-unsustainable-bird-map-ko/
image: /assets/images/portfolio/koreaves-gis.jpg
image_width: 1440
image_height: 900
published: true
seo:
  title: "KoreAves developer's bird-map article in Unsustainable Magazine"
  description: "My November 6, 2026 Unsustainable Magazine article draws on KoreAves development to explain what source-backed bird maps can and cannot tell readers."
---

> 한국어판: [KoreAves 개발자의 조류 지도 해석 기고, Unsustainable Magazine에 게재](/koreaves-unsustainable-bird-map-ko/)

On November 6, 2026, **[Unsustainable Magazine published my article, *Why a Bird Map Is Not a Bird Count*](https://www.unsustainablemagazine.com/why-a-bird-map-is-not-a-bird-count/)**. Its original page credits Jihun Oh as the author, notes **“Edited and reviewed by Brett Stadelmann”**, and identifies KoreAves as the project behind the work. That is an editorial credit for a published contribution, not evidence of scientific peer review.

The article came from a problem I kept meeting while building [KoreAves](https://koreaves.com/), a public, source-linked reference for South Korean birds. A map can make a collection of records look complete. Without context about when, where and how those records were collected, readers can mistake it for a direct measure of the birds living in an area.

<figure>
  <img src="/assets/images/portfolio/koreaves-gis.jpg" alt="Original KoreAves interface showing a regional bird-evidence map with a source-linked exploration layout." width="1440" height="900" loading="lazy" style="width:100%;height:auto;">
  <figcaption>The project's own GIS interface. This is a previously published first-party screenshot, not an image from Unsustainable Magazine or a count of living birds.</figcaption>
</figure>

## A convincing map still needs an explanation

Suppose observations of one species appear in several regions. The coloured regions describe the available records after a particular set of checks. They do not tell us how many individuals live there. People may have searched more often in one place, reported at different times or left large areas unrecorded.

When I designed KoreAves's regional explorer, this became a question about the data model and the interface. The project has to distinguish the bird's taxonomic identity from an individual source record, and a source record from evidence eligible to support a dated regional summary. An observation can remain useful for provenance even when it cannot support the specific map claim being shown.

I wrote the article around that distinction because it is easy to lose once the evidence is rendered as a familiar map.

## The engineering work behind the byline

KoreAves connects names, taxon references and source-backed observations so a reader can move from a regional view to the supporting material. I built an interface that exposes those relationships, with accompanying dataset and methodology pages explaining what the records represent.

This work required decisions about source provenance, dates, spatial assignment and how to describe missing evidence. A region without an eligible observation should not automatically be labelled a place where the species is absent. A high count of reported records should not automatically become an abundance estimate.

The published essay turned those engineering decisions into an explanation for readers interested in ecology and biodiversity, even if they have never opened the application's source code. It is an example of communicating the limits of a technical system using the same evidence on which the system relies.

## What publication makes possible

The [original Unsustainable Magazine article](https://www.unsustainablemagazine.com/why-a-bird-map-is-not-a-bird-count/) is a public, author-credited work sample on an environmental publication outside the KoreAves website. A potential research collaborator, educator or data reviewer can read the reasoning and then check the corresponding [KoreAves GIS explorer](https://koreaves.com/gis/) and [methodology](https://koreaves.com/methodology/). That gives them something concrete to evaluate: where the map's claims stop and where a source can be checked.

It does not establish peer-reviewed research, verified readership or conservation impact. The article is a published contribution, and the maps remain a source-qualified reference that needs to be read with its stated limitations.

Two earlier contributions to [10,000 Birds](/koreaves-published-contributions-en/) addressed image permission and the experience of presenting a place to birders. This essay examines the inference a reader may draw from an observation map. The broader [KoreAves development case](/koreaves-bird-evidence-atlas-en/) explains the data and interface choices in more detail.

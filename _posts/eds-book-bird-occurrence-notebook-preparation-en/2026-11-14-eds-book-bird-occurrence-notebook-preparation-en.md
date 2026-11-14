---
title: "EDS Book: A Bird-Map Notebook Idea Reached Preparation"
date: 2026-11-14
tags: ["EDS Book", "environmental data science", "biodiversity", "GBIF", "reproducible notebooks", "Python", "data provenance"]
permalink: /eds-book-bird-occurrence-notebook-preparation-en/
layout: default
lang: en
alternate_lang: ko
alternate_url: /eds-book-bird-occurrence-notebook-preparation-ko/
description: "An EDS Book editor confirmed the teaching idea is in scope. I built an author-owned bird-records notebook and tested its offline Binder path; a citable GBIF selection is still needed."
excerpt: "The editor asked to see a working version of a bird-observation map lesson. Here is the notebook I built, what the test records show, and why it is not yet ready for editorial review."
seo:
  title: "EDS Book Bird-Map Notebook: From Idea to Working Draft"
  description: "An EDS Book editor confirmed this bird-records teaching idea is in scope. How I built a Binder-tested draft, checked spatial-grid interpretations, and identified the missing GBIF download DOI."
  keywords:
    - EDS Book notebook idea
    - bird occurrence map
    - biodiversity observation data
    - GBIF data provenance
    - presence-only records
    - spatial aggregation
    - reproducible Python notebook
    - Binder notebook
image: /assets/img/ogp.png
image_width: 717
image_height: 341
---

# A bird-map notebook idea reached EDS Book's preparation stage

**An EDS Book editor confirmed that my proposed lesson fits the publication's subject area and asked me to share a working notebook when it is ready for feasibility review.** I built a public, author-owned Python draft and ran its default offline teaching path in Binder. The draft is still in preparation: I have not submitted it for editorial review, and its GBIF occurrence selection does not yet have the frozen download citation it needs.

<p style="border-left: 3px solid #5e9dde; padding: 10px 14px; margin: 14px 0 24px;">
  <strong>한국어:</strong> <a href="/eds-book-bird-occurrence-notebook-preparation-ko/">EDS Book에서 조류 관측 지도 교육 노트북을 준비한 과정</a>
</p>

The interesting part of the project is the data question. When a map contains bird sightings in one area and none in another, it is tempting to treat the empty region as a place where that species is absent. Opportunistic occurrence records cannot support that conclusion on their own. The missing observations could reflect observer access, timing, reporting practices, or data coverage.

I wanted students to see that distinction themselves instead of memorizing a warning about data quality.

## The external editorial milestone

I posted the [notebook idea in EDS Book's public discussion](https://github.com/eds-book/notebooks-ideas/issues/14). The editor questioned geographic scope, the choice of visualization tools, what grid resolution means, and how the proposed reflection exercise would work.

After that discussion, the editor said the idea was within EDS Book's scope and directed me to its Preparation process. In a later follow-up, the editor asked me to notify the thread when a first working version is ready for an Editor-in-Chief feasibility check.

That is an actual exchange with an external editor. It is not a peer-review acceptance, a published EDS Book chapter, or evidence that students have used the notebook. EDS Book's [author guidelines](https://edsbook.org/guidelines-authors#preparation) place reproducibility and an editor check before the review and publication stages.

## What I implemented

The [public preparation repository](https://github.com/saramjh/bird-records-not-absence-notebook) and its [author-owned draft PR #1](https://github.com/saramjh/bird-records-not-absence-notebook/pull/1) contain an original Python lesson using the EDS Book template. It separates the precision of individual observations from the grid size chosen by an analyst.

The pilot lets a reader examine the same screened records at two aggregation scales. For illustration, I used 10 km and 50 km grid cells in an appropriate projected coordinate system. A blank cell in either grid means only that no *qualifying record* was plotted there under the selected filtering rules.

### What the bounded trial actually showed

My original preparation notes record a first-page check of 100 GBIF human-observation records from a 2024 query, not a random sample of all South Korean observations.

| Original author-side check | Observed in that limited page |
|---|---:|
| Records inspected | 100 |
| Passed an illustrative reported-coordinate-uncertainty threshold of 1,000 m or less | 50 |
| Missing that uncertainty field | 39 |
| Exceeded that threshold | 11 |
| Occupied cells after screening at 10 km | 12 |
| Occupied cells after screening at 50 km | 8 |

These are **test-input and plotting results**, not a census, estimated abundance, geographic range, or year-on-year change. The 1,000 m threshold was chosen to teach a screening decision; it is not presented as a universal scientific standard. The record set was not designed to represent the country's bird population.

The visible change from 12 occupied cells to eight comes from choosing different aggregation units for the *same* screened records. No new observations were added. That is the precise lesson the exercise can demonstrate.

### Working notebook versus reproducible scientific input

My [draft PR's author-side test record](https://github.com/saramjh/bird-records-not-absence-notebook/pull/1) reports that the default offline path executed all four notebook code cells on Binder at a specified commit. I inspected the rendered figure and corrected overlapping and low-contrast map labels. The draft also documents separate historical offline tests. Those are implementation checks performed by the author, not editorial or independent scientific review.

The remaining data dependency matters more than another clean CI run. The current teaching aggregate came from a bounded, mutable API first page. The notebook needs a properly specified, stable occurrence selection and a citable GBIF occurrence-download record, together with the contributing dataset information and licensing checks. An individual dataset DOI does not automatically cite a particular selection of occurrence records.

[GBIF's citation guidance](https://www.gbif.org/citation-guidelines) explains the distinction between dataset citations, occurrence downloads, and derived datasets. Its [API download documentation](https://techdocs.gbif.org/en/data-use/api-downloads) also states that issuing a new occurrence download requires a registered account and authenticated request. I have not represented that download as completed.

## A worksheet that does not need a grading system

I adapted the editor's suggestion into a short Markdown exercise inside the notebook. Students can write down three things:

| Prompt | Example answer |
|---|---|
| Supported claim | Qualifying observation records appear in these plotted cells for the specified data selection. |
| Evidence | Record provenance, dates, filtering decisions, coordinate uncertainty and grid definition. |
| Unsupported claim | A species must be absent from every blank cell; the map does not show sampling coverage. |

The question can be answered from the notebook output without introducing an unsupported automated scoring feature. If someone wants to test biological absence, they would first need a study design that records sampling effort and detection limits.

## What this shows about the development work

The useful contribution here is an instructional software workflow that keeps the meaning of the source data attached to the visualization. It combines source-aware filtering, spatial computation, execution testing and an explanation of the boundaries of the result.

I developed [KoreAves, a regional bird-evidence atlas](/koreaves-bird-evidence-atlas-en/), and that experience motivated the example. KoreAves is not the raw data provider for this notebook, and a reference atlas is not a substitute for primary occurrence records.

The next substantive step is to replace the mutable trial selection with a versioned, rights-checked and citable primary-source download, then rerun the lesson and its Binder checks. Only after that work should I notify the EDS Book editor that the draft is ready for feasibility review.

**Primary evidence:** [EDS Book idea and editor discussion](https://github.com/eds-book/notebooks-ideas/issues/14) · [Author-owned preparation PR](https://github.com/saramjh/bird-records-not-absence-notebook/pull/1) · [EDS Book guide](https://edsbook.org/guidelines-authors) · [GBIF data citation guidance](https://www.gbif.org/citation-guidelines).

*Status checked November 14, 2026. This is an author-side preparation case, not a publication or endorsement.*

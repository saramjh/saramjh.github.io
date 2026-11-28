---
layout: project
portfolio_ui: true
last_modified_at: 2026-11-28
title: "KoreAves | Project case study"
description: "An independent source-linked reference connecting taxon identities, regional occurrence evidence, and media provenance without equating records with populations."
slug: koreaves
order: 1
name: KoreAves
subtitle: Evidence atlas for South Korean birds
field: Biodiversity / data provenance
summary: An independent source-linked reference connecting taxon identities, regional occurrence evidence, and media provenance without equating records with populations.
image: /assets/images/portfolio/koreaves-desktop.jpg
image_alt: Screenshot of the KoreAves bird evidence atlas
site_url: https://koreaves.com/
writing_url: /koreaves-oneearth-author-achievement-en/
status: Publicly available
stack:
  - JavaScript
  - HTML / CSS
  - GIS visualisation
  - Data normalisation
  - GBIF occurrence data
---
## The problem

A bird name, an occurrence record, a regional map, and a publishable photograph are four different kinds of evidence. Combining them without preserving their boundaries creates misleading interpretations.

## What I built

KoreAves connects bird profiles, regional evidence views, source documentation, and permission-aware media. Its interface explicitly distinguishes **documented occurrence evidence** from population estimates or biological range polygons.

## Engineering decisions

- Maintain the distinction between 597 species and 20 subspecies in the 617-taxon reference.
- Keep source provenance accessible rather than burying it in a single methodology page.
- Treat image reuse rights and taxon identity as separate checks.
- Explain source and sampling limitations directly beside maps.

## Recent production work

On November 16, 2026, I fixed a CSS rule that kept non-matching region cards visible after a search and adjusted the catalogue's mobile spacing. The production release changed 19 HTML pages and a content-hashed stylesheet; the other 3,874 files in the previous 3,894-file deployment manifest retained their hashes. Live browser checks covered 32 cases across five viewport widths and all 17 regional detail pages. Read the [Korean case study](/koreaves-region-search-mobile-hotfix-ko/) or the [English case study](/koreaves-region-search-mobile-hotfix-en/).

The November 26 release added English display labels for all 617 checklist taxa. Twelve subspecies use a composite of the parent species name and subspecies epithet. The [English case study](/koreaves-english-display-labels-en/) and [Korean edition](/koreaves-english-display-labels-ko/) explain how the display layer preserves taxonomic rank and source context.

On November 28, I checked all 17 regional catalogue pages. The 5,464 region-taxon entries matched the regional counts, with a taxon identity, source note, media-credit slot and distinct detail link for each entry. See the [regional counts and audit method in English](/koreaves-regional-catalogue-enumeration-en/) or [Korean](/koreaves-regional-catalogue-enumeration-ko/).

## Published explanations beyond the project

On November 23, 2026, the [British Ornithologists’ Union (BOU) published *When Records Become Maps* under my byline](https://bou.org.uk/blog-oh-when-records-become-maps/). The article links to KoreAves, its methodology and source records, and explains why a recorded occurrence should not be read as a population estimate. Read the [English case note](/koreaves-bou-when-records-become-maps-en/) or the [Korean edition](/koreaves-bou-when-records-become-maps-ko/). This is an author-credited BOU blog contribution, not peer-reviewed research, a formal partnership, or evidence of measured adoption.

[One Earth published my KoreAves article on October 28, 2026](https://www.oneearth.org/koreaves/). It describes the evidence-linked bird atlas for readers encountering the project outside its own site. In [English](/koreaves-oneearth-author-achievement-en/) and [Korean](/koreaves-oneearth-author-achievement-ko/), I explain how its taxonomy, source records and regional views fit together.

On November 6, [Unsustainable Magazine published my essay about the limits of bird observation maps](https://www.unsustainablemagazine.com/why-a-bird-map-is-not-a-bird-count/). It builds on the same mapping decisions: a recorded observation cannot on its own establish a region's bird population. The [English article note](/koreaves-unsustainable-bird-map-en/) and [Korean edition](/koreaves-unsustainable-bird-map-ko/) link the editorial credit to the source-backed GIS implementation.

Two earlier [10,000 Birds contributions](/koreaves-published-contributions-en/) covered photo permissions and a sourced profile of Suncheon Bay. The original [photo essay](https://www.10000birds.com/the-bird-photo-i-could-use-was-not-the-bird-photo-i-wanted.htm) and [Suncheon Bay article](https://www.10000birds.com/suncheon-bay-wetland-south-korea-profile-for-birders.htm) carry author credits. These publications document writing and technical explanation for outside audiences; readership and conservation outcomes have not been measured. The [Korean notes](/koreaves-published-contributions-ko/) collect both contributions.

## Where to explore

Read the [methodology](https://koreaves.com/methodology/) and [dataset notes](https://koreaves.com/dataset/), or try the [regional explorer](https://koreaves.com/gis/).

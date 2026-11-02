---
layout: project
portfolio_ui: true
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
writing_url: /koreaves-bird-evidence-atlas-en/
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

## Where to explore

Read the [methodology](https://koreaves.com/methodology/) and [dataset notes](https://koreaves.com/dataset/), or try the [regional explorer](https://koreaves.com/gis/).

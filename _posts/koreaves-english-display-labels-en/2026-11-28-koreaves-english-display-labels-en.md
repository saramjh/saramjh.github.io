---
title: "What an English display label means in a 617-taxon bird checklist"
description: "KoreAves now has an English display label for all 617 taxa in its adopted Korean checklist. See how species, subspecies and composite labels differ."
date: 2026-11-28
tags: ["KoreAves", "bird taxonomy", "English display labels", "South Korean birds", "data provenance"]
permalink: /koreaves-english-display-labels-en/
layout: default
lang: en
alternate_lang: ko
alternate_url: /koreaves-english-display-labels-ko/
published: true
seo:
  title: "English display labels for 617 KoreAves taxa"
  description: "The November 2026 KoreAves update added English display labels for 597 species and 20 subspecies. Here is what composite subspecies labels mean."
---

> 한국어판: [KoreAves의 617개 분류군에 영문 표시명을 제공하며](/koreaves-english-display-labels-ko/)

An English value beside every taxon can look like a list of separate common names. The taxonomic rank and the role of each label still matter. A taxon has an identity and a rank; a display label is the text readers see when they browse or search for it.

In the November 26, 2026 release, I added English display labels for all 617 taxa in KoreAves' adopted Korean checklist. This completes the English display layer while keeping canonical taxon identities and occurrence records unchanged.

## The checklist still contains 617 taxa

KoreAves follows the National Institute of Biological Resources' 2025 National List of Species of Korea, version 1.0:

- 597 bird species
- 20 bird subspecies
- 617 taxa in total

The 20 subspecies are counted separately from the 597 species. Keeping the rank visible matters when a reader compares names or follows a reference to its source.

## What changed in the November 26 release

The [release note](https://koreaves.com/updates/english-display-names/) records several parts of the work:

- 44 previously missing names were linked through reviewed same-rank reference connections.
- Four historical names and eight sourced subspecies names or labels were added.
- Twelve subspecies labels combine the parent species' English name with the subspecies epithet. The release describes these as display labels, not independent common names.

The update also changed photo presentation, full-row search selection, and tooltip behavior for mouse and touch input.

The release states that canonical taxon identities and occurrence records remain unchanged.

## A display label is not always a separate common name

The distinction is clearest for the twelve composite subspecies labels. Each combines the English name of the parent species with the subspecies epithet. The composite label gives the interface a readable string for the subspecies record. The release presents it as a display label, not as a separate common name.

Treating every displayed string as an independently accepted common name would say more than the data supports. The display field helps readers find the taxon. Its rank and source context remain part of the interpretation.

## What the public manifest confirms

The November 2026 public dataset is version `evidence-v1-3cf525699943`. I checked its 617 unique taxon records and found a non-empty `identity.english_name` value for every one.

That is a field-coverage check. It confirms that the display value is present across the adopted checklist. It does not prove that every label is used by every national authority or birding community, and it is not an independent linguistic review of all 617 names.

The checklist remains anchored to the 2025 v1.0 reference. The November update leaves the adopted taxa and occurrence records unchanged. The [dataset page](https://koreaves.com/dataset/) and [methodology](https://koreaves.com/methodology/) describe the evidence sources and their separate roles.

## Try the labels in context

The [species and subspecies browser](https://koreaves.com/species/browse/) lets readers search by Korean name, English display label or scientific name. The [Azure-winged Magpie profile](https://koreaves.com/species/cyanopica-cyanus/) shows its English label alongside its scientific and Korean names. Regional evidence appears separately from the name fields.

For the wider project and its source-linked regional records, see [KoreAves: Explore South Korean Bird Records with Sources and Regional Evidence](/koreaves-bird-evidence-atlas-en/). The earlier [BOU article on records and maps](/koreaves-bou-when-records-become-maps-en/) explains why a regional evidence map must not be read as a biological range map.

The release gives English readers a label for every taxon in the adopted checklist. Read each label alongside its taxonomic rank and source context. If you find a mismatch, use the [KoreAves corrections and contribution route](https://koreaves.com/contact/) and include the taxon and supporting source.

---
title: "Selecting the right bird while composing Korean text in KoreAves"
description: "The November 26, 2026 KoreAves search update addresses suggestions during Korean input composition and preserves the chosen taxon as results change."
date: 2026-11-29
tags: ["KoreAves", "Frontend Engineering", "Korean IME", "Search"]
permalink: /koreaves-korean-search-identity-en/
layout: default
lang: en
alternate_lang: ko
alternate_url: /koreaves-korean-search-identity-ko/
published: true
seo:
  title: "Korean IME and reliable taxon selection in KoreAves"
  description: "Why search suggestions during Korean composition and stable taxon selection need separate handling."
---

> 한국어판: [한글 조합 중에도 올바른 새를 선택하는 KoreAves 검색](/koreaves-korean-search-identity-ko/)

The [November 26, 2026 KoreAves release](https://koreaves.com/updates/korean-search-selection/) introduces search suggestions during Korean text composition and keeps the chosen taxon identity separate from changes in the results list. The aim is to make it easier to find the intended bird before opening its evidence map.

For a bird evidence atlas, choosing the wrong species can lead a reader to examine the wrong map or source records. The search needs to support Korean typing while keeping the selected taxon reliable.

## Search text changes during composition

An input method editor (IME) combines Korean characters as the reader types. The text may change before the composition is committed. Browsers expose composition events and the [InputEvent.isComposing property](https://developer.mozilla.org/en-US/docs/Web/API/InputEvent) to distinguish this part of the input process.

MDN marks [InputEvent.isComposing](https://developer.mozilla.org/en-US/docs/Web/API/InputEvent/isComposing) as having limited availability. The target browser and input-method combinations still need to be tested.

Waiting for composition to finish before refreshing suggestions makes search less responsive while someone is typing. Treating every key event as a confirmed selection is also a risk. The [MDN notes on keydown and IMEs](https://developer.mozilla.org/en-US/docs/Web/API/Element/keydown_event#keydown_events_with_ime) explain why event ordering deserves attention.

## Keep the chosen taxon separate from its list position

Imagine a taxon appearing first in the suggestions, then moving to second place when the search text changes. If the application remembers only the first position, the refreshed list could lead to a different taxon.

A useful design is to associate the selection with a stable taxon identifier and track the displayed position separately. This example illustrates the design principle.

## Why this matters across the atlas

The public release note reports verification across Home, Species Reference, GIS Explorer, Taxon Compare, and Sources & evidence. A reader choosing a name in the [species catalogue](https://koreaves.com/species/browse/) or [GIS Explorer](https://koreaves.com/gis/) needs to know that the following evidence view refers to the selected taxon.

The release note is the source for the reported improvements. The examples here explain their design implications; they do not establish the internal implementation or compatibility with a particular IME and browser.

The earlier [KoreAves selection and share-link article](/koreaves-selected-bird-share-links-en/) covers a different part of the experience: carrying a selected taxon between views. The [project portfolio](/portfolio/koreaves/) links the wider development work.

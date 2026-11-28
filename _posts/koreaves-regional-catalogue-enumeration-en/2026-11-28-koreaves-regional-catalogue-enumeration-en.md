---
title: "A 17-region audit of the KoreAves bird catalogue"
description: "I checked the regional counts and compared five HTML structures across all 17 live KoreAves detail pages."
date: 2026-11-28
tags: ["KoreAves", "bird records", "regional evidence", "Frontend Engineering", "data provenance"]
permalink: /koreaves-regional-catalogue-enumeration-en/
layout: default
lang: en
alternate_lang: ko
alternate_url: /koreaves-regional-catalogue-enumeration-ko/
published: true
seo:
  title: "KoreAves regional catalogue: auditing 5,464 taxon entries"
  description: "A live check of all 17 regional pages matched the catalogue counts to identity cards, source notes, media-credit slots and taxon links."
---

> 한국어판: [KoreAves 지역 목록의 5,464개 항목을 점검했다](/koreaves-regional-catalogue-enumeration-ko/)

KoreAves lists 5,464 region-level taxon entries across South Korea's 17 first-level administrative divisions. I checked all 17 detail pages on 28 November 2026. Every page returned HTTP 200, and the card, identity-row, source-note, media-credit and distinct taxon-link counts matched the regional index.

## Counts by region

The [26 November release note](https://koreaves.com/updates/regional-discovery-and-search/) added documented-taxon counts to the regional index. It says the 5,464 regional entries use shared identification cards, with source provenance and media credit retained. The same update synchronised map and list selection across screen sizes.

Each number below is the number of taxa with eligible records in that division. A detail page shows the English display name, scientific name, Korean name and regional source information for each taxon.

<div class="overflow-table" role="region" aria-label="Taxa with eligible records by region" tabindex="0">
<table>
<thead>
<tr><th scope="col">Region</th><th scope="col">Taxa with eligible records</th></tr>
</thead>
<tbody>
<tr><td><a href="https://koreaves.com/regions/seoul/">Seoul</a></td><td>327</td></tr>
<tr><td><a href="https://koreaves.com/regions/busan/">Busan</a></td><td>346</td></tr>
<tr><td><a href="https://koreaves.com/regions/daegu/">Daegu</a></td><td>197</td></tr>
<tr><td><a href="https://koreaves.com/regions/incheon/">Incheon</a></td><td>421</td></tr>
<tr><td><a href="https://koreaves.com/regions/gwangju/">Gwangju</a></td><td>196</td></tr>
<tr><td><a href="https://koreaves.com/regions/daejeon/">Daejeon</a></td><td>238</td></tr>
<tr><td><a href="https://koreaves.com/regions/ulsan/">Ulsan</a></td><td>270</td></tr>
<tr><td><a href="https://koreaves.com/regions/sejong/">Sejong</a></td><td>211</td></tr>
<tr><td><a href="https://koreaves.com/regions/gyeonggi/">Gyeonggi-do</a></td><td>392</td></tr>
<tr><td><a href="https://koreaves.com/regions/gangwon/">Gangwon-do</a></td><td>379</td></tr>
<tr><td><a href="https://koreaves.com/regions/chungbuk/">Chungcheongbuk-do</a></td><td>256</td></tr>
<tr><td><a href="https://koreaves.com/regions/chungnam/">Chungcheongnam-do</a></td><td>396</td></tr>
<tr><td><a href="https://koreaves.com/regions/jeonbuk/">Jeonbuk-do</a></td><td>395</td></tr>
<tr><td><a href="https://koreaves.com/regions/jeonnam/">Jeollanam-do</a></td><td>388</td></tr>
<tr><td><a href="https://koreaves.com/regions/gyeongbuk/">Gyeongsangbuk-do</a></td><td>344</td></tr>
<tr><td><a href="https://koreaves.com/regions/gyeongnam/">Gyeongsangnam-do</a></td><td>333</td></tr>
<tr><td><a href="https://koreaves.com/regions/jeju/">Jeju-do</a></td><td>375</td></tr>
<tr><th scope="row">All 17 regions</th><td>5,464</td></tr>
</tbody>
</table>
</div>

## What I checked on each page

I fetched each regional page once. All responses were HTTP 200 and decoded as UTF-8. For each page I counted:

- `catalog-item` elements for regional taxon cards
- `ka-taxon-identity` rows for names and taxonomic identity
- `regional-source-note` elements for occurrence-source information
- `catalog-media-credit` slots
- distinct `/species/` detail links

The five counts matched the regional index on all 17 pages. The audit covers the served page structure; it does not assess the biological accuracy of individual records or the validity of image licences.

## What the total means

The 5,464 figure is the sum of the 17 regional counts. A taxon documented in several divisions contributes once to each regional count, so the total represents region-taxon entries. The national checklist contains 597 species and 20 subspecies, [617 taxa in total](https://koreaves.com/dataset/).

A regional count identifies taxa with eligible records in a division. Individual bird numbers and population size require different evidence. The absence of an eligible record cannot establish biological absence. The [KoreAves guide](https://koreaves.com/guide/) and [methodology](https://koreaves.com/methodology/) explain how to read the evidence and its limits.

To browse by place, start with the [17-region index](https://koreaves.com/regions/). To compare the documented regions for a selected taxon, continue to the [Regional GIS](https://koreaves.com/gis/).

Related reading: [the mobile region-search repair](/koreaves-region-search-mobile-hotfix-en/), [keeping a selected bird across maps and shared views](/koreaves-selected-bird-share-links-en/), [English display labels for the 617 checklist taxa](/koreaves-english-display-labels-en/), and the [KoreAves project](/portfolio/koreaves/).

---
title: "My tools drew 300 Google Search clicks in 37 days"
description: "Google Search Console recorded 300 web-search clicks and 3,601 impressions for my GitHub Pages property from October 15 to November 20, 2026. The top pages were a scratch simulator, an Epson guide and a face-comparison tool."
seo:
  title: "300 Google Search clicks to independent tools in 37 days"
  description: "First-party Search Console figures: 300 clicks and 3,601 impressions in 37 days, with page-level results for Scratch Lottery, Epson and RichChecker."
date: 2026-11-23
tags: ["Google Search Console", "Independent Software", "Search Discovery", "Scratch Lottery", "Epson", "RichChecker", "Measuring Outcomes"]
permalink: /independent-tools-google-search-results-en/
layout: default
lang: en
alternate_lang: ko
alternate_url: /independent-tools-google-search-results-ko/
image: /scratch-lottery-simulation/scratchlottery-2026-fast-simulation.png
image_width: 1200
image_height: 681
published: true
---

> 한국어판: [직접 만든 도구들이 37일 동안 구글 검색 클릭 300회를 기록했다](/independent-tools-google-search-results-ko/)

**Google Search brought 300 clicks and 3,601 impressions to pages on my GitHub Pages property in the 37 days from October 15 through November 20, 2026.** I checked the original URL-prefix property in Google Search Console using finalized Web search data. Its reported click-through rate was 8.33%.

The pages people reached were not a generic portfolio landing screen. Search was bringing them to tools and documentation I built to answer particular questions: a scratch-ticket simulation, a printer troubleshooting guide and a browser-based face-comparison experiment.

## The pages people clicked from Google

| Page | Search clicks | Search impressions |
| :--- | ---: | ---: |
| [Scratch Lottery simulator](/scratchLottery/) | 120 | 1,416 |
| [Epson waste-ink-pad guide](/epson-waste-ink-pad-reset-without-key/) | 88 | 485 |
| [RichChecker face-comparison experiment](/richChecker/) | 73 | 236 |

These are **page-level results**, reported separately from the 300-click property-wide total. Search Console aggregates property and page reports differently. Adding these rows or subtracting them from 300 would not give a reliable total for the other pages.

The property also includes code and content that live under one GitHub Pages hostname without sharing a single application repository. The numbers above describe the search visibility of those exact URLs, not all the products I operate on other domains.

![An original screenshot of the Scratch Lottery simulator, one of the independently hosted pages measured above.](/scratch-lottery-simulation/scratchlottery-2026-fast-simulation.png)

*This is the simulator's own interface, not a screenshot of the Search Console report. The measurement period and metric definitions come from the first-party report.*

## What I built, and what the numbers tell me

[Scratch Lottery](/scratch-lottery-simulation/) simulates ticket outcomes. I built the interaction, the probability controls and faster batch simulation. Its 120 Google-result clicks indicate that the tool was found through search. They do not reveal whether someone ran a simulation or returned for another session.

The [Korean Epson guide](/epson-waste-ink-pad-reset-without-key/) documents a real printer-maintenance problem and the model-specific limits of possible fixes. Its 88 Google-result clicks are a reason to keep the model cautions prominent, not evidence that 88 printers were repaired. I previously checked the bilingual guide's acquisition using [GA4 and Search Console over different earlier windows](/gh-pages-analytics-notes-6-search-traffic-en/); those figures cannot be added to this overlapping report.

[RichChecker](/richChecker/) is a browser-based facial-feature comparison experiment. Its 73 Google-result clicks establish discovery of the page, not use of the camera, completion of an analysis or any scientific validity of the comparisons.

The useful engineering signal is that a focused tool or a carefully scoped guide can be found for the problem it addresses. I can evaluate each entry point against the question that brought a searcher to it, then improve the tool or the surrounding explanation instead of assuming a successful task from the click alone.

## How the measurement was checked

I queried the verified original [Google Search Console](https://support.google.com/webmasters/answer/7042828?hl=en) URL-prefix property for **Web search**, **October 15–November 20, 2026**, with **final** data. One report used *property aggregation* for 300 clicks, 3,601 impressions and 8.33% CTR. A separate *page aggregation* returned the individual URLs above. This is Google search-result interaction data, not Google Analytics sessions.

The [aggregate, non-identifying report snapshot](/assets/data/dev-c127-gsc-search-performance-20261123.json) records the query scope, figures and limitations. The underlying Search Console property is private, so readers cannot independently rerun the owner report from that public JSON.

**The confirmed outcome is 300 Google search-result clicks to this property during the stated window.** The report does not establish 300 distinct people, product sign-ups, completed tasks or adoption. That distinction is part of how I evaluate software I have shipped.

The [portfolio](/portfolio/) now separates this first-party measurement from its [external publications and resource listings](/portfolio/recognition/), which are independently sourced records rather than traffic reports.

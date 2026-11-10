---
title: "Changing an Open Graph image from SVG to PNG broke my CI test"
description: "I switched eight bilingual Jekyll posts to raster social previews. The first CI run failed on a hard-coded SVG assertion, and the first Korean PNG lost its text."
date: 2026-11-10
tags: ["Jekyll", "Open Graph", "Regression Testing", "GitHub Actions", "Developer Notes"]
permalink: /jekyll-svg-to-png-og-ci-regression-en/
layout: default
lang: en
alternate_lang: ko
alternate_url: /jekyll-svg-to-png-og-ci-regression-ko/
image: /spoonie-author-header-consistency-en/author-header-en-og.png
image_width: 1200
image_height: 630
published: true
seo:
  title: "SVG to PNG Open Graph images broke a Jekyll CI assertion"
  description: "A real Jekyll regression: SVG social images became 1200×630 PNGs, an old test failed, and a Korean font vanished during rasterization."
---

> 한국어판: [OG 이미지를 SVG에서 PNG로 바꾸자 회귀 테스트가 실패했다](/jekyll-svg-to-png-og-ci-regression-ko/)

**I changed the social image metadata on my Jekyll blog, and a regression test failed before deployment.** The old assertion expected an SVG filename and its original height. The new Open Graph asset was a PNG. The mismatch is visible in [PR #27](https://github.com/saramjh/saramjh.github.io/pull/27).

Four Korean/English article pairs, **eight posts**, previously pointed their Open Graph and Twitter image metadata at SVG diagrams. To avoid relying on SVG support in every link-preview renderer, I kept those diagrams inside the articles and exported **1200×630 PNGs** for the metadata. The posts shared one diagram across languages, so the change needed **seven PNG files**, not eight.

<figure>
  <a href="/spoonie-author-header-consistency-en/author-header-en-og.png"><img src="/spoonie-author-header-consistency-en/author-header-en-og.png" alt="The 1200 by 630 PNG exported from the existing Spoonie author-header comparison diagram, showing the Recipe and Recipeed page-header layouts." width="1200" height="630" loading="lazy" style="width:100%;height:auto;"></a>
  <figcaption>The exported image comes from a first-party blog diagram, not an Instagram or Threads screenshot. The [Spoonie author-header case study](/spoonie-author-header-consistency-en/) explains the layout; the [original SVG](/spoonie-author-header-consistency-en/author-header-en.svg) remains available.</figcaption>
</figure>

## The test was checking an old implementation detail

The existing `tests/test_ga4_report_window_release.py` checked for `timeline-ko.svg` or `timeline-en.svg` in the GA4 case study's image metadata. It also expected a height of **620 pixels**. After the change, the social image paths pointed to files such as `timeline-ko-og.png`, with a height of **630 pixels**.

The [first GitHub Actions run](https://github.com/saramjh/saramjh.github.io/actions/runs/42726645118) failed. I updated the test to check two separate contracts: the original SVG still appears in the article body, and the social metadata points to a valid 1200×630 PNG.

The PNG check can be reduced to this small Python example:

```python
from pathlib import Path

png = Path("_posts/spoonie-author-header-consistency-en/author-header-en-og.png").read_bytes()
assert png[:8] == b"\x89PNG\r\n\x1a\n"
assert png[12:16] == b"IHDR"

width = int.from_bytes(png[16:20], "big")
height = int.from_bytes(png[20:24], "big")
assert (width, height) == (1200, 630)
```

It tests the file signature and dimensions. It cannot tell whether the diagram is legible or whether a particular social platform will fetch the image.

## The first Korean raster export also lost text

I inspected the first generated PNGs rather than treating successful file creation as visual QA. Some Hangul text was missing from the Korean previews.

For those derivatives, I rendered the existing SVGs again with an installed `Noto Sans CJK KR` font. I did not change the source diagrams or the inline images in the articles. I checked both the full-size Korean output and a reduced contact sheet, because legibility at social-preview scale matters.

## What the deployment proves

The updated [PR #27](https://github.com/saramjh/saramjh.github.io/pull/27) passed CI and merged on **November 10, 2026**. The [GitHub Pages build and deployment](https://github.com/saramjh/saramjh.github.io/actions/runs/42727063117) then succeeded.

I fetched all **eight published article URLs** and their **seven PNG assets**. Every URL returned HTTP 200; the images were served as `image/png` at **1200×630**, with SHA-256 hashes matching the local release files. The rendered pages pointed `og:image` and `twitter:image` at the PNGs while preserving their canonical URLs, reciprocal `hreflang` tags and original inline SVGs.

Those checks establish that the site serves the intended assets. They do **not** establish how Instagram, Threads or another platform renders a link card. I have no verified card-preview screenshot, click result or readership increase from this change.

A related [UTF-8 content QA incident](/utf8-caption-hash-is-not-text-quality-en/) showed that a correct file hash can coexist with damaged text. This release exposed another boundary: file-type tests, actual pixel inspection and live URL checks answer different questions. The [PR #27 file diff](https://github.com/saramjh/saramjh.github.io/pull/27/files) shows the test change and the published assets.

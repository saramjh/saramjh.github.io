---
title: "My Jekyll project pages were being published as blog posts"
description: "A collection date sent three project pages down the BlogPosting JSON-LD branch. I fixed the Liquid order and verified the deployed HTML for KoreAves, Space Atlas, and Spoonie."
date: 2026-11-13
tags: ["Jekyll", "Structured Data", "JSON-LD", "Liquid", "Developer Notes"]
permalink: /jekyll-project-schema-date-en/
layout: default
lang: en
alternate_lang: ko
alternate_url: /jekyll-project-schema-date-ko/
image: /jekyll-project-schema-date-en/jekyll-schema-en-og.png
image_width: 1200
image_height: 630
published: true
seo:
  title: "Why three Jekyll project pages emitted BlogPosting JSON-LD"
  description: "A real Liquid branch-order mistake made portfolio project cases use BlogPosting and synthetic publication dates. The merged fix and live JSON-LD checks."
---

> 한국어판: [Jekyll 프로젝트 페이지가 블로그 글로 표시된 이유](/jekyll-project-schema-date-ko/)

Three pages in my developer portfolio were emitting `BlogPosting` structured data with a publication timestamp that came from the build. The pages were project cases for KoreAves, Space Atlas, and Spoonie. In [PR #98](https://github.com/saramjh/saramjh.github.io/pull/98), I changed which Liquid condition runs first and checked all three rendered pages after deployment.

The mistake was in the template. It had been using `page.date` as the first test for whether a document was a blog post. During the project-page build, that value was present, so a project case reached the `BlogPosting` branch. The output made a project overview appear to be a dated article.

<figure>
  <a href="/jekyll-project-schema-date-en/jekyll-schema-en-og.png"><img src="/jekyll-project-schema-date-en/jekyll-schema-en-og.png" alt="Diagram of the actual Jekyll schema selection error: the old first condition selected BlogPosting for an undated project page; the deployed project-first condition selects WebPage with a WebApplication main entity" width="1200" height="630" loading="lazy" style="width:100%;height:auto;"></a>
  <figcaption>A diagram reconstructed from the merged template change in PR #98. It explains the condition order; it is not a screenshot from Google Search Console.</figcaption>
</figure>

## Where the wrong type came from

The old Liquid selector tested for `page.date` before checking the project's layout. In the build output, that condition was true for the project documents. The generated JSON-LD used `BlogPosting` and supplied `datePublished` from the document's date value.

The deployed template checks a more specific identity first:

```liquid
{% raw %}{% if page.layout == 'project' and page.site_url and page.slug %}
  {# WebPage with a WebApplication mainEntity #}
{% elsif page.date %}
  {# BlogPosting for a dated article #}
{% endif %}{% endraw %}
```

The snippets above show the decision order. [The exact merged diff](https://github.com/saramjh/saramjh.github.io/pull/98/files) contains the JSON-LD and Liquid filters.

## What the project pages now describe

Each project case is a `WebPage` whose `mainEntity` is a `WebApplication`. I bind the application's name, summary, website, image, and author to the page's existing front matter rather than copying those fields into a second manually maintained list.

The optional `subjectOf` entries refer to source-verified external *directory listings* already recorded in the site data. They are separate `WebPage` objects, not endorsements, reviews, star ratings, or partner claims. The deployed source has five such entries for [KoreAves](/portfolio/koreaves/), one for [Space Atlas](/portfolio/space-atlas/), and two for [Spoonie](/portfolio/spoonie/). Those are counts of existing references in the schema, not new placements.

## How I checked the result

I added [a regression test](https://github.com/saramjh/saramjh.github.io/blob/main/tests/test_portfolio_project_structured_evidence.py) that requires the project branch to appear ahead of the date branch. The test also checks that project URLs and names are drawn from their first-party project files. The full Jekyll build passed alongside 95 Python tests and three existing portfolio JavaScript tests.

After [GitHub Pages deployment](https://github.com/saramjh/saramjh.github.io/actions/runs/43240987471), I fetched all three published case pages and parsed their `application/ld+json` scripts. Each returned HTTP 200 with a `WebPage` and a `WebApplication`. Their synthetic `datePublished` and `dateModified` values were gone. I checked one [dated science article](/space-atlas-science-accuracy-en/) as a control: it still emits `BlogPosting` with its actual November 12 date.

For a similar Jekyll bug, inspect the **rendered HTML**, not only the front matter. A successful build proves that the Liquid template ran; parsing its resulting JSON-LD shows which branch actually won. The [Schema.org WebApplication definition](https://schema.org/WebApplication) describes the intended entity type; it does not promise search rankings or a rich result. I have not measured search-index changes, traffic or reader adoption from this fix.

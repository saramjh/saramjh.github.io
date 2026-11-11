---
title: "Publishing Spoonie's first-record problem on Disquiet"
description: "I published a first-person Spoonie development retrospective on Disquiet on October 13, 2026. How Recipe, Recipeed, and the difficult first user contribution changed what I wanted to measure."
date: 2026-11-11
tags: ["Spoonie", "Disquiet", "Product Engineering", "UGC", "Developer Writing", "User Experience"]
permalink: /spoonie-disquiet-first-record-en/
layout: default
lang: en
alternate_lang: ko
alternate_url: /spoonie-disquiet-first-record-ko/
image: /spoonie-social-cooking-early-users/recipe-record-flow.svg
image_width: 1200
image_height: 400
published: true
seo:
  title: "My Spoonie development retrospective published on Disquiet"
  description: "What I learned after building Recipe and Recipeed for Spoonie, and why a new cooking community needs a reason for someone's first real record."
---

> 한국어판: [Disquiet에 Spoonie 개발 회고를 공개하며 돌아본 첫 요리 기록](/spoonie-disquiet-first-record-ko/)

**On October 13, 2026, I published a first-person account of Spoonie's early user problem on [Disquiet](https://disquiet.io/articles/MVsxQv).** The Korean article, *레시피 SNS를 만들고 깨달은 것: 기능보다 먼저 ‘첫 기록의 이유’가 필요했다*, appeared under the DevTestudinidae author name. It described a problem that remained after I had built the features of a cooking community: giving a visitor a useful reason to make their first personal record.

I wanted to explain the product decision in public, where other developers could examine the question. A working recipe calculator, a publishing form, and a social feed are things I can build and demonstrate. They do not, by themselves, explain why someone should spend time contributing to a new community.

<figure>
  <img src="/spoonie-social-cooking-early-users/recipe-record-flow.svg" alt="Original developer diagram of Spoonie's proposed relationship: someone reads a Recipe, cooks, and records the experience as a Recipeed linked to its source." width="1200" height="400" loading="lazy" style="width:100%;height:auto;">
  <figcaption>My existing Recipe-to-Recipeed design diagram, previously published in the Spoonie development log. It represents a product relationship, not measured user activity.</figcaption>
</figure>

## The problem that remained after the features worked

I built [Spoonie](https://spoonie.kr/) around two kinds of content. A **Recipe** holds the ingredients and cooking steps. A **Recipeed** records what someone cooked, the photo they took, and changes they made. When a Recipe has serving-size information, readers can adjust the amount and review the corresponding ingredient quantities.

Public Recipes are available to read without creating an account. Writing a Recipeed requires signing in. That distinction matters when the product is new. Asking for registration before someone has found anything worth using creates a different first experience from letting them solve a cooking problem and decide whether to leave a record afterward.

The central question in my Disquiet article was simple: why should a person make their first cooking record here? Making the form shorter might help a willing contributor. It cannot supply a reason to contribute in the first place.

## Separating exposure from a first contribution

For a community product, it is tempting to count published promotional posts as progress toward active participation. I wanted to keep those events separate.

A visitor can open a Recipe without registering. Someone who registers may still never publish. A first Recipeed is a different event again, and a person returning to record another meal would tell me something that a one-time post cannot. Each stage requires its own evidence before I can describe it as an outcome.

In the October 13 article, I explicitly said that I could not yet claim a verified first Recipeed from a newly recruited outside creator. That statement described what I could substantiate at publication time. It does not establish the product's present participation numbers, and I am not treating later activity as if it were already known then.

The design experiment was to lead with an immediate task: find a public recipe, check ingredient quantities for the serving size, cook, and then decide whether keeping a personal record would help next time. I was testing whether that order made more sense to a visitor than asking them to join another social network.

## What this publication demonstrates

Publishing the retrospective on Disquiet gave me a public, dated account of how I connected the implementation to a product question. I had worked on the content structure and the interface, then identified the behavior those features still needed to support.

That is a useful developer work sample for someone considering a community product. The [original Disquiet article](https://disquiet.io/articles/MVsxQv) documents the reasoning. A reader can also open a [real public Spoonie Recipe](https://spoonie.kr/recipes/554ae9ef-15a1-4806-944e-170884d17a96) and compare the experience with the questions I wrote about.

The broader Recipe and Recipeed design is explained in my [earlier development log](/spoonie-social-cooking-early-users/). A separate [Web Apps Directory listing](/spoonie-webapps-directory-en/) records an external discovery route for the finished public service. Those are different kinds of evidence, and I keep them separate.

This was a self-authored developer article on an external community platform. It was not an independent review, and the publication itself does not establish user adoption or conversion growth.

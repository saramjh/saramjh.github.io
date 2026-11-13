---
title: "How recipeCalc grew into Spoonie, one cooking problem at a time"
description: "The development trail from my 2024 recipe-scaling utility to the separate Spoonie repository and its public Recipe and Recipeed experience, with links to the original code and product."
date: 2026-11-11
tags: ["Spoonie", "recipeCalc", "Recipe Scaling", "Product Engineering", "Independent Development", "Cooking"]
permalink: /recipe-calc-to-spoonie-origin-en/
layout: default
lang: en
alternate_lang: ko
alternate_url: /recipe-calc-to-spoonie-origin-ko/
image: /spoonie-social-cooking-early-users/recipe-record-flow-og.png
image_width: 1200
image_height: 630
published: true
seo:
  title: "From recipeCalc to Spoonie: the development of a cooking record product"
  description: "How a 2024 ingredient-ratio calculator led to Spoonie's Recipe and Recipeed structure, with the original GitHub code, historical screenshot and public product."
---

> 한국어: [재료의 비율을 계산하던 recipeCalc가 Spoonie로 이어지기까지](/recipe-calc-to-spoonie-origin-ko/)

**The first version of what became Spoonie was a small recipe-scaling utility.** I built [recipeCalc](https://github.com/saramjh/recipeCalc) to solve a recurring kitchen calculation: when one ingredient changes, how much should the others change to keep the same proportions? It was a focused web tool. The idea of keeping recipes and returning to them came afterward.

The public development timeline gives the story a few fixed points. I created the recipeCalc GitHub repository on **August 22, 2024**, and documented the working utility in a [September 3, 2024 development post](/recipe-scaling-application/). The separate [Spoonie repository](https://github.com/saramjh/spoonie) was created on **July 19, 2025**. Those repository dates establish when the projects existed, not when a later public service was launched. Today, [Spoonie](https://spoonie.kr/) and a [real public Recipe](https://spoonie.kr/recipes/554ae9ef-15a1-4806-944e-170884d17a96) show where the product went.

## A calculator for the ingredient you actually have

The original use case was adjusting quantities in dessert-café recipes. A recipe rarely fits every cooking situation. Someone may have less of a key ingredient than the instructions require or want to prepare a larger batch. Changing one number means recalculating the others to preserve the intended ratios. Doing that repeatedly by hand was a small but worthwhile problem to remove.

In recipeCalc, I could enter ingredient names, quantities and units, choose a reference ingredient, and calculate the adjusted quantities. I also added bulk ingredient entry and basic editing and deletion. The [original source repository](https://github.com/saramjh/recipeCalc) and the [2024 feature walkthrough](/recipe-scaling-application/) document those choices. The tool is still available as a [standalone web app](https://saramjh.github.io/recipeCalc/).

<figure>
  <img src="/recipe-scaling-application/recipescalingapplication.jpg" alt="Original 2024 screenshot from the recipeCalc development post showing the ingredient input and scaling interface." width="900" height="886" loading="lazy" style="display:block;width:100%;max-width:600px;height:auto;margin-inline:auto;">
  <figcaption>The original 2024 recipeCalc interface from my development blog. It is a historical screenshot, not a mock-up of today's Spoonie.</figcaption>
</figure>

The calculator answered the question in front of me. But I kept coming back to a different one: where should the recipe live so I could find and use it again?

## Why a recipe needed a home

During a move, I came across a handwritten recipe notebook. It had become worn from use and was eventually discarded. I regretted losing access to the recipes inside. A calculator could adjust ingredient quantities, but it could not keep the original recipe somewhere I could return to. That loss made the idea of a lasting recipe book much more concrete. I am not reproducing the notebook or identifying its writer here.

That led me toward a recipe book and eventually a separate product. The Spoonie repository, created in July 2025, marks the point when the work had its own codebase. I was no longer designing only an input form and a calculation. I needed to represent ingredients and instructions as reusable content, make them readable to other people, and think about how someone would use the recipe during cooking.

The engineering problems changed with the scope. A calculator needs clear inputs and predictable arithmetic. A recipe service needs a content structure that stays understandable across many different dishes and serving sizes. I had to design for the reader who comes back later, not only the person typing quantities right now.

## Two kinds of cooking content

Spoonie's current content model distinguishes a **Recipe** from a **Recipeed**. A Recipe contains ingredients and cooking instructions. A Recipeed is designed for a record of someone's own cooking experience connected to a source Recipe. The two actions are different: reading a method and documenting what happened when someone used it.

<figure>
  <img src="/spoonie-social-cooking-early-users/recipe-record-flow.svg" alt="Original developer diagram showing how a public Spoonie Recipe may lead to a cooking experience recorded as a related Recipeed." width="1200" height="400" loading="lazy" style="display:block;width:100%;height:auto;">
  <figcaption>My existing Recipe-to-Recipeed design diagram, reused from an earlier developer note. It illustrates the information model, not actual user participation.</figcaption>
</figure>

A visitor can read a public Recipe to answer an immediate cooking question. A separate record format gives someone who has cooked the dish a place to describe their result. The earlier ingredient-calculation problem has not disappeared; it now sits within a larger experience of finding a method, adjusting it to fit a meal, and deciding whether the result is worth recording.

This progression also forced me to distinguish product capability from user behavior. Building the Recipeed structure cannot tell me whether a new visitor will choose to post a first record. I discussed that uncertainty in my [first-person Disquiet retrospective](/spoonie-disquiet-first-record-en/), which is about participation rather than the project's technical beginnings.

## What I can show today

The [2024 calculator](https://saramjh.github.io/recipeCalc/) and the [current Spoonie recipe page](https://spoonie.kr/recipes/554ae9ef-15a1-4806-944e-170884d17a96) are both public. The repositories record the change in scope from a small utility to a cooking-content service. They demonstrate how I carried an everyday problem through several rounds of product design and implementation, with real software available for someone else to inspect.

Spoonie also has a documented [Web Apps Directory listing](/spoonie-webapps-directory-en/). That gives the public product another route for discovery. How often people return to cook from a Recipe or publish a Recipeed still requires real usage evidence.

I continue to work on the part that first interested me: making a useful recipe easy to find, understand, adjust, and return to when it is time to cook again.

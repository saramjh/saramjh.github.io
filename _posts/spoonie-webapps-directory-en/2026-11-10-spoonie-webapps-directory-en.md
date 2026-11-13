---
title: "Spoonie is listed in Web Apps Directory's Food & Drink catalogue"
description: "Spoonie's recipe community appears in Web Apps Directory. I built the browser-based Recipe and Recipeed flow, and this listing gives people outside the product site another way to find it."
date: 2026-11-10
tags: ["Spoonie", "Web Apps Directory", "Web App", "Recipe Community", "Developer Portfolio"]
permalink: /spoonie-webapps-directory-en/
layout: default
lang: en
alternate_lang: ko
alternate_url: /spoonie-webapps-directory-ko/
image: /spoonie-social-cooking-early-users/recipe-record-flow-og.png
image_width: 1200
image_height: 630
published: true
seo:
  title: "Spoonie listed in Web Apps Directory's Food & Drink category"
  description: "An independent web-app directory lists Spoonie, the recipe sharing and cooking-record service I developed. The listing and the product design behind it."
---

> 한국어판: [Spoonie, Web Apps Directory 음식·요리 분야에 등재](/spoonie-webapps-directory-ko/)

**Spoonie has a public entry in [Web Apps Directory's Food & Drink category](https://webapps.directory/directory/spooniespoonie).** The directory labels the entry "Catalogued October 25, 2026" and links directly to [spoonie.kr](https://spoonie.kr/). People looking through its web-app catalogue can now find a Korean home-cooking service that I built outside the service's own website.

The entry describes recipe discovery, ingredient quantities that adapt to serving size, and a way for users to record what they cooked. Those are useful starting points for someone encountering Spoonie for the first time. The product idea goes further: I want a recipe and the experience of someone who tried it to remain connected.

<figure>
  <img src="/spoonie-social-cooking-early-users/recipe-record-flow.svg" alt="Original Spoonie developer diagram: a published Recipe leads to someone's cooking attempt and a Recipeed record that can reference the source Recipe." width="1200" height="400" loading="lazy" style="width:100%;height:auto;">
  <figcaption>My original diagram of the Recipe-to-Recipeed relationship. It explains a design, not actual user activity or a screenshot from Web Apps Directory.</figcaption>
</figure>

## The work behind a small directory entry

I separated two kinds of content in the product. A **Recipe** is the structured source: ingredients, quantities, cooking instructions and an author. A **Recipeed** is a record of an actual cooking attempt, such as a finished dish, a substitution or a short note about the outcome. When the cook identifies the Recipe they followed, the product can preserve that reference.

Serving-size adjustment solves a different, immediate problem. A person making a dish for one or four people should be able to see appropriate ingredient quantities without rewriting the recipe. The [live Spoonie site](https://spoonie.kr/) describes the search, ingredient and cooking-record workflow, and a [public Recipe](https://spoonie.kr/recipes/554ae9ef-15a1-4806-944e-170884d17a96) gives visitors a concrete page to inspect.

I worked on the boundary between these experiences: a recipe needs a reliable source, and someone's cooking note should remain their own story. Making that distinction visible in a browser interface is a product-design and data-modeling problem, not simply a matter of storing another photograph.

## What an external catalogue changes

The directory adds a discovery route alongside Spoonie’s own pages and direct links: its [Food & Drink catalogue](https://webapps.directory/directory/spooniespoonie) now contains an entry describing the product and linking to the actual service. It also classifies Spoonie as a browser app, so a visitor knows that the product can be opened from a web browser.

A second original record, [LaunchFree.io's Spoonie listing](https://launchfree.io/listings/spoonie.html), categorizes Spoonie as **Community / Beta**, dates the entry **October 12, 2026**, and links to the live service.

This gives a prospective collaborator or international reader a public, independently hosted reference to examine alongside the working product. Someone evaluating a recipe platform can check whether the directory's description matches the experience on Spoonie. It is also a modest exercise in making a Korean-language product understandable to an audience that may first discover it through an English catalogue.

I can point to both listings as evidence of **external discoverability**. Neither listing establishes changes in registrations, repeated cooking records or referral traffic. The current Korean-language interface also limits immediate use by people who do not read Korean.

## What I would measure next

The next question is whether someone who discovers a recipe follows it, leaves a cooking record and returns for another dish. The product can support that sequence; user retention requires separate, real usage evidence.

For the original records, see [Web Apps Directory](https://webapps.directory/directory/spooniespoonie), [LaunchFree.io](https://launchfree.io/listings/spoonie.html) and the [source-linked portfolio archive](/portfolio/recognition/). The earlier [Spoonie Recipe and Recipeed development note](/spoonie-social-cooking-early-users/) explains the social-cooking model in more detail. [Open Spoonie](https://spoonie.kr/) to inspect the current interface.

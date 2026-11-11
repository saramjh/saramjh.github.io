---
title: "I shipped a directory for Spoonie's 18 editorial profiles"
description: "The public Spoonie directory links 18 platform-operated editorial profiles after checking their exact identifiers and public status. This is a product release, not evidence of 18 human chefs or active contributors."
date: 2026-11-11
tags: ["Spoonie", "Product Engineering", "Editorial Identity", "Supabase", "Profile Discovery"]
permalink: /spoonie-editorial-curators-en/
layout: default
lang: en
alternate_lang: ko
alternate_url: /spoonie-editorial-curators-ko/
image: /spoonie-editorial-curators-en/spoonie-curator-flow.svg
image_width: 1280
image_height: 600
published: true
seo:
  title: "Building Spoonie's verified editorial profile directory"
  description: "How I connected 18 Spoonie-operated editorial profiles to a public directory using pinned IDs, verified public fields and existing profile pages, without confusing accounts with authors or readership."
---

> 한국어: [스푸니에 공식 큐레이터 프로필 18개를 탐색하는 화면을 만들었다](/spoonie-editorial-curators-ko/)

**I built and shipped a public directory for Spoonie's editorial profiles.** On November 11, 2026, the [live page](https://spoonie.kr/curators) displayed links to 18 profiles: ten for cooking, four for desserts and four for drinks. These are **Spoonie-operated editorial identities** for introducing recipes. They are not evidence that 18 independent chefs signed up, or that 18 contributors are already publishing.

## Make official identity something the code checks

A directory can be assembled by searching for matching names. I did not want an ordinary member with a similar profile name to appear as an official Spoonie editor.

In [merged PR #16](https://github.com/saramjh/spoonie/pull/16), I pinned the expected public identifiers and fetched their matching public profiles. Before displaying an entry, the code checks the profile's identifier, account handle, organization type, public visibility and editorial profile description. An unrelated or mismatched profile is left out. If the public-profile query fails, the page shows an unavailable state instead of filling the screen with invented accounts or activity.

The result is a small but useful ownership boundary. Public profile data can be read for display, while account provisioning remains a separate administrative operation. I did not move privileged account creation or service keys into the public browser.

<figure>
  <img src="/spoonie-editorial-curators-en/spoonie-curator-flow.svg" alt="Developer-authored flow diagram showing 18 Spoonie-owned editorial identities checked against exact public IDs and account fields, then shown in cooking, dessert and drink groups that link to existing profile pages" width="1280" height="600" loading="lazy" style="display:block;width:100%;height:auto;">
  <figcaption>My diagram of the implementation in PR #16 and the public directory observed November 11. These are editorial account counts, not recipe totals or engagement metrics.</figcaption>
</figure>

## What a visitor can actually use

The [directory](https://spoonie.kr/curators) groups profiles by cooking, desserts and drinks, then links each one to Spoonie's existing profile view. It reuses the product's profile and follow entry points rather than introducing a separate social identity system.

There is a disclosure below the list: the curators are recipe-introduction accounts operated by Spoonie, while an individual recipe's creator and source are identified on that recipe. I wanted that boundary visible on the page, not just documented in code.

At the time PR #16 merged, these editorial accounts had not yet published new recipes. The directory was therefore configured with `noindex, follow`. I verified that setting and the 18 public profile links in the live HTML on November 11. The directory being online does not establish readership, actual follows or an active recipe catalogue.

## The developer result

The practical achievement is an identity-aware directory integrated with an existing product: a controlled set of public accounts, checks that exclude lookalikes, and links to the existing profile interface. It is a foundation for editorial discovery rather than a claim of community traction.

The next meaningful evidence will come from recipes published with their own source and image rights intact, followed by real reader behavior. I use the same distinction in my [Spoonie recipe-poll implementation](/spoonie-live-polls-en/): shipped code and a working public example can be verified, while adoption requires separate measurement.

## Four original visual notes

I drew four diagrams of the implemented path from verified editorial account to directory and public profile. These are schematic illustrations, not the actual curators' portraits, Spoonie avatars, or product screenshots.

[18 platform-operated profiles](/assets/img/dev-spoonie-curators-ig-20261111/card-01.jpg) · [Cooking, desserts and drinks](/assets/img/dev-spoonie-curators-ig-20261111/card-02.jpg) · [Public identity checks](/assets/img/dev-spoonie-curators-ig-20261111/card-03.jpg) · [Directory to existing follow flow](/assets/img/dev-spoonie-curators-ig-20261111/card-04.jpg)


Sources: [live Spoonie editorial directory](https://spoonie.kr/curators), [original merged implementation PR #16](https://github.com/saramjh/spoonie/pull/16), [Spoonie project case](/portfolio/spoonie/).

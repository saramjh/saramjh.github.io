---
title: "Building a real Spoonie recipe poll, then sharing it with member posts"
description: "A poll is present in a public Spoonie recipe. I trace the original PR #19 and PR #20 implementation, the vote-counting access rules and the boundary between merged code and production verification."
date: 2026-11-11
tags: ["Spoonie", "Recipe Poll", "Product Engineering", "Supabase", "Authorization"]
permalink: /spoonie-live-polls-en/
layout: default
lang: en
alternate_lang: ko
alternate_url: /spoonie-live-polls-ko/
image: /spoonie-live-polls-en/spoonie-poll-flow-og.png
image_width: 1200
image_height: 630
published: true
seo:
  title: "How I built a Spoonie recipe poll and generalized member authoring"
  description: "A live public Spoonie recipe has a poll. The merged PR #19 and PR #20 code shows how questions, votes and access controls support Recipes and Recipeed posts."
---

> 한국어: [Spoonie 공개 레시피 투표를 구현하고 회원 글쓰기로 확장한 과정](/spoonie-live-polls-ko/)

**I connected a real poll to a public Spoonie recipe.** A reader can answer a question about how they prefer to prepare a dish, with the site returning recorded vote totals. The [public example](https://spoonie.kr/recipes/6eaa37a1-6c0f-4841-aadd-7a2d980fbdbf) serves an active question with two answer choices. When I inspected the server response on November 11, 2026, it contained one recorded vote. That count belongs to the moment of inspection. It does not identify the voter or establish an audience trend.

I shipped the underlying code in two steps. [PR #19](https://github.com/saramjh/spoonie/pull/19), merged November 11 at 02:47 UTC, connected an optional poll to published curator Recipes. [PR #20](https://github.com/saramjh/spoonie/pull/20), merged at 03:25 UTC the same day, expanded the authoring model to allow ordinary members to add an optional poll to a Recipe or a Recipeed. Both changes have first-party code and merge histories to inspect.

## Give a recipe question its own data

A recipe description may already ask readers how they prefer to eat a dish. If the question stays only in the prose, there is nowhere reliable to store an answer or count its alternatives. I separated the question and choices from the recipe's description.

The initial implementation supported one question with two to four choices for a published curator recipe. Recipes without a configured poll retained their existing presentation, and their original cooking instructions, author and source attribution remained unchanged.

<figure>
  <img src="/spoonie-live-polls-en/spoonie-poll-flow.svg" alt="Developer-authored diagram of a Spoonie Recipe or Recipeed linked to a question, authenticated vote recording and an aggregate-only response" width="1280" height="560" loading="lazy" style="display:block;width:100%;height:auto">
  <figcaption>A diagram of the first-party data flow in PR #19 and PR #20. It is not a product screenshot or an engagement chart.</figcaption>
</figure>

The next change connected the same PollComposer to the Recipe and Recipeed writing and editing forms. A question is optional and collapsed until an author chooses to add one. Both post detail views use ItemPoll to display a saved poll, if one exists.

Post saving and poll saving are also separate operations. If the post succeeds but the poll fails to save, the interface needs to report that partial outcome and allow a later edit. The implementation handles that case without showing the post itself as a failure.

## Keep voters separate from the totals

A reader needs the number of votes for each answer, not the identities of the accounts behind those votes. The [first implementation](https://github.com/saramjh/spoonie/pull/19) separates public aggregate reads from authenticated vote writes and restricts direct access to voter records.

The [shared-item implementation](https://github.com/saramjh/spoonie/pull/20) uses item_polls and item_poll_votes for both Recipes and Recipeed posts. It allows one current vote per user and item, permits a member to change their selection, and prevents an author from changing answer options after votes have been recorded. The code tests include authorization checks, invalid payloads and consistency between option counts and totals.

That model gives the public page a structured question and a result without returning a list of voters. The permissions are part of the product design because a cooking poll should not expose more personal information than the interaction needs.

## What I verified on the public site

The [sample Recipe](https://spoonie.kr/recipes/6eaa37a1-6c0f-4841-aadd-7a2d980fbdbf) returned HTTP 200. Its server-rendered initialPoll contained an active flag, two choices and a total of one vote when inspected. The live value can change.

PR #20 contains merged code for general member authoring, but I have not independently completed the entire authenticated create, edit and vote flow on the production service during this review. The existence of merged code does not prove that specific end-to-end deployment path works.

The concrete result is a public recipe with structured poll data and a reusable implementation for member-created cooking posts. The earlier engineering path, from an [ingredient-scaling utility to Spoonie](/recipe-calc-to-spoonie-origin-en/), is documented separately.

Original evidence: [first poll PR #19](https://github.com/saramjh/spoonie/pull/19), [generalized authoring PR #20](https://github.com/saramjh/spoonie/pull/20), [public sample Recipe](https://spoonie.kr/recipes/6eaa37a1-6c0f-4841-aadd-7a2d980fbdbf).

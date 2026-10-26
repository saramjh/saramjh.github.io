---
title: "What Can the First Screen Honestly Offer Before OAuth?"
description: "A Social Relations Lab developer note on useful first actions when Instagram OAuth is not configured: explicit fictional examples, honest empty states and a testable tradeoff."
date: 2026-10-26
tags: ["Social Relations Lab", "Onboarding", "Instagram", "Product Design", "Empty States", "Developer Notes"]
permalink: /soclab-first-action-before-oauth-en/
layout: default
lang: en
alternate_lang: ko
alternate_url: /soclab-first-action-before-oauth-ko/
image: /soclab-first-action-before-oauth-en/soclab-first-action-en-1200x630.png
image_width: 1200
image_height: 630
published: true
robots: "index, follow, max-image-preview:large"
seo:
  title: "First Value Before Instagram OAuth | Social Relations Lab"
  description: "Why the unconnected account should remain visibly unconnected, and whether one clearly fictional source example can provide an honest first action."
  keywords: ["Instagram OAuth onboarding", "first user value", "honest empty state", "synthetic demo UX", "Social Relations Lab"]
---

> **한국어 판:** [인스타그램 연결 전, 첫 화면은 무엇을 보여줘야 할까?](/soclab-first-action-before-oauth-ko/)

I was reviewing the first-account screen for Social Relations Lab(소셜 릴레이션스 랩), an unfinished local experiment in preserving the sources and history of authorized social interactions so that the human operator can decide what to do next.

The question is awkwardly simple. What can the first screen offer if the service operator has not configured a usable official Instagram OAuth app?

**I think an account with no authorized observations should remain visibly empty.** A polished fictional relationship graph cannot substitute for access rights. Yet a disabled login button on its own does not help a visitor understand what the tool would eventually do.

<figure>
<img src="/soclab-first-action-before-oauth-en/soclab-first-action-en-1200x630.png" alt="An original synthetic concept showing unconnected account, permitted self-owned import and a clearly fictional evidence example as separate options. Not a released product UI." width="1200" height="630" loading="lazy" style="width:100%;height:auto;">
<figcaption>A concept based entirely on fictional records, not a screenshot of a customer account or released interface.</figcaption>
</figure>

## What is actually implemented

On October 26, 2026, I checked the Mac-local project implementation and its onboarding components. CustomerOnboarding explicitly tells the operator that entering an account identifier does not verify ownership or reveal activity. InstagramConnector disables the official Instagram login action when the service operator has not configured the necessary Meta application.

This is an important truthful boundary. The repository implements parts of an official OAuth integration with offline tests, but it has not demonstrated a live, authorized new customer connection.

The same prototype does contain two independently fictional example workspaces and a separate, consent-based import path for a limited subset of user-owned Instagram message JSON ZIP data. Imported files, live-provider observations and invented demonstrations do not have equivalent provenance, and should not share a visual claim of being verified current account data.

## A first action without pretending a relationship exists

I would distinguish two scenarios.

Someone without an eligible source can inspect **one visibly fictional card** showing provenance, what is unknown and a possible human-controlled next step. It should never be attached to their purported account.

Someone who has their own authorized export should be told exactly which formats the current importer can handle, then choose whether to consent to processing. Unsupported formats cannot quietly become successful imports.

The official account-first connection remains the target user journey, not a workflow to simulate by capturing login cookies.

## The opposing argument

A visitor seeking analysis of their own Instagram contacts may find a fictional card confusing or even dishonest. A simple first screen saying that the official connection is unavailable, with a clear reason, may earn more trust than another branching wizard.

So I do not want to build an elaborate onboarding flow. I would compare the honest existing empty state against **the same components with only one plainly fictional example and one valid next action**. If the example causes false beliefs, the simpler version wins.

## A falsifiable usability comparison

Use two fully synthetic workspaces. No real account login, credential, import or external customer records are needed.

| Condition | Display | What to check |
| :--- | :--- | :--- |
| A: existing empty state | Ownership unverified, no observed events, unavailable official connection | Can people explain what is missing? |
| B: fictional first action | A visibly fictional source card, unknown coverage and a valid next action | Do people confuse the example with their own data? |

Ask evaluators to classify what is **real**, **fictional** and **unknown**. Observe whether they choose a supported next step or keep trying a disabled connection. A successful demo click is not evidence of a useful relationship decision.

The proposal is in the Mac developer inbox, awaiting review. **No test participants have been recruited, and there is no developer acceptance, real user feedback or shipped improvement to report.**

## Trust starts before the first connection

Earlier I explored [what a comment can actually prove](/soclab-instagram-evidence-boundary-en/), [why an attempted outbound comment is not a delivery receipt](/soclab-comment-delivery-receipt-en/) and [what disconnect, withdrawal and erasure mean](/soclab-consent-disconnect-erase-en/).

The first screen should respect the same principle. Empty may be an honest and necessary account state. The design challenge is to make an eligible next action legible without replacing unknown information with convincing fiction.

Social Relations Lab is not a public beta or a service with confirmed unrestricted access to social inboxes. I would rather make that limitation understandable than hide it.

Other [developer notes](/) and the [Korean edition](/soclab-first-action-before-oauth-ko/) are available.

---

*This is an independent design hypothesis grounded in local source inspection on October 26, 2026, not a report of new customer usage, an implemented feature or a completed usability experiment.*

---
title: "When a Comment Has No Timestamp, What Does Recent Mean?"
description: "A first-person Social Relations Lab source-code reproduction: an original event time may be unknown while its observation time is known. Why this changes the meaning of a relationship timeline."
date: 2026-10-26
tags: ["Social Relations Lab", "Evidence Provenance", "Event Timestamps", "Relationship History", "Developer Notes", "UX"]
permalink: /soclab-event-time-observed-time-en/
layout: default
lang: en
alternate_lang: ko
alternate_url: /soclab-event-time-observed-time-ko/
image: /soclab-event-time-observed-time-en/soclab-two-clocks-en-1200x630.png
image_width: 1200
image_height: 630
published: true
robots: "index, follow, max-image-preview:large"
seo:
  title: "Authored Time Is Not Observation Time | Social Relations Lab"
  description: "A comment can have an unknown original timestamp yet a known observation date. A synthetic source-code reproduction and the UX tradeoff for relationship timelines."
  keywords: ["event time versus observed time", "relationship timeline", "unknown comment date", "source provenance", "Social Relations Lab"]
---

> **한국어 판:** [댓글이 언제 쓰였는지 모를 때, 최근 대화라는 말은 맞을까?](/soclab-event-time-observed-time-ko/)

I went back to a date field while working on Social Relations Lab(소셜 릴레이션스 랩), an unfinished local experiment for keeping provenance and history of authorized social interactions so the human operator can decide what comes next.

**The date we observe a comment does not necessarily tell us when somebody wrote it.** Treating those dates as interchangeable could make an old comment discovered today look like a fresh inbound reply.

<figure>
<img src="/soclab-event-time-observed-time-en/soclab-two-clocks-en-1200x630.png" alt="Original conceptual graphic of two clocks for a fictional comment. Authored time unknown, observation time known. Neither a real customer event nor shipped product screenshot." width="1200" height="630" loading="lazy" style="width:100%;height:auto;">
<figcaption>Two different questions, two clocks. This is fictional illustrative data, not the current product interface.</figcaption>
</figure>

## Two fields the source code already separates

On October 26, 2026, I inspected the current Mac-local Interaction model. It records occurredAt for the source-supported time of an event and observedAt for when the system observed it.

This is valuable for third-party public index records that lack reliable original comment timestamps. Their occurredAt value can remain null without silently manufacturing an authored date.

But the groupRelationships function sorts records using event time or, if missing, observation time. It then returns relationship-level firstAt and lastAt based only on the selected records' event times. In the Contact 360 view those fields are used in labels for first and latest observation.

I wanted to see what that meant in a real function call before treating it as a user-facing defect.

## A single synthetic event, actually executed

I ran the current TypeScript domain function read-only in Node.js. No real account, imported user records, code change or network connection was involved.

| Input or output | Observed result from the synthetic case |
| :--- | :--- |
| Event authored time, occurredAt | null |
| Event observation time, observedAt | 2026-10-26 12:00 UTC |
| Grouped relationship stage | observed |
| Relationship firstAt | empty string |
| Relationship lastAt | empty string |
| Observation timestamp on the event | still present |

The relationship exists and its original event retains the observation date. Yet the relationship-level dates are blank. A message that says 'authored time unknown' is accurate. A summary that says 'first observation time unknown' can be misleading when the system did observe the record at a known time.

This is **one contract reproduction using wholly fictional input**, not a report that every timestamp feature is broken or that any real customer was affected.

## Why not fill the missing date automatically?

Because it would answer the wrong question.

| Question | Acceptable evidence | Unsupported inference |
| :--- | :--- | :--- |
| When was the comment written? | A native/source-backed event time | Treat observation as authored time |
| When did the system find it? | Ingestion or observation time | Claim it did not exist beforehand |
| Was there reciprocal dialogue? | Connected and attributable reply evidence | Treat one public observation as a verified response |

This matters in any small operator's contact history. A late import of an old exchange is not a new voluntary customer message. A chart that presents both under the same time label could change which follow-up a person chooses.

## The argument for keeping the interface simpler

Not every relationship card needs two clocks. The operator may care more about context and next steps than additional date fields. We could keep an explicit 'original date unknown' label and show the observation date only within the source-coverage detail panel.

That may be preferable to adding another timestamp widget. More data does not automatically improve comprehension.

## The smallest useful test

I sent the Mac development owner a four-case synthetic evaluation proposal: known authored date with later observation, unknown authored date with known observation, an old record imported late, and observation-only source material.

Compare the current Contact 360 wording with a minimal distinction between authored and observation time. The intended success condition is that readers stop treating a newly observed old event as a fresh exchange while still recognizing when source evidence was actually collected.

No developer decision or usability experiment is complete, and this is not a shipped timeline change.

Earlier I wrote about [what incoming comments can prove](/soclab-instagram-evidence-boundary-en/) and [why a clicked Post control is not a delivery receipt](/soclab-comment-delivery-receipt-en/). This time I am asking what a known source can actually tell us about *when* an event happened.

Other [developer notes](/) and the [Korean edition](/soclab-event-time-observed-time-ko/) provide the rest of the series.

---

*This diary is based on a read-only synthetic call to the current Mac domain function on October 26, 2026. It includes no real person's messages and does not claim implemented fixes, verified user feedback or a public beta.*

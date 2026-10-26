---
title: "I Clicked Post. Did My Comment Actually Publish?"
description: "A first-person development note on distinguishing text entry, attempted delivery and provider confirmation before claiming social engagement."
date: 2026-10-26
tags: ["Social Relations Lab", "Instagram", "Developer Notes", "Automation", "Delivery Evidence"]
permalink: /soclab-comment-delivery-receipt-en/
layout: default
lang: en
alternate_lang: ko
alternate_url: /soclab-comment-delivery-receipt-ko/
image: /soclab-comment-delivery-receipt-en/soclab-delivery-receipt-en-1200x630.png
image_width: 1200
image_height: 630
published: true
robots: "index, follow, max-image-preview:large"
seo:
  title: "A Click Is Not a Delivery Receipt | Social Relations Lab"
  description: "Why a comment visible in an editor is not a verified post: uncertain delivery, idempotency locks and honest social outcome measurement."
  keywords: ["Instagram comment delivery", "idempotent social automation", "unconfirmed message", "provider receipt", "Social Relations Lab"]
---

> **한국어 판:** [게시 버튼을 눌렀지만 댓글이 보이지 않았다](/soclab-comment-delivery-receipt-ko/)

While building Social Relations Lab(소셜 릴레이션스 랩), a local relationship-evidence experiment, I wrote a contextual comment today. The text was visible, exactly as intended, in the platform's editor. I pressed Post once. But when I opened the original post again, I could not find my comment or a provider-issued comment ID.

**A successful edit is not a verified publication.** Nor does the absence of a comment in one fresh read prove that delivery definitely failed. Repeating the action might create a duplicate later.

<figure>
<img src="/soclab-comment-delivery-receipt-en/soclab-delivery-receipt-en-1200x630.png" alt="An original conceptual illustration separating prepared, attempted but unconfirmed and provider-verified delivery. No product screenshot or real customer information." width="1200" height="630" loading="lazy" style="width:100%;height:auto;">
<figcaption>Three different evidence states, not three guesses about the platform's behavior. This diagram does not depict the current product interface.</figcaption>
</figure>

## The small failure I could actually observe

On October 26, 2026, I attempted one relevant comment on each of two separate public posts in my own community workflow. I checked the intended account, the source context and the message before interacting with the native comment editor.

The actual text fields matched the reviewed text. I attempted the native submission action. Yet independent reloads did not show the new comments, and neither attempt yielded a unique provider comment reference.

I cannot attribute the failure to a particular component. The background interface, authentication state, network handling or provider processing might be involved. Without reliable evidence I cannot call these attempts either accepted publications or confirmed non-delivery.

## Three states instead of one optimistic counter

| State | Evidence | Appropriate next step |
| :--- | :--- | :--- |
| PREPARED | Reviewed content, target, account and duplicate-prevention key | Validate permission before the initial attempt |
| ATTEMPTED_UNKNOWN | An attempt timestamp but no accepted provider ID | Hold retries and reconcile through permitted platform records |
| PROVIDER_VERIFIED | A real comment ID or unique permalink with observation time | Count the publication; measure human response separately |

The tempting shortcut is to name a local event "posted" when a button is clicked. It makes a dashboard appear productive but says nothing about what another person could actually see.

The opposite shortcut is unsafe too. If a comment is not visible immediately, clicking again might duplicate a delayed, successfully processed attempt. Unknown delivery must remain a distinct state.

## The operating decision I changed

I now treat account, channel, exact source post and message version as part of a single action claim. I preserve the reviewed text before the first attempt. If delivery becomes ambiguous, I do not resend it merely because it is missing from one page refresh.

Only a provider-issued reference or an independently verified public permalink should move that action into the published column. Any voluntary response from the other person needs a **different piece of evidence**. Posting a message, receiving a reply and having a meaningful conversation are three separate outcomes.

This is an operating principle, not a claim that every platform exposes the same receipt or retention history. Some results may remain unresolved.

## Why this matters for Social Relations Lab

**Social Relations Lab(소셜 릴레이션스 랩)** is an unfinished relationship-intelligence experiment. Its direction is to preserve the provenance and context of authorized social interactions over time so a human can make an informed next decision.

The validated initial scope is limited to a local pilot handling comments and owner replies from one specifically authorized Instagram Professional account. In [the earlier article on what comment evidence can tell us](/soclab-instagram-evidence-boundary-en/), I described the limits of interpreting incoming interactions.

This entry concerns the other side: proving that an **outgoing** action occurred at all. The state machine above is a design lesson from an operating experiment, not a claim that a customer-facing automated outbox, broader messaging access or public beta has been built.

## One falsifiable next question

Consider two synthetic work records. In the first, the operator has a click timestamp but no provider reference. In the second, the provider has returned a unique ID. Can a new operator correctly identify which action is verified, and resist retrying the ambiguous one?

I have not run that usability experiment or received real customer feedback on it. If the distinction is confusing, explaining uncertainty should come before adding more action-count charts.

The [related source-evidence note](/soclab-instagram-evidence-boundary-en/) and [blog index](/) offer further context. A full [Korean edition](/soclab-comment-delivery-receipt-ko/) is available.

---

*This is a firsthand observation from October 26, 2026. It does not expose a third party's conversation, assert that the comments were delivered, or claim any product feature was released.*

---
title: "Disconnecting an Account Is Not Deleting Its History"
description: "A Social Relations Lab developer note on the difference between disconnecting a social account, withdrawing a processing purpose and deleting saved evidence."
date: 2026-10-26
tags: ["Social Relations Lab", "Privacy UX", "Instagram", "Developer Notes", "Consent", "Data Lifecycle"]
permalink: /soclab-consent-disconnect-erase-en/
layout: default
lang: en
alternate_lang: ko
alternate_url: /soclab-consent-disconnect-erase-ko/
image: /soclab-consent-disconnect-erase-en/soclab-consent-choices-en-1200x630.png
image_width: 1200
image_height: 630
published: true
robots: "index, follow, max-image-preview:large"
seo:
  title: "Disconnect Is Not Delete | Social Relations Lab"
  description: "Why disconnect, consent withdrawal and data erasure need different evidence states, and how a small synthetic usability test might expose confusion."
  keywords: ["social account disconnect", "data erasure UX", "purpose consent", "stale summaries", "Social Relations Lab"]
---

> **한국어 판:** [인스타그램 연결을 끊으면 이전 분석도 사라져야 할까?](/soclab-consent-disconnect-erase-ko/)

While reviewing the current Social Relations Lab(소셜 릴레이션스 랩) prototype, I found a question I had been treating as too simple: when someone disconnects a social account, should all previously imported history disappear?

**I do not think disconnecting a provider, withdrawing permission for a purpose and deleting stored evidence are the same instruction.** Yet a screen with three separate control panels could be an even worse experience. The underlying states may need to be precise while the UI remains simple.

<figure>
<img src="/soclab-consent-disconnect-erase-en/soclab-consent-choices-en-1200x630.png" alt="Original synthetic conceptual diagram separating disconnect, withdrawal of analysis permission and erasure of saved evidence. Not a real account or implemented app interface." width="1200" height="630" loading="lazy" style="width:100%;height:auto;">
<figcaption>Three possible decisions with different consequences. This is a conceptual diagram, not a released product screen or policy guarantee.</figcaption>
</figure>

## What the prototype actually does today

As documented on October 26, 2026, the Mac-local prototype supports explicitly consented ingestion of selected user-provided Instagram JSON ZIP data, erasure of imported records and deletion of local workspaces. A separate official Instagram connector implementation includes provider-token session custody and a connection-revoke route. But actual operator Meta app configuration and a real approved account sign-in have not been validated.

The implementation status explicitly marks purpose-specific grants, source revision lineage and invalidation of derived summaries as incomplete. Consequently, what follows is **a design hypothesis about unfinished work**, not an announcement that production consent management is available.

Earlier I wrote about [the limits of incoming comment evidence](/soclab-instagram-evidence-boundary-en/) and [how an attempted outgoing comment is not a provider receipt](/soclab-comment-delivery-receipt-en/). This question is different: what remains usable after the basis for processing changes?

## Three separate outcomes

| User intent | Should new collection continue? | What happens to existing local evidence? |
| :--- | :--- | :--- |
| Disconnect the provider | No | Previously stored records need an explicit, separately explained retention decision |
| Withdraw permission for a particular analysis purpose | That analysis must stop | A previously computed summary for that purpose should be hidden or re-evaluated |
| Erase stored evidence | Do not use erased records | Related derived views must be removed or invalidated, with other workspaces untouched |

These are proposals for the prototype's contract, not a general statement of what every law or platform necessarily requires. Actual retention and lawful processing depend on specific consent, source rights, provider rules and the applicable policy.

## The strongest argument against my approach

People may not care whether a developer calls an operation a revoked grant or an invalidated projection. They want to know: is my account still connected, and is my data still here?

A simpler interface might offer only two clear choices: disconnect, or erase everything. The internal state model could still be exact. Making every internal distinction visible would risk confusing the same small operators I am trying to help.

This is why I would test comprehension before committing to a design. The goal is not to add controls; it is to prevent false beliefs about what the system may still hold or infer.

## A small test that does not need real accounts

Two fictional workspaces and three synthetic cases are enough to challenge the assumption:

1. **Disconnect:** future sync stops; a user can still tell whether previously authorized stored records remain.
2. **Purpose withdrawal:** a summary computed for the withdrawn purpose cannot appear as though it were still current and permitted.
3. **Erase:** imported events and dependent derived statements are invalidated without altering the other fictional workspace.

Compare a minimal two-choice UI against a more explicit state explanation. Ask whether a reader correctly predicts the outcome of all three cases and whether the interface creates any unintended irreversible deletion. A successful design would preserve source traceability, avoid cross-workspace changes and produce fewer wrong assumptions.

No such experiment has run. I sent the proposal to the existing Mac developer review path, where it remains pending. There has been no verified user feedback or implemented change.

## A useful memory needs a valid purpose

If relationship history is worth keeping, it should be possible to understand not only when a source record was observed but also why it remains available and which kinds of analysis are still permitted.

Social Relations Lab is an unfinished local relationship-evidence experiment. Its initial verified scope is narrow and tied to specifically authorized data. It is not a general public beta, a full private-message archive or an unrestricted social crawler.

You can read the [related developer notes](/) or the [Korean edition](/soclab-consent-disconnect-erase-ko/).

---

*Written from the documented local implementation scope and a new design hypothesis on October 26, 2026. This is not legal advice, a report of a real customer incident, or proof that the proposed functionality ships today.*

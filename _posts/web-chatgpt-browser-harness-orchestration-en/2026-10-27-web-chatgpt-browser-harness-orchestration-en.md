---
title: "Running Four AI Agents in ChatGPT Web: A Browser Harness Without Local LLMs"
description: "A practical architecture for managing ChatGPT web sessions with a browser harness, session supervisor, and local orchestrator without running a local LLM or calling a model API directly."
date: 2026-10-27
tags: ["ChatGPT Web", "Browser Harness", "AI Agents", "Orchestration", "Engineering"]
permalink: /web-chatgpt-browser-harness-orchestration-en/
layout: default
lang: en
alternate_lang: ko
alternate_url: /web-chatgpt-browser-harness-orchestration-ko/
image: /assets/img/web-chatgpt-browser-harness-orchestration/architecture.svg
image_width: 1100
image_height: 680
seo:
  title: "ChatGPT Web Agents Without Local LLMs: Browser Harness Design"
  description: "How a browser harness, session supervisor, and local orchestrator manage four ChatGPT web agent sessions, with evidence gates and practical limits."
  keywords: ["ChatGPT web agents", "browser harness", "session supervisor", "multi-agent orchestration", "no local LLM"]
---

> **한국어:** [웹 ChatGPT로 네 개의 AI 에이전트 운영하기](/web-chatgpt-browser-harness-orchestration-ko/)

**Short answer:** This experiment uses ordinary **ChatGPT web conversations as the agents' execution environment**. It does not run a local LLM or directly call a model API for inference. A local browser harness observes and interacts with the web UI, a session supervisor manages continuity, and an orchestrator tracks strategy and outcomes. This is not a promise of unlimited usage or unattended reliability.

## Why use the ChatGPT web interface for agents?

Model APIs are convenient to program against, but usage-based inference charges can grow with repeated work. Running local models requires hardware and model maintenance. I wanted to test whether an existing ChatGPT subscription could support a different workflow: separate web conversations acting as specialized agents, coordinated by local software.

The economic appeal is **no separate per-token model API bill within the subscription's permitted usage**, not unlimited inference. ChatGPT web usage limits, conversation length, authentication, and service terms still apply. I have not measured a universal cost advantage, and this is not an official replacement for a model API.

## What does the browser harness do?

The harness does not contain an inference engine. It handles browser connectivity, UI observation, permitted interactions, and verification of what the interface actually did.

A **session supervisor** sits above that browser interaction layer. It monitors responses, repeat cycles, checkpoints, conversation handoff, and guarded recovery. A **local orchestrator** coordinates goals, priorities, permissions, and evidence across several agent sessions.

<figure>
  <img src="/assets/img/web-chatgpt-browser-harness-orchestration/architecture.svg" alt="Architecture diagram with a local orchestrator, session supervisor, browser harness and four ChatGPT web sessions" width="1100" height="680" loading="lazy" style="width:100%;height:auto;">
  <figcaption>Figure 1. A conceptual responsibility map, not a claim that every proposed feature is fully implemented.</figcaption>
</figure>

The harness does not modify ChatGPT's servers. Because it interacts with a changing web interface, selectors, authentication state, and session continuity are operational concerns.

## Why four separate ChatGPT sessions?

Four independent conversations are used as specialized workspaces. For privacy, they are labeled Agent A through D rather than revealing actual project names, accounts, or local paths.

The agents work on different types of research, communication, content, and feedback. A shared orchestration layer can compare priorities and inspect records, but **choosing an action is not the same as performing an external write**. A publication or message must pass the appropriate account and authorization checks.

## What happens during one execution cycle?

<figure>
  <img src="/assets/img/web-chatgpt-browser-harness-orchestration/execution-cycle.svg" alt="Six-stage cycle from session observation to decision, execution, verification, evaluation and improvement" width="1100" height="680" loading="lazy" style="width:100%;height:auto;">
  <figcaption>Figure 2. The intended feedback loop includes verified actions and outcome analysis, not merely repeated prompts.</figcaption>
</figure>

1. **Observe:** Check browser and conversation state.
2. **Decide:** Select the next useful action based on goals and previous evidence.
3. **Execute:** Use a permitted browser or provider-specific route.
4. **Verify:** Inspect a native receipt, published URL, or provider result.
5. **Evaluate:** Distinguish a completed attempt from a meaningful response.
6. **Improve:** Feed verified findings into the next strategy cycle.

The system is still evolving. This diagram describes the operating model rather than claiming every step succeeds autonomously on every run.

## Why are prompts, posts, and outcomes different?

<figure>
  <img src="/assets/img/web-chatgpt-browser-harness-orchestration/evidence-ladder.svg" alt="Evidence ladder distinguishing local activity, verified external action and real-world outcomes" width="1100" height="680" loading="lazy" style="width:100%;height:auto;">
  <figcaption>Figure 3. A prompt, an external receipt, and a human response are different levels of evidence.</figcaption>
</figure>

A prompt being submitted does not prove a post was published. A delivered email does not prove it was read, accepted, or acted upon. A successful browser click does not prove the remote service committed the action.

That is why the system tracks **local activity**, **provider-verifiable external actions**, and **real-world outcomes** separately. Ambiguous external actions require inspection before retrying, especially when duplicates could cause harm.

## Did any of this lead to real-world results?

Yes. In one small independent information project supported by this operating experiment, the work progressed beyond drafts and outreach attempts to **external publication and substantive professional relationships**.

The project prepared specialist material, researched relevant publications and experts, and explored appropriate opportunities for collaboration. Its externally observable outcomes included:

- A contributed article actually published by an international specialist publication.
- A public resource link added by an external specialist organization.
- Content usage permission granted by a subject-matter expert.
- An unsolicited follow-up proposal from an expert for additional content and potential collaboration.
- A separate editorial collaboration that advanced beyond initial contact, without claiming final publication.

<figure>
  <img src="/assets/img/web-chatgpt-browser-harness-orchestration/external-outcomes.svg" alt="Anonymized progression from outreach to publication, expert trust, and new collaboration opportunities" width="1100" height="600" loading="lazy" style="width:100%;height:auto;">
  <figcaption>Figure 4. A privacy-preserving overview of externally verified milestones, not a measured conversion funnel or causal impact chart.</figcaption>
</figure>

The most interesting shift was **from approaching experts to receiving a new collaboration proposal initiated by an external expert**. That is a relationship outcome, not just another completed prompt.

These milestones do not prove the AI acted autonomously throughout. Human judgment, contributors, permissions, and editorial processes all mattered. They also do not prove mass adoption or formal institutional endorsement.

Project and partner names, subject area, URLs, and dates are intentionally omitted to avoid identification. The defensible claim is that **real external outcomes occurred during AI-assisted operations**, not that the harness alone caused them.

## What has been difficult in practice?

**A changing web UI.** Browser automation needs observations and verified receipts, not assumptions based on a button click.

**Conversation limits and handoff.** A successor chat must recover completed work, unresolved tasks, and duplicate-prevention state rather than merely copy the last message.

**Legacy and unified paths.** As more agent workspaces were added, older project-specific code and newer shared registries could coexist. Consistent state models and tests are necessary.

**Activity without progress.** A healthy repeat loop can still spend too much time researching or drafting. Real publication, dialogue, adoption, and feedback need independent measurement.

These are active engineering problems. A proposed state-machine design should not be confused with a fully deployed implementation.

## Frequently asked questions

### Does this use a local LLM?

No. The browser harness and orchestration workflow do not run a local inference model. ChatGPT web provides the model-backed conversations.

### Does it call the OpenAI model API directly?

Not for agent inference in this setup. APIs used to interact with other services are a separate concern.

### Is ChatGPT web usage unlimited?

No. Subscription entitlements, model-specific limits, conversation length, and service terms still apply. This architecture does not bypass those constraints.

### Does keeping sessions active guarantee useful results?

No. The system must separately verify external actions and genuine responses. A running session is an operational signal, not a business outcome.

## Closing note: a broke AI developer's architecture

The motivation was not entirely grand or theoretical. I wanted several agents, but paying a growing model API bill was unappealing, and building a local LLM workstation was not exactly cheap either.

Then I thought: **"I already pay for ChatGPT on the web. What if I use that as the agents' workspace?"**

One browser harness led to a session supervisor. That led to an orchestrator. Suddenly I was spending my evenings thinking about recovery, idempotency, and evidence ledgers.

I may have saved on API tokens only to pay the difference in debugging hours.

Still, the lesson has been valuable: **running multiple AI conversations is easy compared with making them work toward verifiable goals.**

If you have questions about browser harnesses, ChatGPT web sessions, handoff, or multi-agent orchestration, **leave a comment**. Alternative designs and practical criticism are welcome.

---

**Related reading:** [Connecting ChatGPT web to local development tools](/en-chatgpt-mcp-local-development-setup/)

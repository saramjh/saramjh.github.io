---
layout: project
portfolio_ui: true
title: "AI Agent Systems | Project case study"
description: "Local orchestration experiments around browser AI sessions, context continuity, deduplicated actions, and project-specific agent workflows."
slug: ai-agent-systems
order: 3
name: AI Agent Systems
subtitle: Browser-based agent operations and continuity
field: AI systems / operational reliability
summary: Local orchestration experiments around browser AI sessions, context continuity, deduplicated actions, and project-specific agent workflows.
image: /assets/images/portfolio/agent-architecture.svg
image_alt: Conceptual diagram of a local Session Supervisor coordinating five separately scoped project workers, including Dev
writing_url: /web-chatgpt-browser-harness-orchestration-en/
status: Evolving engineering work
stack:
  - Node.js
  - JavaScript
  - SQLite
  - Playwright
  - Model Context Protocol
---
## The problem

Browser-based AI agents have session boundaries, mutable external state, and action retries. Without continuity and evidence of execution, long-running work becomes fragile.

## What I built

An evolving set of local orchestration tools and experiments for keeping multiple project agents separated while tracking progress and recovering context between browser sessions.

## Engineering decisions

- Separate account identity, project scope, and execution authority.
- Distinguish requested actions from externally confirmed results.
- Preserve deduplication and opt-out rules while avoiding unwarranted global locks.
- Record observable test results instead of treating an architecture proposal as implemented behaviour.

## Further reading

Read the [browser-harness engineering write-up](/web-chatgpt-browser-harness-orchestration-en/) for the broader architecture. This is a changing development record, not a guarantee that every discussed feature is deployed.

For the practical problem of resuming work after a new coding session, see [how I use cokacremote with Git and checkpoints](/en-ai-coding-context-continuity-cokacremote/). It explains which state to trust first, rather than assuming older chat memory is current.

A separate quality problem comes up when agents edit user interfaces. In [my hands-on Impeccable review](/en-impeccable-review-ai-ui-design/), I show how critique and deterministic design checks helped with two products, including detector false positives. That is a design-review workflow, not a Session Supervisor feature.

---
title: "ChatGPT Text Chats Are Unlimited* — Codex Usage Is Not"
date: 2026-10-05
tags: ChatGPT, unlimited ChatGPT, ChatGPT text chats, Codex, Codex usage limits, Codex credits, AI coding, MCP
permalink: /en-chatgpt-unlimited-text-vs-codex-limits/
layout: default
lang: en
alternate_lang: ko
alternate_url: /chatgpt-unlimited-text-vs-codex-limits/
description: "OpenAI's current pricing table marks everyday text chats as unlimited* on Free, Go, Plus and Pro, while Codex has separate usage limits and credits. Here is what is actually unlimited and what is not."
excerpt: "The ordinary ChatGPT conversation UI and Codex do not use the same allowance structure. This post separates unlimited everyday text chats from model, tool and Codex limits using current OpenAI documentation."
seo:
  title: "ChatGPT Unlimited Text Chats vs Codex Usage Limits"
  description: "ChatGPT everyday text chats are unlimited* on personal plans, while Codex has separate usage limits. The exact difference between chat, tools, reasoning models and Codex."
  keywords:
    - ChatGPT unlimited messages
    - ChatGPT unlimited text chats
    - ChatGPT message limit
    - Codex usage limits
    - Codex credits
    - ChatGPT vs Codex
faq:
  - q: "Are ChatGPT text chats really unlimited?"
    a: "As of October 2026, OpenAI's pricing table marks Everyday text chats as Unlimited for Free, Go, Plus and Pro, subject to abuse-prevention guardrails. Files, images, voice, advanced reasoning models, tools and Codex can have separate limits."
  - q: "If ChatGPT chats are unlimited, is Codex unlimited too?"
    a: "No. Codex included with personal ChatGPT plans has separate usage limits that vary by plan, model and task. When you reach a limit you may need to wait for a reset or use credits if they are available to your account."
  - q: "Does unlimited chat mean one thread has unlimited context?"
    a: "No. Message allowance and context length are different. A long conversation is still subject to context, memory and session behavior; unlimited chat does not mean infinite memory in one thread."
image: /en-chatgpt-unlimited-text-vs-codex-limits/chatgpt-vs-codex-og.png
image_width: 1200
image_height: 630
---

# ChatGPT everyday text chats are unlimited*

**Codex usage is not. Those two limits are easy to conflate because they live under the same ChatGPT account.**

<p style="background: rgba(0, 120, 212, 0.08); border-left: 4px solid #0078d4; padding: 10px 14px; margin-bottom: 22px; border-radius: 4px; font-size: 0.95rem;">
  🌐 <strong>한국어 버전:</strong> <a href="/chatgpt-unlimited-text-vs-codex-limits/">웹 ChatGPT 일반 텍스트 채팅은 무제한이다*</a>
</p>

While writing about [using the ChatGPT web app as a control surface for my local Mac](/en-chatgpt-mcp-local-development-setup/), I rechecked a distinction that seems surprisingly easy to miss.

**The ordinary text-chat experience in ChatGPT is currently listed as unlimited* in OpenAI's pricing table.** Free, Go, Plus and Pro all show `Unlimited*` for `Everyday text chats`.

**Codex has a separate usage system.** Even when Codex is included in the same ChatGPT subscription, its allowance depends on plan, model, task complexity and the usage pool available to the account.

<picture>
  <source media="(max-width: 600px)" srcset="chat-vs-codex-mobile.svg">
  <img src="chat-vs-codex.svg" alt="Comparison between unlimited everyday ChatGPT text chats and separate Codex usage limits" width="1200" height="660" style="width:100%;height:auto;">
</picture>

## What "unlimited" actually means

The unlimited item in OpenAI's pricing table is **everyday text chats**.

As of October 2026, the personal-plan comparison is effectively:

| Feature | Free | Go | Plus | Pro |
|---|---|---|---|---|
| Everyday text chats | Unlimited* | Unlimited* | Unlimited* | Unlimited* |
| Codex | Limited / separate allowance | Limited / separate allowance | Expanded usage | Maximum usage |
| Files, images, voice, some tools | Separate limits | Separate limits | Expanded limits | Higher limits |

The asterisk matters: **unlimited text chats are still subject to abuse-prevention guardrails.**

It would be wrong to turn that into:

> Everything I do inside ChatGPT is unlimited.

It is not.

<picture>
  <source media="(max-width: 600px)" srcset="unlimited-is-not-everything-mobile.svg">
  <img src="unlimited-is-not-everything.svg" alt="Diagram separating unlimited everyday text chats from features with separate limits" width="1200" height="640" style="width:100%;height:auto;">
</picture>

File uploads, image generation, voice, data analysis, deep research, some advanced reasoning models and tools can have their own limits. OpenAI's Help Center explicitly separates unlimited everyday text chats from these other allowances.

## Codex uses a different allowance structure

The Codex pricing page has an explicit **usage limits** table.

For personal plans, Codex usage varies with the selected model and the work being done. The usage dashboard shows the remaining allowance and reset state. If you run out, the available options can include switching to a cheaper model, waiting for a reset, or using additional credits when the account is eligible.

A useful mental model is:

```text
ChatGPT web app
└─ Everyday text chats: unlimited*
   ├─ Some advanced models/reasoning: separate limits may apply
   ├─ Files/images/voice/tools: separate limits may apply
   └─ Codex: separate agentic usage allowance / credits
```

A long Codex task and a normal text turn in the ChatGPT web UI may both feel like "one request," but they do not use the same allowance model.

## Why this matters to my MCP setup

I did not look into this just to say "unlimited is cheaper."

My current workflow uses **the normal ChatGPT conversation UI at `chatgpt.com` in an internet browser** and connects that web product to my Mac through MCP. The MCP server can expose local files, terminal commands, Git, tests and browser automation.

That means a large part of the planning, review and decision-making loop can happen in ordinary ChatGPT conversation, while local tools are invoked only when needed.

This does **not** mean the ChatGPT web app replaces every Codex capability. Codex is a dedicated coding agent with purpose-built workflows and integrations.

The point is narrower: **you do not necessarily have to spend Codex allowance for every part of a coding workflow.** A browser ChatGPT + MCP architecture gives you another way to split conversation, reasoning and local execution.

One important caveat:

**OpenAI does not state that every MCP tool invocation is unlimited.** The pricing table says `Everyday text chats` are unlimited. I would not extend that claim to every tool, connector or future policy unless OpenAI documents it explicitly.

## Unlimited messages are not unlimited context

This is a separate problem.

**Unlimited chat does not mean one conversation thread remembers everything forever.**

Long-running conversations still run into context, memory, compaction and session-boundary issues. I noticed that problem more clearly after using the ChatGPT web app for sustained local development.

That led to a separate project: [I had installed Serena, Ponytail and claude-mem expecting better continuity, but the sessions still did not reliably carry the project state forward. I eventually built a deterministic context layer into cokacremote.](/en-ai-coding-context-continuity-cokacremote/)

So I now separate two questions:

- **Usage:** how many more messages or agent tasks can I run?
- **Continuity:** can a fresh session recover the correct decisions, constraints and current project state?

They are not the same problem.

## Why this is easy to miss

Both products live under the same account.

Codex is included with ChatGPT plans, and the ordinary ChatGPT interface uses the same subscription. From the user side, it is natural to assume there is one common message bucket.

The official documentation separates them:

- ChatGPT pricing: **Everyday text chats = Unlimited***
- Codex documentation: **Usage limits vary by plan**
- When Codex usage runs out: check the usage dashboard, wait for reset, or use available credits

That difference is significant when you design an AI coding workflow rather than just use one product at a time.

## My current reading of the policy

As of October 2026:

1. **Everyday text chats are unlimited* on ChatGPT Free, Go, Plus and Pro.**
2. **That does not make every model, tool, file upload, image, reasoning mode or agent feature unlimited.**
3. **Codex has a separate usage-limit and credit structure.**
4. **Unlimited messages do not mean infinite context in one thread.**
5. For development workflows, it is useful to treat **chat allowance, coding-agent allowance and context continuity as separate resources.**

OpenAI can change pricing and allowances, so this is not a permanent rule. The official pages below are the source of truth.

## Official sources

- [ChatGPT pricing — personal plans](https://chatgpt.com/pricing/)
- [Codex pricing and usage limits](https://chatgpt.com/codex/pricing/)
- [OpenAI Help — Using Codex with your ChatGPT plan](https://help.openai.com/en/articles/11369540-using-codex-with-your-chatgpt-plan)
- [OpenAI Help — What is ChatGPT? Web access is chatgpt.com](https://help.openai.com/en/articles/12677804-what-is-chatgpt-faq)
- [ChatGPT release notes — unlimited text chats and the Work/Codex distinction](https://help.openai.com/en/articles/6825453-chatgpt-release-notes)

*Unlimited is subject to OpenAI's abuse-prevention guardrails.*

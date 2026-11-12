---
title: "Inline recipe references in Spoonie's posts and comments"
description: "How Spoonie PRs #32 and #33 added inline recipe chips to posts and comments while retaining text storage and access controls."
date: 2026-11-12
tags: ["Spoonie", "Frontend", "Editor"]
permalink: /spoonie-inline-recipe-references-en/
layout: default
lang: en
alternate_lang: ko
alternate_url: /spoonie-inline-recipe-references-ko/
published: true
seo:
  title: "Building inline recipe references in Spoonie"
  description: "A first-party engineering note on inline recipe chips, serialization, and access checks in Spoonie PRs #32 and #33."
---

> 한국어: [Spoonie 레시피 본문과 댓글에 인라인 인용 칩을 넣은 과정](/spoonie-inline-recipe-references-ko/)

Spoonie added a way to reference another recipe directly inside a post or comment. [PR #32](https://github.com/saramjh/spoonie/pull/32) merged on November 12, 2026, and [PR #33](https://github.com/saramjh/spoonie/pull/33) followed with a related recipe-body fix.

## A reference inside the editor

Typing `[[` opens a recipe search and selection flow. The selected recipe appears as a clickable inline chip with its thumbnail and title. The editor uses ProseMirror/Tiptap inline nodes across post bodies, comments, and replies, with keyboard and touch selection supported in the implementation.

## Keeping the existing storage model

The editor serializes a selected recipe ID as `[[recipe:<UUID>]]` in text. This retains the existing text columns and save paths instead of introducing a separate storage model for each chip.

When content is displayed, the application resolves recipe references through the existing database row-level security (RLS) rules. A deleted or inaccessible recipe receives an unavailable state rather than a working link. Citation search also reuses the existing search function.

## What was verified

The PR records unit tests, type checking, a production build, and isolated editor checks. A JavaScript chunk served by the public Spoonie site contains the recipe citation UI labels. That is evidence of deployed client code; it does not establish real-user completion rates, citation adoption, or retention.

The subsequent [PR #34 engineering note](/spoonie-route-loading-citation-en/) covers route loading and changes to the citation search interface.

[Implementation PR #32](https://github.com/saramjh/spoonie/pull/32) · [Follow-up PR #33](https://github.com/saramjh/spoonie/pull/33) · [Visit Spoonie](https://spoonie.kr/)

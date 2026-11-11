---
title: "I repaired two data-loss boundaries in Spoonie"
description: "How I replaced separate post-and-poll writes with one PostgreSQL transaction, and reordered account deletion to avoid destroying images before the database operation succeeded."
date: 2026-11-11
tags: ["Spoonie", "PostgreSQL", "Supabase", "Transactions", "Data Integrity", "Product Engineering"]
permalink: /spoonie-atomic-poll-data-en/
layout: default
lang: en
alternate_lang: ko
alternate_url: /spoonie-atomic-poll-data-ko/
image: /spoonie-atomic-poll-data-en/spoonie-atomic-flow.svg
image_width: 1280
image_height: 650
published: true
seo:
  title: "How I made Spoonie's post-and-poll save atomic"
  description: "A first-party developer account of an atomic PostgreSQL save path, ownership checks, and safer deletion order in Spoonie PR #25, with explicit testing limits."
---

> 한국어판: [투표가 실패하면 글도 저장되지 않도록: Spoonie의 데이터 경계를 고쳤다](/spoonie-atomic-poll-data-ko/)

**I changed Spoonie's post-and-poll save from two independent writes to one PostgreSQL transaction.** In [PR #25, merged November 11, 2026](https://github.com/saramjh/spoonie/pull/25), I also reversed an account-deletion sequence that could remove a person's photos before the database deletion had succeeded. Both changes concern the result a user is left with when an operation fails.

## One save should have one committed result

Spoonie's Recipe and Recipeed editors previously committed the post first, then called a second RPC to save its optional poll. If the poll request failed, the post could remain without the intended poll. The form carried a separate error path, and mismatched draft keys made recovery of new and edited poll options less reliable.

The merged implementation calls `save_item_with_poll_atomic` to save the item and apply the poll operation inside one PostgreSQL transaction. For Recipes, it reuses the existing `save_recipe_atomic` routine. For the poll, it calls the existing `save_item_poll`, which already handles authorship and restrictions on changing options after votes. That avoids rebuilding those checks in a second SQL path. A failure rolls back the item and poll changes together.

The Recipeed branch writes only allowed fields for the authenticated owner, using `auth.uid()`. The function is `SECURITY INVOKER` and grants execution to `authenticated`, not anonymous callers. The editor marks its save complete and clears its draft only after this single operation succeeds.

<figure>
  <img src="/spoonie-atomic-poll-data-en/spoonie-atomic-flow.svg" alt="Developer-authored comparison: separate item and poll writes could leave partially saved content; the new PostgreSQL transaction commits both or rolls back. Account deletion now performs the database operation before file cleanup." width="1280" height="650" loading="lazy" style="display:block;width:100%;height:auto;">
  <figcaption>My diagram of the boundaries changed in PR #25. It is an implementation comparison, not a measured incident or usage report.</figcaption>
</figure>

## Delete the account record before deleting its photos

The previous deletion route removed image files before calling the database routine. If the latter failed, the account could still exist while its images were gone. Changing that order was more important than adding another retry button.

The new route checks the current user, the server-side secret and storage-read availability before attempting the database operation. Only after `delete_user_data` succeeds does it remove the user's stored images and avatar. On a database failure, it does not delete those files. If a later storage cleanup fails, the response identifies the partial outcome with `media_cleanup_pending`.

This is deliberately not described as a distributed transaction: the database operation and Storage API cleanup still have a boundary between them.

## What I could verify

The original PR records **363 passing Vitest tests across 82 files**, a TypeScript check and a successful Next.js 16 production build. It also documents a read-only check of the operating Supabase permissions and the applied migration for the new database function. I have not independently verified that the newly merged frontend code is active in the production member flow.

The technical lesson is a practical one: a product can appear to save correctly in the normal case while producing the wrong result after the second operation fails. Putting the commit boundary in the database, and handling file cleanup as a separately reported step, makes those failure states more explicit. The original work did not run a destructive end-to-end deletion against a real member account; its failure coverage is based on tests.

Related first-party records: [the public Recipe poll](/spoonie-live-polls-en/), [the Spoonie project](/portfolio/spoonie/), and [the merged source PR #25](https://github.com/saramjh/spoonie/pull/25).

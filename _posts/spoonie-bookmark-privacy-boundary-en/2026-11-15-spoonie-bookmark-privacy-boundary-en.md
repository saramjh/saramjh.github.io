---
title: "Keeping Spoonie's bookmark rows private at the database boundary"
description: "Spoonie PR #39 blocks anonymous reads of raw bookmark relationships while preserving owner-scoped saves and aggregate signals for recipe discovery."
date: 2026-11-15
tags: ["Spoonie", "Security", "Supabase", "PostgreSQL", "Privacy"]
permalink: /spoonie-bookmark-privacy-boundary-en/
layout: default
lang: en
alternate_lang: ko
alternate_url: /spoonie-bookmark-privacy-boundary-ko/
image: /spoonie-bookmark-privacy-boundary-en/bookmark-privacy-boundary-og.png
image_width: 1200
image_height: 630
published: true
seo:
  title: "Spoonie bookmark privacy: blocking anonymous row access"
  description: "How Spoonie PR #39 removes anonymous bookmark reads, keeps account-owned saves, and preserves aggregate recipe-discovery signals."
---

> 한국어판: [Spoonie 북마크의 공개 범위를 데이터베이스에서 제한했다](/spoonie-bookmark-privacy-boundary-ko/)

# A public recipe does not make its bookmark history public

Spoonie now blocks anonymous REST requests from reading raw bookmark rows. [PR #39](https://github.com/saramjh/spoonie/pull/39) merged on November 13, 2026. It removes the broad SELECT policy from `public.bookmarks` and revokes table-level SELECT from PostgreSQL's `anon` role. On November 15, the production migration ledger contained one application record, RLS was enabled, and an anonymous HTTP HEAD request returned 401.

A bookmark records a relationship between an account and an item. Publishing a recipe does not require publishing the identity of everyone who saved it. PR #39 enforces that distinction in the database.

## The old public read path

Row-level security (RLS) was enabled on `bookmarks`, but a broad policy named `All users can view bookmarks` remained in place alongside SELECT permission for the `anon` role. Together, those settings allowed an unauthenticated client to query raw user-to-item bookmark relationships.

The client repository filters its query with `.eq('user_id', userId)`. That limits the normal screen request. A caller can bypass the UI and send a REST request directly, so the database must enforce the same ownership rule.

## Anonymous reads are denied; owner access remains

The PR #39 migration closes the public read path with two statements:

```sql
drop policy if exists "All users can view bookmarks" on public.bookmarks;
revoke select on table public.bookmarks from anon;
```

The first removes the broad row-visibility policy. The second removes the anonymous role's table-level SELECT privilege.

The existing authenticated policy, `Users can manage their bookmarks`, remains in place. Its `USING` and `WITH CHECK` clauses both require `user_id = auth.uid()`, so a signed-in user can manage only rows owned by that account. The production database also retains authenticated SELECT, INSERT, UPDATE and DELETE privileges.

<figure>
  <img src="/spoonie-bookmark-privacy-boundary-en/bookmark-privacy-boundary.svg" alt="Spoonie bookmark access diagram. Anonymous requests cannot read raw rows; authenticated users manage rows matching auth.uid; recipe discovery uses aggregate save counts rather than saver identities." width="1200" height="630" loading="lazy" style="display:block;width:100%;height:auto;">
  <figcaption>An original diagram based on PR #39 and the production database state.</figcaption>
</figure>

## Recipe discovery uses counts rather than saver identities

Blocking anonymous access to raw bookmark rows leaves the product's aggregate save signals available.

`get_explore` uses the count of distinct non-owner accounts that saved each public recipe during the previous 30 days as one ranking signal. It does not return those accounts. `get_recipe_activity` returns a save count to the authenticated owner of a recipe and omits the saver list.

Public discovery can therefore use aggregate activity while raw bookmark relationships remain scoped to their owners.

## Production verification

The production database records migration `20261113054444` once. RLS is enabled on `public.bookmarks`; `anon` has no SELECT privilege; authenticated SELECT, INSERT, UPDATE and DELETE privileges remain.

| Check | Production result |
|---|---|
| Migration `20261113054444` | One recorded application |
| RLS on `public.bookmarks` | Enabled |
| Anonymous SELECT privilege | Revoked |
| Authenticated SELECT / INSERT / UPDATE / DELETE | Retained |
| SELECT policies available to `anon` | 0 |
| Anonymous REST request | HTTP 401 |

The PR adds a Vitest contract test for the migration and the user-scoped client query. The live HTTP HEAD check returned 401 and transferred no bookmark rows.

I did not run a production end-to-end test with two real member accounts switching sessions. The checks here cover the migration record, database permissions and anonymous REST access.

## Source and related work

- [Spoonie PR #39: prevent anonymous bookmark relationship disclosure](https://github.com/saramjh/spoonie/pull/39)
- [Merge commit](https://github.com/saramjh/spoonie/commit/34603198d682a148e370c78c052ee139dd19b0a2)
- [Spoonie project overview](/portfolio/spoonie/)
- [Separating likes and saves by viewer](/spoonie-viewer-cache-isolation-en/)
- [Removing newly private posts from other viewers' caches](/spoonie-privacy-cache-transition-en/)
- [Spoonie](https://spoonie.kr/)

---
title: "Spoonie 북마크의 공개 범위를 데이터베이스에서 제한했다"
description: "Spoonie PR #39에서 익명 북마크 행 조회를 차단하고, 로그인 사용자의 본인 북마크 관리와 레시피 탐색용 집계 수치는 유지했다."
date: 2026-11-15
tags: ["Spoonie", "보안", "Supabase", "PostgreSQL", "개인정보"]
permalink: /spoonie-bookmark-privacy-boundary-ko/
layout: default
lang: ko
alternate_lang: en
alternate_url: /spoonie-bookmark-privacy-boundary-en/
image: /spoonie-bookmark-privacy-boundary-ko/bookmark-privacy-boundary-og.png
image_width: 1200
image_height: 630
published: true
seo:
  title: "Spoonie 북마크 개인정보 보호: 익명 SELECT 차단과 RLS"
  description: "Spoonie PR #39의 데이터베이스 권한 변경, 계정별 북마크 접근 유지, 운영 REST API 검증을 정리한다."
---

> English: [Keeping Spoonie's bookmark rows private at the database boundary](/spoonie-bookmark-privacy-boundary-en/)

# 공개 레시피라도 저장한 사람의 기록은 공개되지 않는다

Spoonie의 데이터베이스는 익명 REST 요청에 북마크 원본 행을 반환하지 않는다. [PR #39](https://github.com/saramjh/spoonie/pull/39)는 2026년 11월 13일 병합됐다. 이 변경은 `public.bookmarks`의 광범위한 SELECT 정책을 제거하고 PostgreSQL `anon` 역할의 테이블 SELECT 권한을 철회한다. 11월 15일 운영 마이그레이션 기록에서 버전 `20261113054444`가 확인됐고, `public.bookmarks`의 RLS는 활성화되어 있었다. 익명 HTTP HEAD 요청은 401을 반환했다.

북마크에는 어떤 계정이 어떤 글을 저장했는지 나타나는 관계 정보가 들어 있다. 레시피를 공개하는 일과 저장한 사람의 기록을 공개하는 일은 별개다. 이번 수정은 데이터베이스가 이 경계를 직접 강제하도록 했다.

## 기존 익명 조회 경로

`bookmarks` 테이블에는 Row Level Security(RLS)가 활성화되어 있었지만, `All users can view bookmarks`라는 공개 SELECT 정책과 `anon` 역할의 SELECT 권한이 함께 남아 있었다. 이 설정에서는 로그인하지 않은 클라이언트도 사용자와 글 사이의 북마크 관계 행을 조회할 수 있었다.

클라이언트의 `bookmark-repository.ts`는 `.eq('user_id', userId)` 조건으로 본인 북마크를 요청한다. 이 조건은 일반 화면의 조회 범위를 제한한다. 호출자는 브라우저 UI를 거치지 않고 REST API에 직접 요청할 수 있으므로, 데이터베이스도 같은 소유권 조건을 적용해야 한다.

## 익명 조회는 막고 본인 데이터 관리는 유지했다

PR #39의 마이그레이션은 두 가지 변경으로 공개 조회 경로를 닫는다.

```sql
drop policy if exists "All users can view bookmarks" on public.bookmarks;
revoke select on table public.bookmarks from anon;
```

첫 문장은 모든 사용자에게 열려 있던 행 조회 정책을 제거한다. 두 번째 문장은 익명 역할이 테이블을 직접 읽을 수 있는 권한을 철회한다.

기존 로그인 사용자용 `Users can manage their bookmarks` 정책은 그대로 유지했다. `USING`과 `WITH CHECK` 모두 `user_id = auth.uid()`를 확인하므로 사용자는 자기 계정에 속한 북마크 행만 관리할 수 있다. 운영 DB에서도 인증 사용자에게 SELECT, INSERT, UPDATE, DELETE 권한이 남아 있는 것을 확인했다.

<figure>
  <img src="/spoonie-bookmark-privacy-boundary-ko/bookmark-privacy-boundary.svg" alt="Spoonie 북마크 접근 경계 도식. 익명 역할의 원본 행 조회는 차단되고, 로그인 사용자는 auth.uid와 일치하는 본인 행만 관리하며, 탐색 기능은 저장자 목록 대신 집계 수치를 사용한다." width="1200" height="630" loading="lazy" style="display:block;width:100%;height:auto;">
  <figcaption>PR #39와 운영 데이터베이스 상태를 바탕으로 직접 작성한 접근 경계 도식.</figcaption>
</figure>

## 레시피 탐색에는 저장자 목록 대신 집계값을 사용한다

북마크 원본 행에 대한 익명 접근을 막아도 레시피 탐색에 필요한 저장 신호는 유지할 수 있다.

`get_explore`는 레시피 소유자를 제외하고 최근 30일 동안 공개 레시피를 저장한 고유 계정 수를 순위 계산에 반영한다. 저장자 계정 목록은 반환하지 않는다. `get_recipe_activity`는 인증된 레시피 소유자에게 자기 레시피의 저장 수를 제공하고 저장자 목록은 반환하지 않는다.

따라서 공개 탐색에는 저장 수를 반영하고, 북마크 원본 관계 행은 계정 소유 범위에 남겨 둔다.

## 운영 환경에서 확인한 결과

운영 Supabase에는 마이그레이션 `20261113054444` 적용 기록이 한 건 있다. `public.bookmarks`의 RLS는 활성화되어 있고 `anon`의 SELECT 권한은 없다. `authenticated`에는 SELECT, INSERT, UPDATE, DELETE 권한이 남아 있다.

| 검증 항목 | 운영 결과 |
|---|---|
| 마이그레이션 `20261113054444` | 적용 기록 1건 |
| `public.bookmarks` RLS | 활성화 |
| 익명 SELECT 권한 | 철회 |
| 인증 사용자 SELECT / INSERT / UPDATE / DELETE | 유지 |
| `anon`에 적용되는 SELECT 정책 | 0개 |
| 익명 REST 요청 | HTTP 401 |

PR에는 마이그레이션 SQL과 사용자별 클라이언트 조회를 확인하는 Vitest 계약 테스트가 추가됐다. 운영 Supabase에 보낸 HTTP HEAD 요청은 401을 반환했다. HEAD 응답으로 북마크 행 데이터를 내려받지는 않았다.

실제 회원 두 계정으로 운영 환경에서 로그인과 계정 전환을 반복하는 E2E 테스트는 실행하지 않았다. 이번 검증은 마이그레이션 기록, 데이터베이스 권한·정책, 익명 REST 요청의 차단 여부를 확인한 범위다.

## 원본 근거와 관련 작업

- [Spoonie PR #39: 익명 북마크 관계 정보 조회 차단](https://github.com/saramjh/spoonie/pull/39)
- [병합 커밋](https://github.com/saramjh/spoonie/commit/34603198d682a148e370c78c052ee139dd19b0a2)
- [Spoonie 프로젝트 소개](/portfolio/spoonie/)
- [계정별 좋아요·저장 캐시 분리](/spoonie-viewer-cache-isolation-ko/)
- [비공개 전환 글을 다른 계정의 캐시에서 제거하기](/spoonie-privacy-cache-transition-ko/)
- [Spoonie](https://spoonie.kr/)

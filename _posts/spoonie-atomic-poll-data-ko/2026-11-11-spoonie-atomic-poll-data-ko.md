---
title: "투표가 실패하면 글도 저장되지 않도록: Spoonie의 데이터 경계를 고쳤다"
description: "Spoonie 레시피·레시피드의 글과 투표를 하나의 PostgreSQL 트랜잭션으로 저장하고, 회원 탈퇴 중 사진 손실을 줄이기 위해 삭제 순서를 수정한 PR #25의 개발 기록."
date: 2026-11-11
tags: ["Spoonie", "PostgreSQL", "Supabase", "트랜잭션", "데이터 무결성", "제품 개발"]
permalink: /spoonie-atomic-poll-data-ko/
layout: default
lang: ko
alternate_lang: en
alternate_url: /spoonie-atomic-poll-data-en/
image: /spoonie-atomic-poll-data-ko/spoonie-atomic-flow.svg
image_width: 1280
image_height: 650
published: true
seo:
  title: "스푸니 투표 저장 원자성과 회원 탈퇴 데이터 손실 방지 설계"
  description: "글만 저장되고 투표가 사라지는 문제를 단일 트랜잭션으로 해결한 코드와, 회원 탈퇴 시 사진 삭제 순서를 바꾼 이유를 원본 PR #25로 설명합니다."
---

> English: [I repaired two data-loss boundaries in Spoonie](/spoonie-atomic-poll-data-en/)

**투표를 포함한 글이 반쪽만 저장될 수 있던 경로를 한 번의 데이터베이스 트랜잭션으로 바꿨다.** 2026년 11월 11일 병합한 [Spoonie PR #25](https://github.com/saramjh/spoonie/pull/25)에서 레시피와 레시피드의 글·투표 저장을 묶고, 회원 탈퇴가 실패했는데 사진부터 사라질 수 있었던 순서도 수정했다. 사용자가 실제 기록을 맡기는 제품에서 필요한 것은 저장 버튼의 반응보다 실패했을 때의 결과다.

## 글 저장 성공과 투표 저장 실패가 서로 다른 결과였던 이유

이전에는 글을 먼저 DB에 확정하고 투표를 별도 RPC로 저장했다. 두 번째 요청만 실패하면 글은 남고 투표는 빠질 수 있었다. 폼에서는 복구 분기가 늘어났고, 새 글과 수정 글의 초안 키도 달라 선택지 복원을 일관되게 보장하기 어려웠다.

새 `save_item_with_poll_atomic` 함수는 글과 투표 작업을 PostgreSQL 트랜잭션 하나에서 수행한다. 레시피는 기존 `save_recipe_atomic` 함수를 재사용하고, 투표는 소유권과 투표 후 선택지 변경 제한을 이미 처리하던 `save_item_poll`을 호출한다. 다른 권한 검사 체계를 새로 복제하지 않았다. 작업 중 오류가 발생하면 두 변경 모두 롤백된다.

레시피드 저장도 작성자 `auth.uid()`에 한정하고 허용된 필드만 변경한다. `SECURITY INVOKER`와 `authenticated` 전용 실행 권한을 사용했으며, 익명·비로그인 호출을 제한한다. 폼은 한 번의 저장 성공 이후에만 완료 상태를 기록하고 초안을 지운다.

<figure>
  <img src="/spoonie-atomic-poll-data-ko/spoonie-atomic-flow.svg" alt="이전에는 글 저장과 투표 저장을 따로 수행해 부분 저장 위험이 있었고, 개선 후 하나의 PostgreSQL 트랜잭션으로 함께 확정하거나 롤백한다. 회원 탈퇴는 DB 작업을 먼저 확인한 뒤 사진을 정리하도록 순서를 변경했다는 원본 개발 도식" width="1280" height="650" loading="lazy" style="display:block;width:100%;height:auto;">
  <figcaption>PR #25를 바탕으로 직접 그린 저장·삭제 순서 비교. 실제 장애 발생 건수나 이용자 행동 통계가 아니다.</figcaption>
</figure>

## 탈퇴가 실패했을 때 사진은 남아 있어야 한다

같은 PR에서 회원 탈퇴 순서도 손봤다. 예전 API는 인증 후 저장소 사진을 먼저 영구 삭제하고 계정 DB 정리를 나중에 시도했다. DB 작업이 실패하면 계정은 남아도 사진은 없어질 수 있는 구조였다.

변경한 경로에서는 먼저 본인 인증과 서버 전용 키, Storage 조회 가능 여부를 확인한다. 그다음 `delete_user_data` DB 작업을 수행하고, 성공했을 때만 이미지와 아바타를 정리한다. DB 실패 이전에는 저장소 삭제를 실행하지 않는다. DB 삭제 후 사진 정리에 문제가 생기면 `media_cleanup_pending`으로 부분 완료 상태를 구분해 알린다. DB와 외부 Storage API 전체가 하나의 트랜잭션이 되는 것은 아니다.

## 구현을 어떻게 검증했나

병합 PR에는 Vitest **82개 파일·363개 테스트 통과**, TypeScript 검사, Next.js 16 프로덕션 빌드 결과가 기록돼 있다. 운영 Supabase의 기존 권한 정의를 읽기 전용으로 확인하고, 신규 함수 마이그레이션이 운영 DB에 적용됐으며 비로그인 실행 권한이 없다는 검증도 PR에 남겼다. 다만 이 글에서 운영 프런트엔드의 새 호출 경로까지 독립적으로 확인한 것은 아니다.

이번 수정으로 내가 보여주려는 것은 기능을 더한 속도가 아니라 **실패 결과를 설계하는 능력**이다. 한 요청의 성공이 다른 요청의 성공을 보장하지 않을 때, 데이터의 확정 경계를 어디에 둘지 먼저 결정해야 한다. 실제 회원의 탈퇴·사진 삭제를 수행하는 파괴적 운영 E2E는 진행하지 않았으며, 그 범위는 실패 시나리오 테스트로 제한했다.

관련 기록: [공개 레시피의 투표 컴포넌트](/spoonie-live-polls-ko/), [Spoonie 프로젝트](/portfolio/spoonie/), [저장·탈퇴 수정 원본 PR #25](https://github.com/saramjh/spoonie/pull/25).

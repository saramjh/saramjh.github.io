---
title: "Spoonie 공개 레시피 투표를 구현하고 회원 글쓰기로 확장한 과정"
description: "실제 Spoonie 공개 레시피에서 투표 데이터가 확인된다. PR #19·#20에 남은 구현, 데이터 접근 설계, 운영 검증의 경계를 정리했다."
date: 2026-11-11
tags: ["Spoonie", "레시피 투표", "제품 개발", "Supabase", "접근 제어"]
permalink: /spoonie-live-polls-ko/
layout: default
lang: ko
alternate_lang: en
alternate_url: /spoonie-live-polls-en/
image: /spoonie-live-polls-ko/spoonie-poll-flow.svg
image_width: 1280
image_height: 560
published: true
seo:
  title: "Spoonie 레시피 투표 개발: 공개 화면과 회원 글쓰기 공용화"
  description: "Spoonie 공개 레시피에서 실제 투표를 확인하고, 레시피·레시피드 공용 투표를 만든 PR #19·#20의 코드 및 데이터 접근 제어를 살펴본다."
---

> English: [Building a real recipe poll in Spoonie and opening it to member posts](/spoonie-live-polls-en/)

**Spoonie의 공개 레시피에 실제 투표를 연결했다.** 조리법을 읽는 사람이 음식에 관한 취향을 선택하고, 저장된 선택 수를 확인할 수 있게 한 기능이다. [공개 시범 레시피](https://spoonie.kr/recipes/6eaa37a1-6c0f-4841-aadd-7a2d980fbdbf)에서는 질문과 두 선택지, 서버가 반환한 집계값을 확인할 수 있다. 2026년 11월 11일의 조회 응답에는 활성 투표와 총 1표가 있었다. 이는 그날의 조회 결과다. 누가 참여했는지나 이용이 늘고 있는지는 이 데이터로 판단할 수 없다.

기능은 두 번에 걸쳐 구현했다. [PR #19](https://github.com/saramjh/spoonie/pull/19)에서는 공식 큐레이터가 올린 공개 레시피에 투표를 연결했다. 같은 날 병합한 [PR #20](https://github.com/saramjh/spoonie/pull/20)에서는 이를 일반 회원의 레시피·레시피드 작성 화면에도 선택적으로 추가할 수 있는 공용 컴포넌트로 확장했다. 두 PR의 병합 시각은 각각 2026년 11월 11일 02:47 UTC와 03:25 UTC다.

## 레시피 본문과 질문을 나눈 이유

레시피 소개글에는 독자의 취향을 묻는 문장이 들어갈 수 있다. 이 질문이 글 속에만 있으면 선택지를 바꾸거나 결과를 집계하기 어렵다. 나는 투표 데이터를 레시피 본문과 별도로 저장하는 방식을 택했다.

첫 구현의 범위는 레시피마다 질문 하나, 선택지 2~4개였다. 투표를 설정하지 않은 레시피의 내용은 그대로 두었다. 원작자가 작성한 레시피 설명과 출처 표시도 수정하지 않았다.

<figure>
  <img src="/spoonie-live-polls-ko/spoonie-poll-flow.svg" alt="공개 레시피 또는 레시피드와 선택형 질문, 로그인 후 투표, 집계 응답을 구분한 개발자 제작 데이터 흐름도" width="1280" height="560" loading="lazy" style="display:block;width:100%;height:auto">
  <figcaption>원본 PR #19·#20의 코드 구조를 설명하기 위해 제작한 도식. 제품 화면 캡처나 실제 사용량 그래프는 아니다.</figcaption>
</figure>

다음 단계에서는 같은 질문 입력 방식을 레시피와 레시피드 작성·수정에 적용했다. 공통 PollComposer는 평소 접힌 상태로 있다가 작성자가 원할 때만 질문을 추가하도록 설계했다. 상세 페이지는 ItemPoll을 통해 해당 글에 저장된 질문을 표시한다. 투표는 글 게시의 필수 항목이 아니다.

글과 투표 저장이 별도의 작업이라는 점도 처리했다. 본문 저장은 성공했으나 투표 저장이 실패하면 둘을 모두 실패한 것처럼 표시해서는 안 된다. 작성자가 어떤 항목을 다시 수정해야 하는지 알 수 있도록 개별 실패 상태와 복구 경로를 구현했다.

## 투표자 명단 없이 결과를 보여주기

질문을 읽는 사람에게 필요한 정보는 각 선택지에 몇 표가 기록됐는지다. 그 표를 행사한 계정의 식별 정보를 함께 공개할 필요는 없다.

[첫 PR의 데이터 설계](https://github.com/saramjh/spoonie/pull/19)는 집계 조회와 로그인 회원의 투표 저장을 분리하고 투표자 원본 테이블의 직접 접근을 제한한다. [일반 회원 확장 PR](https://github.com/saramjh/spoonie/pull/20)에서는 동일한 모델을 두 글 유형에 적용하는 item_polls, item_poll_votes 구조로 정리했다. 회원당 한 개의 현재 투표만 기록하고, 선택을 변경할 수 있으며, 투표가 발생한 뒤에는 질문의 선택지를 변경하지 못하게 하는 조건이 있다.

이 설계로 공개 레시피는 질문, 선택지, 항목별 합계와 총 표 수를 전달한다. 계정별 투표 내역은 공개 집계 응답에 포함하지 않는다. 구현 테스트에는 입력 검증과 집계 일치성, 권한 제어가 포함돼 있다.

## 공개된 것과 남은 검증

실제 [시범 레시피](https://spoonie.kr/recipes/6eaa37a1-6c0f-4841-aadd-7a2d980fbdbf)가 HTTP 200으로 열리고 서버 렌더링 응답에 initialPoll이 포함된 것을 확인했다. 조회 당시 선택지는 두 개, 총 투표 수는 한 개였다. 값은 이후 변경될 수 있다.

PR #20은 회원의 작성·수정 UI를 포함한 채 저장소 main에 병합됐다. 다만 이번 확인에서는 일반 회원 계정으로 실제 운영 사이트에서 글을 작성하고 투표 저장까지 완료하는 전 과정을 독립적으로 실행하지 않았다. 회원 작성 기능의 운영 배포와 종단 간 동작은 추가 확인이 필요하다.

공개 투표 하나를 만들어 실제 데이터를 제공하는 일과 이를 다양한 작성자의 글에 적용할 수 있도록 설계하는 일은 서로 다른 개발 과제였다. 그 이전의 출발점인 [재료량 계산기에서 Spoonie로 발전한 과정](/recipe-calc-to-spoonie-origin-ko/)도 별도로 기록했다.

원본 근거: [투표 첫 구현 PR #19](https://github.com/saramjh/spoonie/pull/19), [일반 회원 공용화 PR #20](https://github.com/saramjh/spoonie/pull/20), [실제 공개 레시피](https://spoonie.kr/recipes/6eaa37a1-6c0f-4841-aadd-7a2d980fbdbf).

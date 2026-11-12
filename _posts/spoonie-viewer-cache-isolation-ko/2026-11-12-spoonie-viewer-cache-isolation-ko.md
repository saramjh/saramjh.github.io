---
title: "Spoonie 계정별 좋아요·저장 캐시 분리"
description: "Spoonie PR #37의 계정별 캐시 분리, 늦게 도착한 응답 처리와 운영 코드 검증 범위."
date: 2026-11-12
tags: ["Spoonie", "Frontend", "Caching"]
permalink: /spoonie-viewer-cache-isolation-ko/
layout: default
lang: ko
alternate_lang: en
alternate_url: /spoonie-viewer-cache-isolation-en/
published: true
seo:
  title: "Spoonie 계정별 좋아요·저장 캐시 분리"
  description: "Spoonie PR #37에서 사용자별 좋아요·저장 캐시와 비동기 응답 처리를 정비한 개발 기록."
---

> English: [Separating likes and saves by viewer in Spoonie](/spoonie-viewer-cache-isolation-en/)

Spoonie의 좋아요·저장 화면 상태가 계정 전환 후 이전 사용자와 섞이지 않도록 캐시 구조를 수정했다. [PR #37](https://github.com/saramjh/spoonie/pull/37)은 2026년 11월 12일 병합됐고, 공개 서비스의 JavaScript에서도 계정별 캐시 키 구성 코드를 확인했다.

## 계정별 화면 상태가 필요했던 이유

레시피 본문과 달리 좋아요·저장 버튼의 화면 캐시는 동일한 글 ID를 기준으로 공유될 수 있었다. 계정 전환 도중 이전 요청이 늦게 완료되면 현재 화면에 이전 사용자의 상태가 나타날 위험도 있었다.

## 변경한 구현

- 화면용 캐시 키를 `itemDetail|사용자ID|글ID`로 분리하고, 초기 인증 중에는 SWR 조회를 기다리도록 했다.
- 목록의 낙관적 갱신과 늦게 도착한 응답을 현재 사용자 기준으로 제한했다.
- 기존 세션 정보를 사용해 중복 사용자·프로필 조회를 줄였다.
- 선택적 좋아요·저장 조회에 실패해도 레시피 본문, 재료, 조리 단계가 사라지지 않도록 처리했다.

설치된 SWR 2.3.4 구조에 맞춘 회귀 테스트가 추가됐다. 원본 PR 작성자는 Vitest 391개 테스트 통과를 보고했다. Dev가 이 테스트를 별도로 재실행한 결과는 아니다.

## 운영 코드에서 확인한 내용

[레시피 상세 페이지](https://spoonie.kr/recipes/aab1f6da-d7d3-4ed0-bbc7-10dae3515718)와 [레시피 목록](https://spoonie.kr/recipes)은 확인 당시 HTTP 200을 반환했다. 두 경로의 Next.js 번들에 사용자별 캐시 키 구성과 사용자 범위의 목록 필터링 코드가 포함돼 있었다.

이 결과는 해당 구현 코드가 운영 환경에서 제공되고 있다는 근거다. 서로 다른 두 계정의 실제 로그인·전환 테스트와 모바일 사용성 평가, 이용자 유지율 측정은 아직 확인되지 않았다.

[이전 Spoonie 작성자 헤더 정비](/spoonie-author-header-consistency-ko/)는 화면의 정보 배치를 다룬다. 이번 변경은 개인별 화면 상태의 캐시 경계를 다룬다.

[변경 코드](https://github.com/saramjh/spoonie/pull/37) · [Spoonie](https://spoonie.kr/)

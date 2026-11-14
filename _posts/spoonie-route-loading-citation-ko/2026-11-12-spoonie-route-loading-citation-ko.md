---
title: "Spoonie의 화면 전환 로딩과 레시피 인용 검색 정비"
description: "Spoonie PR #34와 #42의 화면 전환 피드백, 목적지 스켈레톤, 레시피 인용 검색 개선 기록."
date: 2026-11-12
tags: ["Spoonie", "Frontend", "User Experience"]
permalink: /spoonie-route-loading-citation-ko/
layout: default
lang: ko
alternate_lang: en
alternate_url: /spoonie-route-loading-citation-en/
published: true
modified: 2026-11-14
seo:
  title: "Spoonie 화면 전환 로딩·레시피 인용 검색 개선"
  description: "Spoonie PR #34의 레시피 인용 검색과 PR #42의 즉시 화면 전환 스켈레톤, 배포 확인 범위."
---

> English: [Route loading and recipe citation search in Spoonie](/spoonie-route-loading-citation-en/)

Spoonie의 화면 전환 로딩과 레시피 인용 검색 인터페이스를 정비했다. [PR #34](https://github.com/saramjh/spoonie/pull/34)는 2026년 11월 12일 병합됐으며, 변경된 코드가 공개 서비스의 JavaScript에도 포함된 것을 확인했다.

## 사용자가 마주하는 두 지점

레시피를 찾다가 다른 화면으로 이동할 때는 전환 상태를 이해할 수 있어야 한다. 다른 레시피를 인용하려는 순간에는 검색 결과를 확인하고 선택하는 흐름이 분명해야 한다. 이번 변경은 이 두 접점을 다룬다.

## 구현과 검증 범위

병합된 변경에는 화면 전환 로딩 처리와 레시피 인용 검색 UI 정비가 포함된다. 원본 코드와 운영 환경에서 제공되는 JavaScript를 대조해 변경 코드의 배포를 확인했다.

다만 공개 번들에 코드가 있다는 사실만으로 실제 체감 속도 개선이나 인용 기능의 사용량을 알 수는 없다. 그런 수치는 별도로 측정되지 않았다.

Spoonie의 다른 화면 상태 문제는 [계정별 좋아요·저장 캐시 분리](/spoonie-viewer-cache-isolation-ko/)에서 다뤘다.

## 11월 14일 후속 개선: 목적지 화면을 먼저 보여주기

기존 진행 막대만으로는 응답이 늦을 때 페이지를 눌렀다는 피드백이 부족했다. [PR #42](https://github.com/saramjh/spoonie/pull/42)의 재현 테스트에서는 `/search` 서버 응답을 늦추자 이전 홈 화면이 700ms 넘게 남았다. 이 문제를 해결하기 위해 내부 화면 이동이 시작되는 즉시 목적지 형태의 스켈레톤을 표시하도록 바꿨다.

검색 화면으로 이동하면 검색창과 필터 자리부터, 레시피·게시물 상세로 이동하면 상세 화면의 자리 표시부터 보인다. 상단 진행 막대는 그대로 두고, 진행 중에도 하단 메뉴로 다른 화면을 선택할 수 있게 했다. 검색 필터처럼 주소의 쿼리만 바뀌는 경우에는 전체 화면을 가리지 않는다.

지연된 경로를 재현한 로컬 Chromium 테스트에서 스켈레톤은 90·200·500·950ms에 표시됐고, 새 화면이 준비되자 사라졌다. 회귀 테스트 405개와 별도 미디어 테스트 6개도 통과했다. 11월 14일 확인한 [운영 Spoonie](https://spoonie.kr/)의 `app/layout` JavaScript는 PR #42 Netlify 미리보기와 바이트 단위로 같았으며, `data-route-feedback` 구현을 포함했다. 실제 방문자의 체감 속도나 이탈률 변화는 아직 측정하지 않았다.

[원본 변경 사항](https://github.com/saramjh/spoonie/pull/34) · [Spoonie](https://spoonie.kr/)

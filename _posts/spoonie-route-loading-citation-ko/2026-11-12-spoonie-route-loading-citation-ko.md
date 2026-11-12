---
title: "Spoonie의 화면 전환 로딩과 레시피 인용 검색 정비"
description: "Spoonie PR #34에서 화면 전환 로딩과 레시피 인용 검색 UI를 수정한 개발 기록."
date: 2026-11-12
tags: ["Spoonie", "Frontend", "User Experience"]
permalink: /spoonie-route-loading-citation-ko/
layout: default
lang: ko
alternate_lang: en
alternate_url: /spoonie-route-loading-citation-en/
published: true
seo:
  title: "Spoonie 화면 전환 로딩·레시피 인용 검색 개선"
  description: "PR #34의 화면 전환 로딩과 레시피 인용 검색 UI 변경, 운영 배포 확인 범위."
---

> English: [Route loading and recipe citation search in Spoonie](/spoonie-route-loading-citation-en/)

Spoonie의 화면 전환 로딩과 레시피 인용 검색 인터페이스를 정비했다. [PR #34](https://github.com/saramjh/spoonie/pull/34)는 2026년 11월 12일 병합됐으며, 변경된 코드가 공개 서비스의 JavaScript에도 포함된 것을 확인했다.

## 사용자가 마주하는 두 지점

레시피를 찾다가 다른 화면으로 이동할 때는 전환 상태를 이해할 수 있어야 한다. 다른 레시피를 인용하려는 순간에는 검색 결과를 확인하고 선택하는 흐름이 분명해야 한다. 이번 변경은 이 두 접점을 다룬다.

## 구현과 검증 범위

병합된 변경에는 화면 전환 로딩 처리와 레시피 인용 검색 UI 정비가 포함된다. 원본 코드와 운영 환경에서 제공되는 JavaScript를 대조해 변경 코드의 배포를 확인했다.

다만 공개 번들에 코드가 있다는 사실만으로 실제 체감 속도 개선이나 인용 기능의 사용량을 알 수는 없다. 그런 수치는 별도로 측정되지 않았다.

Spoonie의 다른 화면 상태 문제는 [계정별 좋아요·저장 캐시 분리](/spoonie-viewer-cache-isolation-ko/)에서 다뤘다.

[원본 변경 사항](https://github.com/saramjh/spoonie/pull/34) · [Spoonie](https://spoonie.kr/)

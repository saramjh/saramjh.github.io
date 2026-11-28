---
title: "한글 조합 중에도 올바른 새를 선택하는 KoreAves 검색"
description: "KoreAves의 2026년 11월 26일 검색 개선을 통해 한글 입력 조합과 검색 결과 선택의 관계를 살펴본다."
date: 2026-11-29
tags: ["KoreAves", "Frontend Engineering", "Korean IME", "Search"]
permalink: /koreaves-korean-search-identity-ko/
layout: default
lang: ko
alternate_lang: en
alternate_url: /koreaves-korean-search-identity-en/
published: true
seo:
  title: "KoreAves 한글 검색과 분류군 선택 개선"
  description: "한글 조합 중 검색 제안 갱신과 선택한 분류군의 정체성을 유지하는 검색 동작을 설명한다."
---

> English version: [Selecting the right bird while composing Korean text in KoreAves](/koreaves-korean-search-identity-en/)

2026년 11월 26일 KoreAves의 [한글 검색 개선 기록](https://koreaves.com/updates/korean-search-selection/)에는 한글 조합 중 검색 제안을 갱신하고, 결과 목록이 바뀌어도 선택한 분류군을 유지하도록 개선한 내용이 담겨 있습니다. 이름을 입력하는 단계부터 지도에서 기록을 확인하기까지 원하는 새를 일관되게 선택할 수 있도록 하는 것이 목적입니다.

조류 자료를 찾다가 다른 종의 페이지로 이동하면 이후 지도나 기록을 잘못 읽을 수 있습니다. 입력 편의성과 정확한 선택을 함께 다뤄야 하는 이유입니다.

## 한글 입력 중에는 검색어가 변한다

한글 자판으로 글자를 입력할 때 입력기(IME)는 자모를 조합하는 과정에서 아직 확정되지 않은 문자열을 처리합니다. 웹 브라우저에서는 조합 시작과 종료를 구분할 수 있고, [InputEvent.isComposing](https://developer.mozilla.org/ko/docs/Web/API/InputEvent)으로 입력 이벤트가 조합 구간에 속하는지 확인할 수 있습니다.

MDN은 [InputEvent.isComposing 속성](https://developer.mozilla.org/en-US/docs/Web/API/InputEvent/isComposing)의 브라우저 지원 범위를 제한적이라고 표시합니다. 실제 서비스에서는 대상 브라우저와 입력기 조합에서 동작을 확인해야 합니다.

검색 제안을 조합 완료 시점까지 갱신하지 않는다면 독자는 입력 도중 원하는 항목을 찾기 어렵습니다. 반대로 입력 중 발생하는 키보드 이벤트를 모두 검색 결과 확정으로 해석하는 것도 적절하지 않습니다. [MDN의 keydown 설명](https://developer.mozilla.org/en-US/docs/Web/API/Element/keydown_event#keydown_events_with_ime)은 IME 조합과 키보드 이벤트 순서에 주의해야 한다고 설명합니다.

## 목록의 순서와 선택 대상은 별개의 상태다

검색어가 바뀌면 제안 목록의 순서도 바뀔 수 있습니다. 예를 들어 어떤 분류군이 첫 번째 결과에 있다가 검색어 갱신 후 두 번째로 이동한다고 가정해 봅시다. 첫 번째라는 위치만 기억하면 갱신된 목록의 다른 분류군을 선택할 수 있습니다.

검색 구현을 설계할 때는 사용자가 고른 항목의 고유 식별자를 유지하고, 현재 목록의 위치와 구분하는 방식이 이 문제를 줄이는 데 도움이 됩니다. 이는 검색 상태를 설계할 때 고려할 수 있는 예시입니다.

## 검색 결과를 다른 화면에서도 신뢰하려면

공개 릴리스 기록은 홈, 종 참조, GIS Explorer, Taxon Compare, Sources & evidence에서 개선된 검색 동작을 확인했다고 밝힙니다. [전체 종·아종 목록](https://koreaves.com/species/browse/)에서 이름을 찾거나 [GIS Explorer](https://koreaves.com/gis/)에서 지도를 탐색할 때 분류군을 정확히 선택하는 것이 기록 해석의 출발점입니다.

개선 내용은 공개 릴리스 기록을 근거로 설명했습니다. 본문의 설계 예시는 내부 구현이나 특정 브라우저와 입력기 조합에서의 동작을 검증한 결과가 아닙니다.

다른 화면으로 선택한 분류군을 이어 보는 방법은 [선택 상태와 공유 링크에 관한 이전 글](/koreaves-selected-bird-share-links-ko/)에 정리했습니다. [KoreAves 프로젝트](/portfolio/koreaves/)에서도 전체 개발 기록을 확인할 수 있습니다.

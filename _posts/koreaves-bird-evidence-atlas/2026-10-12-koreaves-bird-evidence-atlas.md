---
title: "한국 조류 지도와 기록 출처를 함께 확인하는 법 — KoreAves 개발 기록"
description: "한국 조류 597종·20아종, 총 617개 분류군의 지역별 공개 기록을 원출처까지 따라가는 무료 KoreAves. GBIF·EcoBank, GIS 지도, 기록 없음과 실제 부재의 차이."
date: 2026-10-12
tags: ["KoreAves", "한국 조류", "탐조", "조류 지도", "생물다양성", "GBIF", "시민과학", "GIS", "데이터 출처"]
permalink: /koreaves-bird-evidence-atlas/
layout: default
lang: ko
alternate_lang: en
alternate_url: /koreaves-bird-evidence-atlas-en/
published: true
---

한국의 새를 검색하면 이름이나 사진은 나옵니다. 하지만 **어느 지역에 관찰 기록의 근거가 있고, 그 원출처가 무엇인지** 확인하려면 여러 사이트를 오가야 할 때가 있습니다.

그 사이를 이어 보려고 만든 무료 참고 사이트가 [KoreAves](https://koreaves.com/?utm_source=devtestudinidae_blog&utm_medium=owned_editorial&utm_campaign=koreaves_evidence_atlas_20261012&utm_content=ko_intro)입니다. 한국 새를 대상으로 한 비상업적 근거 아틀라스이며, 영문 중심에 한국어도 제공합니다.

**English article:** [KoreAves: A Source-Linked Atlas of South Korean Bird Records](/koreaves-bird-evidence-atlas-en/)

## 617종이 아니라 617개 분류군입니다

기준은 2025년 한국 국가생물종목록의 **597종 + 20아종 = 617개 분류군**입니다. 종과 아종을 하나의 종수로 합칠 수는 없습니다.

KoreAves는 분류학적 정체성을 나타내는 목록 자료와 관찰 기록 자료를 구분합니다. 비슷한 학명이 있다고 임의로 같은 분류군으로 통합하거나, 확인되지 않은 영문 이름을 만들어 붙이지 않도록 설계했습니다.

## 지도에서 색이 칠해진 지역은 무엇을 뜻할까요?

[지역별 조류 기록 GIS 탐색기](https://koreaves.com/gis/?utm_source=devtestudinidae_blog&utm_medium=owned_editorial&utm_campaign=koreaves_evidence_atlas_20261012&utm_content=ko_gis)에서 새 이름을 검색하면 현재 대한민국의 17개 광역 행정구역 중 적격한 기록 근거가 확인된 지역을 살펴볼 수 있습니다. 지역을 선택하면 어떤 자료원이 그 근거를 지원하는지도 표시됩니다.

여기에는 중요한 한계가 있습니다.

- **기록 있는 지역 ≠ 새가 그 행정구역 전체에 산다는 뜻**: 색칠은 공개 자료의 기록 범위 표시입니다.
- **기록 없는 지역 ≠ 새의 실제 부재**: 현재 분석에 포함된 자료와 적격성 조건에서 근거를 찾지 못했다는 뜻입니다.
- **기록 건수 ≠ 개체수나 개체군 규모**: 조사 노력과 데이터 공개 정도가 달라도 행 수가 달라집니다.
- **같은 지역 기록 ≠ 동시에 함께 관찰**: 두 분류군의 지역별 근거가 겹쳐도 같은 장소나 시간에 관찰됐다는 증거는 아닙니다.

따라서 지도는 공식 생물 분포도나 개체수 추정도가 아니라, **기록과 해석의 출발점을 찾는 도구**입니다.

## 어떤 자료를 연결하나요?

[데이터셋 버전 설명](https://koreaves.com/dataset/)에는 정규화된 소스 행 **1,970,745건**, 분석 근거의 버전, 출처별 역할이 공개되어 있습니다. GBIF의 occurrence 근거와 국립생태원 EcoBank 조사는 서로 다른 자료체계이므로, 같은 의미의 개체수처럼 합치지 않습니다.

국가목록은 분류군의 정체성을, 실제 공개 기록은 문서화된 occurrence 근거를, SGIS 경계는 행정구역별 화면 구성을 맡습니다. 각각의 역할은 [방법론](https://koreaves.com/methodology/)과 [출처 목록](https://koreaves.com/sources/)에서 확인할 수 있습니다.

사진도 비슷합니다. 공개된 사진이 있다고 마음대로 다시 써도 되는 것은 아닙니다. 대표 이미지는 종·아종이 맞는지, 촬영자와 원본이 누구인지, 재사용 조건이 무엇인지를 따로 살펴야 합니다.

## 회원가입 없이 직접 확인하기

1. [KoreAves](https://koreaves.com/?utm_source=devtestudinidae_blog&utm_medium=owned_editorial&utm_campaign=koreaves_evidence_atlas_20261012&utm_content=ko_try)에서 한글 이름, 영어 이름이나 학명을 검색합니다.
2. 종 페이지에서 기본 정보와 기록 근거를 봅니다.
3. GIS 지도의 17개 지역 중 하나를 선택하고 연결된 출처를 확인합니다.
4. 필요하면 분류군 비교 기능으로 각 지역의 근거 범위를 비교합니다.

이 프로젝트는 새로운 조류 관찰을 접수하는 시민과학 앱이 아니며, 기관의 공식 조사 결과를 대체하지도 않습니다. 공개 기록의 출처와 해석상 한계를 따라갈 수 있도록 만든 독립적인 비상업 참고 도구입니다.

탐조를 하거나 조류 자료를 연구하는 분, 공개 데이터를 GIS로 보여주는 개발자에게 얼마나 도움이 되는지 확인하는 중입니다. 잘못된 학명이나 지역별 근거, 화면에서 오해하기 쉬운 표현을 발견했다면 [서면 정정·기여 안내](https://koreaves.com/contact/)로 알려주시면 확인하겠습니다.

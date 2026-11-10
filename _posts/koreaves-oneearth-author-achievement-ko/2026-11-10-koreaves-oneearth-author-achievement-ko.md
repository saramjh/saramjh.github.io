---
title: "One Earth에 KoreAves 개발 기고가 실렸다"
description: "2026년 10월 28일 One Earth에 KoreAves를 소개하는 작성자 기고가 게재됐다. 한국 조류 자료의 출처와 지역별 관찰 근거를 연결하는 웹 서비스를 개발한 과정과 해외 독자에게 설명한 가치를 정리했다."
date: 2026-11-10
tags: ["KoreAves", "One Earth", "해외 기고", "조류 데이터", "GIS", "개발자 포트폴리오"]
permalink: /koreaves-oneearth-author-achievement-ko/
layout: default
lang: ko
alternate_lang: en
alternate_url: /koreaves-oneearth-author-achievement-en/
image: /assets/images/portfolio/koreaves-gis.jpg
image_width: 1440
image_height: 900
published: true
seo:
  title: "One Earth에 소개된 KoreAves 개발자의 조류 데이터 기고"
  description: "One Earth 2026년 10월 28일 원문에 작성자로 크레딧된 KoreAves 개발 실적. 617개 분류군과 17개 지역의 출처 기반 지도 설계를 해외 독자에게 설명했다."
---

> English version: [My KoreAves article was published by One Earth](/koreaves-oneearth-author-achievement-en/)

**2026년 10월 28일, [One Earth에 *Mapping South Korea’s birdlife, one observation at a time* 기고문](https://www.oneearth.org/koreaves/)이 게재됐다.** 원문에는 Jihun Oh가 작성자로 표시돼 있고, 직접 개발한 프로젝트 KoreAves의 창작자로 소개돼 있다. 한국 조류 정보를 탐색하는 서비스를 국제 환경 매체의 독자에게 설명할 수 있게 된 성과다.

[KoreAves](https://koreaves.com/)를 만들면서 해결하고 싶었던 문제는 명확했다. 한국어 자료에 익숙하지 않은 사람도 새의 이름을 찾고, 어느 지역에서 관찰 근거가 기록됐는지 보고, 그 표시를 뒷받침하는 원문 출처까지 따라갈 수 있어야 한다는 것이다. 지도에 색을 칠하는 기능을 구현하면서는 **어떤 기록을 지도에 표시해도 되는가**를 계속 구분해야 했다.

<figure>
  <img src="/assets/images/portfolio/koreaves-gis.jpg" alt="KoreAves에서 지역별 조류 관찰 근거와 출처를 함께 탐색하는 실제 GIS 화면의 기존 프로젝트 이미지." width="1440" height="900" loading="lazy" style="width:100%;height:auto;">
  <figcaption>직접 만든 KoreAves 서비스의 기존 GIS 화면. One Earth의 사진이나 실제 유입 통계를 가져온 자료가 아니다.</figcaption>
</figure>

## 개발자가 실제로 구현한 부분

KoreAves는 기준 목록의 **597종과 20아종, 총 617개 분류 항목**을 다룬다. 617종이라고 표시하면 아종을 종과 중복해서 계산하게 되므로 항목 수와 종 수를 구분했다. 영어 중심 화면에 한국어 명칭과 탐색 기능도 제공한다.

[지역별 GIS 탐색 화면](https://koreaves.com/gis/)에서는 한국의 17개 광역 행정구역 가운데 해당 조류의 적격 관찰 근거가 확인되는 곳을 살펴볼 수 있다. 색이 표시된 지역은 기록의 존재를 보여준다. 거기에 사는 개체 수나 생물학적 분포 범위가 정확히 그 모양이라는 의미는 아니다.

이 차이를 사용자가 알 수 있도록 분류군 이름, 관찰 자료, 날짜와 출처, 지도에 사용할 수 있는 기록의 범위를 분리해 설계했다. 기록이 없는 곳을 해당 새가 살지 않는 지역으로 단정해서도 안 된다. 서비스의 [방법론 페이지](https://koreaves.com/methodology/)에는 이런 판단 기준을 설명해 두었다.

## 기고를 통해 보여준 개발 역량

[One Earth 원문](https://www.oneearth.org/koreaves/)은 한국의 새를 궁금해하는 독자에게 KoreAves를 소개하면서, 지도와 원본 자료의 관계를 읽는 방법을 설명한다. 개발 과정에서 다뤘던 출처 추적 문제를 일반 독자에게 전달할 수 있는 언어로 옮긴 글이다.

개발자로서는 낯선 자료를 다루는 사람이 어떤 근거를 먼저 확인해야 하는지 화면과 설명을 함께 설계한 경험을 보여줄 수 있다. 특히 해외 교육자나 데이터 검토자가 기고문을 읽은 뒤 실제 사이트에서 지도를 조작하고 방법론을 확인할 수 있다는 점이 실용적이다. 협업을 논의할 때도 제품 소개 자료와 공개된 작성자 기고를 함께 제시할 수 있다.

확인된 실적은 **One Earth에 게재된 작성자 기고문**이다. 이를 공식 제휴나 별도의 독립 평가, 실제 학교 도입 성과로 확대할 근거는 없다. 읽은 사람의 수나 KoreAves로 이동한 방문자 수도 현재 확인하지 않았다.

[One Earth의 기고문과 작성자 표시](https://www.oneearth.org/koreaves/)를 원본 근거로 남긴다. [포트폴리오 외부 성과 원장](/portfolio/recognition/)에서 게시 유형을 확인할 수 있고, [KoreAves 데이터 지도 개발 기록](/koreaves-bird-evidence-atlas/)에서 구현 방법을 더 자세히 볼 수 있다. 이후 지도 해석의 문제를 더 구체적으로 다룬 [Unsustainable Magazine의 기고문](https://www.unsustainablemagazine.com/why-a-bird-map-is-not-a-bird-count/)도 공개됐다.

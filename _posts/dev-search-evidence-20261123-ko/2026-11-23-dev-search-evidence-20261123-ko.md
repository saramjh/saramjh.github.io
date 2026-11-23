---
title: "37일간 구글 검색 클릭 300회, 직접 만든 도구들의 실제 유입을 확인했다"
description: "2026년 10월 15일~11월 20일 원본 Search Console에서 검색 클릭 300회와 노출 3,601회를 확인했다. 스크래치 복권 시뮬레이터, 엡손 정비 안내, 얼굴 비교 도구의 검색 유입을 분리해 살펴본다."
seo:
  title: "구글 검색 클릭 300회: 독립 개발 도구의 실제 유입 측정"
  description: "37일간 검색 클릭 300회와 노출 3,601회. Google Search Console의 원본 속성과 페이지별 실적을 구분해 확인한 기록."
date: 2026-11-23
tags: ["Google Search Console", "독립 개발", "검색 유입", "스크래치 복권 시뮬레이터", "엡손 정비 안내", "RichChecker", "성과 측정"]
permalink: /independent-tools-google-search-results-ko/
layout: default
lang: ko
alternate_lang: en
alternate_url: /independent-tools-google-search-results-en/
image: /scratch-lottery-simulation/scratchlottery-2026-fast-simulation.png
image_width: 1200
image_height: 681
published: true
---

> English version: [My tools drew 300 Google Search clicks in 37 days](/independent-tools-google-search-results-en/)

**2026년 10월 15일부터 11월 20일까지 37일 동안 내 GitHub Pages 속성에 구글 검색 클릭 300회, 노출 3,601회가 기록됐다.** 원본 Google Search Console의 확정된 웹 검색 데이터를 조회했으며, 전체 클릭률은 8.33%였다.

검색으로 방문한 곳은 포트폴리오 소개 화면만이 아니었다. 직접 만든 복권 시뮬레이터, 프린터 정비 안내, 얼굴 특징 비교 실험처럼 특정 문제를 해결하거나 탐색하는 화면으로 유입이 발생했다.

## 어떤 페이지가 검색에서 클릭됐나

| 페이지 | 구글 검색 클릭 | 검색 노출 |
| :--- | ---: | ---: |
| [Scratch Lottery 시뮬레이터](/scratchLottery/) | 120회 | 1,416회 |
| [엡손 잉크 패드 정비 안내](/epson-waste-ink-pad-reset-without-key/) | 88회 | 485회 |
| [RichChecker 얼굴 특징 비교 실험](/richChecker/) | 73회 | 236회 |

이 표는 **개별 페이지 집계**다. 앞의 클릭 300회는 **속성 전체 집계**이므로 페이지별 숫자를 합쳐 300회와 직접 대조하거나, 차이만큼을 다른 페이지의 클릭 수로 계산하면 안 된다. Google Search Console은 속성과 페이지별 검색 결과를 서로 다른 기준으로 집계할 수 있다.

같은 GitHub Pages 주소 아래에 있지만 별도 코드베이스로 운영하는 도구도 있다. 이 수치는 각각의 URL에서 관측된 구글 검색 결과 클릭일 뿐 KoreAves, Spoonie, Space Atlas 같은 다른 도메인의 실적을 포함하지 않는다.

![검색 유입이 측정된 페이지 중 하나인 Scratch Lottery 시뮬레이터의 원본 화면](/scratch-lottery-simulation/scratchlottery-2026-fast-simulation.png)

*직접 만든 시뮬레이터 화면이다. Search Console 보고서 화면이 아니며 검색 수치의 출처는 별도로 기록했다.*

## 개발한 기능과 검색 유입의 관계

[Scratch Lottery](/scratch-lottery-simulation-ko/)에서는 복권 결과를 가상으로 확인하고 당첨 확률과 일괄 시뮬레이션 조건을 조절할 수 있게 만들었다. 구글에서 기록된 클릭 120회는 검색 결과에서 이 도구를 찾은 사례가 있었다는 뜻이다. 각 방문자가 실제 시뮬레이션을 실행했는지, 재방문했는지는 이 수치만으로 알 수 없다.

[엡손 잉크 패드 정비 안내](/epson-waste-ink-pad-reset-without-key/)는 실제 프린터 문제를 다루면서 모델별 적용 가능성과 안전상 한계를 구분한 문서다. 검색 클릭 88회는 그 안내를 찾는 검색 유입이 있었다는 근거지만, 프린터 88대를 수리했다는 뜻은 아니다. 앞서 [GA4와 Search Console로 확인한 기존 엡손 검색 유입 기록](/gh-pages-analytics-notes-6-search-traffic-kr/)은 측정 기간이 겹치므로 이번 수치에 합산하지 않는다.

[RichChecker](/richChecker/)는 브라우저에서 얼굴 특징을 비교하는 실험 도구다. 구글 검색 클릭 73회가 있었지만, 사진 분석 완료 수나 비교 결과의 과학적 타당성을 입증하는 지표는 아니다.

이번 확인에서 얻은 실질적인 정보는 기능과 글이 외부 검색에서 발견된다는 점이다. 어떤 질문을 가지고 그 페이지에 들어오는지 이해하고 안내 문구와 기능을 개선할 근거로 삼을 수 있다. 클릭이 발생했다는 사실만으로 사용자의 목적이 달성됐다고 판단하지는 않겠다.

## 측정 방법과 범위

원본 [Google Search Console](https://support.google.com/webmasters/answer/7042828?hl=ko) URL 접두어 속성에서 검색 유형을 **웹**, 기간을 **2026년 10월 15일~11월 20일**, 데이터 상태를 **확정(final)**으로 지정했다. 속성 전체 조회에서 클릭 300회, 노출 3,601회, CTR 8.33%를 확인하고, 별도로 페이지별 URL과 클릭 수를 조회했다. 구글 검색 결과에 대한 통계이며 GA4 세션 수와 동일하지 않다.

[집계값과 조회 범위를 남긴 공개 JSON](/assets/data/dev-c127-gsc-search-performance-20261123.json)에는 개인을 식별할 정보 없이 출처·기간·집계 기준을 기록했다. 원본 Search Console 속성은 비공개이므로 이 JSON만으로 제3자가 보고서를 독립 재현할 수 있는 것은 아니다.

**확인한 성과는 해당 기간 이 속성의 구글 검색 클릭 300회다.** 고유 사용자 300명, 서비스 가입 300건 또는 제품 채택 실적으로 바꾸어 말할 수 없다.

[개발 포트폴리오](/portfolio/)에서는 이 자체 측정 실적을 [외부 기고·자료 목록 등재](/portfolio/recognition/ko/)와 별도로 구분했다. 외부 발표 사실과 검색 유입은 서로 다른 종류의 성과이기 때문이다.

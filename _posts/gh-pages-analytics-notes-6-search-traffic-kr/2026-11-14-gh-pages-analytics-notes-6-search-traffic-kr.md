---
title: "엡손 정비 글의 검색 유입을 GA4와 Search Console로 검증해보니"
description: "엡손 잉크패드 정비 안내의 30일간 자연 검색 유입 110세션을 확인했다. 검색엔진별 세션과 Google 검색 클릭을 구분해 해석한 기록."
seo:
  title: "엡손 잉크패드 안내 글 검색 유입: GA4 110세션 실측"
  description: "한국어·영어 프린터 정비 안내 글의 자연 검색 유입을 GA4·Search Console로 검증하고 세션과 검색 클릭의 차이를 정리했습니다."

date: 2026-11-14
tags: ["GA4", "Google Search Console", "검색 유입", "엡손 잉크패드", "기술 문서", "데이터 분석"]
permalink: /gh-pages-analytics-notes-6-search-traffic-kr/
layout: default
lang: ko
alternate_lang: en
alternate_url: /gh-pages-analytics-notes-6-search-traffic-en/
image: /gh-pages-analytics-notes-6-search-traffic-kr/search-channels-og.png
image_width: 1200
image_height: 630
published: true
---

> English: [A printer guide's search traffic, checked in GA4 and Search Console](/gh-pages-analytics-notes-6-search-traffic-en/)

프린터에서 잉크패드 수명 경고가 뜨면 기종과 오류 문구부터 검색하게 된다. 예전에 직접 정비했던 L3106을 바탕으로 [엡손 잉크패드 정비 안내](/epson-waste-ink-pad-reset-without-key/)를 작성했다. 이후 다른 모델까지 같은 방식으로 작동하는 것처럼 읽히지 않도록 호환성 범위와 실제 패드 정비의 필요성을 보완했다.

그 글에 실제로 자연 검색 유입 세션이 기록되는지 확인했다. **2026년 10월 15일~11월 13일** 한국어·영어 안내 페이지에 도착한 자연 검색 유입은 **GA4 기준 110세션**, 그중 **참여 세션은 96건**이었다. 검색으로 글을 발견했다는 근거다. 프린터 96대가 수리됐다는 뜻은 아니다.

## 검색엔진별로 나눈 첫 방문 경로

원본 GA4 블로그 속성의 웹 스트림이 사이트에 설정된 측정 ID와 일치하는지 먼저 대조했다. **landingPage**에는 안내 글 두 개의 정확한 경로만 포함하고, **sessionSourceMedium**으로 검색 유입처를 구분했다. 같은 GitHub Pages 주소에서 별도로 운영하는 다른 도구의 방문은 제외했다.

![엡손 정비 안내를 검색해 방문한 세션 수: Google 72, Bing 33, Naver 3, Yahoo 2를 표시한 가로 막대그래프.](/gh-pages-analytics-notes-6-search-traffic-kr/search-channels-og.png)

| 자연 검색 유입처 | 세션 | 참여 세션 |
| :--- | ---: | ---: |
| Google | 72 | 63 |
| Bing | 33 | 28 |
| Naver | 3 | 3 |
| Yahoo | 2 | 2 |
| **합계** | **110** | **96** |

집계 기간은 **10월 15일~11월 13일**, GA4 속성의 **Asia/Seoul 시간대**다. 직접 방문과 일반 추천 링크는 포함하지 않았다. 한국어 페이지에는 Google 68세션·Bing 13세션, 영어 페이지에는 Google 4세션·Bing 20세션이 유입됐다. 두 언어판이 서로 다른 검색 경로로 발견된다는 점은 볼 수 있다. 방문자의 거주 국가까지 확인된 것은 아니다.

[GA4 참여 세션의 기준](https://support.google.com/analytics/answer/12195621?hl=en)은 10초 초과 체류, 주요 이벤트 발생, 페이지·화면 조회 2회 이상 중 하나다. 안내 내용을 이해하거나 정비를 완료했는지는 측정하지 못한다. 운영자 방문과 자동화 유입이 완전히 제거됐다고 볼 수도 없다.

## Search Console에서는 어떻게 보였나

Google Search Console에서는 검색어별 일부 행이 아니라 두 안내 페이지의 **정확한 URL**을 기준으로 조회했다. 확정 데이터가 제공된 **2026년 10월 15일~11월 10일** 결과다.

| 안내 페이지 | Google 검색 클릭 | 노출 |
| :--- | ---: | ---: |
| [한국어 안내](/epson-waste-ink-pad-reset-without-key/) | 68 | 322 |
| [영어 안내](/en-epson-waste-ink-pad-reset-without-key/) | 5 | 87 |
| **합계** | **73** | **409** |

Search Console은 Google 검색 결과에서 발생한 [클릭·노출](https://support.google.com/webmasters/answer/7042828?hl=en)을 집계한다. GA4는 사이트에 도착한 뒤의 세션을 측정한다. 이번에는 기간도 다르고, Search Console의 일별 기준은 미국 태평양 시간이다. 따라서 **73클릭과 110세션을 나눠 전환율로 계산하면 안 된다.**

실제 검색어에는 '엡손 잉크 패드 리셋 프로그램 무료', 'l3156 잉크패드 리셋' 같은 표현이 포함됐다. 기종이 다른 사람이 같은 안내에 도착할 수 있다는 뜻이다. 그래서 원래 L3106 사례를 다른 모델의 검증 결과로 확대하지 않고, 소프트웨어 카운터 리셋과 물리적인 잉크패드 정비를 구분해 설명하는 일이 중요하다.

## 확인한 성과와 남은 질문

직접 경험한 기기 문제를 정리한 글이 Google·Bing·Naver·Yahoo를 통해 실제로 발견됐다. 이를 검증하려면 공유 호스트의 전체 방문자 숫자보다 페이지별 첫 진입 경로와 검색 유입처를 살펴야 했다. 여기에 Search Console의 별도 검색 데이터를 대조하니 어느 부분까지 확인할 수 있는지도 분명해졌다.

아직 확인하지 못한 것은 독자가 **자기 프린터에 맞는 안전한 정비 방법을 판단했는지**다. 지금 가진 방문·검색 지표만으로는 알 수 없다. 이번 결과는 안내 글의 **검색 발견과 방문**으로 범위를 한정한다.

이 글은 [애널리틱스 고민 노트 5편](/gh-pages-analytics-notes-5-followup-kr/)에서 다뤘던 공유 호스트 측정 문제의 후속 사례다. 사용한 원본 기간·경로·검색엔진별 집계는 [집계 요약 JSON](/assets/data/dev-c622-epson-organic-search-20261114.json)에 남겼다.

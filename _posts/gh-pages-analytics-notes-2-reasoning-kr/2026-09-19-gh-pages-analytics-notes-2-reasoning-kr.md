---
title: "혼자 여러 GitHub Pages를 굴리다 보니 생긴 애널리틱스 고민 (2) — 근거 탐색"
description: "GA4 속성을 합칠지 나눌지, Search Console은 도메인 단위인지 프로젝트 단위인지. AI와의 논의에서 나온 근거를 실제 인용이 아니라 GA4/SEO의 일반 원리로 재구성해서 정리합니다."
date: 2026-09-18
tags: ["GA4", "Google Analytics", "Search Console", "Microsoft Clarity", "GitHub Pages", "SEO"]
permalink: /gh-pages-analytics-notes-2-reasoning-kr/
layout: default
lang: ko
alternate_lang: en
alternate_url: /gh-pages-analytics-notes-2-reasoning-en/
---

<p style="background: rgba(0, 120, 212, 0.08); border-left: 4px solid #0078d4; padding: 10px 14px; margin-bottom: 16px; border-radius: 4px; font-size: 0.95rem;">
  🌐 <strong>English Edition available:</strong> Read the English version at <a href="/gh-pages-analytics-notes-2-reasoning-en/"><strong>Analytics Notes (English Edition)</strong></a>.
</p>

<p style="background: rgba(120, 90, 0, 0.08); border-left: 4px solid #b8860b; padding: 10px 14px; margin-bottom: 24px; border-radius: 4px; font-size: 0.9rem;">
  📚 <strong>시리즈 목차</strong> — <a href="/gh-pages-analytics-notes-1-problem-kr/">1편 문제 정의</a> · 2편 <strong>근거 탐색</strong> (현재 글) · <a href="/gh-pages-analytics-notes-3-decision-kr/">3편 결정과 적용</a> · <a href="/gh-pages-analytics-notes-4-open-kr/">4편 지금 상태와 열린 질문</a> · <a href="/gh-pages-analytics-notes-5-followup-kr/">5편 네이버 2위와 트래픽 증가 이후</a>
</p>

## 미리 밝혀둘 것

이 글에 정리한 논리는 실제로 AI와 나눴던 대화를 그대로 인용한 게 아닙니다. 그 세션의 로그를 지금 갖고 있지 않아서, 여기서는 **GA4·Search Console·Clarity의 공식 문서와 업계에서 통용되는 일반 원리**를 바탕으로 당시 논의의 핵심을 다시 구성했습니다. "AI가 이렇게 말했다"가 아니라 "이런 원리에 근거해서 그 조언이 그럴듯해 보였다"로 읽어주시면 됩니다.

## GA4: 속성(Property)과 데이터 스트림(Data Stream)은 다른 층위다

GA4 구조를 이해하는 데 가장 헷갈렸던 지점은 "속성"과 "데이터 스트림"이 다른 개념이라는 것이었습니다.

- **속성(Property)**: 데이터가 집계되는 최상위 단위. 보고서, 데이터 보존 기간, 무료 등급의 데이터 임계값(threshold), BigQuery 연결 등이 전부 속성 단위로 독립적입니다.
- **데이터 스트림(Data Stream)**: 웹사이트나 앱에서 속성으로 데이터를 보내는 수집 소스입니다. 하나의 속성에 여러 스트림을 둘 수 있지만, Google은 일반적으로 속성당 웹 스트림 하나를 권장합니다.

당시에는 도구마다 속성을 따로 만드는 방식이 필요 이상으로 세분화한 것이라고 생각했습니다. 실제 기준은 도구들이 같은 논리적 사용자 집단에 속하고 데이터를 함께 분석해야 하는지에 따라 달라집니다. 별도 스트림이 언제나 별도 속성을 대체하는 것은 아닙니다.

**2026-11-20 정정.** 앞서 여러 웹 스트림을 하나의 속성에 넣는 방식을 Google의 일반 권장안처럼 설명했습니다. 정확하지 않았습니다. Google은 속성을 하나의 사용자 집단에 대한 데이터로 설명합니다. 함께 분석할 데이터는 한 속성에 두고, 서로 다른 논리적 사용자 집단은 별도 속성으로 나눌 수 있습니다. 일반적인 경우 속성당 웹 스트림 하나를 권장합니다. 3편에 기록한 여러 스트림 구성은 제가 실제로 선택했던 설정이지 보편적인 권장안은 아닙니다 ([Google 계정 구조 안내](https://support.google.com/analytics/answer/9679158?hl=en)).

여러 스트림을 한 속성에 두면 한 속성의 보고서에서 데이터를 함께 볼 수 있습니다. 하지만 그것만으로 스트림 사이의 사용자 여정이 이어지는 것은 아닙니다. 교차 도메인 측정에는 각 도메인에 같은 웹 스트림의 같은 태그 ID를 사용해야 합니다 ([Google 교차 도메인 측정 안내](https://support.google.com/analytics/answer/10071811?hl=en)). 3편에 기록한 것처럼 도구마다 별도 웹 스트림을 사용했으므로, 속성 하나로 묶었다는 사실만으로 블로그에서 도구로 이동한 사용자가 하나의 여정으로 이어졌다고 단정할 수 없습니다. 실제 태그와 보고서로 확인해야 합니다.
- 호스트 이름(hostname)이나 스트림 이름을 보조 측정기준(dimension)으로 두고, 탐색 분석이나 비교(comparison) 기능으로 "이 도구만" 또는 "블로그만" 필터링해서 볼 수 있습니다. (실제로 앞서 이 대화에서 `hostName` 기준으로 세션을 나눠 조회했던 것도 같은 원리입니다.)
- 반대로 속성을 나누면, 각 속성이 무료 등급 데이터 임계값이나 보관 기간을 각자 따로 소진하고, 사용자 여정은 원천적으로 끊깁니다.

## Search Console: Domain과 URL 접두사 속성의 범위와 검증 방식

Search Console에는 검증 범위와 조건이 다른 두 가지 속성 유형이 있습니다.

- **도메인 속성(Domain property)**: 서브도메인·프로토콜·하위 경로를 포함하지만, 소유권을 확인하려면 **DNS 검증**이 필요합니다. GitHub Pages 저장소에서는 기본 주소인 `saramjh.github.io`의 DNS 레코드를 직접 수정할 수 없습니다.
- **URL 접두사 속성(URL-prefix property)**: `https://saramjh.github.io/`를 등록하면 같은 HTTPS 호스트 아래의 프로젝트 경로까지 포함합니다. `https://saramjh.github.io/scratchLottery/`처럼 좁게 지정하면 해당 경로 아래만 포함됩니다. HTML 파일이나 태그로 소유권을 확인할 수 있습니다.

**2026-11-20 정정.** 앞서 도메인 속성 하나로 통합하면 된다고 썼지만, DNS 검증 조건을 빠뜨렸습니다. 기본 GitHub Pages 주소에서는 **사이트 루트 URL 접두사 속성**으로도 같은 HTTPS 하위 경로를 묶을 수 있습니다. 프로젝트마다 사이트맵을 제출했는지는 속성 유형과 별개의 문제입니다. 실제 Search Console 계정에서 어떤 유형이 검증됐는지는 원본 소유권 확인 영수증을 확보하지 못했으므로 **확실하지 않습니다**. [Google의 속성 범위 안내](https://support.google.com/webmasters/answer/34592?hl=en)와 [소유권 확인 방법](https://support.google.com/webmasters/answer/9008080?hl=en)을 근거로 수정했습니다.

## 루트 도메인을 공유한다고 확인되는 것과 확인되지 않는 것

Google 공식 문서가 뒷받침하는 내용은 더 구체적입니다. 같은 루트 도메인의 모든 경로가 동일한 순위 권위를 물려받는다는 일반 규칙은 확인되지 않습니다.

- **하위 경로와 서브도메인:** Google은 색인·순위 측면에서 어느 쪽도 선호하지 않는다고 안내합니다. 정리·관리하기 쉬운 구조를 선택하면 됩니다. 크롤링 예산 문서에서는 고유 호스트 이름을 하나의 사이트로 정의하므로, 서브도메인은 별도의 크롤링 예산을 가집니다. 이는 크롤링 경계이지 순위 우위가 아닙니다.
- **크롤링 예산:** Google이 크롤링할 수 있고 크롤링하려는 URL의 집합입니다. 크롤링 자체는 순위 신호가 아니며, 이 지침은 주로 매우 크거나 자주 갱신되는 사이트를 대상으로 합니다.
- **링크와 순위:** Google은 링크를 페이지 발견과 관련성 판단에 사용합니다. 순위 시스템은 주로 페이지 단위로 작동하면서 일부 사이트 전체 신호도 함께 사용합니다. 그렇다고 루트 도메인 아래 모든 경로에 동일한 신뢰 점수가 전달된다는 뜻은 아닙니다.
- **도메인 나이:** 등록 기간이 순위 이점을 만든다는 근거를 이 글에서 확인할 수 없어, 지원되는 순위 신호 목록에서 제외했습니다.

`saramjh.github.io`는 하나의 호스트 이름 아래 여러 경로를 사용합니다. 따라서 크롤링 예산은 호스트 단위로 공유하지만, 이것만으로 Google이 각 경로의 관련성이나 순위를 하나의 점수로 합친다고 볼 수는 없습니다 ([하위 경로와 서브도메인 FAQ](https://developers.google.com/search/help/crawling-index-faq?hl=en); [크롤링 예산 안내](https://developers.google.com/crawling/docs/crawl-budget?hl=en); [크롤링 관련 오해](https://developers.google.com/crawling/docs/myths-about-crawling); [링크 모범 사례](https://developers.google.com/search/docs/crawling-indexing/links-crawlable); [순위 시스템 안내](https://developers.google.com/search/docs/appearance/ranking-systems-guide); [Google Search Central의 도메인 나이 영상](https://www.youtube.com/watch?v=-pnpg00FWJY)).

정리하면, 같은 호스트를 쓴다는 사실은 URL과 크롤링 구조에 관한 정보이지 순위 신뢰를 자동으로 공유한다는 증거는 아닙니다. 각 페이지는 콘텐츠와 검색 의도에 맞는 관련성을 스스로 확보해야 합니다.

## Clarity: 프로젝트 단위는 결국 "무엇을 함께 보고 싶은가"의 문제

Clarity는 Search Console의 Domain/URL-prefix 속성 검증 방식을 사용하지 않습니다. 프로젝트 추적 코드를 설치한 여러 사이트에서 데이터를 모을 수 있고, 같은 스크립트를 여러 서브도메인에도 설치할 수 있습니다. Microsoft는 도메인이 다른 사이트에는 프로젝트를 분리할 것을 권장합니다. 하나의 호스트 아래 여러 경로가 있는 경우에는 녹화와 히트맵을 함께 볼지에 따라 구성을 정합니다 ([Clarity FAQ](https://learn.microsoft.com/en-us/clarity/faq/); [설치 안내](https://learn.microsoft.com/en-us/clarity/setup-and-installation/clarity-setup)).

- 같은 프로젝트로 묶으면: 모든 도구의 세션 리플레이/히트맵을 한 대시보드에서 볼 수 있지만, 도구별로 트래픽 규모가 다르면 특정 도구의 세션이 다른 도구의 세션에 묻힐 수 있습니다.
- 프로젝트를 나누면: 도구별 분석은 깔끔해지지만, 관리해야 할 대시보드 수가 도구 수만큼 늘어납니다.

## 이 근거들을 종합하면

**2026-11-20 보충.** GA4, Search Console, Clarity는 데이터를 묶는 기준이 서로 다릅니다.

- **GA4:** 함께 분석할 논리적 사용자 집단을 기준으로 속성을 선택합니다. Google은 일반적으로 속성당 웹 스트림 하나를 권장합니다. 여러 스트림을 한 속성에 두면 보고서에서는 함께 볼 수 있지만 스트림 사이의 사용자 여정이 자동으로 이어지지는 않습니다. 교차 도메인 측정에는 각 도메인에 같은 웹 스트림의 같은 태그 ID를 사용해야 합니다 ([Google 계정 구조 안내](https://support.google.com/analytics/answer/9679158?hl=en); [교차 도메인 측정 안내](https://support.google.com/analytics/answer/10071811?hl=en)).
- **Search Console:** 도메인 속성은 하위 도메인, 프로토콜, 경로를 모두 포함하지만 DNS 검증이 필요합니다. URL 접두사 속성은 지정한 접두사로 시작하는 주소만 포함하므로 `https://saramjh.github.io/`는 이 호스트의 HTTPS 프로젝트 경로를 포함합니다 ([속성 유형](https://support.google.com/webmasters/answer/34592?hl=en); [소유권 확인 방법](https://support.google.com/webmasters/answer/9008080?hl=en)).
- **Clarity:** 프로젝트 추적 코드를 설치한 여러 사이트의 데이터를 한 프로젝트에서 모을 수 있습니다. Microsoft는 도메인이 다른 사이트에는 프로젝트를 분리할 것을 권장합니다. 같은 호스트의 여러 경로는 녹화와 히트맵을 함께 볼지에 따라 프로젝트 구성을 결정할 수 있습니다 ([Clarity FAQ](https://learn.microsoft.com/en-us/clarity/faq/); [설치 안내](https://learn.microsoft.com/en-us/clarity/setup-and-installation/clarity-setup)).

3편에서는 실제로 바꾼 설정과 그대로 둔 부분을 정리합니다.

→ [3편: 결정과 적용으로 이어집니다](/gh-pages-analytics-notes-3-decision-kr/)

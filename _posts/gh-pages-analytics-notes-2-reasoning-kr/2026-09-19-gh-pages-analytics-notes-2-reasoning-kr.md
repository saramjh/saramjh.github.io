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
- **데이터 스트림(Data Stream)**: 하나의 속성 안에서 데이터를 수집하는 개별 소스(웹사이트 하나, 앱 하나)를 뜻합니다. 하나의 속성에 여러 개의 웹 데이터 스트림을 등록할 수 있습니다.

즉, "도구마다 새 속성을 만든다"는 제 기존 습관은 사실 **도구마다 새 데이터 스트림을 만드는 것으로 충분했을 수도 있는 상황**에서, 매번 한 단계 위인 속성까지 쪼개고 있었던 셈입니다.

구글이 여러 사이트/앱을 하나의 브랜드로 묶어 보고 싶은 조직에 권장하는 방식도 "하나의 속성 + 여러 데이터 스트림"입니다. 이 구조를 쓰면:

- 사용자가 블로그 글을 읽고 도구로 이동해도, 같은 속성 안에서 하나의 사용자 여정으로 이어볼 수 있습니다(크로스 도메인 측정 설정이 되어 있다는 전제하에).
- 호스트 이름(hostname)이나 스트림 이름을 보조 측정기준(dimension)으로 두고, 탐색 분석이나 비교(comparison) 기능으로 "이 도구만" 또는 "블로그만" 필터링해서 볼 수 있습니다. (실제로 앞서 이 대화에서 `hostName` 기준으로 세션을 나눠 조회했던 것도 같은 원리입니다.)
- 반대로 속성을 나누면, 각 속성이 무료 등급 데이터 임계값이나 보관 기간을 각자 따로 소진하고, 사용자 여정은 원천적으로 끊깁니다.

## Search Console: 검증 단위가 도메인이냐 URL 접두사냐가 핵심

Search Console은 두 가지 검증(verification) 방식을 지원합니다.

- **도메인 속성(Domain property)**: `saramjh.github.io` 전체를 한 번에 검증. 서브도메인, 프로토콜(http/https), 그리고 `/scratchLottery/`, `/richChecker/` 같은 모든 하위 경로가 자동으로 이 하나의 속성 아래 포함됩니다.
- **URL 접두사 속성(URL-prefix property)**: `https://saramjh.github.io/scratchLottery/`처럼 특정 경로만 정확히 검증.

제가 프로젝트마다 사이트맵을 따로 등록해온 건 URL 접두사 방식에 가까웠는데, 전부 같은 도메인이라면 애초에 도메인 속성 하나로 통합해서 관리하는 편이 검증·데이터 관리 측면에서 중복이 없습니다. 사이트맵 자체는 여전히 프로젝트별로 나눠 제출할 수 있지만(`robots.txt`에 각 도구의 사이트맵 경로를 각각 명시하는 식으로), 이를 감독하는 속성은 도메인 단위 하나로 충분합니다.

## "루트 도메인이 신뢰를 공유한다"는 말의 의미와 한계

이 부분이 가장 조심스러운 지점입니다. "같은 루트 도메인 아래 있으면 신뢰(권위)를 함께 가져간다"는 말은 SEO 커뮤니티에서 자주 언급되지만, 구글이 이를 정확히 어떤 알고리즘으로 반영하는지는 공개되어 있지 않습니다. 다만 아래는 비교적 근거가 명확한 사실들입니다.

- 서브디렉터리(`/scratchLottery/`처럼 경로로 나뉜 구조)는 서브도메인이나 완전히 다른 도메인보다, 검색엔진이 같은 사이트의 일부로 인식하기 쉽습니다. 이건 커스텀 도메인을 붙이지 않은 제 프로젝트 페이지들에 원래부터 해당되는 이야기였습니다.
- 사이트 전체의 크롤링 예산(crawl budget), 백링크, 도메인 나이 같은 신호는 도메인 단위로 누적됩니다. 다만 이게 "구글이 정말로 게재 순위에 반영한다"는 것과 "정확히 어느 정도 반영하는지"는 별개의 문제이고, 후자는 공식적으로 검증하기 어렵습니다.
- 반대로 각 도구는 콘텐츠 성격과 검색 의도가 서로 다르기 때문에, 신뢰를 공유한다고 해서 관련 없는 검색어에서 순위가 저절로 오르는 건 아닙니다.

정리하면, "하나의 루트 도메인 = 신뢰 공유"라는 논리는 **완전히 틀린 말은 아니지만, 인과관계가 실증적으로 증명된 것도 아닌, 업계에서 합리적으로 받아들여지는 정도의 설명**이라고 보는 게 정확할 것 같습니다.

## Clarity: 프로젝트 단위는 결국 "무엇을 함께 보고 싶은가"의 문제

Clarity는 GA4나 Search Console과 달리 공식적으로 "도메인 단위 검증"이라는 개념이 없습니다. 하나의 Clarity 프로젝트 코드를 여러 도메인/경로에 심어도 기술적으로는 동작합니다. 즉 이건 원리의 문제가 아니라 **운영 방침의 문제**에 가까웠습니다.

- 같은 프로젝트로 묶으면: 모든 도구의 세션 리플레이/히트맵을 한 대시보드에서 볼 수 있지만, 도구별로 트래픽 규모가 다르면 특정 도구의 세션이 다른 도구의 세션에 묻힐 수 있습니다.
- 프로젝트를 나누면: 도구별 분석은 깔끔해지지만, 관리해야 할 대시보드 수가 도구 수만큼 늘어납니다.

## 이 근거들을 종합하면

정리하면, 세 도구 모두에서 반복해서 나온 구조는 다음과 같았습니다.

1. **가능한 한 넓은 단위(도메인 전체)에서 검증/속성을 만들고**
2. **그 안에서 하위 경로·호스트네임 같은 필터로 필요할 때만 좁혀서 본다**

이게 제가 실제로 채택한 방향과 같습니다. 다음 편에서는 이 논리를 실제로 어떻게 적용했는지 — 언제, 무엇을 병합했는지 — 를 정리하겠습니다.

→ [3편: 결정과 적용으로 이어집니다](/gh-pages-analytics-notes-3-decision-kr/)

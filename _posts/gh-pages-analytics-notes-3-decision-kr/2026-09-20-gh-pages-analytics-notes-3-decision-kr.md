---
title: "혼자 여러 GitHub Pages를 굴리다 보니 생긴 애널리틱스 고민 (3) — 결정과 적용"
description: "2026년 9월, 프로젝트마다 나눠뒀던 GA4 속성을 하나로 병합했습니다. 무엇을 바꿨고, 왜 이 정도까지만 바꿨는지, 그리고 여전히 자신 없는 부분은 무엇인지 기록합니다."
date: 2026-09-18
tags: ["GA4", "Google Analytics", "Search Console", "Microsoft Clarity", "GitHub Pages", "SEO"]
permalink: /gh-pages-analytics-notes-3-decision-kr/
layout: default
lang: ko
alternate_lang: en
alternate_url: /gh-pages-analytics-notes-3-decision-en/
---

<p style="background: rgba(0, 120, 212, 0.08); border-left: 4px solid #0078d4; padding: 10px 14px; margin-bottom: 16px; border-radius: 4px; font-size: 0.95rem;">
  🌐 <strong>English Edition available:</strong> Read the English version at <a href="/gh-pages-analytics-notes-3-decision-en/"><strong>Analytics Notes (English Edition)</strong></a>.
</p>

<p style="background: rgba(120, 90, 0, 0.08); border-left: 4px solid #b8860b; padding: 10px 14px; margin-bottom: 24px; border-radius: 4px; font-size: 0.9rem;">
  📚 <strong>시리즈 목차</strong> — <a href="/gh-pages-analytics-notes-1-problem-kr/">1편 문제 정의</a> · <a href="/gh-pages-analytics-notes-2-reasoning-kr/">2편 근거 탐색</a> · 3편 <strong>결정과 적용</strong> (현재 글) · <a href="/gh-pages-analytics-notes-4-open-kr/">4편 지금 상태와 열린 질문</a>
</p>

## 무엇을 바꿨나

2026년 9월 중순, 도구별로 나눠뒀던 GA4 속성들을 `saramjh.github.io` 도메인을 대표하는 하나의 GA4 속성으로 병합했습니다. 구체적으로는:

- 기존에 도구마다 따로 있던 GA4 속성들을 정리하고, 블로그가 쓰던 속성(측정 ID `G-4DYFKSNFBG`) 하나로 통합했습니다.
- 각 도구는 이 하나의 속성 아래 별도의 웹 데이터 스트림으로 등록했습니다. [1편](/gh-pages-analytics-notes-1-problem-kr/)에서 나열한 richChecker, scratchLottery, SquircleSimulator, pomodorotimerKR/EN, resizeIMG, space_atlas_student 등이 여기 해당합니다.
- 리포트에서 도구별 트래픽만 보고 싶을 때는 `hostName`(호스트 이름) 기준으로 필터링합니다. 실제로 이 시리즈를 준비하면서 GA4 Data API로 `hostName` 차원을 기준 삼아 세션을 조회해봤는데, `saramjh.github.io`(블로그 및 프로젝트 페이지 대부분)와 로컬 테스트 트래픽(`localhost`, `127.0.0.1`)이 명확히 구분되어 나오는 걸 확인했습니다.

Search Console은 원래도 프로젝트별 사이트맵 제출 방식이었던 걸, 도메인 속성(`saramjh.github.io` 전체 검증) 하나로 관리 단위를 통일했습니다. 사이트맵 자체는 여전히 도구별 경로를 각각 명시해서 제출합니다.

## 바꾸지 않은 것

Microsoft Clarity는 이번에 손대지 않았습니다. [2편](/gh-pages-analytics-notes-2-reasoning-kr/)에서 정리했듯 이건 원리보다는 운영 방침의 문제였고, 아직 도구 수가 각 프로젝트별 세션이 서로를 가릴 만큼 트래픽이 크지 않다고 판단했기 때문입니다. 다만 이건 GA4/Search Console처럼 "구조적으로 이게 맞다"는 확신이 있어서가 아니라, "지금 당장 문제가 크게 느껴지지 않아서 미룬" 결정에 가깝습니다. 트래픽이 늘면 다시 판단해야 할 항목입니다.

## 왜 이 논리를 그대로 받아들였나

솔직히 말하면, [2편](/gh-pages-analytics-notes-2-reasoning-kr/)에서 정리한 논리 중 "GA4 속성/데이터 스트림 구조" 부분은 공식 문서로 명확히 확인되는 내용이라 받아들이는 데 큰 저항이 없었습니다. 반면 "루트 도메인이 신뢰를 공유한다"는 부분은 지금도 반신반의합니다. 다만 이 병합 결정 자체는 그 불확실한 전제가 맞든 틀리든 손해 볼 게 크지 않다고 판단했습니다.

- GA4 속성을 합쳐서 잃는 것: 도구별로 완전히 독립된 대시보드를 보고 싶을 때 필터를 한 번 더 걸어야 하는 정도의 번거로움.
- 합쳐서 얻는 것: 속성 수만큼 늘어나던 관리 부담이 줄고, 블로그 글 → 도구 사용으로 이어지는 흐름을 같은 속성 안에서 볼 수 있게 됨.

즉 "SEO에 긍정적일 것"이라는, 검증되지 않은 기대보다는, "관리가 쉬워지고 손해는 적다"는 훨씬 확실한 이유가 실제 결정의 더 큰 비중을 차지했습니다.

## 마이그레이션하면서 겪은 실무적인 함정

- **속성을 병합하면 과거 데이터는 따라오지 않습니다.** 기존 도구별 속성에 쌓여있던 히스토리는 그대로 각 속성에 남고, 새 통합 속성은 병합 시점부터 데이터가 쌓이기 시작합니다. 과거 데이터가 필요하면 예전 속성을 삭제하지 말고 읽기 전용으로 남겨둬야 합니다.
- **측정 ID를 코드에서 교체하는 걸 잊기 쉽습니다.** 도구마다 레포가 다르다 보니, 새 측정 ID로 바꾸는 작업을 레포 수만큼 반복해야 했고, 하나라도 빠뜨리면 그 도구만 계속 옛날 속성으로 데이터를 보내는 상태가 됩니다.
- **무료 등급 데이터 임계값(threshold)이 하나의 속성으로 합쳐지면서 재적용됩니다.** 트래픽이 아주 많지 않은 지금은 문제가 없었지만, 도구 수가 더 늘어나면 이 부분을 다시 살펴봐야 할 수도 있습니다.

다음 편에서는 이 구조로 바꾼 뒤 지금 실제로 보이는 데이터와, 여전히 답을 모르는 채로 남아있는 질문들을 정리하겠습니다.

→ [4편: 지금 상태와 열린 질문으로 이어집니다](/gh-pages-analytics-notes-4-open-kr/)

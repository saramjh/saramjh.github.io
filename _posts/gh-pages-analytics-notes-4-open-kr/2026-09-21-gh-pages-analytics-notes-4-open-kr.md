---
title: "혼자 여러 GitHub Pages를 굴리다 보니 생긴 애널리틱스 고민 (4) — 지금 상태와 열린 질문"
description: "속성을 병합한 지 얼마 안 됐기 때문에 '효과가 있었다'고 말할 수 있는 데이터는 아직 없습니다. 지금 보이는 스냅샷과, 여전히 답을 모르는 채로 남은 질문들을 정리하며 시리즈를 마칩니다."
date: 2026-09-18
tags: GA4, Google Analytics, Search Console, Microsoft Clarity, GitHub Pages, SEO
permalink: /gh-pages-analytics-notes-4-open-kr/
layout: default
lang: ko
alternate_lang: en
alternate_url: /gh-pages-analytics-notes-4-open-en/
---

<p style="background: rgba(0, 120, 212, 0.08); border-left: 4px solid #0078d4; padding: 10px 14px; margin-bottom: 16px; border-radius: 4px; font-size: 0.95rem;">
  🌐 <strong>English Edition available:</strong> Read the English version at <a href="/gh-pages-analytics-notes-4-open-en/"><strong>Analytics Notes (English Edition)</strong></a>.
</p>

<p style="background: rgba(120, 90, 0, 0.08); border-left: 4px solid #b8860b; padding: 10px 14px; margin-bottom: 24px; border-radius: 4px; font-size: 0.9rem;">
  📚 <strong>시리즈 목차</strong> — <a href="/gh-pages-analytics-notes-1-problem-kr/">1편 문제 정의</a> · <a href="/gh-pages-analytics-notes-2-reasoning-kr/">2편 근거 탐색</a> · <a href="/gh-pages-analytics-notes-3-decision-kr/">3편 결정과 적용</a> · 4편 <strong>지금 상태와 열린 질문</strong> (현재 글)
</p>

## 먼저 분명히 할 것: 이건 "효과 검증"이 아닙니다

병합한 지 아직 얼마 되지 않았고, 병합 전후를 비교할 만큼 충분한 기간의 데이터도, 통제된 비교군도 없습니다. 그래서 이 글은 "GA4를 통합했더니 트래픽/순위가 올랐다"를 증명하는 글이 아닙니다. 지금 시점에 보이는 걸 스냅샷으로 남기고, 앞으로 이 구조가 맞았는지 스스로 점검할 수 있는 기준을 정리해두는 정도입니다.

## 지금 보이는 스냅샷

통합된 GA4 속성에서 최근 90일 기준 `hostName`으로 세션을 나눠보면 대략 이런 모양입니다.

| 호스트 | 세션 | 활성 사용자 |
| :--- | :--- | :--- |
| saramjh.github.io | 672 | 651 |
| 127.0.0.1 (로컬 테스트) | 16 | 16 |
| localhost (로컬 테스트) | 1 | 1 |

여기서 확인할 수 있는 건 딱 한 가지입니다 — **호스트네임 필터가 실제로 의도대로 작동한다는 것**. 로컬 개발 중 발생한 트래픽이 실제 사용자 트래픽과 명확히 분리되어 잡히고 있으니, "필요할 때 좁혀서 본다"는 [2편](/gh-pages-analytics-notes-2-reasoning-kr/)의 설계 의도는 최소한 기능적으로는 성립합니다. 이 숫자 자체가 병합의 "효과"를 뜻하지는 않습니다 — 병합 전에 이 구조로 같은 기간을 비교해본 적이 없기 때문입니다.

## 여전히 답을 모르는 것들

- **SEO에 실제로 영향이 있었는가**: [2편](/gh-pages-analytics-notes-2-reasoning-kr/)에서 짚었듯, 루트 도메인 신뢰 공유는 인과관계가 실증된 적이 없는 설명입니다. Search Console에서 몇 달 뒤 색인/노출 추이를 지켜봐야 뭔가 말할 수 있을 텐데, 지금은 판단할 근거가 없습니다.
- **Clarity를 언제 통합해야 하는가**: 지금은 트래픽이 적어 미룬 결정인데, 어느 시점(어느 정도 트래픽)이 되면 다시 검토해야 할지 기준을 정해두지 않았습니다.
- **도구가 훨씬 더 늘어나면 이 구조가 그대로 버틸까**: 데이터 스트림이 지금의 10개 안팎에서 수십 개로 늘어나면, 하나의 속성 안에서 관리하는 게 여전히 최선일지 다시 봐야 할 것 같습니다. 무료 등급 데이터 임계값도 그때 다시 확인이 필요합니다.
- **애초에 이 문제가 "1인 개발자, 다중 프로젝트, 단일 루트 도메인"이라는 조합에서만 유효한 고민인지**: 팀 단위로 여러 서비스를 운영하는 경우와는 상황이 다를 수 있어서, 이 시리즈의 결론을 그대로 일반화하기는 조심스럽습니다.

## 같은 고민을 하는 분들께

같은 상황(커스텀 도메인 없는 GitHub Pages 프로젝트 페이지 여러 개)에 계신 분이라면, 최소한 아래 세 가지는 자신의 계정에서 직접 확인해보시길 권합니다.

1. 실제로 커스텀 도메인을 안 붙인 프로젝트들이 전부 같은 루트 도메인 아래 있는지 (`https://<계정>.github.io/<레포>/` 형태인지)
2. GA4에서 "속성"과 "데이터 스트림"을 구분해서 쓰고 있는지, 아니면 저처럼 매번 속성을 새로 만들고 있었는지
3. Search Console을 도메인 속성으로 검증했는지, URL 접두사로 프로젝트마다 따로 검증했는지

이 시리즈가 정답을 제시하지는 못했지만, 적어도 이 세 가지 질문 자체는 확인해볼 가치가 있다고 생각합니다. 저도 트래픽이 늘거나 새로운 사실을 알게 되면, 이 시리즈에 이어서 다시 기록을 남기겠습니다.

← [1편부터 다시 보기](/gh-pages-analytics-notes-1-problem-kr/)

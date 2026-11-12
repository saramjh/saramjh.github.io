---
title: "Spoonie 첫 화면의 브랜드 인트로를 다시 살린 이유"
description: "Spoonie PR #35에서 첫 홈 방문 스플래시를 복원하고 화면 이동과 오류 상황을 분리한 구현 기록."
date: 2026-11-12
tags: ["Spoonie", "Frontend", "User Experience"]
permalink: /spoonie-first-visit-splash-ko/
layout: default
lang: ko
alternate_lang: en
alternate_url: /spoonie-first-visit-splash-en/
published: true
seo:
  title: "Spoonie 첫 방문 브랜드 스플래시 복원 | PR #35"
  description: "첫 방문 인트로와 내부 페이지 로딩을 분리한 Spoonie PR #35의 구현과 검증 범위."
---

> English: [Restoring Spoonie's first-visit introduction](/spoonie-first-visit-splash-en/)

Spoonie의 첫 홈 방문에서 보이던 브랜드 인트로를 복원했다. [PR #35](https://github.com/saramjh/spoonie/pull/35)는 2026년 11월 12일 병합됐다. 앞선 성능 정비에서 첫 화면 인트로까지 제거된 회귀를 바로잡은 변경이다.

## 첫 방문과 화면 이동은 다르게 다뤄야 한다

브랜드 인트로는 사이트를 처음 만나는 순간에만 필요하다. 레시피를 읽다가 다른 페이지로 이동할 때마다 같은 화면이 나타나면 탐색을 방해한다. 그래서 최초 홈 진입과 내부 경로 이동을 구분했다.

## 실제 변경 내용

- 첫 홈 진입에 정적 SSR 로고 인트로를 다시 표시한다.
- 같은 탭에서 이미 표시했는지는 `sessionStorage`로 관리한다.
- 인트로는 약 1.6초 뒤 종료되며, React 초기화가 늦어져도 CSS가 화면을 가린 상태로 남지 않게 한다.
- 내부 이동이나 직접 연 레시피 상세 주소에는 인트로를 띄우지 않는다.

원본 PR에는 Vitest 377개 통과, TypeScript·ESLint·프로덕션 빌드 및 로컬 화면 폭별 확인이 기록돼 있다. 이는 PR 작성자의 테스트 보고이며 Dev가 동일한 브라우저 시나리오를 재실행한 결과는 아니다.

## 운영 환경에서 확인한 범위

[공개 홈페이지](https://spoonie.kr/)는 HTTP 200을 반환했고, 제공된 HTML에 `spoonie-splash` 세션 키와 `splash-seen` 처리 코드가 포함돼 있었다. 복원에 필요한 초기 진입 로직이 배포되어 있다는 근거다. 다만 실제 사용자 브라우저에서 1.6초 표시·종료 동작을 재현하거나 이용자 반응을 측정하지는 않았다.

[변경 코드 보기](https://github.com/saramjh/spoonie/pull/35) · [Spoonie 방문](https://spoonie.kr/) · [이전 로딩 최적화 기록](/spoonie-route-loading-citation-ko/)

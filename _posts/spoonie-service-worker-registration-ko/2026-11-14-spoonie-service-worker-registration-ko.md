---
title: "Spoonie PWA: 서비스 워커 등록 실패 경로 정비"
description: "Spoonie PR #40에서 Workbox 자동 등록을 제거하고 브라우저 기본 등록 API로 전환한 이유와 운영 번들 확인 결과."
date: 2026-11-14
tags: ["Spoonie", "PWA", "Frontend"]
permalink: /spoonie-service-worker-registration-ko/
layout: default
lang: ko
alternate_lang: en
alternate_url: /spoonie-service-worker-registration-en/
published: true
seo:
  title: "서비스 워커 등록 오류를 처리한 Spoonie PWA 수정"
  description: "브라우저가 등록을 거부할 때 발생할 수 있는 Workbox 오류를 줄이기 위해 등록 경로를 바꾼 개발 사례."
---

> English: [Handling blocked service worker registration in Spoonie](/spoonie-service-worker-registration-en/)

레시피를 읽는 데 서비스 워커 등록이 선행될 필요는 없다. 그런데 Spoonie의 이전 PWA 자동 등록 경로에서는 브라우저가 등록을 거부할 때 `Workbox-window`가 유효하지 않은 등록 객체를 다루며 오류를 낼 수 있었다. 2026년 11월 13일 병합된 [PR #40](https://github.com/saramjh/spoonie/pull/40)에서 이 경로를 수정했다.

## 등록을 맡는 코드가 둘이었다

`next-pwa`의 `register: true`가 자동 등록을 처리했고, 앱의 `ServiceWorkerUpdater`는 별도로 서비스 워커 업데이트를 관리했다. 자동 등록 단계에서 문제가 생기면 업데이트 컴포넌트가 그 실패를 통제하기 어려웠다.

수정한 설정은 `register: false`다. 대신 기존 업데이트 컴포넌트가 `navigator.serviceWorker.register("/sw.js", { scope: "/" })`를 호출한다. 브라우저 지원 여부와 프로덕션 환경을 먼저 확인하고, 결과가 없거나 컴포넌트가 해제된 경우 후속 작업을 멈춘다. 등록 Promise가 실패하는 경우도 컴포넌트 안에서 처리한다.

서비스 워커 등록에 성공한 환경에서는 기존 `updatefound`와 `controllerchange` 업데이트 흐름을 유지한다. 런타임 캐시 설정도 제거하지 않았다.

## 운영 사이트에서 확인한 코드

2026년 11월 14일 [Spoonie](https://spoonie.kr/)는 HTTP 200을 반환했다. 실제 제공된 Next.js `app/layout` JavaScript 번들에는 `/sw.js`를 직접 등록하고 등록 결과를 검사한 뒤 `.catch()`로 실패를 처리하는 코드가 포함돼 있었다. [변경 커밋](https://github.com/saramjh/spoonie/commit/bc2349b231dee6af087bb210488e53ec7c087f9b)의 핵심 등록 방식이 운영 코드에도 들어간 것이다.

PR에 추가된 회귀 테스트 2개는 자동 등록 비활성화, 캐시 설정 유지, 수동 등록 코드를 검사한다. 소스 수준 테스트이며, 서비스 워커를 실제로 차단한 브라우저별 실행 시험은 별도로 확인되지 않았다. 오류 발생률이나 레시피 조회 증가도 측정되지 않았다.

## 다른 PWA에서도 살펴볼 점

[MDN의 `register()` 문서](https://developer.mozilla.org/en-US/docs/Web/API/ServiceWorkerContainer/register)에 따르면 등록은 Promise를 반환하고 실패할 수 있다. 성공 경로와 함께 등록 거부 시 앱이 어떻게 동작하는지 시험하는 편이 좋다.

앞서 진행한 [사용자별 좋아요·저장 캐시 분리](/spoonie-viewer-cache-isolation-ko/)는 계정별 화면 데이터의 경계를 다뤘다. 이번 수정은 PWA 초기화 과정의 실패 처리를 다룬다.

[PR #40 보기](https://github.com/saramjh/spoonie/pull/40) · [Spoonie 열기](https://spoonie.kr/)

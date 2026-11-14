---
title: "Spoonie의 화면 전환 로딩과 레시피 인용 검색 정비"
description: "Spoonie 화면 전환 중 잘못된 로딩 표시와 지연 복구를 수정한 사례. 목적지 스켈레톤·입력 제어·레시피 인용 검색을 함께 다룹니다."
date: 2026-11-12
tags: ["Spoonie", "Frontend", "User Experience"]
permalink: /spoonie-route-loading-citation-ko/
layout: default
lang: ko
alternate_lang: en
alternate_url: /spoonie-route-loading-citation-en/
published: true
modified: 2026-11-14
seo:
  title: "Spoonie 화면 전환 로딩·레시피 인용 검색 개선"
  description: "Spoonie 목적지 스켈레톤·숨겨진 입력창 제어·취소된 링크와 지연된 화면 이동 복구의 구현 및 배포 검증."
---

> English: [Route loading and recipe citation search in Spoonie](/spoonie-route-loading-citation-en/)

Spoonie의 화면 전환 로딩과 레시피 인용 검색 인터페이스를 정비했다. [PR #34](https://github.com/saramjh/spoonie/pull/34)는 2026년 11월 12일 병합됐으며, 변경된 코드가 공개 서비스의 JavaScript에도 포함된 것을 확인했다.

## 사용자가 마주하는 두 지점

레시피를 찾다가 다른 화면으로 이동할 때는 전환 상태를 이해할 수 있어야 한다. 다른 레시피를 인용하려는 순간에는 검색 결과를 확인하고 선택하는 흐름이 분명해야 한다. 이번 변경은 이 두 접점을 다룬다.

## 구현과 검증 범위

병합된 변경에는 화면 전환 로딩 처리와 레시피 인용 검색 UI 정비가 포함된다. 원본 코드와 운영 환경에서 제공되는 JavaScript를 대조해 변경 코드의 배포를 확인했다.

다만 공개 번들에 코드가 있다는 사실만으로 실제 체감 속도 개선이나 인용 기능의 사용량을 알 수는 없다. 그런 수치는 별도로 측정되지 않았다.

Spoonie의 다른 화면 상태 문제는 [계정별 좋아요·저장 캐시 분리](/spoonie-viewer-cache-isolation-ko/)에서 다뤘다.

## 11월 14일 후속 개선: 목적지 화면을 먼저 보여주기

기존 진행 막대만으로는 응답이 늦을 때 페이지를 눌렀다는 피드백이 부족했다. [PR #42](https://github.com/saramjh/spoonie/pull/42)의 재현 테스트에서는 `/search` 서버 응답을 늦추자 이전 홈 화면이 700ms 넘게 남았다. 이 문제를 해결하기 위해 내부 화면 이동이 시작되는 즉시 목적지 형태의 스켈레톤을 표시하도록 바꿨다.

검색 화면으로 이동하면 검색창과 필터 자리부터, 레시피·게시물 상세로 이동하면 상세 화면의 자리 표시부터 보인다. 상단 진행 막대는 그대로 두고, 진행 중에도 하단 메뉴로 다른 화면을 선택할 수 있게 했다. 검색 필터처럼 주소의 쿼리만 바뀌는 경우에는 전체 화면을 가리지 않는다.

지연된 경로를 재현한 로컬 Chromium 테스트에서 스켈레톤은 90·200·500·950ms에 표시됐고, 새 화면이 준비되자 사라졌다. 회귀 테스트 405개와 별도 미디어 테스트 6개도 통과했다. 11월 14일 확인한 [운영 Spoonie](https://spoonie.kr/)의 `app/layout` JavaScript는 PR #42 Netlify 미리보기와 바이트 단위로 같았으며, `data-route-feedback` 구현을 포함했다. 실제 방문자의 체감 속도나 이탈률 변화는 아직 측정하지 않았다.

### 11월 14일 후속 보완: 가려진 입력과 잘못된 로딩 표시 없애기

목적지 스켈레톤 뒤에 남아 있는 검색창에 키보드로 입력할 수 있는 문제가 있었다. [PR #43](https://github.com/saramjh/spoonie/pull/43)은 화면 이동 중 이전 `main`에 `inert`를 적용해 입력을 막고, 목적지에서 계산할 수 있는 중복 `needsHeader` 상태를 제거했다. 사진 터치 후 포인터가 벗어나더라도 기존 300ms 싱글탭·더블탭 판정 시간에는 눌림 표시가 유지된다.

이후에는 앱에서 취소한 링크도 전역 클릭 감지기가 화면 이동으로 오인하는 문제가 드러났다. 실제로 이동하지 않는데도 전체 스켈레톤이 나타날 수 있었다. [PR #44](https://github.com/saramjh/spoonie/pull/44)는 전역 클릭 감지를 제거하고, 링크의 이동이 취소되지 않았을 때만 Next.js `onNavigate`에서 시작 신호를 보낸다. 코드로 이동하거나 뒤로 가는 동작은 기존 경로를 사용한다.

목적지 응답이 10초 넘게 지연되면 진행 상태를 그냥 지우지 않고 **이전 화면 유지**와 **다시 시도**를 선택할 수 있게 했다. 쿼리만 바뀌는 이동은 기존 동작을 유지한다. PR #44에는 Vitest 407개·미디어 안전성 검사 6개 통과와 취소된 링크·뒤로 가기·키보드 포커스·재시도를 다룬 Chromium 테스트가 기록돼 있다. [11월 14일 운영 레이아웃 번들](https://spoonie.kr/_next/static/chunks/app/layout-ef63d2df452ac6a9.js)에서도 복구 문구와 화면 전환 구현을 확인했다. 이는 코드의 배포 근거이며 실제 이용자의 이탈 감소를 측정한 결과는 아니다.

### 실제 배포 미리보기에서 회귀검사하기

소스 파일에 특정 문자열이 있는지만 검사해서는 사용자가 보는 화면이 정상인지 알 수 없다. [PR #45](https://github.com/saramjh/spoonie/pull/45)에서는 화면 이동 관련 코드가 바뀐 PR마다 GitHub Actions가 **해당 PR의 정확한 커밋**에 대한 Netlify 배포 미리보기 성공을 확인한 뒤, 배포된 페이지를 Chromium으로 테스트하도록 했다. Next.js의 네 개 `loading.tsx` 컴포넌트도 파일 내용 검색 대신 실제 렌더링 결과로 검증한다.

구현한 PR에서도 검사가 실행됐다. [GitHub Actions 실행 #43580339700](https://github.com/saramjh/spoonie/actions/runs/43580339700)은 `e4bc2ef` 커밋의 미리보기를 확인하고 일반 링크 이동, 뒤로 가기, 취소된 링크, 지연 상태 취소·재시도, 사진 첫 터치 표시를 검사해 통과했다. 브라우저 JavaScript 예외도 없었다. 이는 앞으로 같은 유형의 변경에서 회귀를 발견하기 위한 장치이며, 실제 방문자 속도나 이탈률을 측정한 결과는 아니다.

[원본 변경 사항](https://github.com/saramjh/spoonie/pull/34) · [Spoonie](https://spoonie.kr/)

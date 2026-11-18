---
title: "Spoonie: iPhone 홈 화면 앱과 검색 상태 복원"
description: "Spoonie PR #47의 서비스 워커 업데이트 확인, 검색어·탭 URL 복원, 결과 수 표시와 브라우저 회귀 테스트를 정리한다."
date: 2026-11-16
tags: ["Spoonie", "PWA", "Frontend", "Search"]
permalink: /spoonie-pwa-search-state-recovery-ko/
layout: default
lang: ko
alternate_lang: en
alternate_url: /spoonie-pwa-search-state-recovery-en/
image: /assets/img/dev/spoonie-pr47-pwa-og-20261118/spoonie-pr47-ko.png
image_width: 1200
image_height: 630
published: true
seo:
  title: "Spoonie iPhone PWA와 검색 상태 복원"
  description: "홈 화면 설치본의 업데이트 확인과 검색 결과에서 상세 화면을 거쳐 돌아오는 흐름을 수정한 Spoonie PR #47 사례."
---

> English: [Restoring Spoonie's iPhone PWA updates and search state](/spoonie-pwa-search-state-recovery-en/)

Spoonie에서 두 가지 사용 흐름이 끊겼다. iPhone 홈 화면에 설치한 앱이 새 배포 이후에도 이전 화면을 보여주는 경우가 있었고, 검색 결과에서 레시피를 열었다가 브라우저 뒤로 가기를 누르면 검색어와 선택한 탭, 결과 목록이 초기화됐다. 검색 결과 수도 모든 페이지를 불러온 뒤에야 표시됐다.

2026년 11월 16일 병합된 [Spoonie PR #47](https://github.com/saramjh/spoonie/pull/47)은 이 세 흐름을 함께 수정했다.

## 레시피를 보고 돌아와도 검색을 이어가기

기존 재현 절차에서는 실제 검색 화면에서 \`김치\`를 입력하면 레시피 링크 19개가 표시됐다. 그중 하나를 열고 뒤로 돌아오면 검색어가 비어 있고 URL에도 검색 조건이 남지 않았다.

이제 검색어를 확정하면 현재 경로에 \`?q=...\`를 기록한다. 레시피·게시물·사용자 탭을 선택하면 필요한 경우 \`?tab=...\`도 함께 저장한다. 기존 URL 매개변수는 유지한다. 페이지가 다시 마운트되거나 브라우저의 \`popstate\`가 발생하면 URL에서 검색어와 탭을 복원한다.

검색 결과를 불러오는 SWR 페이지 캐시는 컴포넌트가 다시 마운트돼도 재사용한다. 새 검색어로 바꾸면 첫 페이지부터 요청해 불필요한 추가 페이지 요청을 만들지 않는다.

결과 수 표기도 바꿨다. 첫 페이지가 도착하면 현재 로드된 항목 수를 바로 보여준다. 더 불러올 페이지가 있으면 \`N+\`로 표시하고, 마지막 페이지까지 받은 뒤에만 최종 개수를 표시한다. PR의 결정적 RPC 테스트 픽스처는 첫 페이지의 20개 이상 결과와 마지막 페이지까지 받은 22개 결과를 검증한다. 이 22는 테스트 데이터이며 실제 이용자 검색량을 뜻하지 않는다.

## iPhone 홈 화면 설치본의 업데이트 확인

기존 서비스 워커 등록과 Workbox 구성을 유지하면서 업데이트 확인 시점을 늘렸다. 등록 직후와 온라인 복귀, \`pageshow\`, 앱이 다시 전면에 나타날 때 기존 등록 객체에 \`update()\`를 요청한다. 업데이트 확인은 1분에 한 번으로 제한한다. 등록 옵션에는 \`updateViaCache: "none"\`을 지정해 오래된 가져오기 스크립트 캐시가 새 서비스 워커 확인을 방해하지 않도록 했다.

새 서비스 워커가 컨트롤러가 되면 독립 실행형 홈 화면 앱은 안전한 경우 현재 페이지를 다시 불러온다. 레시피나 게시물을 편집하는 경로, 입력창 또는 편집 가능한 요소에 포커스가 있는 동안에는 자동 새로고침하지 않는다. 일반 브라우저에서는 기존 수동 업데이트 안내를 유지한다.

로컬 저장소나 작성 중인 초안을 지우는 방식은 사용하지 않는다.

## 브라우저 테스트와 운영 코드 확인

[PR #47](https://github.com/saramjh/spoonie/pull/47)은 2026년 11월 16일 \`e563ab228642d4262cbca95a6c2c0d96468c185f\`로 병합됐다. [GitHub Actions 실행 43877018376](https://github.com/saramjh/spoonie/actions/runs/43877018376)은 성공했다. 이 작업은 해당 커밋의 Netlify 미리보기 배포를 기다린 뒤 실제 Chromium 브라우저 회귀 테스트를 실행했다.

테스트는 검색어·탭·결과·스크롤 위치를 유지한 채 상세 화면으로 이동하고 뒤로 돌아오는 흐름, 페이지별 결과 수, 이전에 로드한 페이지의 재사용, 새 검색어의 첫 페이지 요청, 독립 실행형 서비스 워커 업데이트 확인, 입력 중 새로고침 방지를 다룬다.

운영 [Spoonie 검색 페이지](https://spoonie.kr/search?q=%EA%B9%80%EC%B9%98)와 [서비스 워커 파일](https://spoonie.kr/sw.js)은 HTTP 200을 반환했다. 제공되는 운영 JavaScript에서도 \`app/layout\` 번들의 \`updateViaCache\`와 \`controllerchange\`, 검색 페이지 번들의 \`popstate\`와 \`URLSearchParams\` 코드를 확인했다.

원격 Chromium 테스트는 통과했지만 실제 iPhone 기기에서 설치된 홈 화면 앱을 대상으로 한 현장 검증은 수행하지 않았다. 업데이트 성공률, 재방문율 또는 이용자 수 변화도 측정하지 않았다.

## 이어서 볼 자료

- [Spoonie 검색 탐색과 검색엔진용 초기 목록](/spoonie-search-discovery-ko/)
- [Spoonie 서비스 워커 등록 실패 처리](/spoonie-service-worker-registration-ko/)
- [Spoonie 북마크 개인정보 경계](/spoonie-bookmark-privacy-boundary-ko/)

[PR #47 보기](https://github.com/saramjh/spoonie/pull/47) · [병합 커밋 보기](https://github.com/saramjh/spoonie/commit/e563ab228642d4262cbca95a6c2c0d96468c185f) · [Spoonie 열기](https://spoonie.kr/)

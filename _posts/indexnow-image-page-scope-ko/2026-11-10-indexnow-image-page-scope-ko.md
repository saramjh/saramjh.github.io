---
title: "이미지 한 장을 바꿨는데 IndexNow에는 URL 120개가 전송됐다"
description: "GitHub Pages에서 이미지 변경을 사이트 전체 변경으로 판단한 문제를 재현하고, 실제 참조 페이지로 전송 범위를 좁힌 개발 기록."
date: 2026-11-10
tags: ["IndexNow", "GitHub Pages", "Jekyll", "Python", "배포 자동화"]
permalink: /indexnow-image-page-scope-ko/
layout: default
lang: ko
alternate_lang: en
alternate_url: /indexnow-image-page-scope-en/
published: true
image: /assets/img/dev-indexnow-image-scope-20261110/indexnow-scope-ko.png
image_width: 1200
image_height: 630
seo:
  title: "IndexNow 이미지 변경 시 전체 URL 전송을 막은 방법"
  description: "포트폴리오 PNG 한 장의 변경으로 URL 120개가 전송된 원인과 수정. Git 참조 검색, permalink, 보수적 예외 처리 및 실제 배포 검증."
---

> **English:** [One image change sent 120 URLs to IndexNow](/indexnow-image-page-scope-en/)

2026년 11월 10일, 개발 블로그의 [포트폴리오](/portfolio/)에 Playwright CI 사례와 원본 이미지를 추가했다. 배포는 성공했지만 검색엔진 알림 단계에서 예상 밖의 결과가 나왔다. 변경된 페이지는 한 곳인데 **IndexNow로 URL 120개가 전송됐고 서버는 HTTP 200 Accepted를 반환했다.**

<figure>
<img src="/assets/img/dev-indexnow-image-scope-20261110/indexnow-scope-ko.png" alt="실제 IndexNow 전송 120개 URL과 HTTP 200 접수, 수정 코드를 이용한 오프라인 재검사에서 /portfolio/ 1개 URL, 수정 후 배포에서는 변경 URL 0개라 전송 생략. 서로 다른 실행 결과." width="1200" height="630" loading="lazy" style="width:100%;height:auto;">
<figcaption>동일한 사건에서 나온 세 종류의 증거. 120은 실제 전송, 1은 오프라인 재검사, 0은 수정 후 별도 배포에서 선택된 URL 수다. 검색 색인이나 유입 수치가 아니다.</figcaption>
</figure>

이 숫자는 [해당 GitHub Actions 실행](https://github.com/saramjh/saramjh.github.io/actions/runs/42760722178)에 남아 있다. 120개 페이지가 모두 바뀌었다는 의미도, 검색엔진이 이를 색인했다는 의미도 아니다. 알림 스크립트가 변경 범위를 너무 넓게 잡았다.

## 왜 이미지 한 장이 사이트 전체 변경이 됐나

배포 스크립트는 이전 커밋과 현재 커밋의 차이를 보고 Bing과 IndexNow에 알릴 URL을 고른다. 초기 구현은 <code>assets/</code> 아래 파일이 바뀌면 그 이미지가 어느 페이지에서 쓰이는지 확인하지 않고 사이트맵 전체를 대상으로 삼았다.

공통 헤더나 스타일을 바꾸면 여러 페이지에 영향을 줄 수 있어 보수적인 판단이 필요하다. 하지만 [PR #38](https://github.com/saramjh/saramjh.github.io/pull/38)에 추가한 PNG는 포트폴리오 페이지에서만 참조했다. 이미지 저장 경로만으로 사이트 전체가 수정됐다고 가정한 것이 문제였다. 이미 접수된 120개 URL 제출 기록은 유지했고 다시 보내지 않았다.

## 파일 위치 대신 참조 페이지를 찾다

[PR #39](https://github.com/saramjh/saramjh.github.io/pull/39/files)에서는 이미지 경로를 실제로 참조하는 원본 파일을 Git에서 검색하도록 바꿨다. 기준은 변경 전과 변경 후, 두 리비전이다. 기존 페이지에서 이미지가 제거된 경우도 놓치지 않기 위해서다.

~~~text
변경된 이미지 경로
    ↓
이전·현재 리비전에서 정확한 이미지 참조 검색
    ↓
참조한 Markdown/HTML의 permalink 확인
    ↓
확인된 페이지 URL만 알림 대상으로 선정
~~~

<code>portfolio/index.html</code>이 포트폴리오용 PNG를 참조하면 해당 이미지 변경은 <code>/portfolio/</code>에 연결한다. 블로그 글에서 사용한 이미지라면 글 주소와, 최신 글 미리보기가 나오는 홈 주소도 고려한다.

모든 이미지를 억지로 한 페이지에 귀속시키지는 않았다. 공통 템플릿에서 참조하거나 실제 사용 위치를 확정할 수 없으면 사이트맵 전체를 대상으로 두는 기존 보수적 처리를 유지한다. Git 차이 자체가 검증되지 않으면 알림을 보내지 않는다.

## 실제 제출과 오프라인 검사 구분하기

| 확인 상황 | URL 선정 결과 | 근거 |
|---|---|---|
| 수정 전 실제 배포 | 120개 URL 전송, HTTP 200 Accepted | [Actions #42760722178](https://github.com/saramjh/saramjh.github.io/actions/runs/42760722178) |
| 수정된 코드로 당시 변경분을 재검사 | <code>/portfolio/</code> 한 페이지 | [PR #39 회귀 테스트](https://github.com/saramjh/saramjh.github.io/pull/39/files) |
| 수정 코드만 배포한 최종 실행 | 변경 페이지 URL 0개, Bing·IndexNow 전송 생략 | [Actions #42761734284](https://github.com/saramjh/saramjh.github.io/actions/runs/42761734284) |

두 번째 행은 **오프라인 재검사 결과**다. 수정 뒤 실제로 URL 한 개를 IndexNow에 다시 보냈다는 뜻이 아니다.

수정 작업은 Python 테스트 26개를 통과했고, PR #39의 병합과 GitHub Pages 배포도 성공했다. 회귀 테스트는 이미지가 한 페이지에서 쓰일 때, 여러 페이지에 쓰일 때, 공통 템플릿에서 쓰일 때, 참조 위치가 확인되지 않을 때를 구분한다.

## 다음 배포에서 확인할 것

앞으로는 변경 파일 목록만 보고 알림이 정확하다고 판단하지 않으려 한다. 실제 사용 페이지로 매핑되는지, 공통 자산을 안전하게 처리하는지, 아무 페이지도 바뀌지 않았을 때 알림을 생략하는지를 배포 로그에서 따로 확인해야 한다.

이번 수정으로 확인한 것은 URL 선정 로직과 배포 동작이다. **검색 색인 증가, 방문자 증가 또는 전환 증가는 측정하지 않았다.** 비슷한 GitHub Actions 개선 기록은 [Playwright 브라우저 준비 시간을 줄인 사례](/playwright-github-actions-runner-chrome-ko/)에 정리했다.

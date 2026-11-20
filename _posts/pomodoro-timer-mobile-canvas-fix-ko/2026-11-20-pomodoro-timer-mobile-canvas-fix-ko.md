---
title: "포모도로 타이머 모바일 레이아웃과 다이얼 입력 수정"
description: "영문·국문 포모도로 타이머의 모바일 가로 넘침과 캔버스 좌표 오류를 수정했다. Node 회귀 테스트와 여섯 화면 크기의 Chrome 검증 결과를 정리했다."
date: 2026-11-20
tags: ["pomodoro", "pomodorotimer", "뽀모도로", "포모도로", "포모도로타이머", "뽀모도로타이머", "JavaScript", "반응형 웹", "Canvas", "모바일"]
related_urls: ["/pomodoro-timer-kr/"]
permalink: /pomodoro-timer-mobile-canvas-fix-ko/
layout: default
lang: ko
alternate_lang: en
alternate_url: /pomodoro-timer-mobile-canvas-fix-en/
image: /pomodoro-timer-mobile-canvas-fix-ko/pomodoro-mobile-fix-ko-og.png
image_width: 1200
image_height: 630
published: true
seo:
  title: "포모도로 타이머 모바일 수정: 레이아웃과 캔버스 입력"
  description: "영문·국문 포모도로 타이머의 모바일 가로 넘침과 캔버스 좌표 오류를 수정했다. Node 회귀 테스트와 여섯 화면 크기의 Chrome 검증 결과를 정리했다."
---

> English edition: [Fixing mobile layout and dial input in the Pomodoro timer](/pomodoro-timer-mobile-canvas-fix-en/)

# 포모도로 타이머 모바일 레이아웃과 다이얼 입력 수정

2026년 11월 20일, 영문과 국문 포모도로 타이머의 모바일 문제를 수정했다. 이제 좁은 화면에서도 타이머 카드가 뷰포트 안에 표시되고, 다이얼은 실제 캔버스 표시 크기를 기준으로 클릭 위치를 계산한다. 기존에는 화면이 좁으면 카드가 뷰포트보다 넓어졌고, 위쪽이 화면 밖으로 밀리기도 했다. CSS가 캔버스를 축소한 상태에서는 다이얼이 누른 위치와 다른 시간을 선택했다.

두 타이머의 기본 설정인 집중 25분과 휴식 5분은 그대로 유지한다. 조작 방법은 [영문 안내](/pomodoro-timer-en/)와 [국문 안내](/pomodoro-timer-kr/)에서 볼 수 있다. 실제 운영 페이지는 [영문 타이머](https://saramjh.github.io/pomodorotimerEN/)와 [국문 타이머](https://saramjh.github.io/pomodorotimerKR/)다.

<figure>
  <img src="pomodoro-ko-mobile.png" alt="390픽셀 모바일 화면에서 실행한 국문 포모도로 타이머. 원형 타이머와 분·초 입력란, 조작 버튼, 타이머 이력이 보인다." width="390" height="844" loading="lazy" style="display:block;width:100%;max-width:390px;height:auto;margin:auto;">
  <figcaption>배포가 끝난 국문 운영 페이지를 390 × 844 CSS 픽셀에서 캡처했다.</figcaption>
</figure>

## 모바일 화면에서 발생한 문제

타이머 컨테이너의 지정 너비는 350픽셀이었고 좌우 패딩은 각각 20픽셀이었다. 기본 박스 모델에서는 패딩이 지정 너비에 포함되지 않아 실제 너비가 390픽셀이 됐다. 본문은 `height: 100vh`로 높이를 고정한 채 카드를 세로 중앙에 배치했다. 카드가 화면보다 길어지면 위쪽이 뷰포트 밖으로 밀렸다.

캔버스 내부 그림은 300 × 300픽셀 버퍼에 그려진다. 모바일에서는 CSS가 표시 크기를 줄이는데, 기존 입력 계산은 실제 표시 크기 대신 캔버스 내부 너비와 높이로 중심을 구했다. 클릭 좌표와 중심점이 서로 다른 기준을 사용하고 있었다.

회귀 테스트는 표시 크기가 200 × 200픽셀이고 시작점이 `left: 20, top: 50`인 캔버스를 사용한다. `219, 150` 지점을 누르면 375초, 즉 6분 15초가 선택되어야 한다. 수정 전 계산 결과는 185초, 즉 3분 5초였다.

## 레이아웃과 다이얼 수정

본문 높이를 고정하는 대신 `min-height: 100vh`를 적용하고 `box-sizing: border-box`와 16픽셀 패딩을 지정했다. 타이머 컨테이너에는 `max-width: 100%`와 border-box를 적용했다. 캔버스는 `max-width: 100%`, `height: auto`로 표시 영역에 맞춰 줄어들면서 비율을 유지한다. 입력란과 버튼에도 border-box를 적용했다.

다이얼 중심은 CSS가 실제로 표시하는 캔버스 사각형에서 계산한다.

```js
const rect = this.canvas.getBoundingClientRect()
const centerX = rect.left + rect.width / 2
const centerY = rect.top + rect.height / 2
```

캔버스 내부의 300 × 300픽셀 버퍼는 그대로 둔다. 클릭 위치를 해석할 때 사용하는 중심점만 화면에 표시된 크기에 맞췄다.

## 회귀 테스트와 운영 브라우저 검증

영문과 국문 저장소에 타이머 입력 테스트를 각각 세 개 추가했다.

1. 실제 `timerCanvas` 요소를 기준으로 앱이 초기화되는지 확인한다.
2. 원의 4분의 1 지점을 누르면 375초가 선택되고 분·초 입력란에 6과 15가 표시되는지 확인한다.
3. CSS로 표시 크기가 200 × 200픽셀로 줄어든 캔버스에서도 같은 결과가 나오는지 확인한다.

두 저장소의 테스트 여섯 개가 모두 통과했다.

이후 영문과 국문 운영 페이지를 headless Chrome으로 열어 280 × 600, 320 × 640, 375 × 667, 390 × 844, 768 × 1024, 1440 × 900 화면에서 확인했다. 여섯 크기 모두 가로 넘침이 없었다. 너비가 280, 320, 375픽셀일 때 타이머 카드의 위쪽은 뷰포트에서 16픽셀 떨어져 있었고, 캔버스 표시 너비는 각각 208, 248, 300픽셀이었다. 세로 스크롤도 가능했으며 데스크톱 레이아웃은 기존 배치를 유지했다.

실제 운영 페이지에서 다이얼 입력도 다시 확인했다. 두 언어 모두 280, 320, 375픽셀 화면에서 원형 다이얼을 눌렀을 때 375초가 선택됐고, 입력란에 6분 15초가 표시됐다.

<figure>
  <img src="pomodoro-en-mobile.png" alt="390픽셀 모바일 화면에서 실행한 영문 포모도로 타이머. 원형 타이머와 분·초 입력란, 조작 버튼, 타이머 이력이 보인다." width="390" height="844" loading="lazy" style="display:block;width:100%;max-width:390px;height:auto;margin:auto;">
  <figcaption>영문 운영 페이지에도 같은 레이아웃과 다이얼 좌표 계산을 적용했다.</figcaption>
</figure>

## 두 애플리케이션 배포 확인

영문 변경은 [영문 저장소 PR #2](https://github.com/saramjh/pomodorotimerEN/pull/2), 국문 변경은 [국문 저장소 PR #2](https://github.com/saramjh/pomodorotimerKR/pull/2)로 병합했다. [영문 병합 커밋](https://github.com/saramjh/pomodorotimerEN/commit/7716a286eac02b90f771ffbe7ba6f86b0efb6600)과 [국문 병합 커밋](https://github.com/saramjh/pomodorotimerKR/commit/f23f6b3033012e0f8b420ba0bbdcbed7d75bb5da)에 CSS, JavaScript, 회귀 테스트 변경이 포함돼 있다.

두 GitHub Pages 배포는 성공했다. 운영 중인 [영문 타이머](https://saramjh.github.io/pomodorotimerEN/)와 [국문 타이머](https://saramjh.github.io/pomodorotimerKR/) 모두 HTTP 200을 반환한다. 실제 제공되는 CSS와 JavaScript 파일도 테스트한 원본과 바이트 단위로 일치한다.

이번 브라우저 검증은 여섯 화면 크기와 테스트한 다이얼 입력 위치를 대상으로 한다. 사용자 증가나 모든 실제 휴대폰에서의 동작까지 측정한 결과는 아니다.

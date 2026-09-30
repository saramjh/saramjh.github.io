---
title: "인공지능 부자 관상 분석"
date: 2024-09-04
tags: 인공지능, face analysis, rich, analysis, forbes rich Korean
permalink: /rich-tester/
layout: default
legacy_asset_url: /posts/rich-tester/
description: "부자 관상 테스트의 초기 프로젝트 기록과 현재 포브스 2026 한국 부자 47인 비교 버전으로 바로 가는 안내 페이지입니다."
---

### 인공지능 부자 관상 분석

> 이 페이지는 2024년에 만든 초기 버전의 기록입니다. 현재 **부자 관상 테스트**는 포브스 2026 한국 부자 47인 표본과 6가지 얼굴 비율을 비교해 가장 가까운 Top 3와 두드러진 특징을 보여주는 버전으로 운영됩니다.

[현재 부자 관상 테스트 시작하기](https://saramjh.github.io/richChecker/)

[현재 버전 설명 보기](/rich-face-test/)

<img src="Screenshot%202024-09-05%20at%2011.48.24.JPG" alt="2024년 인공지능 부자 관상 분석 초기 버전 화면">

## 현재 부자 관상 테스트

현재 버전은 사진 한 장에서 얼굴 랜드마크를 찾고, 이마 높이, 눈 사이 거리, 코 길이, 입 너비, 하안부 길이, 얼굴 종횡비를 계산합니다. 이 6가지 비율을 포브스 2026 한국 부자 47인 표본과 비교해 전체 비율이 가까운 Top 3를 보여줍니다.

- 성별 선택 없이 하나의 통합 표본으로 비교
- 전체 6개 얼굴 비율 기준 Top 3 제공
- 가장 두드러진 얼굴 특징과 특징별 가까운 인물 표시
- 결과 카드 저장 및 기기 공유 지원
- 별도 가입 없음
- 얼굴 매칭용 사진은 서버에 업로드하지 않고 브라우저에서 처리

[사진 한 장으로 현재 부자 관상 테스트 해보기](https://saramjh.github.io/richChecker/)

## 2024년 초기 버전 기록

초기 버전은 대한민국 주요 부자와 경제인 표본을 대상으로 사용자의 얼굴 특징을 비교하는 실험적인 웹 애플리케이션이었습니다. 당시에는 성별을 먼저 선택하고 사진을 업로드한 뒤 단일 결과를 확인하는 흐름이었습니다.

### 초기 버전 주요 기능

- 사용자 사진 업로드
- 성별 선택 후 비교
- 얼굴 특징 유사도 계산
- 결과 이미지 저장

## 현재 구현

현재 서비스는 MediaPipe Face Landmarker를 사용해 얼굴 랜드마크를 분석하고, 브라우저에서 계산한 6개 얼굴 비율을 사전 계산된 표본과 비교합니다. 결과는 얼굴 비율의 엔터테인먼트용 비교이며 재산, 성격, 성공 가능성을 예측하지 않습니다.

얼굴 분석용 사진 자체는 매칭 목적으로 서버에 업로드하지 않습니다. 사이트 이용 통계와 광고에는 Google Analytics와 Google AdSense가 사용될 수 있습니다.

#### Links

- [현재 부자 관상 테스트](https://saramjh.github.io/richChecker/)
- [현재 버전 소개 글](/rich-face-test/)
- [Github Repository: richChecker](https://github.com/saramjh/richChecker)

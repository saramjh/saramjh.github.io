---
title: "메모를 남긴 달력을 URL로 공유하세요!"
description: 작성한 메모를 포함한 달력 상태를 URL로 공유할 수 있습니다.
date: 2024-09-12
tags: utility, sharing via URL, calendar, memo
permalink: /calendar-sharing-via-URL/
comments: true
---

# URL 공유 달력 - 메모 및 일정 관리

## 소개

<img src="{{site.assets}}{{ page.permalink }}366762842-9ead0fd1-97c8-47e4-9743-111ec526303a.png" alt="달력에 남긴 메모를 URL로 공유하는 페이지">
<img src="{{site.assets}}{{ page.permalink }}tutorial.gif" alt="달력에 남긴 메모를 URL로 공유하는 페이지 사용법">

이 프로젝트는 사용자가 일정을 관리하고 메모를 작성할 수 있는 달력 애플리케이션입니다. 사용자는 작성한 메모를 URL로 공유하고, 다른 사용자와 메모를 공유하거나, 자신이 작성한 메모를 언제든지 불러올 수 있습니다. 이 애플리케이션은 메모를 로컬 스토리지에 저장하고, 페이지 URL의 쿼리 파라미터를 통해 데이터를 공유하는 기능을 제공합니다.

## 기능

- **다국어 지원**: English, Español, 한국어, 日本語, 中文, Deutsch, Italiano, Français, Tiếng Việt, Bahasa Indonesia
- **달력 표시**: 현재 월의 달력을 표시하며, 날짜를 클릭하여 메모를 작성하거나 편집할 수 있습니다.
- **메모 관리**: 날짜별로 메모를 추가, 수정 및 삭제할 수 있습니다.
- **URL 공유**: 작성한 메모를 포함한 달력 상태를 URL로 공유할 수 있습니다.
- **메모 개수 표시**: 과거와 미래의 메모 개수를 화면에 표시합니다.

## 사용법

1. **달력 탐색**:

   - 좌측 화살표 버튼 (`prev-mon`)을 클릭하여 이전 달로 이동합니다.
   - 우측 화살표 버튼 (`next-mon`)을 클릭하여 다음 달로 이동합니다.

2. **메모 작성 및 수정**:

   - 달력에서 날짜를 클릭하여 해당 날짜의 메모를 작성하거나 수정할 수 있습니다.
   - 메모의 시간, 내용, 완료 여부를 입력하고 저장할 수 있습니다.

3. **메모 삭제**:

   - 메모를 삭제하려면 삭제 버튼 (`delete-memo`)을 클릭합니다.

4. **URL 공유**:
   - 공유 버튼 (`share-button`)을 클릭하여 현재 달력 상태와 메모를 포함한 URL을 클립보드에 복사합니다. 이 URL을 다른 사람과 공유하여 동일한 달력과 메모를 볼 수 있습니다.

## 코드 구조

- **HTML 파일**:

  - `index.html`: 애플리케이션의 기본 구조와 레이아웃을 정의합니다.

- **CSS 파일**:

  - `css/style.css`: 애플리케이션의 스타일을 정의합니다.

- **JavaScript 파일**:
  - `js/script.js`: 애플리케이션의 기능과 동작을 구현합니다.

## 주요 기능 설명

### 암호화 및 복호화

- **`encodeBase64(str)`**: 문자열을 Base64로 인코딩합니다.
- **`decodeBase64(str)`**: Base64로 인코딩된 문자열을 디코딩합니다.

### URL 파라미터 관리

- **`setQueryParam(param, value)`**: URL 파라미터를 설정합니다.
- **`getQueryParam(param)`**: URL 파라미터 값을 가져옵니다.

### 달력 렌더링

- **`renderCalendar()`**: 현재 월의 달력을 생성하고 표시합니다.
- **`selectDate(dateString)`**: 선택한 날짜의 메모를 표시합니다.

### 메모 관리

- **`saveMemo(dateString)`**: 메모를 저장합니다.
- **`deleteMemo(dateString)`**: 메모를 삭제합니다.

### 데이터 로딩 및 공유

- **`loadFromURL()`**: URL에서 데이터를 로드하여 달력을 렌더링합니다.
- **`shareURL()`**: 현재 달력 상태와 메모를 포함한 URL을 생성하고 클립보드에 복사합니다.

### 메모 개수 업데이트

- **`updateMemoCounts()`**: 과거와 미래의 메모 개수를 계산하고 표시합니다.
- **`updateCountsFromURL()`**: URL에서 메모 개수 값을 가져와서 화면에 표시합니다.

### 도움받은 소스

[aengzu.log](https://velog.io/@aengzu/2024-%EB%8F%99%EA%B8%B0%EA%B3%84%EC%A0%88-%EB%AA%A8%EA%B0%81%EC%BD%94-3%ED%9A%8C%EC%B0%A8-html-css-js-%EB%A1%9C-%EC%BA%98%EB%A6%B0%EB%8D%94-%EC%9B%B9%ED%8E%98%EC%9D%B4%EC%A7%80-%EC%A0%9C%EC%9E%91%ED%95%98%EA%B8%B0)

## 개발자

- **Author**: saramjh
- **Website**: [saramjh.github.io](https://saramjh.github.io)

#### Links

- [URL 공유 달력 - 메모 및 일정 관리](https://saramjh.github.io/URLschedule)
- [Github Repository: URL 공유 달력 - 메모 및 일정 관리](https://github.com/saramjh/URLschedule)

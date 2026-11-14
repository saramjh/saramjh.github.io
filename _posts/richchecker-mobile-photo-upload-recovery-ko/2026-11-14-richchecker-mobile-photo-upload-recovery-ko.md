---
title: "Richchecker KR: 안드로이드 사진 업로드가 멈추던 경로를 바꾸다"
description: "Android Chrome의 사진 읽기 오류를 분석하고 Richchecker KR의 FileReader 경로를 Blob URL로 바꾼 개발 사례. 테스트와 운영 확인 범위를 구분했다."
date: 2026-11-14
tags: ["Richchecker", "Frontend", "Android Chrome", "Debugging"]
permalink: /richchecker-mobile-photo-upload-recovery-ko/
layout: default
lang: ko
alternate_lang: en
alternate_url: /richchecker-mobile-photo-upload-recovery-en/
published: true
seo:
  title: "Richchecker KR 안드로이드 사진 업로드 오류 개선"
  description: "GA4의 file_read 오류 8건에서 시작한 Richchecker KR 사진 업로드 수정: Blob URL, 파일 사전검사, Chrome 회귀 테스트와 실제 배포 검증."
---

> English: [Fixing the photo upload path in Richchecker KR](/richchecker-mobile-photo-upload-recovery-en/)

**2026년 11월 13일, [Richchecker KR](https://saramjh.github.io/richChecker/)의 사진 업로드 경로를 수정해 배포했다.** Android Chrome에서 사진 선택 후 분석으로 넘어가지 못한 오류 기록을 확인하고, 파일 전체를 Base64로 복사하던 코드를 제거했다. 파일 형식 검사와 실패 단계별 진단도 추가했다. 구현과 테스트 기록은 [PR #1](https://github.com/saramjh/richChecker/pull/1)과 [PR #2](https://github.com/saramjh/richChecker/pull/2)에 남아 있다.

## 사진은 선택됐는데 분석이 시작되지 않았다

11월 12일 Richchecker KR 전용 GA4 기록을 기기와 오류 단계로 나눠 확인했다.

| 관측된 이벤트 | 횟수 | 측정 사용자 |
| --- | ---: | ---: |
| 사진 업로드 시작 | 14 | 5명 |
| 사진 업로드 오류 (file_read) | 8 | 3명 |
| 얼굴 분석 완료 | 6 | 3명 |

file_read 오류 8회는 모두 국내 모바일 **Android Chrome**에서 기록됐다. 이 브라우저 집계에는 시작 9회, 오류 8회, 완료 1회가 포함됐다. 하지만 집계된 이벤트를 개별 사용자의 시도와 일대일로 연결할 수 없다. **8/9를 실제 업로드 실패율이라고 계산할 수는 없다.** 확인한 집계 차원과 남은 불확실성은 [원본 조사 문서](https://github.com/saramjh/richChecker/blob/main/docs/ANDROID_UPLOAD_READ_FAILURE_20261113.md)에 있다.

## 파일 전체를 복사하지 않고 이미지 열기

기존 FileReader.readAsDataURL(file) 방식은 선택한 사진 전체를 Base64 문자열로 만든 뒤 이미지에 전달했다. 큰 사진에서는 원본 외에 추가 문자열이 메모리를 차지할 수 있다.

수정한 업로드는 다음 순서로 진행한다.

1. 빈 파일, 명백한 비이미지 파일, SVG 및 50MiB 초과 파일을 선택 단계에서 거부한다.
2. URL.createObjectURL(file)로 브라우저 내부 Blob URL을 만든 뒤 이미지 로드를 기다린다.
3. 디코딩한 이미지가 5천만 픽셀을 넘는지 검사하고, 적합하면 기존 MediaPipe 분석으로 넘긴다.
4. 사진 재선택·초기화·실패 시 URL.revokeObjectURL()로 더는 쓰지 않는 URL을 해제한다.

이미지 로딩은 20초를 초과하면 타임아웃으로 처리한다. HEIC를 현재 브라우저에서 디코딩할 수 없으면 JPG로 다시 저장하라고 안내한다. **선택한 얼굴 사진을 분석 서버로 업로드하지 않는 기존 구조**는 유지했다.

## 실패가 발생한 지점을 알 수 있도록

이제 업로드 실패를 사전검사(preflight), Blob URL 생성(object_url), 이미지 디코딩(decode) 단계로 구분한다. 제한된 이미지 형식 그룹과 파일 크기 구간도 함께 기록한다. 사진 원본 바이트, 파일명, Blob URL, 브라우저 오류 메시지는 분석 이벤트에 담지 않는다.

분석용 캔버스 스냅샷 생성이 실패했을 때 로딩 표시가 남을 수 있던 경로도 수정했다. 오류 처리를 try/finally의 정리 흐름 안에 두고 canvas_snapshot으로 구분한다.

다만 새 upload_format·upload_size_band를 GA4 맞춤 측정기준으로 등록하는 작업은 Analytics Admin 쓰기 권한 부족(HTTP 403)으로 거부됐다. 애플리케이션에서 이벤트 매개변수를 전송해도 **현재 일반 GA4 보고서에서는 이 두 구간을 조회할 수 없다.** 기존 error_type·stage 및 기기별 집계로 추적해야 한다.

## 검증한 것과 아직 모르는 것

Android 화면 크기와 사용자 에이전트를 모의한 **데스크톱 Chrome에서 20개 업로드·복구 시나리오가 통과**했다. 일반 이미지, HEIC 디코딩 실패, 손상 파일, 지나치게 큰 파일·픽셀 수, Blob URL 실패, 사진 재선택과 캔버스 실패를 검사했다. 별도 실행에서는 실제 MediaPipe 얼굴 감지부터 결과 화면까지 확인했다.

두 PR은 [GitHub Pages 배포 작업](https://github.com/saramjh/richChecker/actions/runs/43371215024)을 통과했다. 11월 14일에는 [운영 Richchecker KR](https://saramjh.github.io/richChecker/)이 제공하는 JavaScript가 원본 저장소 main의 js/script.js와 **바이트 단위로 일치**하는 것도 확인했다.

## 배포 후 확인: 디코딩 단계에서 오류가 계속됐다

11월 14일에 서비스 전용 GA4를 다시 조회했다. 11월 13일 **코드 배포가 끝난 이후**의 Android Chrome 이벤트에는 새로운 `image_decode` 오류가 남아 있었다.

| Android Chrome 이벤트 | 11월 12일 (수정 전) | 11월 13일 (배포 후) |
| --- | ---: | ---: |
| 업로드 시작 | 9 | 6 |
| 업로드 오류 | 8 (`file_read`) | 5 (`image_decode`, `decode` 단계) |
| 분석 완료 | 1 | 1 |

이는 같은 사용자 집단이나 개별 업로드 시도를 연결한 결과가 아니다. 따라서 **8/9와 5/6을 비교해 성공률이 개선됐다고 계산할 수 없다.** 새 오류가 더 구체적인 디코딩 단계로 기록된 점은 확인했지만, 오류를 일으킨 사진 형식이나 단말 환경은 특정하지 못했다. 현재 GA4에서 파일 형식 구간을 조회할 권한도 확보하지 못했다.

**Android 실기기에서 문제가 해결됐는지는 여전히 확인되지 않았다.** 배포된 코드는 파일 읽기 경로와 오류 진단을 개선했지만 디코딩 오류가 계속 관측된다. 다음 단계는 권한이 있는 운영 기록과 실제 기기 재현을 통해 원인을 좁히는 것이다.

원본: [Richchecker KR 소스와 테스트](https://github.com/saramjh/richChecker) · [같은 호스트의 서비스별 분석 범위 구분](/gh-pages-analytics-notes-5-followup-kr/)

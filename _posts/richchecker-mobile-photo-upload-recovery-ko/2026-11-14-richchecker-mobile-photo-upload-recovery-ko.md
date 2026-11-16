---
title: "Richchecker KR·US: Android 사진 업로드 복구"
description: "Android Chrome의 사진 읽기·디코딩 오류를 계기로 Richchecker KR·US에 HEIC·TIFF 브라우저 내부 복구와 취소 처리를 배포한 개발 기록. 테스트 범위와 실기기 검증 한계를 함께 설명한다."
date: 2026-11-14
modified: 2026-11-17
last_modified_at: 2026-11-17
tags: ["Richchecker", "Frontend", "Android Chrome", "HEIC", "TIFF", "Debugging"]
permalink: /richchecker-mobile-photo-upload-recovery-ko/
layout: default
lang: ko
alternate_lang: en
alternate_url: /richchecker-mobile-photo-upload-recovery-en/
published: true
seo:
  title: "Richchecker KR·US Android 사진 업로드 복구"
  description: "Android Chrome의 file_read·image_decode 오류를 계기로 KR·US 양쪽에 HEIC·TIFF 브라우저 내부 복구와 취소 처리를 배포했다. 회귀 테스트와 실기기 검증 한계를 기록한다."
---

> English: [Android photo upload recovery in both Richchecker editions](/richchecker-mobile-photo-upload-recovery-en/)

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

이미지 로딩은 20초를 초과하면 타임아웃으로 처리한다. 기본 디코더가 HEIC를 열지 못하면 지원 가능한 HEIC/HEIF의 브라우저 내부 변환을 시도한다. 변환이 실패하거나 제한을 넘는 파일은 JPG 또는 PNG로 저장해 다시 선택하도록 안내한다. **선택한 얼굴 사진을 분석 서버로 업로드하지 않는 구조**는 유지했다.

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

## 11월 14일 추가 배포: 파일 형식에 맞는 실패 안내

최초 수정 뒤에도 디코딩 오류가 남아, [11월 14일 변경](https://github.com/saramjh/richChecker/commit/eede7730408b6aa2ec6afc9b2e4e5d6ab1531609)에서 안내 문구를 보완했다. Android의 사진 제공자가 파일명과 MIME 유형을 JPEG로 전달하더라도 실제 파일은 HEIC·TIFF일 수 있다. 이것은 **가능한 원인**이지, 앞서 관측한 오류의 원인으로 확정된 사실은 아니다.

정상적으로 열리는 사진은 그대로 처리한다. `image_decode` 오류가 발생했을 때만 브라우저 안에서 `File.slice(0, 16).arrayBuffer()`로 처음 **16바이트**를 확인한다. HEIC·TIFF 서명이 보이면 JPG 또는 PNG로 다시 저장해 선택하라고 안내하고, 헤더를 읽지 못하거나 **250ms** 안에 응답이 없으면 기존 일반 안내를 사용한다. 전체 사진을 두 번 읽거나 서버에 전송하지 않으며, GA4에는 파일 바이트나 새 개인정보 항목을 추가하지 않았다.

원본 변경에는 **브라우저 테스트 24개와 계약 검사 5개 통과**가 기록돼 있고, [GitHub Actions 배포](https://github.com/saramjh/richChecker/actions/runs/43578267276)도 성공했다. 운영 JavaScript가 현재 원본 저장소 `main`과 바이트 단위로 일치하는 것까지 확인했다. 하지만 **실제 안드로이드 기기에서 해결됐다는 증거는 아직 없습니다.** 안내의 정확성을 높인 변경이지, 사용자의 업로드 성공이나 분석 완료가 늘었다는 결과는 아니다.

## 2026-11-15: 배포 후 실제 분석 완료 신호

11월 14일 17:58(KST) [이미지 디코딩 안내 개선 코드](https://github.com/saramjh/richChecker/commit/eede7730408b6aa2ec6afc9b2e4e5d6ab1531609)가 운영에 배포됐다. 다음 날 Richchecker KR **제품 전용** GA4 속성을 다시 조회했다. 운영 코드의 측정 ID와 제품 스트림이 일치하는 것을 먼저 확인했으며, 속성의 시간대는 서울이다.

배포 이후 11월 14일 **19시 3건**, **20시 1건**의 `analysis_complete` 이벤트가 GA4에서 Android Chrome 모바일로 분류됐다. 같은 날 20시에는 Windows Chrome 1건도 기록됐다. 이 날짜의 해당 이벤트 유입 출처는 `google / organic`이었다. 비교를 위해 배포 이전 14시에도 Android Chrome 완료 이벤트 1건이 있었다는 사실을 남긴다.

원본 분석 코드에서는 `renderResults` 호출 뒤에 `analysis_complete`를 전송한다. 따라서 적어도 결과 생성 단계까지 진행됐다는 **제품 계측 신호**가 확인됐다. 다만 **완료 이벤트 4건은 사용자 4명을 뜻하지 않습니다.** GA4의 운영체제 분류만으로 실제 물리 기기를 확인할 수 없고, 동일 사용자 반복 실행이나 자체 테스트 여부도 구별할 수 없다. **기존 오류가 해결됐다는 증거는 아닙니다.** 특히 문제를 일으켰던 사진 제공자·파일 형식과 새 완료 이벤트를 연결할 데이터가 없어 수정 전후 성공률이나 인과관계를 계산하지 않는다.

## 2026-11-16: KR·US 에디션에 로컬 사진 복구 추가

11월 15일 KR 제품 전용 GA4의 Android Chrome 모바일 06시 집계에는 측정 사용자 1명, upload_started 15건, image_decode 13건, analysis_complete 2건이 기록됐다. US판에서는 11월 4일 19시(로스앤젤레스 속성 시간)에 측정 사용자 1명의 Android Chrome에서 file_read 오류 2건이 발생했다. GA4 기록만으로는 원본 사진과 파일 제공자를 식별할 수 없었다. 이벤트 수를 파일 수나 업로드 실패율로 해석할 수는 없다.

[KR PR #4](https://github.com/saramjh/richChecker/pull/4)는 정상 Blob URL 디코딩을 유지하고, 이미지 로드가 실패한 경우에만 createImageBitmap(file, { imageOrientation: "from-image" })를 한 번 시도한다. 입력 파일은 20 MiB 이하, 디코딩은 7초 이내, 픽셀 수는 5천만 이하로 제한한다. 복구 이미지는 긴 변 2,200px 이하의 JPEG로 만들며 인코딩 제한은 5초다. 결과 이미지는 기존 MediaPipe 분석과 미리보기·공유 흐름에 연결한다. 늦게 끝난 bitmap은 닫고 사용이 끝난 Blob URL도 해제한다. 사진을 서버로 전송하지 않으며 native 복구 경로에는 새 의존성을 추가하지 않았다. [US PR #1](https://github.com/saramjh/richChecker-us/pull/1)은 전체 사진을 Base64로 읽던 FileReader 경로를 제거하고 브라우저 내부 Blob URL과 실패 시 native ImageBitmap 복구를 적용했다.

별도로 확인한 640×640 ISO HEIC 파일은 Chrome의 기본 이미지 로더와 native ImageBitmap에서 모두 열리지 않았다. [KR PR #5](https://github.com/saramjh/richChecker/pull/5)와 [US PR #2](https://github.com/saramjh/richChecker-us/pull/2)는 이 경우에만 셀프 호스팅한 MIT 라이선스 heic2any@0.0.4를 늦게 불러와 HEIC/HEIF를 브라우저 안에서 JPEG로 변환한다. 디코딩 실패 뒤 파일 헤더는 최대 16바이트만 확인한다. 원본 HEIC는 12 MiB 이하, 변환 대기는 10초, 출력 JPEG는 20 MiB 이하이며 기존 50MP(5천만 픽셀) 제한도 적용한다. JPEG·PNG·WebP의 정상 경로에서는 변환 라이브러리를 불러오지 않는다. 사진 바이트는 네트워크로 전송하지 않는다.

네 PR은 모두 main에 병합됐다. 각 PR에 기록된 브라우저 회귀 테스트는 KR native 복구 28/28, US native 복구 29/29, KR HEIC 복구 29/29, US HEIC 복구 30/30이다. 네 변경 모두 실제 MediaPipe 분석 E2E와 결과 렌더링을 확인했고, 기존 계약 검사도 통과했다. [KR native 배포](https://github.com/saramjh/richChecker/actions/runs/43821895201), [US native 배포](https://github.com/saramjh/richChecker-us/actions/runs/43824121306), [KR HEIC 배포](https://github.com/saramjh/richChecker/actions/runs/43842302246), [US HEIC 배포](https://github.com/saramjh/richChecker-us/actions/runs/43842311161)는 모두 성공했다. 운영 중인 [KR판](https://saramjh.github.io/richChecker/)과 [US판](https://saramjh.github.io/richChecker-us/), 양쪽 JavaScript 및 HEIC 변환 파일도 HTTP 200으로 확인했다.

640×640 HEIC 테스트 파일은 별도의 재현 가능한 HEIC 실패 경로를 확인한 것이다. 이것이 앞서 관측한 KR 13건이나 US 2건의 원인이라는 증거는 없다. 실제 문제가 발생한 Android 기기에서 재현하지 못했고, 사진 갤러리·클라우드 제공자와 원본 파일도 아직 확인하지 못했다. 따라서 해당 기기에서 수정이 확인됐다고 말할 수 없으며 운영 P0를 닫지 않는다.


## 2026-11-16: TIFF 복구와 이전 작업 취소

11월 16일 [KR PR #6](https://github.com/saramjh/richChecker/pull/6)과 [US PR #3](https://github.com/saramjh/richChecker-us/pull/3)을 main에 병합했다. 사진을 다시 선택하거나 도구를 초기화하면 이전 사진 제공자 읽기 요청, 이미지 디코딩, MediaPipe 모듈·모델 로딩 대기를 취소한다. 마지막에 선택한 사진만 미리보기와 분석을 이어간다.

TIFF는 취소할 수 있는 Web Worker에서 브라우저 내부로 변환한다. 변환 전 IFD 메타데이터와 타일·스트립 개수를 확인한다. 디코딩 제한은 8MP/32MiB이며 원본 파일은 12MiB 이하로 제한한다. Deflate 압축 해제 결과에도 출력 크기 제한을 적용한다. HEIC와 TIFF 복구 과정에서 사진 바이트를 서버로 보내지 않는다.

각 저장소의 회귀 테스트에서 이미지 형식·실패·적대적 입력 38/38, 취소·재선택·초기화·모델 대기 9/9가 통과했다. 실제 JPEG, HEIC, TIFF를 사용한 MediaPipe E2E와 얼굴이 없는 이미지의 제어된 오류 처리 및 로딩 정리도 확인했고, 페이지 오류는 0건이었다. 테스트 환경은 macOS Chrome에 Android 14/Pixel 8 사용자 에이전트와 모바일 뷰포트를 적용한 것이며, 실제 Android 기기 테스트는 아니다.

[KR 배포 작업](https://github.com/saramjh/richChecker/actions/runs/43888945586)은 2026-11-16 14:45:15 UTC, [US 배포 작업](https://github.com/saramjh/richChecker-us/actions/runs/43888946580)은 14:45:18 UTC에 성공했다. 운영 KR·US 페이지와 각 `js/script.js`, `tiff-worker.js`, `utif.js`, `pako_inflate.min.js`는 모두 HTTP 200을 반환했다. 두 제품의 JavaScript에서 TIFF 복구 함수와 취소 상태 코드를 확인했다.

최종 배포 이후의 짧은 GA4 구간도 다시 조회했다. KR은 11월 16일 23:45 KST부터 11월 17일 01:25 KST까지, US는 11월 16일 06:45부터 08:25까지(로스앤젤레스 속성 시간) Android 모바일의 `upload_started`, `upload_error`, `analysis_started`, `analysis_complete`, `upload_decode_recovered`, `photo_picker_opened` 이벤트를 조회했다. 두 속성 모두 일치하는 행이 없었다. 이전 조회의 19:57 KST와 02:59 PST 이벤트는 이 두 배포보다 먼저 발생했으므로 새 코드의 결과로 계산하지 않았다. 짧은 조회 구간에서 행이 없었다는 사실만으로 사용자 활동이나 오류가 없었다고 판단할 수 없다.

실제 영향을 받은 Android 기기와 사진 제공자, 원본 사진은 여전히 확인하지 못했다. 테스트는 TIFF 처리와 취소 경로가 구현됐다는 점을 확인했으며, 해당 기기에서 업로드가 복구됐다는 증거는 없다. 운영 P0는 계속 열린 상태다.

원본: [Richchecker KR 소스와 테스트](https://github.com/saramjh/richChecker) · [Richchecker US 소스](https://github.com/saramjh/richChecker-us) · [같은 호스트의 서비스별 분석 범위 구분](/gh-pages-analytics-notes-5-followup-kr/) · [KR PR #6](https://github.com/saramjh/richChecker/pull/6) · [US PR #3](https://github.com/saramjh/richChecker-us/pull/3) · [KR 배포](https://github.com/saramjh/richChecker/actions/runs/43888945586) · [US 배포](https://github.com/saramjh/richChecker-us/actions/runs/43888946580)

---
title: "Space Atlas가 NCASE 교육자료 목록에 실렸다: 달 위상 수업 자료로 이어진 개발"
description: "NCASE 교육자료 목록에 실린 Space Atlas와 Share My Lesson의 작성자 게시 달 위상 활동지. 직접 만든 시뮬레이터를 교육용 자료로 연결한 과정과 교사 검토 사항."
date: 2026-11-16
permalink: /space-atlas-educator-discovery-ko/
layout: default
lang: ko
alternate_lang: en
alternate_url: /space-atlas-educator-discovery-en/
tags: ["Space Atlas", "NCASE", "Share My Lesson", "과학교육", "달의 위상", "인터랙티브 시뮬레이션"]
image: /assets/img/dev-ncase-spaceatlas-educator-20261116/space-atlas-ncase-ko.png
image_width: 1200
image_height: 630
published: true
seo:
  title: "Space Atlas의 NCASE 수록과 Share My Lesson 달 위상 활동지"
  description: "미국 NCASE의 공개 교육자료 목록과 Share My Lesson의 작성자 게시 활동지로 이어진 Space Atlas 개발 사례. 실제 출처와 검토 지점."
---

> English edition: [Space Atlas on NCASE and a Moon Phases lesson for educators](/space-atlas-educator-discovery-en/)

**Space Atlas가 미국 NCASE의 우주·항공 교육자료 목록에 실렸다.** [NCASE Programs](https://ncase.org/programs/)의 일반 교육자료 영역에 독립 개발 프로젝트로 소개되어 있다. 별도로, 제가 만든 달 위상 시뮬레이터에 맞춘 활동지를 2026년 10월 19일 [Share My Lesson](https://sharemylesson.com/teaching-resource/moon-phases-predict-test-explain-interactive-grades-4-8-lesson-412086)에 공개했다.

두 기록은 성격이 다르다. NCASE는 **외부 목록에 실제 수록된 사례**이고, Share My Lesson 자료는 **개발자가 직접 작성해 게시한 수업 자료**다. 둘 다 조회 가능한 출처가 있지만, 이를 학교의 사용 승인이나 수업 효과 검증으로 확대할 근거는 없다.

<figure>
  <a href="/space-atlas-student/space-atlas-moon-phases.png"><img src="/space-atlas-student/space-atlas-moon-phases.png" width="1280" height="820" loading="lazy" style="width:100%;height:auto" alt="Space Atlas 달 위상 시뮬레이터의 기존 자체 스크린샷. 왼쪽에는 지구와 달의 공전 위치를 보는 시스템 뷰, 오른쪽에는 지구에서 보이는 밝은 달 표면의 관측 뷰가 있다."></a>
  <figcaption>직접 개발한 달 위상 시뮬레이터의 기존 화면. 2026년 9월 게시한 [원래 프로젝트 소개 글](/space-atlas-student/)에 포함된 자체 이미지이며, 현재 UI를 새로 캡처한 화면은 아니다.</figcaption>
</figure>

## 무엇을 만들었고, 왜 교육자료가 되었나

웹에서 [달 위상 모델](https://spaceatlasedu.org/moon/phases/)을 열면 지구·달·태양의 상대 위치와 지구에서 보이는 달의 밝은 부분을 함께 살펴볼 수 있다. 실제 관측과 동떨어진 정지 그림을 외우게 하기보다, **달의 위치를 바꾸면 왜 위상이 달라 보이는지**를 두 시점으로 비교할 수 있게 설계했다.

기술적으로는 조작하는 궤도상의 위치와 지구 관측자의 화면을 연결하는 일이 중요했다. 모델의 거리와 천체 크기는 개념 설명을 위해 단순화했다. 실제 천문력이나 일식·월식 예측 도구로 사용하도록 만든 것은 아니다.

NCASE의 공개 목록은 이 시뮬레이터를 달 위상, 지구 자전축에 따른 계절, 천문학적 축척을 다루는 무료 학습 모델로 소개한다. 이 항목이 중요한 이유는 수업 준비를 하는 사람이 제가 운영하는 웹사이트가 아닌 **외부 교육자료 목록**을 통해 도구를 찾을 경로가 생겼기 때문이다. 실제 클릭 수나 학교 채택 수는 여기서 확인되지 않는다.

## 시뮬레이터를 20–25분 활동지로 바꾼 방식

[Share My Lesson에 게시한 활동지](https://sharemylesson.com/teaching-resource/moon-phases-predict-test-explain-interactive-grades-4-8-lesson-412086)는 *Moon Phases: Predict, Test, Explain*이라는 제목의 **4–8학년용 2쪽짜리 워크시트**다. 교사가 검토할 수 있도록 활동의 흐름을 구체적으로 적었다.

1. **먼저 예상하기.** 삭·상현·보름·하현에서 달의 밝은 부분이 얼마나 보일지 그림으로 예상한다.
2. **모델로 비교하기.** 시뮬레이터에서 네 위치를 차례로 선택하고, 태양–지구–달 전체 위치와 지구 관측 뷰를 비교한다.
3. **이유 설명하기.** 매달 반복되는 달의 위상이 일상적인 지구 그림자 때문이 아닌 이유를 자신의 문장으로 정리한다.

게시된 활동지에는 교사 안내와 정답 참고, 관측 기하학의 단순화 설명이 포함되어 있다. **20–25분은 작성자가 제안한 수업 시간**으로, 실제 수업에서 측정한 평균이 아니다. 자료는 공개적으로 소개되어 있지만 PDF 다운로드에는 Share My Lesson 로그인이 필요할 수 있다.

이 작업에서 구현 능력을 보여주는 부분은 모델 자체보다도, 학생의 예상과 조작·설명이 연결되도록 **인터랙션을 학습 과제로 번역한 설계**다. 소프트웨어 기능을 교육자료 형식으로 제공할 수 있다는 실물 사례가 됐다.

## 수업 사용 전에 확인할 것

교사는 먼저 [NCASE의 원본 소개](https://ncase.org/programs/), [Share My Lesson의 원본 활동지 페이지](https://sharemylesson.com/teaching-resource/moon-phases-predict-test-explain-interactive-grades-4-8-lesson-412086), [모델 화면](https://spaceatlasedu.org/moon/phases/)을 직접 검토할 수 있다. Share My Lesson에는 활동지에 **CC BY-NC-ND** 조건이 표시된다. 이 표기는 해당 PDF에 관한 것이며 Space Atlas 소프트웨어 전체에 적용되는 라이선스가 아니다.

어린 학생을 대상으로 할 때는 별도의 확인이 필요하다. 자료 소개에는 사이트의 분석·광고 기술 사용 사실이 기재되어 있으며, 학교의 개인정보·접근성·기기 정책에 부합하는지는 교사가 별도로 검토해야 한다. **어린이 대상 개인정보 적합성이 인증되었다고 주장하지 않는다.**

확인된 성과는 외부 목록의 게시와 작성자 수업자료의 공개다. 실제 학급 사용, 학습 효과, 제휴·추천 또는 방문자 증가를 나타내는 영수증은 없다. [기존 Space Atlas 프로젝트 글](/space-atlas-student/)과 [개발 포트폴리오](/portfolio/)에서 구현 배경을 더 볼 수 있다.

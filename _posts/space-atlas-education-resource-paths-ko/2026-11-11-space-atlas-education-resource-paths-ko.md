---
title: "Space Atlas 수업 자료가 NCASE 목록과 Share My Lesson에 공개됐다"
description: "Space Atlas의 달 위상 시뮬레이터를 교사용 활동으로 확장했다. NCASE 교육 자료 목록 등재와 Share My Lesson에 직접 게시한 4~8학년 활동지를 원문으로 확인한다."
date: 2026-11-11
tags: ["Space Atlas", "달 위상", "과학교육", "NCASE", "Share My Lesson", "수업 자료", "개발 기록"]
permalink: /space-atlas-education-resource-paths-ko/
layout: default
lang: ko
alternate_lang: en
alternate_url: /space-atlas-education-resource-paths-en/
image: /space-atlas-student/space-atlas-hero.png
image_width: 1280
image_height: 820
published: true
seo:
  title: "Space Atlas의 NCASE 목록 등재와 Share My Lesson 달 위상 수업 자료"
  description: "Space Atlas NCASE 교육 자료 등재와 Share My Lesson 달 위상 활동지의 작성자, 실제 개발 작업, 이용 범위 및 라이선스를 정리한 개발자 기록."
---

> English version: [Where Space Atlas reached educators: NCASE and Share My Lesson](/space-atlas-education-resource-paths-en/)

[미국 NCASE의 공개 교육 자료 목록](https://ncase.org/programs/)에 Space Atlas가 독립 개발자 **Jihun Oh**의 무료 천문학 학습 도구로 올라와 있다. 별도로 [Share My Lesson](https://sharemylesson.com/teaching-resource/moon-phases-predict-test-explain-interactive-grades-4-8-lesson-412086)에서는 내가 만든 달 위상 시뮬레이터를 사용하는 **4~8학년 대상 수업 활동지**를 확인할 수 있다. 하나는 교육 자료 목록의 링크이고, 다른 하나는 제작자가 직접 기여한 수업 자료다.

## 수업용 자료로 바꾸기 위해 구현한 것

[Space Atlas 달 위상 시뮬레이터](https://spaceatlasedu.org/moon/phases/)에서는 달이 지구를 도는 위치를 바꿔가며 태양이 비추는 면과 지구에서 밝게 보이는 면을 함께 살필 수 있다. 달이 삭, 상현, 보름, 하현에 있을 때 학생이 무엇을 관찰하는지가 이 모델의 중심이다.

Share My Lesson에 공개한 *Moon Phases: Predict, Test, Explain*은 이 기능을 **예측 → 네 위치에서 실험 → 관찰한 내용을 설명**하는 20~25분짜리 활동으로 묶었다. 공개 자료 페이지에 따르면 학생용 표와 질문, 교사용 진행 순서와 해설이 담긴 두 쪽의 PDF이며, 자료 작성자는 Jihun Oh로 명시돼 있다. 다운로드 파일 옆의 날짜는 **2026년 10월 19일**이다. 이것을 교실에서 실제로 사용했다는 근거로 해석하지는 않는다.

<figure>
  <img src="/space-atlas-student/space-atlas-hero.png" width="1280" height="820" loading="lazy" alt="Space Atlas의 기존 달 위상과 천문학 학습 모델을 보여 주는 자체 제작 화면 이미지" style="width:100%;height:auto;">
  <figcaption>이전에 개인 개발 블로그에 공개한 Space Atlas 화면. NCASE와 Share My Lesson의 사진이나 PDF 미리보기를 가져온 것이 아니다.</figcaption>
</figure>

## NCASE에서 찾을 수 있는 범위

NCASE의 Programs 페이지는 Space Atlas의 달 위상, 지구의 계절, 천문학적 규모 모델을 소개하면서 현재 [spaceatlasedu.org](https://spaceatlasedu.org/)로 연결한다. 2026년 11월 11일 공개 항목을 확인했지만, 처음 등재된 날짜는 알 수 없다. 이 링크를 통해 영어권 교육자가 실제 시뮬레이터와 설명을 직접 검토할 수 있게 됐다.

개발자로서 두 경로가 보여 주는 일은 다르다. 교육 목록에 등록될 정도로 **도구가 공개돼 있고 설명과 접근 경로가 마련됐다는 사실**이 NCASE에서 확인된다. Share My Lesson에서는 그 도구를 바탕으로 **수업 질문, 진행 단계, 학습자의 관찰 기록**을 하나의 활동으로 조직한 결과를 확인할 수 있다.

## 공개 근거와 이용 시 주의점

- [NCASE Programs 원문](https://ncase.org/programs/) — Space Atlas 항목과 현재 서비스 링크
- [Share My Lesson 활동지 원문](https://sharemylesson.com/teaching-resource/moon-phases-predict-test-explain-interactive-grades-4-8-lesson-412086) — 작성자, 자료 유형, 이용 조건 및 PDF 파일 표시
- [Space Atlas 달 위상 시뮬레이터](https://spaceatlasedu.org/moon/phases/) — 실제로 조작할 수 있는 모델
- [기존 천문학 모델 개발 기록](/space-atlas-student/) — 구현 배경

Share My Lesson에 표시된 **CC BY-NC-ND** 조건은 해당 활동지 PDF에 적용된다. 나는 PDF와 플랫폼의 미리보기 이미지를 이 블로그로 옮기지 않았다. 시뮬레이터는 천체 크기와 거리를 교육 목적으로 단순화하며, 서비스에는 GA4와 Google AdSense가 사용된다. 학교에서 쓰려는 교사는 학습자 개인정보·접근성·기기 조건을 별도로 검토해야 한다.

이번에 검증된 것은 **공개 목록 등재와 제작자 명의의 활동지 게시**다. 교육기관 인증이나 실제 수업 효과의 증거는 아니다. 구현 과정의 다른 사례는 [Space Atlas 개발 포트폴리오](/portfolio/space-atlas/)에 정리돼 있다.

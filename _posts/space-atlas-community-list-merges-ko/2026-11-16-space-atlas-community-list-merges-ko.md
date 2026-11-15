---
title: "Space Atlas의 오픈소스 교육 자료 목록 기여 6건이 병합되기까지"
description: "직접 개발한 Space Atlas 천문학 모델을 여섯 개 해외 오픈소스 교육·과학 자료 목록에 제안했고, 각 저장소 관리자가 PR을 병합했다. 원본 기록과 실제 개발 작업을 확인한다."
date: 2026-11-16
tags: ["Space Atlas", "오픈소스", "과학교육", "천문학", "GitHub", "개발 기록"]
permalink: /space-atlas-community-list-merges-ko/
layout: default
lang: ko
alternate_lang: en
alternate_url: /space-atlas-community-list-merges-en/
image: /space-atlas-student/space-atlas-hero.png
image_width: 1280
image_height: 820
published: true
seo:
  title: "Space Atlas의 해외 오픈소스 교육 목록 6건 병합 기록"
  description: "Space Atlas를 소개하는 여섯 개 외부 오픈소스 자료 목록 PR이 독립 유지관리자에 의해 병합됐다. 정확한 PR과 원본 천문학 모델을 살펴본다."
---

> English edition: [Six open-source learning lists merged my Space Atlas contributions](/space-atlas-community-list-merges-en/)

**2026년 10월 16일부터 11월 6일까지, 내가 제출한 Space Atlas 소개 변경이 해외 오픈소스 교육·과학 자료 목록 여섯 곳에 병합됐다.** 각 저장소의 관리자가 변경 사항을 받아들인 기록은 GitHub에 남아 있다. 하나의 목록에서 주소만 수정한 후속 PR은 별도 등재로 세지 않았다.

Space Atlas는 달 위상, 지구의 계절, 천체의 크기와 거리처럼 그림만으로 이해하기 어려운 개념을 **직접 조작하는 브라우저 모델**로 만든 프로젝트다. 이번 기여의 핵심은 새 시뮬레이터 출시가 아니라, 이미 동작하는 모델을 학습 자료를 찾는 사람들이 발견할 수 있도록 정확히 설명하고 연결한 일이다.

<figure>
  <img src="/space-atlas-student/space-atlas-hero.png" width="1280" height="820" loading="lazy" alt="개발자가 직접 제작한 Space Atlas 천문학 학습 모델 화면" style="display:block;width:100%;height:auto;">
  <figcaption>기존 개발 기록에 공개한 자체 제작 화면. 외부 목록의 이미지나 로고를 가져오지 않았다.</figcaption>
</figure>

## 서로 다른 여섯 개 자료 목록에 병합된 변경

아래 날짜는 원본 PR의 **UTC 병합일**이다. 각 링크에서 내가 제출한 설명과 관리자의 병합 기록을 직접 확인할 수 있다.

- **10월 16일 — [Awesome Study Resources PR #404](https://github.com/StudentSuite/awesome-study-resources/pull/404):** 무료로 접근하는 인터랙티브 학습 자료.
- **10월 16일 — [Awesome Interactive Learning PR #2](https://github.com/hamid-moghadam/awesome-interactive-learning/pull/2):** 달 위상과 계절을 실험하는 모델.
- **10월 20일 — [Awesome MINT Kids Resources PR #2](https://github.com/augustunbear/awesome-MINT-Kids-Resources/pull/2):** 보호자·교사가 함께 살펴볼 과학 활동 자료.
- **10월 27일 — [Kids Edutainment Links PR #11](https://github.com/vorburger/kids-edutainment-links/pull/11):** 가정에서 사용해 볼 천문학 학습 링크.
- **11월 5일 — [Awesome Physics PR #19](https://github.com/wbierbower/awesome-physics/pull/19):** 천체물리학 자료 목록의 오픈소스 모델.
- **11월 6일 — [Awesome Homeschooling PR #9](https://github.com/muriloime/awesome-homeschooling/pull/9):** 가정 과학교육용 브라우저 기반 실험.

여섯 PR은 모두 내가 제안했고 **각 프로젝트에서 나와 다른 관리자가 병합**했다. 현재 각 저장소 기본 브랜치의 README에서도 Space Atlas 항목을 확인할 수 있다. [Awesome MINT Kids Resources PR #5](https://github.com/augustunbear/awesome-MINT-Kids-Resources/pull/5)는 동일한 목록의 서비스 주소를 수정한 후속 작업이므로 일곱 번째 등재로 계산하지 않는다.

## 목록 뒤에 있는 실제 개발 작업

[달 위상 모델](https://spaceatlasedu.org/moon/phases/)에서는 달의 위치를 바꿔 태양이 비추는 면과 지구에서 보이는 밝은 면을 비교한다. [지구의 계절 모델](https://spaceatlasedu.org/earth/seasons/)에서는 지축 기울기를 바꾸며 계절이 단순히 태양과의 거리 차이로 생기는 것이 아님을 탐구한다. 그림을 보는 데 그치지 않고 질문과 관찰을 이어 갈 수 있도록 조작 가능한 도구로 구현했다.

자료 목록에 기여할 때는 **실제로 작동하는 교육용 웹사이트**와 **소스 코드 저장소**를 구분하고, 각 목록의 목적에 맞춰 모델의 기능을 설명해야 했다. 외부 관리자가 받아들인 것은 이 프로젝트를 소개하는 **목록 변경 사항**이다. 학교 도입이나 학습 효과를 검증받았다는 뜻은 아니다. 수업에서 사용하려는 경우에는 현재 서비스의 개인정보·광고 안내와 기기 조건을 별도로 확인해야 한다.

구현 배경은 [Space Atlas 개발 기록](/space-atlas-student/)에서, 시뮬레이터를 실제 수업 질문으로 연결한 과정은 [NCASE와 Share My Lesson 사례](/space-atlas-education-resource-paths-ko/)에서 볼 수 있다.

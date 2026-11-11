---
title: "EUSci에 우주 과학 도해 기고문이 실렸다"
description: "EUSci가 2026년 11월 10일 게재한 우주 과학 도해 기고문과, Space Atlas 개발에서 다뤘던 관찰 시점과 모델의 한계를 연결해 기록했다."
date: 2026-11-11
tags: ["Space Atlas", "EUSci", "천문학", "과학 커뮤니케이션", "개발자 기고", "교육용 시뮬레이션"]
permalink: /space-atlas-eusci-diagrams-ko/
layout: default
lang: ko
alternate_lang: en
alternate_url: /space-atlas-eusci-diagrams-en/
image: /space-atlas-student/space-atlas-hero.png
image_width: 1280
image_height: 820
published: true
seo:
  title: "EUSci 우주 과학 도해 기고 | Space Atlas 개발 기록"
  description: "EUSci에 게재된 Jihun Oh의 2026년 11월 10일 기고를 소개한다. 달 위상, 계절, 일식 도해의 설명 한계를 Space Atlas 개발 경험과 연결한다."
---

> English version: [My astronomy diagram essay was published by EUSci](/space-atlas-eusci-diagrams-en/)

2026년 11월 10일, [EUSci(University of Edinburgh Science Media)가 내 기고문 *Three Space Diagrams, Three Missing Clues*를 공개했다](https://eusci.org.uk/2026/11/10/three-space-diagrams-three-missing-clues/). 원문에 작성자는 **Jihun Oh**로 표시돼 있으며, EUSci의 온라인 뉴스 편집자인 Priscilla Wong이 편집했다고 명시돼 있다. [Space Atlas](https://spaceatlasedu.org/)를 개발하며 고민했던 천문학 도해의 설명 방식을 외부 과학 매체에서 다룬 작업이다.

글의 출발점은 간단했다. 교과서나 웹 화면의 도해가 정확한 형태를 갖췄더라도, 무엇을 생략했는지 독자가 알지 못하면 잘못된 결론을 내릴 수 있다. 3D 시뮬레이터를 만드는 입장에서는 시점과 좌표계, 고정된 방향을 화면에서 어떻게 보여주는지가 실제 기능 설계의 문제다.

<figure>
  <img src="/space-atlas-student/space-atlas-hero.png" alt="개발자가 이전에 공개한 Space Atlas의 3D 태양계 학습 화면. EUSci 기사에 실린 도해를 복제한 이미지는 아니다." width="1280" height="820" loading="lazy" style="width:100%;height:auto;">
  <figcaption>기존 Space Atlas 소개에 사용한 자체 학습 화면. EUSci 기사에 실린 이미지와는 별도로, 내가 제작해 공개해 둔 화면이다.</figcaption>
</figure>

## 도해의 빈칸을 실제 인터랙션으로 다루다

[달 위상 모델](https://spaceatlasedu.org/moon/phases/)에서는 태양빛을 받는 달의 절반과 지구에서 보이는 밝은 부분을 구분해야 한다. 관찰자의 위치를 빼면 '상현달의 절반이 밝게 보이는 이유'를 그림만으로 설명하기 어렵다. 실제 모델에서 달의 위치를 바꿔가며 지구 시점의 변화를 보게 만든 이유다.

[계절 모델](https://spaceatlasedu.org/earth/seasons/)은 다른 문제를 다룬다. 지구가 공전하는 동안 자전축이 공간에서 거의 같은 방향을 유지한다는 사실이 보이지 않으면, 여름과 겨울을 태양과의 거리 차이로 해석하기 쉽다. 기울기의 방향과 관찰 위치를 함께 제시하는 설계가 필요했다.

일식과 월식은 평면 그림의 한계를 드러낸다. 달의 궤도면이 지구 공전면에 대해 약 5도 기울어져 있다는 점을 빠뜨리면 매달 식이 일어나지 않는 이유를 설명할 수 없다. 기고문은 평면도에 더해 궤도면의 옆모습과 교점을 보여주는 설명 방식을 다뤘다.

세 사례는 과학적 정확성을 챙기려면 더 많은 그래픽을 넣어야 한다는 주장이 아니다. 독자가 판단에 필요한 관계를 볼 수 있도록 무엇을 표시할지 결정해야 한다는 개발 경험에 가깝다. 실제 모형과 교육용 단순화 사이의 차이를 UI에서 설명하는 능력을 글에서도 시험했다.

## 외부 기고가 남긴 개발 실적

이번에 확인 가능한 결과는 **EUSci의 실제 게재 페이지, 작성자 표시, 편집자 크레딧**이다. 공개된 기고문은 Space Atlas의 인터랙티브 모델을 일반 독자에게 설명하는 별도의 작업물이 됐다. 교육자나 잠재적 협업자는 글에서 문제의식을 읽고 [실제 달 위상 모델](https://spaceatlasedu.org/moon/phases/)을 열어 설명과 구현을 비교해 볼 수 있다.

원문에는 AI가 초안 작성과 편집을 보조했다는 공개 문구도 있다. 과학적 설명은 기사에 연결된 NASA 자료 등을 바탕으로 점검했다고 명시돼 있다. 매체 게재는 확인되지만, 대학의 공식 보증이나 실제 수업 적용·학습 효과까지 확인된 것은 아니다.

- [EUSci 기고문 원문과 편집자 표기](https://eusci.org.uk/2026/11/10/three-space-diagrams-three-missing-clues/)
- [NASA: 달 위상의 원리](https://science.nasa.gov/moon/moon-phases/)
- [Space Atlas 개발 사례](/portfolio/space-atlas/) 및 [기존 기술 소개](/space-atlas-student/)

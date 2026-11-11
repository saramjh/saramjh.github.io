---
title: "재료의 비율을 계산하던 recipeCalc가 Spoonie로 이어지기까지"
description: "2024년 재료량 계산기 recipeCalc에서 시작해 2025년 Spoonie 저장소, 2026년 공개 Recipe·Recipeed 설계로 이어진 개발 과정. 실제 저장소와 서비스를 근거로 돌아봤다."
date: 2026-11-11
tags: ["Spoonie", "recipeCalc", "레시피", "독립 개발", "제품 설계", "개발 회고"]
permalink: /recipe-calc-to-spoonie-origin-ko/
layout: default
lang: ko
alternate_lang: en
alternate_url: /recipe-calc-to-spoonie-origin-en/
image: /spoonie-social-cooking-early-users/recipe-record-flow.svg
image_width: 1200
image_height: 400
published: true
seo:
  title: "recipeCalc에서 Spoonie까지: 레시피 계산기를 요리 기록 서비스로 확장한 과정"
  description: "2024년 recipeCalc의 재료 비율 계산에서 Spoonie의 Recipe·Recipeed 구조까지. 실제 공개 코드와 화면으로 확인하는 독립 개발 기록."
---

> English: [From a recipe calculator to Spoonie: how the problem changed](/recipe-calc-to-spoonie-origin-en/)

**Spoonie는 처음부터 요리 커뮤니티로 기획한 프로젝트가 아니었다.** 2024년에 내가 먼저 만든 것은 재료의 양을 맞추는 작은 웹 계산기 [recipeCalc](https://github.com/saramjh/recipeCalc)였다. 필요한 재료 한 가지의 양이 달라지면 나머지 재료도 같은 비율로 다시 계산하는 도구였다. 이후 레시피를 보관하고 다시 찾아보는 문제에 관심이 옮겨갔고, 별도의 [Spoonie 저장소](https://github.com/saramjh/spoonie)를 만들어 지금의 레시피 서비스로 발전시켰다.

이 과정은 공개 기록으로 구분할 수 있다. recipeCalc 저장소는 **2024년 8월 22일**에, Spoonie 저장소는 **2025년 7월 19일**에 만들어졌다. 저장소 생성일이 서비스 출시일을 의미하는 것은 아니다. 현재 작동하는 결과는 [Spoonie](https://spoonie.kr/)와 [공개된 실제 레시피](https://spoonie.kr/recipes/554ae9ef-15a1-4806-944e-170884d17a96)에서 볼 수 있다.

## 첫 문제는 재료 한 가지의 양이었다

처음 해결하고 싶었던 것은 반복되는 계량이었다. 레시피에 적힌 양대로 조리할 수 없는 날이 있다. 준비한 재료가 적을 수도 있고, 한 번에 더 많은 분량을 만들어야 할 수도 있다. 이때 한 재료의 양만 바꾸면 다른 재료들도 같은 비율로 조정해야 한다.

recipeCalc에서는 재료 이름과 수량, 단위를 입력하고 기준이 될 재료를 선택했다. 예를 들어 밀가루를 원래 분량의 절반만 쓸 수 있다면 다른 재료의 수량도 같은 비율로 계산한다. 여러 재료를 한 번에 입력하거나 입력한 항목을 수정하고 지우는 기능도 만들었다. 당시 기능과 사용 방법은 [2024년 9월 3일에 쓴 첫 개발 기록](/recipe-scaling-application/)과 [공개 코드](https://github.com/saramjh/recipeCalc)에 남아 있다.

<figure>
  <img src="/recipe-scaling-application/recipescalingapplication.jpg" alt="2024년 recipeCalc의 실제 웹 인터페이스를 기록한 원본 스크린샷. 재료 이름과 수량을 입력하고 조정하는 계산기 화면이다." width="900" height="886" loading="lazy" style="display:block;width:100%;max-width:600px;height:auto;margin-inline:auto;">
  <figcaption>2024년 개발일지에 남긴 recipeCalc 원본 화면. 현재 Spoonie 화면을 재구성한 이미지가 아니다.</figcaption>
</figure>

이 도구는 계산을 빠르게 해 주었다. 그런데 계산하고 나면 또 다른 일이 남았다. 같은 레시피를 나중에 다시 쓰려면 어디에 정리하고 어떻게 찾아야 할까?

## 계산기에서 레시피를 보관하는 제품으로

오래 손으로 정리된 레시피 노트를 본 경험도 방향을 바꿨다. 노트에는 단순한 숫자 외에 시간이 쌓여 있었다. 레시피를 그때그때 입력하는 도구를 넘어, 다시 찾고 실제 조리할 때 쓸 수 있는 형태로 남기고 싶어졌다. 이 글에는 그 노트의 내용이나 작성자의 신상을 공개하지 않는다.

2025년 7월에 별도의 Spoonie 저장소를 만든 것은 그런 변화의 기록이다. 재료 비율 계산만 처리하던 도구에서 **레시피 자체를 하나의 콘텐츠로 다루는 서비스**로 범위가 넓어졌다. 재료와 만드는 방법을 읽고, 필요한 분량을 확인하고, 나중에 다시 찾아보는 흐름을 고려해야 했다.

구현 관점에서도 문제는 달라졌다. 계산기는 사용자가 입력한 값으로 정해진 연산을 수행한다. 레시피 서비스는 다양한 형식의 내용을 일정하게 표현하고, 다른 사람이 읽을 화면을 마련하고, 원본 정보가 이후 경험과 어떻게 연결되는지 설계해야 한다. 내가 배운 것은 계산 로직을 더 복잡하게 만드는 방법만이 아니었다. 작은 기능을 지속해서 이용할 수 있는 정보 구조로 바꾸는 일이었다.

## Recipe와 Recipeed로 나눈 이유

현재 Spoonie에서는 **Recipe**가 재료와 조리 방법을 담는다. **Recipeed**는 누군가 그 레시피를 참고해 실제로 요리한 뒤 남기는 기록으로 설계했다. 레시피를 읽는 일과 개인의 요리 경험을 남기는 일은 별도 행동이기 때문이다.

<figure>
  <img src="/spoonie-social-cooking-early-users/recipe-record-flow.svg" alt="개발자가 제작한 Spoonie의 Recipe와 Recipeed 관계도. 레시피를 읽고 조리한 경험을 원본 레시피에 연결해 기록하는 설계 흐름." width="1200" height="400" loading="lazy" style="display:block;width:100%;height:auto;">
  <figcaption>기존 개발일지에서 사용한 개발자 제작 관계도. 제품의 정보 구조를 설명하며 실제 이용자 수를 나타내지는 않는다.</figcaption>
</figure>

이 구분 덕분에 먼저 레시피를 읽고 싶은 사람은 공개 콘텐츠에서 필요한 정보를 확인할 수 있고, 요리 경험을 남길 사람에게는 별도의 기록 형태를 제공할 수 있다. 계산 도구에서 시작했지만 최종 설계는 *레시피를 참고하는 경험*과 *그 후에 남기는 기록*을 모두 고려하게 되었다.

한편 기능을 구현하는 일과 실제 사용자가 기록을 남기는 일은 별개다. 어떤 방문자가 첫 레시피를 찾고, 요리하고, 다시 돌아와 기록을 남기는지는 제품의 실제 이용 데이터로 평가해야 한다. 그 문제는 [Disquiet에 기고한 첫 기록에 관한 개발 회고](/spoonie-disquiet-first-record-ko/)에서 따로 다뤘다.

## 지금 공개된 결과와 남은 질문

2024년의 [계산기](https://saramjh.github.io/recipeCalc/)는 지금도 별도 웹 도구로 접근할 수 있다. Spoonie는 [공개된 레시피 상세 페이지](https://spoonie.kr/recipes/554ae9ef-15a1-4806-944e-170884d17a96)에서 현재의 콘텐츠 구조를 확인할 수 있다. 각각의 원본을 비교하면 작은 입력·계산 기능에서 공개 레시피와 요리 기록을 다루는 서비스로 개발 범위가 어떻게 바뀌었는지 볼 수 있다.

Spoonie는 [Web Apps Directory에도 등록](/spoonie-webapps-directory-ko/)되어 외부에서 찾을 수 있는 경로가 하나 생겼다. 이는 제품의 공개성과 발견 가능성에 관한 사실이다. 사람들이 실제로 얼마나 자주 조리하고 기록을 남기는지는 별도의 측정이 필요하다.

두 저장소와 공개 화면은 내가 문제를 발견하고, 작은 계산 도구를 만들고, 장기간에 걸쳐 그 문제를 제품 구조로 확장해 온 근거다. 앞으로도 기능의 수보다 실제 요리할 때 다시 찾고 싶어지는 레시피 경험을 개선하는 데 집중하고 싶다.

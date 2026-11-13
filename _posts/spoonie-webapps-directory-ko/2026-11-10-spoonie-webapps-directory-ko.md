---
title: "Spoonie, Web Apps Directory 음식·요리 분야에 등재"
description: "직접 개발한 집밥 레시피 커뮤니티 Spoonie가 Web Apps Directory에 등록됐다. 레시피 검색과 인분 조절, 요리 기록 연결을 구현한 과정과 외부에서 제품을 발견할 경로가 생긴 의미를 정리한다."
date: 2026-11-10
tags: ["Spoonie", "Web Apps Directory", "집밥 레시피", "요리 SNS", "웹앱 개발"]
permalink: /spoonie-webapps-directory-ko/
layout: default
lang: ko
alternate_lang: en
alternate_url: /spoonie-webapps-directory-en/
image: /spoonie-social-cooking-early-users/recipe-record-flow-og.png
image_width: 1200
image_height: 630
published: true
seo:
  title: "Spoonie의 Web Apps Directory 음식·요리 분야 등재"
  description: "직접 만든 레시피 커뮤니티 Spoonie가 외부 웹앱 목록에 등록됐다. Recipe와 Recipeed의 연결 구조, 개발 역량, 해외 이용자에게 발견될 가능성을 살펴본다."
---

> English version: [Spoonie is listed in Web Apps Directory's Food & Drink catalogue](/spoonie-webapps-directory-en/)

직접 개발한 집밥 레시피 커뮤니티 **Spoonie가 [Web Apps Directory의 Food & Drink 목록](https://webapps.directory/directory/spooniespoonie)에 등록됐다.** 현재 공개된 항목에는 2026년 10월 25일 수록됐다고 표시돼 있고, 실제 서비스인 [spoonie.kr](https://spoonie.kr/)로 연결된다. 국내 사용자를 위해 만든 한국어 서비스를 해외 웹앱 목록에서도 찾아볼 수 있게 된 것이다.

디렉터리는 레시피 검색, 인분에 따른 재료량 조절, 요리 경험 기록 기능을 소개한다. 처음 Spoonie를 보는 사람에게는 이 세 기능이 제품의 입구가 된다. 개발하면서 더 오래 고민한 부분은 레시피를 공개한 사람의 원본과, 그 레시피를 직접 따라 만든 사람의 기록이 서로 연결될 수 있는가였다.

<figure>
  <img src="/spoonie-social-cooking-early-users/recipe-record-flow.svg" alt="Spoonie의 Recipe 원본에서 요리한 경험이 생기고 Recipeed로 기록된 뒤 원본 출처로 연결되는 구조를 설명한 개발자 제작 도식." width="1200" height="400" loading="lazy" style="width:100%;height:auto;">
  <figcaption>직접 제작해 기존 개발일지에 공개한 Recipe와 Recipeed의 관계도. 실제 이용자 수나 Web Apps Directory 화면을 나타내는 자료는 아니다.</figcaption>
</figure>

## 등재된 제품에서 직접 만든 기능

Spoonie에서는 두 종류의 콘텐츠를 구분해 설계했다. **Recipe**는 재료, 조리 순서, 작성자를 포함한 원본 레시피다. **Recipeed**는 사용자가 음식을 만들어 본 뒤 사진이나 짧은 메모로 남기는 기록이다. Recipeed 작성자가 참고한 Recipe를 지정하면 그 관계를 연결할 수 있도록 구성했다.

인분 조절은 사용자가 바로 체감할 수 있는 기능이다. 같은 요리를 1인분 또는 4인분으로 만들 때 재료량을 다시 계산할 필요가 없도록 표시하는 것이다. [Spoonie 홈페이지](https://spoonie.kr/)에서는 레시피 검색과 요리 기록의 기본 흐름을 볼 수 있다. 공개된 [실제 Recipe 페이지](https://spoonie.kr/recipes/554ae9ef-15a1-4806-944e-170884d17a96)를 열어보면 음식 정보가 어떻게 정리돼 있는지도 확인할 수 있다.

개발 과정에서는 데이터 구조와 화면 동작을 함께 고민했다. 원본 조리법을 보존하면서도 누군가의 재료 변경이나 완성 사진은 별개의 경험으로 남아야 한다. 출처를 명확히 표시하고 기록을 이어보는 기능은 이 관계를 실제 제품에서 표현하는 방법이다.

## 외부 목록이 만들어 준 새로운 발견 경로

Spoonie 공식 사이트와 직접 링크에 이어, 이제 [Web Apps Directory 원문](https://webapps.directory/directory/spooniespoonie)에도 Spoonie가 브라우저에서 이용하는 요리 분야 서비스로 소개돼 있다. 처음 접한 방문자가 서비스 설명을 읽고 실제 Spoonie 화면으로 이동할 수 있는 공개 경로가 하나 더 생겼다.

개발자나 협업 상대가 제품을 평가할 때 제3자 웹앱 목록의 설명과 실제 서비스를 대조할 수 있다는 점도 도움이 된다. 한국어 전용 서비스가 영어로 작성된 목록에 실렸다는 사실은 해외에서 발견될 가능성을 넓히지만, 한국어를 모르는 사람이 곧바로 모든 기능을 편하게 쓸 수 있다는 뜻은 아니다.

이번에 확인된 성과는 **외부 목록에 실리고 실제 제품으로 연결되는 경로**다. 이 등재를 통해 가입자가 늘었는지, 다시 요리 기록을 남겼는지는 별도의 사용 기록으로 확인해야 한다.

## 이후에 확인할 사용자 행동

레시피를 발견한 사람이 실제로 만들고, 자신의 기록을 남기고, 다음 요리를 찾으러 돌아오는지 살펴보려 한다. 원본과 요리 경험을 연결한 구조가 반복 사용에 도움이 되는지는 이런 실제 흐름이 있어야 판단할 수 있다.

[Web Apps Directory 원문](https://webapps.directory/directory/spooniespoonie)과 [외부 성과 원본 목록](/portfolio/recognition/)에서 등재 사실을 확인할 수 있다. Recipe와 Recipeed 구조를 처음 설계한 과정은 [Spoonie 요리 SNS 개발일지](/spoonie-social-cooking-early-users/)에 정리했다. [실제 Spoonie](https://spoonie.kr/)에서 현재 제공되는 기능도 확인할 수 있다.

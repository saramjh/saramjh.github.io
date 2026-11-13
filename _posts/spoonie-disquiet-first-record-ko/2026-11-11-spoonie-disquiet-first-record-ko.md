---
title: "Disquiet에 Spoonie 개발 회고를 공개하며 다시 본 첫 요리 기록의 조건"
description: "2026년 10월 13일 Disquiet에 공개한 Spoonie 개발 회고. 레시피 인분 조절과 Recipeed 기록을 만든 뒤에도 첫 작성자가 생기기 어려웠던 이유와 검증할 사용자 행동을 정리했다."
date: 2026-11-11
tags: ["Spoonie", "Disquiet", "프로덕트 개발", "UGC", "사용자 경험", "개발자 기고"]
permalink: /spoonie-disquiet-first-record-ko/
layout: default
lang: ko
alternate_lang: en
alternate_url: /spoonie-disquiet-first-record-en/
image: /spoonie-social-cooking-early-users/recipe-record-flow-og.png
image_width: 1200
image_height: 630
published: true
seo:
  title: "Disquiet에 공개한 Spoonie 개발 회고와 초기 사용자 검증"
  description: "Spoonie를 1인 개발하며 겪은 첫 요리 기록 문제를 Disquiet에 공개했다. Recipe·Recipeed 설계와 실제 사용자 행동을 구분해 검증하는 방법."
---

> English version: [Publishing my Spoonie cold-start lesson on Disquiet](/spoonie-disquiet-first-record-en/)

**2026년 10월 13일, Spoonie를 개발하며 겪은 초기 사용자 문제를 [Disquiet에 직접 기고했다](https://disquiet.io/articles/MVsxQv).** 글의 제목은 「레시피 SNS를 만들고 깨달은 것: 기능보다 먼저 ‘첫 기록의 이유’가 필요했다」다. DevTestudinidae 명의로 공개한 이 회고에서는 기능 개발을 끝내는 일과 새로운 사용자가 자기 이야기를 남기기 시작하는 일이 왜 다른지 설명했다.

이 글을 외부 개발자 커뮤니티에 공개한 이유는 완성된 제품을 홍보하기 위해서만은 아니었다. 레시피를 정리하고 인분에 맞춰 재료량을 계산하는 기능이 있어도, 사람이 굳이 새 서비스에 첫 요리 기록을 남길 이유는 따로 설계해야 한다는 문제를 구체적으로 제시하고 싶었다.

<figure>
  <img src="/spoonie-social-cooking-early-users/recipe-record-flow.svg" alt="개발자가 만든 Spoonie 개념도. 공개 Recipe를 참고한 요리 경험이 Recipeed 기록으로 남고, 원본과 연결되는 흐름을 나타낸다." width="1200" height="400" loading="lazy" style="width:100%;height:auto;">
  <figcaption>기존 개발일지에 공개한 Recipe–Recipeed 관계도. 실제 사용자 활동이나 가입 수를 보여주는 통계는 아니다.</figcaption>
</figure>

## 기능을 만든 다음에 남은 질문

[Spoonie](https://spoonie.kr/)에는 조리법과 재료를 정리한 **Recipe**, 요리한 뒤 사진과 바꾼 점을 남기는 **Recipeed**가 있다. Recipe에서는 인분을 바꾸면 등록된 재료량을 함께 확인할 수 있다. 공개 Recipe는 로그인하지 않고 읽을 수 있고, 본인의 Recipeed를 작성할 때는 로그인이 필요하다.

이 흐름을 구현한 뒤에도 중요한 질문이 남았다. 사용자는 레시피를 찾아서 읽을 수 있지만, 왜 굳이 다른 곳이 아닌 여기에서 첫 요리 기록을 작성해야 할까? 버튼을 더 눈에 띄게 만들거나 입력 칸을 줄이는 것만으로 대답하기 어려운 질문이었다.

Disquiet에 쓴 글에서는 방문자에게 가입부터 요구하기보다 당장 만들 요리에 필요한 재료를 먼저 확인하게 하고, 요리한 뒤 자신의 다음 조리에 도움이 되는 기록을 남기도록 안내하는 순서를 설명했다. **사용자가 실제로 해결하려는 일과 서비스가 요구하는 행동의 순서**를 맞추려는 시도였다.

## 어떤 사용자 행동을 확인해야 하나

개발자는 페이지가 공개되고 홍보 게시물이 늘어나는 것을 쉽게 확인할 수 있다. 그러나 요리 SNS에서 더 중요한 일은 사용자가 처음으로 자기 기록을 남기고, 나중에 다시 돌아와 기록하는지다.

나는 이 과정을 서로 다른 단계로 보려 했다. 공개 레시피를 살펴본 방문자, 기록을 남기기 위해 가입한 사람, 첫 Recipeed를 실제로 작성한 사람, 다음 요리를 기록하러 돌아온 사람은 같은 성과 지표가 아니다. 한 단계의 활동을 다른 단계가 달성된 것처럼 표시하면 초기에 무엇을 고쳐야 할지 판단하기 어려워진다.

2026년 10월 13일 원문에서는 외부 제작자의 첫 Recipeed 작성이 확인된 성과라고 주장할 수 없다고 명시했다. 이것은 당시 공개한 검증 상태다. 이후의 실제 사용량이나 재방문 결과를 이 글에 소급해서 만들어 넣지 않는다.

## 기고가 개발 경험으로 남긴 것

이번 공개 글의 실적은 **내가 직접 만든 서비스를 대상으로 한 문제 정의와 검증 기준을 외부 개발자 커뮤니티에 설명했다**는 사실이다. Recipe와 Recipeed라는 데이터·화면 구조를 만든 작업뿐 아니라, 첫 사용자의 행동을 어떤 순서로 관찰할지까지 제품 설계의 대상으로 다뤘다.

비슷한 사용자 생성 콘텐츠 서비스를 만드는 개발자나 협업 상대는 [Disquiet 원문](https://disquiet.io/articles/MVsxQv)에서 그 당시의 판단을 확인하고, [실제 공개 Recipe](https://spoonie.kr/recipes/554ae9ef-15a1-4806-944e-170884d17a96)를 열어 제품의 입구를 살펴볼 수 있다. 독자가 문제에 동의하지 않더라도 구현한 기능과 검증하려던 행동을 구분해 논의할 수 있는 자료가 된다는 점이 의미 있다.

Recipe와 Recipeed를 연결하게 된 배경은 [기존 Spoonie 개발일지](/spoonie-social-cooking-early-users/)에, 외부 웹앱 목록에 실제로 등록된 성과는 [Web Apps Directory 등재 기록](/spoonie-webapps-directory-ko/)에 따로 정리했다.

이 Disquiet 기고는 개발자가 직접 작성해 공개한 회고이며, 독립적인 제품 평가나 사용자 증가를 증명하는 자료는 아니다.

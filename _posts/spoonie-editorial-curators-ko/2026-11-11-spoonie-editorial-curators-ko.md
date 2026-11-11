---
title: "스푸니에 공식 큐레이터 프로필 18개를 탐색하는 화면을 만들었다"
description: "Spoonie가 운영하는 편집 계정 18개를 정확한 공개 식별자로 확인하고, 요리·디저트·음료별 프로필 화면에 연결한 구현과 그 한계를 기록했다."
date: 2026-11-11
tags: ["Spoonie", "큐레이터", "프로필", "제품 개발", "Supabase", "권한 관리"]
permalink: /spoonie-editorial-curators-ko/
layout: default
lang: ko
alternate_lang: en
alternate_url: /spoonie-editorial-curators-en/
image: /spoonie-editorial-curators-ko/spoonie-curator-flow.svg
image_width: 1280
image_height: 600
published: true
seo:
  title: "스푸니 공식 편집 프로필 디렉터리 개발 기록"
  description: "18개 Spoonie 운영 편집 계정을 공개 프로필로 연결하면서 식별자, 공개 권한, 계정 출처를 검증한 이유. 실제 이용자 수나 레시피 발행 실적으로 혼동하지 않는다."
---

> English: [I shipped a directory for Spoonie's 18 editorial profiles](/spoonie-editorial-curators-en/)

**스푸니에 공식 큐레이터 프로필을 찾아볼 수 있는 페이지를 만들었다.** [공개 디렉터리](https://spoonie.kr/curators)는 2026년 11월 11일 확인 당시 요리 10개, 디저트 4개, 음료 4개, 모두 18개의 프로필로 연결됐다. 여기서 큐레이터는 **Spoonie가 직접 운영하는 레시피 소개 계정**이다. 실제 요리 전문가 18명이 참여했다거나, 18명의 이용자가 콘텐츠를 발행했다는 뜻은 아니다.

## 계정 목록보다 중요한 것은 누구의 계정인지 확인하는 일

프로필 이름을 검색해서 비슷한 계정을 모두 큐레이터로 표시하면, 일반 회원 계정까지 공식 계정처럼 보이게 할 수 있다. 그래서 [구현 PR #16](https://github.com/saramjh/spoonie/pull/16)에서는 사전에 검증한 공개 식별자를 기준으로 조회하도록 만들었다.

공개 프로필을 가져온 후에는 등록된 식별자와 계정 이름, `organization` 유형, 공개 여부, 공식 큐레이터를 나타내는 소개 문구를 다시 확인한다. 조건에 맞지 않는 프로필은 목록에 넣지 않는다. 프로필 조회가 실패하면 임의의 사람이나 활동 수치를 채우는 대신 불러오지 못했다는 상태를 보여준다.

이런 검사는 작은 디렉터리에도 필요하다. 사용자는 프로필을 보고 계정의 성격을 판단하기 때문이다. 공개 DB 조회로 화면을 만들되 관리자용 등록 작업과 권한은 클라이언트로 옮기지 않았다.

<figure>
  <img src="/spoonie-editorial-curators-ko/spoonie-curator-flow.svg" alt="Spoonie가 운영하는 편집 계정 18개를 등록된 공개 식별자와 계정 속성으로 확인한 뒤, 요리 10개·디저트 4개·음료 4개로 분류해 공개 프로필에 연결하는 개발 도식" width="1280" height="600" loading="lazy" style="display:block;width:100%;height:auto;">
  <figcaption>원본 PR #16과 11월 11일 공개 페이지를 기준으로 직접 작성한 구조도. 계정 수를 보여주는 자료이며 사람의 활동이나 레시피 발행량을 나타내지 않는다.</figcaption>
</figure>

## 공개 화면에서 확인할 수 있는 범위

[큐레이터 페이지](https://spoonie.kr/curators)는 세 범주를 나누고, 각 항목을 기존 Spoonie 프로필 화면에 연결한다. 별도 팔로우 서비스를 만들지 않고 원래 있던 프로필과 팔로우 진입점을 활용했다. 화면 아래에는 이 계정들이 Spoonie 운영 계정이며 **실제 레시피 원작자와 출처는 개별 레시피에서 별도로 안내한다**고 명시했다.

PR #16이 병합될 당시 이 운영 계정들에는 새 레시피가 발행되지 않았다. 그래서 디렉터리의 검색엔진 설정도 `noindex, follow`로 두었다. 11월 11일 공개 HTML에서 이 설정과 프로필 링크 18개를 확인했다. 현재 페이지를 볼 수 있다는 사실만으로 레시피가 쌓였거나 팔로우·활동이 늘었다고 말할 수는 없다.

## 구현으로 보여준 것

이번 작업은 공개 콘텐츠와 계정 신원을 분리해서 다룬 사례다. 검증된 계정만 드러내고, 일반 회원을 공식 편집자로 잘못 표시하지 않으며, 콘텐츠가 생겼을 때 이미 있는 프로필 화면을 활용할 수 있도록 했다. 공개 식별자·공개 권한·기존 사용자 화면을 함께 다루는 제품 구현이라는 점에서 의미가 있다.

그다음 과제는 계정 수를 늘리는 일이 아니다. 원본과 이미지 사용 권한을 확인한 실제 레시피를 발행하고, 사용자가 그 콘텐츠를 유용하게 읽거나 기록하는지 별도로 살펴야 한다. 이전에 만든 [공개 레시피 투표 기능](/spoonie-live-polls-ko/) 역시 코드와 공개 페이지의 존재, 실제 이용 성과를 구분해 기록했다.

## 네 장의 구현 도식

공개 계정 검증에서 실제 프로필 탐색으로 이어지는 개발 흐름을 네 장의 그림으로 정리했다. Spoonie 운영 큐레이터의 실제 얼굴이나 아바터, 서비스 화면을 복제한 이미지는 아니다.

[18개 운영 프로필](/assets/img/dev-spoonie-curators-ig-20261111/card-01.jpg) · [요리·디저트·음료 분류](/assets/img/dev-spoonie-curators-ig-20261111/card-02.jpg) · [공개 계정 확인](/assets/img/dev-spoonie-curators-ig-20261111/card-03.jpg) · [프로필·팔로우 탐색](/assets/img/dev-spoonie-curators-ig-20261111/card-04.jpg)


근거: [Spoonie 공식 큐레이터 페이지](https://spoonie.kr/curators), [병합된 구현 PR #16](https://github.com/saramjh/spoonie/pull/16), [Spoonie 개발 프로젝트 기록](/portfolio/spoonie/).

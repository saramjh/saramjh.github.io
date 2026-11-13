---
title: "Spoonie 레시피드의 댓글 수와 JSON-LD가 어긋난 문제"
description: "Spoonie PR #41에서 공개 댓글을 SocialMediaPosting 구조화 데이터에 반영하고 실제 게시물 13개로 확인한 과정."
date: 2026-11-14
tags: ["Spoonie", "SEO", "Structured Data", "Next.js"]
permalink: /spoonie-public-comments-jsonld-ko/
layout: default
lang: ko
alternate_lang: en
alternate_url: /spoonie-public-comments-jsonld-en/
published: true
seo:
  title: "Spoonie SocialMediaPosting 댓글 구조화 데이터 수정"
  description: "댓글 수만 있고 댓글 본문은 빠진 상황을 수정한 PR #41과 공개 13개 페이지의 JSON-LD 검증."
---

> English: [Fixing comment data in Spoonie’s SocialMediaPosting schema](/spoonie-public-comments-jsonld-en/)

댓글이 있는 글인데 구조화 데이터에는 댓글이 없는 것으로 표현될 수 있었다. Spoonie의 레시피드 상세 조회는 댓글 수를 가져오지만, 구조화 데이터를 만드는 데 쓰던 `comments_data` 배열까지 항상 포함하지는 않았다. 이전 `PostSchema`는 그 배열의 길이로 `commentCount`를 계산했다.

[Spoonie PR #41](https://github.com/saramjh/spoonie/pull/41)에서 공개 댓글의 실제 데이터와 JSON-LD를 연결했다. 배포 후 [공개 사이트맵](https://spoonie.kr/sitemap.xml)에 있는 레시피드 게시물 13개를 직접 확인했다.

## 데이터가 빠지던 위치

문제는 화면에 보이는 댓글 수와 검색엔진에 제공하는 JSON-LD가 서로 다른 데이터 경로를 사용한다는 데 있었다. `initialItem.comments_count`에는 댓글 총수가 있었지만, 예전 스키마 생성 코드는 `item.comments_data || []`에서 읽은 길이를 사용했다. 상세 조회에 배열이 포함되지 않으면 댓글을 0개로 기술할 수 있었다.

수정된 서버 경로는 **공개 게시물이고 댓글 수가 1개 이상일 때만** `comments` 테이블에서 삭제되지 않은 댓글을 조회한다. 작성일 오름차순으로 최대 50개를 가져와 `PostSchema`에 넘긴다. 스키마의 `commentCount`는 원래 게시물의 총수 값을 유지하고, 실제 본문이 있는 댓글만 `comment` 객체로 출력한다. 댓글이 없는 글에는 객체를 만들어 넣지 않는다.

댓글이 50개를 넘는 글에서는 총수와 JSON-LD에 포함된 댓글 객체 수가 다를 수 있다. 이 제한은 공개 HTML의 크기를 제어하기 위한 구현상의 선택이다.

## 운영 게시물 13개에서 확인

2026년 11월 14일(KST), 공개 사이트맵에는 레시피드 URL 13개가 있었고, 각 URL은 HTTP 200을 반환했다. 모든 페이지에 `SocialMediaPosting` JSON-LD가 있었다.

| 검사한 항목 | 결과 |
| --- | ---: |
| 댓글이 있는 공개 게시물 | 3개 |
| 댓글이 없는 공개 게시물 | 10개 |
| JSON-LD에 포함된 댓글 객체 | 4개 (1개·1개·2개) |
| 선언된 `commentCount`와 객체 수 불일치 | 0건 |

예를 들어 [댓글 2개가 있는 공개 글](https://spoonie.kr/posts/577808ef-555f-40cb-a71c-dcad1a1b6058)의 JSON-LD에는 `commentCount: 2`와 실제 `Comment` 객체 2개가 포함돼 있었다. 댓글이 없는 공개 글의 JSON-LD에는 `commentCount: 0`만 있고 `comment` 객체는 없었다. 검증에서는 댓글 원문과 작성자 정보를 별도로 저장하지 않았다.

이 결과는 **검사한 13개 공개 페이지의 현재 출력**에 대한 것이다. Google의 수집 시점, 검색 노출, 클릭 증가나 사용자 참여 변화는 아직 측정하지 않았다.

## 같은 유형의 문제를 점검할 때

스키마를 만드는 컴포넌트 테스트만으로는 운영 데이터 경로의 누락을 발견하기 어렵다. PR #41은 실제 댓글과 빈 댓글, 표시 개수 상한에 대한 회귀 테스트 3개를 추가했고, 운영 점검에서는 완성된 HTML의 `application/ld+json`을 직접 파싱했다.

[Schema.org의 SocialMediaPosting](https://schema.org/SocialMediaPosting)과 [Comment](https://schema.org/Comment)는 구조화 데이터의 어휘를 정의한다. 실제 검색 결과 형식이나 순위를 보장하지는 않는다. 이전 [Spoonie 사이트맵 XML 오류 수정](/spoonie-sitemap-xml-image-escaping-ko/)도 소스 테스트와 운영 출력 검증을 분리해 다뤘다.

[원본 PR #41](https://github.com/saramjh/spoonie/pull/41) · [Spoonie](https://spoonie.kr/)

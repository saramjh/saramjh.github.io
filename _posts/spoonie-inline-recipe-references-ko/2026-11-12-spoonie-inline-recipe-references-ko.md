---
title: "Spoonie 레시피 본문과 댓글에 인라인 인용 칩을 넣은 과정"
description: "Spoonie PR #32·#33에서 레시피 본문과 댓글에 다른 레시피를 연결하는 인라인 칩을 구현한 방식과 운영 검증 범위를 정리했습니다."
date: 2026-11-12
tags: ["Spoonie", "Frontend", "Editor"]
permalink: /spoonie-inline-recipe-references-ko/
layout: default
lang: ko
alternate_lang: en
alternate_url: /spoonie-inline-recipe-references-en/
published: true
seo:
  title: "Spoonie 인라인 레시피 인용 칩 구현"
  description: "본문·댓글의 레시피 인용, 저장 형식과 접근 권한 처리: Spoonie PR #32·#33 개발 기록."
---

> English: [Inline recipe references in Spoonie's posts and comments](/spoonie-inline-recipe-references-en/)

Spoonie의 레시피 글과 댓글에서 다른 레시피를 바로 연결할 수 있도록 인라인 인용 칩을 구현했습니다. [PR #32](https://github.com/saramjh/spoonie/pull/32)는 2026년 11월 12일 병합됐고, [PR #33](https://github.com/saramjh/spoonie/pull/33)에서 레시피 본문 관련 지원을 보완했습니다.

## 글을 쓰는 자리에서 레시피 연결하기

편집기에서 `[[`를 입력하면 인용할 레시피를 검색하고 선택할 수 있습니다. 선택된 레시피는 썸네일과 제목을 포함한 클릭 가능한 칩으로 나타납니다. 게시글 본문뿐 아니라 댓글과 답글에도 같은 편집 방식을 적용했습니다. 키보드와 터치 선택을 고려한 구성입니다.

## 저장 형식과 접근 권한

편집기에는 ProseMirror/Tiptap의 인라인 노드를 사용하지만, 저장할 때는 레시피 ID를 `[[recipe:<UUID>]]` 형태의 텍스트로 직렬화합니다. 기존 텍스트 컬럼과 저장 경로를 유지하기 위한 선택입니다.

공개 화면에서는 기존 데이터베이스의 행 단위 접근 제어(RLS)로 조회 가능한 레시피만 링크형 칩으로 표시하도록 구현했습니다. 삭제됐거나 비공개로 전환된 레시피는 연결 불가 상태로 처리합니다. 인용 검색에는 기존 검색 함수를 재사용했습니다.

## 확인된 범위

PR #32의 기록에는 단위 테스트, 타입 검사, 빌드와 격리된 화면 검증이 포함돼 있습니다. 운영 Spoonie 사이트에서 인용 관련 문자열이 포함된 JavaScript 청크가 제공되는 것도 확인했습니다. 다만 실제 이용자의 편집·저장 성공률이나 인용 사용량은 측정하지 않았습니다.

화면 전환과 인용 검색 UI의 후속 정비는 [PR #34 개발 기록](/spoonie-route-loading-citation-ko/)에서 확인할 수 있습니다.

[원본 구현 PR #32](https://github.com/saramjh/spoonie/pull/32) · [보완 PR #33](https://github.com/saramjh/spoonie/pull/33) · [Spoonie](https://spoonie.kr/)

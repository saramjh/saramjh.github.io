---
title: "20개 뒤에 있는 레시피까지 찾도록 Spoonie 검색을 고쳤다"
description: "Spoonie 검색에서 레시피와 레시피드의 서버 페이지 조회를 분리하고 제목이 같은 레시피를 작성자별로 유지하도록 개선한 개발 기록이다."
date: 2026-11-12
tags: ["Spoonie", "레시피 탐색", "제품 개발", "Supabase", "검색"]
permalink: /spoonie-search-discovery-ko/
layout: default
lang: ko
alternate_lang: en
alternate_url: /spoonie-search-discovery-en/
image: /spoonie-search-discovery-ko/spoonie-search-flow-og.png
image_width: 1200
image_height: 630
published: true
seo:
  title: "Spoonie 검색 개선: 레시피 정렬·페이지 조회·참고 레시피 선택"
  description: "같은 이름을 가진 레시피를 분리하고, 레시피·레시피드를 20건씩 조회하는 Spoonie PR #31 개발 과정과 공개 배포 확인 내용을 정리했다."
---

> English: [How I made Spoonie's recipe search work past its first twenty results](/spoonie-search-discovery-en/)

**Spoonie의 레시피 검색을 각 유형별로 다음 페이지까지 탐색할 수 있도록 고쳤다.** [PR #31](https://github.com/saramjh/spoonie/pull/31)은 2026년 11월 12일(한국 시간) 병합됐으며, [운영 검색 화면](https://spoonie.kr/search)에서 배포된 검색용 JavaScript가 새 페이지 조회 인자와 ‘더 보기’ 버튼을 제공하는 것을 확인했다.

<p class="article-live-demo"><a class="article-live-demo-link" href="https://spoonie.kr/search">스푸니에서 레시피 검색 직접 해보기</a><span class="article-live-demo-note">레시피와 레시피드 결과를 나누어 찾아볼 수 있습니다.</span></p>

## 이전 검색이 놓치던 결과

기존 검색 함수는 한 검색어에 대해 최대 20개 항목을 받아 레시피와 레시피드로 나눠 보여줬다. 결과가 그보다 많아도 다음 묶음을 요청할 방법이 없었다. 게다가 같은 제목의 요리는 다른 작성자가 각자의 방법으로 만들 수 있다. 검색에서 제목만 보고 하나로 합치면 별개의 레시피를 찾기 어렵다.

이번 변경은 레시피 탭과 레시피드 탭에서 서버 조회를 각각 실행한다. 한 번에 21건을 요청해 20건을 표시하고, 마지막 한 건으로 다음 페이지 유무를 판단한다. 남은 결과가 있을 때만 ‘레시피 더 보기’ 또는 ‘레시피드 더 보기’를 보여준다. 더 읽을 데이터가 없는데 끝없이 목록을 요청하는 방식은 쓰지 않았다.

<figure>
  <img src="/spoonie-search-discovery-ko/spoonie-search-flow.svg" alt="검색어를 서버에서 정렬한 뒤 레시피와 레시피드를 개별 20건 페이지로 제공하고, 남은 결과가 있을 때 더 보기로 이어지는 개발자 제작 도식" width="1280" height="530" loading="lazy" style="display:block;width:100%;height:auto;">
  <figcaption>PR #31의 조회 구조를 그린 도식. 실제 서비스 화면이나 사용자 행동 통계는 아니다.</figcaption>
</figure>

## 같은 이름, 서로 다른 레시피

서버의 검색 순서는 제목 완전 일치를 먼저 고려한 뒤 관련도, 작성일, 고유 ID를 사용해 결정한다. 제목이 같더라도 서로 다른 ID와 작성자를 가진 글은 그대로 남는다. 결과 카드에는 기존 썸네일과 작성자 정보가 사용되므로, 이용자는 어느 글을 선택할지 판단할 수 있다.

[병합된 SQL 변경](https://github.com/saramjh/spoonie/pull/31/files)은 검색 함수 search_items_optimized에 항목 종류와 결과 시작 위치를 받는 인자를 추가했다. 이전 호출과의 호환을 위해 기본값을 두었고, SECURITY INVOKER 설정을 유지해 기존 행 단위 접근 제어(RLS)를 따르도록 했다. PR의 검증 기록에는 구형 함수 호출과 익명 조회 시 비공개 레시피 노출 여부, 페이지 사이의 중복 여부에 관한 확인이 포함돼 있다.

## 글을 작성할 때의 참고 레시피 선택

레시피나 레시피드에 참고한 글을 붙일 때도 제목이 겹칠 수 있다. 종전 선택창은 작성자와 레시피를 클라이언트에서 따로 찾았다. 이를 하나의 서버 함수 search_citable_recipes로 통합해 제목과 작성자 검색을 처리하고, 한 번에 10개씩 더 볼 수 있도록 수정했다. 입력 후 300ms 지연, 이전 요청 취소, 기존 이미지와 작성자 표시는 유지했다.

검색 결과에 표시된다는 사실이 남의 레시피 본문·사진을 복제할 권한을 뜻하지는 않는다. 인용할 글을 찾는 일과 그 콘텐츠를 재사용하는 권리는 구분해야 한다.

## 운영에서 확인한 범위

2026년 11월 12일, Spoonie의 [검색 페이지](https://spoonie.kr/search)는 HTTP 200이었다. 배포된 검색 스크립트에서 result_offset, item_type_filter 인자와 ‘레시피 더 보기’, ‘레시피드 더 보기’ UI 코드를 확인했다.

다만 운영 데이터에서 20개가 넘는 실제 결과를 모두 눌러 살펴보는 종단 간 테스트나 검색 성공률 측정은 수행하지 않았다. **확인한 성과는 별도 페이지 조회를 지원하는 검색 구현의 병합과 공개 배포**다.

관련 제품 사례로는 [Spoonie 공식 큐레이터 탐색](/spoonie-editorial-curators-ko/)과 [레시피 투표 구현](/spoonie-live-polls-ko/)이 있다. 전체 개발 맥락은 [Spoonie 프로젝트 페이지](/portfolio/spoonie/)에 정리했다.

원본 근거: [Spoonie PR #31](https://github.com/saramjh/spoonie/pull/31), [공개 검색 페이지](https://spoonie.kr/search).

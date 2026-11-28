---
title: "KoreAves 지역 목록의 5,464개 항목을 점검했다"
description: "17개 시도별 분류군 수를 합산하고, 각 지역 상세 페이지의 카드와 출처 요소를 대조했다."
date: 2026-11-28
tags: ["KoreAves", "bird records", "regional evidence", "Frontend Engineering", "data provenance"]
permalink: /koreaves-regional-catalogue-enumeration-ko/
layout: default
lang: ko
alternate_lang: en
alternate_url: /koreaves-regional-catalogue-enumeration-en/
published: true
seo:
  title: "KoreAves 17개 지역 목록: 5,464개 분류군 항목 점검"
  description: "17개 지역의 분류군 수 합계와 상세 페이지의 식별 카드, 출처 표시, 종 상세 링크를 실제 운영 HTML에서 확인했다."
---

> English: [A 17-region audit of the KoreAves bird catalogue](/koreaves-regional-catalogue-enumeration-en/)

KoreAves의 지역 목록에는 17개 행정구역에서 적격 기록이 확인된 5,464개 분류군 항목이 표시된다. 2026년 11월 28일 17개 상세 페이지를 조회해 목록 수치와 HTML 구조를 비교했다. 모든 페이지가 HTTP 200으로 응답했고, 카드·식별 행·지역 출처 표시·이미지 크레디트 영역·고유 종 상세 링크의 수가 각 지역의 목록 수치와 일치했다.

## 지역별 분류군 수

[11월 26일 업데이트 공지](https://koreaves.com/updates/regional-discovery-and-search/)에 따르면, 지역 목록에 분류군 수가 추가됐고 5,464개 지역별 항목에는 공통 식별 카드와 출처·이미지 크레디트가 적용됐다. 같은 업데이트에서 지도와 목록의 선택 상태를 화면 크기와 관계없이 동기화했다.

아래 수치는 각 행정구역에서 적격 기록이 확인된 분류군 수다. 지역별 상세 목록에서 해당 조류의 영문 표시명, 학명, 국명과 출처 정보를 확인할 수 있다.

<div class="overflow-table" role="region" aria-label="지역별 분류군 수" tabindex="0">
<table>
<thead>
<tr><th scope="col">지역</th><th scope="col">분류군 수</th></tr>
</thead>
<tbody>
<tr><td><a href="https://koreaves.com/regions/seoul/">서울특별시</a></td><td>327</td></tr>
<tr><td><a href="https://koreaves.com/regions/busan/">부산광역시</a></td><td>346</td></tr>
<tr><td><a href="https://koreaves.com/regions/daegu/">대구광역시</a></td><td>197</td></tr>
<tr><td><a href="https://koreaves.com/regions/incheon/">인천광역시</a></td><td>421</td></tr>
<tr><td><a href="https://koreaves.com/regions/gwangju/">광주광역시</a></td><td>196</td></tr>
<tr><td><a href="https://koreaves.com/regions/daejeon/">대전광역시</a></td><td>238</td></tr>
<tr><td><a href="https://koreaves.com/regions/ulsan/">울산광역시</a></td><td>270</td></tr>
<tr><td><a href="https://koreaves.com/regions/sejong/">세종특별자치시</a></td><td>211</td></tr>
<tr><td><a href="https://koreaves.com/regions/gyeonggi/">경기도</a></td><td>392</td></tr>
<tr><td><a href="https://koreaves.com/regions/gangwon/">강원특별자치도</a></td><td>379</td></tr>
<tr><td><a href="https://koreaves.com/regions/chungbuk/">충청북도</a></td><td>256</td></tr>
<tr><td><a href="https://koreaves.com/regions/chungnam/">충청남도</a></td><td>396</td></tr>
<tr><td><a href="https://koreaves.com/regions/jeonbuk/">전북특별자치도</a></td><td>395</td></tr>
<tr><td><a href="https://koreaves.com/regions/jeonnam/">전라남도</a></td><td>388</td></tr>
<tr><td><a href="https://koreaves.com/regions/gyeongbuk/">경상북도</a></td><td>344</td></tr>
<tr><td><a href="https://koreaves.com/regions/gyeongnam/">경상남도</a></td><td>333</td></tr>
<tr><td><a href="https://koreaves.com/regions/jeju/">제주특별자치도</a></td><td>375</td></tr>
<tr><th scope="row">17개 지역 합계</th><td>5,464</td></tr>
</tbody>
</table>
</div>

## 상세 페이지에서 확인한 항목

각 지역 페이지를 한 번씩 요청해 HTTP 상태와 UTF-8 디코딩을 확인했다. 페이지마다 다음 다섯 항목을 셌다.

- `catalog-item`: 지역 목록의 분류군 카드
- `ka-taxon-identity`: 영문명, 학명, 국명을 담은 식별 행
- `regional-source-note`: 지역 기록의 출처 표시
- `catalog-media-credit`: 이미지 크레디트 영역
- `/species/` 링크: 서로 다른 분류군 상세 페이지로 연결되는 링크

17개 페이지 모두에서 다섯 항목의 수가 해당 지역 목록의 분류군 수와 같았다. 이번 검증은 운영 페이지의 항목 수와 인터페이스 구조를 대상으로 한다. 개별 관찰 기록의 생물학적 정확성이나 이미지 라이선스의 유효성은 평가하지 않았다.

## 5,464를 읽는 방법

5,464는 17개 지역별 분류군 수의 합계다. 한 분류군이 여러 시도에 기록되면 각 지역 수치에 한 번씩 포함된다. 따라서 이 값은 지역과 분류군의 조합 수다. 국가 체크리스트는 597종과 20아종, 합계 [617개 분류군](https://koreaves.com/dataset/)으로 별도 관리된다.

지역 수치는 해당 행정구역에서 적격 기록이 확인된 분류군을 보여준다. 개체 수와 개체군 규모는 별도의 근거가 필요하다. 적격 기록이 없다는 사실만으로 생물학적 부재를 판단할 수 없다. 기록과 지도 범위는 [KoreAves 안내서](https://koreaves.com/guide/)와 [방법론](https://koreaves.com/methodology/)에서 설명한다.

지역을 먼저 고르려면 [17개 지역 목록](https://koreaves.com/regions/)에서 시작하면 된다. 특정 분류군의 지역별 근거를 비교하려면 [지역 GIS](https://koreaves.com/gis/)에서 이어서 확인할 수 있다.

관련 글: [지역 검색의 모바일 오류 수정](/koreaves-region-search-mobile-hotfix-ko/), [선택한 새를 지도와 비교 화면까지 이어 보기](/koreaves-selected-bird-share-links-ko/), [617개 분류군의 영문 표시명](/koreaves-english-display-labels-ko/), [KoreAves 프로젝트](/portfolio/koreaves/).

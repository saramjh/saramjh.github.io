---
title: "Jekyll 프로젝트 페이지가 블로그 글로 표시된 이유"
description: "Jekyll의 날짜 조건이 프로젝트 페이지를 BlogPosting으로 분류해 잘못된 게시일을 출력했다. Liquid 분기 순서를 수정하고 세 프로젝트의 운영 HTML을 확인했다."
date: 2026-11-13
tags: ["Jekyll", "구조화 데이터", "JSON-LD", "Liquid", "개발 기록"]
permalink: /jekyll-project-schema-date-ko/
layout: default
lang: ko
alternate_lang: en
alternate_url: /jekyll-project-schema-date-en/
image: /jekyll-project-schema-date-ko/jekyll-schema-ko-og.png
image_width: 1200
image_height: 630
published: true
seo:
  title: "Jekyll 프로젝트 페이지가 BlogPosting으로 출력된 원인과 수정"
  description: "프로젝트 페이지에 빌드 시각이 게시일처럼 들어간 Jekyll Liquid 조건 오류를 수정하고 운영 JSON-LD를 검증한 개발 기록."
---

> English version: [My Jekyll project pages were being published as blog posts](/jekyll-project-schema-date-en/)

개발자 포트폴리오의 프로젝트 소개 페이지 세 곳에서 이상한 구조화 데이터가 출력되고 있었다. KoreAves, Space Atlas, Spoonie를 소개하는 페이지인데 검색엔진용 JSON-LD의 유형은 `BlogPosting`이었다. 게시일에는 실제 글 작성일이 아닌 빌드 과정에서 나온 날짜가 들어갔다. [PR #98](https://github.com/saramjh/saramjh.github.io/pull/98)에서 Liquid 조건의 순서를 고쳤고, 배포 후 세 페이지의 HTML을 직접 확인했다.

문제는 페이지 본문이 아니라 구조화 데이터 템플릿에 있었다. 글인지 확인하기 위해 `page.date`를 맨 먼저 검사했는데, 프로젝트 컬렉션 문서를 빌드할 때도 그 값이 존재했다. 결국 프로젝트 소개 페이지가 블로그 글 분기로 들어갔다.

<figure>
  <a href="/jekyll-project-schema-date-ko/jekyll-schema-ko-og.png"><img src="/jekyll-project-schema-date-ko/jekyll-schema-ko-og.png" alt="Jekyll 분기 조건의 실제 수정 내용. 이전에는 프로젝트에서 page.date가 먼저 참이 돼 BlogPosting이 출력됐고, 수정 후에는 프로젝트 레이아웃을 먼저 확인해 WebPage 및 WebApplication으로 출력한다" width="1200" height="630" loading="lazy" style="width:100%;height:auto;"></a>
  <figcaption>원본 PR #98의 Liquid 분기 변경을 직접 그린 설명도. Google Search Console의 실제 화면을 캡처한 이미지는 아니다.</figcaption>
</figure>

## 어느 조건에서 잘못 분류됐나

이전 템플릿은 먼저 `page.date`가 있는지 검사했다. 빌드된 프로젝트 문서에서는 이 조건이 참이었고, `datePublished`를 포함한 `BlogPosting`이 생성됐다. 프로젝트 페이지를 새로 작성한 날짜라는 근거는 없었다.

수정한 템플릿은 프로젝트의 식별 조건을 먼저 검사한다.

```liquid
{% raw %}{% if page.layout == 'project' and page.site_url and page.slug %}
  {# WebPage와 WebApplication을 생성 #}
{% elsif page.date %}
  {# 실제 날짜가 있는 블로그 글에 BlogPosting 적용 #}
{% endif %}{% endraw %}
```

위 코드는 조건을 이해하기 위한 발췌다. 실제 필터와 JSON-LD 생성 코드는 [병합된 PR의 변경 파일](https://github.com/saramjh/saramjh.github.io/pull/98/files)에서 확인할 수 있다.

## 프로젝트 페이지의 JSON-LD

현재 프로젝트 소개는 `WebPage`이고, 그 안의 `mainEntity`가 `WebApplication`이다. 애플리케이션 이름, 설명, 공식 주소, 대표 이미지와 작성자 정보는 각 프로젝트의 기존 프런트매터에서 가져온다. 같은 내용을 관리하는 별도 목록을 만들지 않았다.

이미 검증된 외부 *디렉터리 등재*만 `subjectOf`에 추가했다. 각각 독립된 `WebPage` 출처이며, 추천이나 제휴, 리뷰, 별점으로 표현하지 않았다. 배포된 구조화 데이터에는 [KoreAves](/portfolio/koreaves/) 5건, [Space Atlas](/portfolio/space-atlas/) 1건, [Spoonie](/portfolio/spoonie/) 2건이 들어 있다. 신규 게재 수가 아니라 기존에 확인했던 출처의 개수다.

## 실제 배포 결과를 확인한 방법

[회귀 테스트](https://github.com/saramjh/saramjh.github.io/blob/main/tests/test_portfolio_project_structured_evidence.py)는 날짜 조건보다 프로젝트 조건이 먼저 나오는지 확인한다. 프로젝트 이름과 공식 URL이 각 프로젝트 소스에 있는 값인지도 검사한다. Jekyll 빌드와 Python 테스트 95개, 기존 포트폴리오 JavaScript 테스트 3개가 통과했다.

[GitHub Pages 배포](https://github.com/saramjh/saramjh.github.io/actions/runs/43240987471) 뒤 실제 공개 HTML에서 `application/ld+json`을 찾아 파싱했다. 세 페이지가 모두 HTTP 200이었고, `WebPage` 안에 `WebApplication`이 있었다. 출처가 불분명했던 프로젝트 게시일과 수정일은 사라졌다. 반대로 실제 작성일이 있는 [Space Atlas 개발 글](/space-atlas-science-accuracy-ko/)은 11월 12일 날짜를 가진 `BlogPosting`으로 유지됐다.

Jekyll에서 비슷한 현상이 생기면 프런트매터만 확인하지 말고 **렌더링된 HTML의 JSON-LD**를 살펴보는 편이 정확하다. 빌드가 성공해도 조건식이 의도한 순서로 실행됐는지는 별개의 문제다. [Schema.org의 WebApplication 유형](https://schema.org/WebApplication)을 맞춰 출력했지만, 이것만으로 검색 순위나 특수 검색 결과가 보장되지는 않는다. 실제 색인 변화와 방문자 증가도 아직 측정하지 않았다.

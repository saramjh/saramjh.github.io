---
title: "OG 이미지를 SVG에서 PNG로 바꾸자 회귀 테스트가 실패했다"
description: "Jekyll 블로그 8개 글의 소셜 미리보기를 PNG로 전환했다. 한글 렌더링 오류와 고정된 SVG 테스트를 수정한 뒤 배포한 실제 사례."
date: 2026-11-10
tags: ["Jekyll", "Open Graph", "회귀 테스트", "GitHub Actions", "개발일지"]
permalink: /jekyll-svg-to-png-og-ci-regression-ko/
layout: default
lang: ko
alternate_lang: en
alternate_url: /jekyll-svg-to-png-og-ci-regression-en/
image: /spoonie-author-header-consistency-ko/author-header-ko-og.png
image_width: 1200
image_height: 630
published: true
seo:
  title: "Jekyll OG 이미지 SVG→PNG 전환과 CI 회귀 테스트"
  description: "한·영 글 8개의 SVG 소셜 이미지를 PNG로 바꾸고, 실패한 GitHub Actions 테스트와 한글 글리프를 검증한 개발 기록."
---

> English edition: [Why changing my Open Graph image to PNG broke CI](/jekyll-svg-to-png-og-ci-regression-en/)

**Jekyll 블로그의 소셜 이미지 경로를 바꾸자, 기존 테스트가 실패했다.** 글 자체는 바뀌지 않았다. 회귀 테스트가 `og:image`의 이전 SVG 파일명과 높이까지 고정해 놓았기 때문이다. 실제 [PR #27](https://github.com/saramjh/saramjh.github.io/pull/27)에서 확인한 문제다.

기존 블로그에는 한국어·영어 글 네 쌍, 총 **8개 글**의 Open Graph와 Twitter 이미지가 SVG로 지정돼 있었다. 플랫폼별 SVG 미리보기 지원에 의존하지 않도록, 본문 도해는 SVG로 유지하고 메타데이터에는 **1200×630 PNG**를 제공하기로 했다. 같은 도해를 쓰는 한·영 글도 있어 PNG 파일은 **7개**면 충분했다.

<figure>
  <a href="/spoonie-author-header-consistency-ko/author-header-ko-og.png"><img src="/spoonie-author-header-consistency-ko/author-header-ko-og.png" alt="기존 Spoonie 작성자 헤더 도해를 1200×630 PNG로 변환한 결과. 중앙에 레시피와 레시피드의 상단바 정렬 비교가 표시된다." width="1200" height="630" loading="lazy" style="width:100%;height:auto;"></a>
  <figcaption>실제 블로그의 SVG 도해를 변환한 PNG다. Instagram·Threads 등 소셜 플랫폼의 링크 카드 캡처는 아니다. [작성자 헤더 정렬 개발 기록](/spoonie-author-header-consistency-ko/)과 [본문용 원본 SVG](/spoonie-author-header-consistency-ko/author-header-ko.svg)를 확인할 수 있다.</figcaption>
</figure>

## 실패했던 검사는 무엇이었나

이전 테스트 `tests/test_ga4_report_window_release.py`는 GA4 사례 글의 이미지 경로가 `timeline-ko.svg` 또는 `timeline-en.svg`인지 확인하고, 메타데이터 높이를 **620**으로 기대했다. 소셜 이미지 경로를 `timeline-ko-og.png` 등으로 바꾸고 높이를 **630**으로 수정하면서 해당 기대값이 낡았다.

[첫 번째 GitHub Actions 실행](https://github.com/saramjh/saramjh.github.io/actions/runs/42726645118)은 이 검증에서 실패했다. 테스트를 없애는 대신 검사 대상을 나눴다. 본문에는 원본 SVG가 남았는지 확인하고, 소셜 이미지에는 PNG 파일 경로, 헤더와 1200×630 크기를 확인하도록 바꿨다.

실제 회귀 테스트에서 PNG 시그니처와 크기를 확인하는 핵심 부분은 다음과 같다.

```python
from pathlib import Path

png = Path("_posts/spoonie-author-header-consistency-ko/author-header-ko-og.png").read_bytes()
assert png[:8] == b"\x89PNG\r\n\x1a\n"
assert png[12:16] == b"IHDR"

width = int.from_bytes(png[16:20], "big")
height = int.from_bytes(png[20:24], "big")
assert (width, height) == (1200, 630)
```

이 검사는 파일 형식과 가로·세로 픽셀 수만 검증한다. 글자가 정상적으로 보이는지, 소셜 플랫폼에서 이미지를 가져오는지는 별도의 검사다.

## 한글이 사라진 첫 PNG 시안

초기 SVG→PNG 변환 결과를 픽셀로 확인했을 때, 한국어 도해의 한글이 빠져 있었다. 파일을 PNG로 저장하는 과정이 끝났다는 사실만으로 화면이 올바른 것은 아니었다.

한국어 파생 이미지를 생성할 때 설치된 `Noto Sans CJK KR` 글꼴을 사용하도록 렌더링 설정을 바꾸고 다시 확인했다. **원본 SVG의 글꼴이나 본문 이미지는 수정하지 않았다.** 축소된 미리보기와 1200×630 원본 크기를 모두 확인했다. 글꼴 변경은 이번 한국어 이미지 파생물의 렌더링에만 적용했다.

## 배포 후 확인한 결과

[수정된 PR #27](https://github.com/saramjh/saramjh.github.io/pull/27)의 빌드가 통과했고, **2026년 11월 10일** 기본 브랜치에 병합됐다. 이후 [GitHub Pages 배포 실행](https://github.com/saramjh/saramjh.github.io/actions/runs/42727063117)이 성공했다.

공개 사이트에서 한·영 글 **8개**와 PNG 파일 **7개**가 모두 HTTP 200으로 응답했다. PNG 응답의 MIME 타입은 `image/png`였고, 크기는 **1200×630**이었다. 서버에서 내려받은 PNG의 SHA-256도 작업 파일과 일치했다. `og:image`, `twitter:image`, canonical, 두 언어 간 `hreflang` 연결, 본문 원본 SVG도 확인했다.

이 결과는 **블로그 배포와 이미지 파일 제공이 정상이라는 증거**다. Instagram·Threads 등의 실제 링크 카드 렌더링이나 클릭·유입 증가는 측정하지 않았다. 그런 결과를 이번 배포의 성과로 쓰지는 않는다.

이전 [UTF-8 문안 검증 사례](/utf8-caption-hash-is-not-text-quality-ko/)에서는 파일 해시가 맞아도 문장이 손상될 수 있음을 확인했다. 이번에는 이미지 형식 검사, 렌더링 육안 검사, 배포된 URL 검사가 각각 다른 실패 가능성을 다룬다는 사실을 작업 기록으로 남겼다. 관련 코드와 변경 파일은 [PR #27의 diff](https://github.com/saramjh/saramjh.github.io/pull/27/files)에서 확인할 수 있다.

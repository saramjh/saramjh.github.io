---
title: "Playwright 테스트는 7초, Chromium 설치는 66초였다"
description: "GitHub Actions에서 반복되던 브라우저 설치 시간을 줄인 실제 사례. 러너 기본 Chrome을 활용하고 기존 반응형 검사를 유지한 배포 기록."
date: 2026-11-10
tags: ["Playwright", "GitHub Actions", "Chrome", "CI", "개발 기록"]
permalink: /playwright-github-actions-runner-chrome-ko/
layout: default
lang: ko
alternate_lang: en
alternate_url: /playwright-github-actions-runner-chrome-en/
published: true
seo:
  title: "GitHub Actions의 Playwright Chromium 설치 시간을 줄인 방법"
  description: "Chromium 설치 66초, 화면 검사 7초. GitHub 러너에 설치된 Chrome을 활용해 한 차례 빌드가 90초에서 40초로 줄어든 기록."
---

> **English:** [Playwright installed Chromium for 66 seconds. The browser test took seven.](/playwright-github-actions-runner-chrome-en/)

**Playwright 테스트를 빠르게 만들기 전에 CI가 브라우저를 설치하는 데 얼마나 쓰는지 확인할 필요가 있다.** GitHub Pages 작업 한 건에서 Chromium 설치는 **66초**, 반응형 브라우저 검사는 **7초**였다. 테스트 코드보다 그 앞의 준비 과정이 느렸다.

이 기록은 Jekyll 개발 블로그의 [PR #36](https://github.com/saramjh/saramjh.github.io/pull/36)에 근거한다. 기존 테스트는 실제 페이지를 **390·768·1440px**에서 열어 배치, JavaScript 오류, 개인정보 처리 조건과 모의 이벤트 연결을 확인한다. 시간을 줄이려고 검사를 삭제하지는 않았다.

## 설치와 검사를 따로 측정하다

기존 GitHub Actions 실행 네 건의 단계별 시간을 확인했다.

| 기존 빌드 | Chromium 설치 | 반응형 브라우저 검사 |
|---|---:|---:|
| [#42740449886](https://github.com/saramjh/saramjh.github.io/actions/runs/42740449886) | 21초 | 3초 |
| [#42745558937](https://github.com/saramjh/saramjh.github.io/actions/runs/42745558937) | 42초 | 4초 |
| [#42747929262](https://github.com/saramjh/saramjh.github.io/actions/runs/42747929262) | 66초 | 7초 |
| [#42742948303](https://github.com/saramjh/saramjh.github.io/actions/runs/42742948303) | 328초 | 6초 |

통제된 성능 실험은 아니지만, 테스트 밖에서 반복되는 비용을 확인할 수 있다. 기존 워크플로는 Python Playwright 설치 후 Chromium과 Linux 의존성을 별도로 내려받았다.

~~~sh
python -m pip install playwright==1.56.0
python -m playwright install --with-deps chromium
~~~

이 사이트는 GitHub 호스팅 **Ubuntu 24.04**에서 빌드한다. [러너 소프트웨어 목록](https://github.com/actions/runner-images/blob/main/images/ubuntu/Ubuntu2404-Readme.md)에는 Google Chrome이 포함돼 있다. Playwright는 해당 브라우저를 [Chrome 채널로 직접 실행](https://playwright.dev/python/docs/browsers)할 수 있다.

## 검사를 삭제하지 않고 준비 단계만 변경하다

[PR #36 변경 내역](https://github.com/saramjh/saramjh.github.io/pull/36/files)에서는 Playwright Python 패키지 버전을 유지하고 러너에 있는 Chrome의 존재 여부를 확인한다.

~~~yaml
- name: Install Playwright for preinstalled Chrome checks
  run: |
    python -m pip install playwright==1.56.0
    command -v google-chrome
    google-chrome --version

- name: Verify portfolio layout in real browser
  env:
    BLOG_TEST_BROWSER_CHANNEL: chrome
  run: |
    python tests/portfolio_layout_smoke.py
~~~

Python 쪽에서는 브라우저 채널만 환경 변수로 선택하도록 했다.

~~~python
import os
from playwright.sync_api import sync_playwright

with sync_playwright() as playwright:
    channel = os.environ.get("BLOG_TEST_BROWSER_CHANNEL") or None
    browser = playwright.chromium.launch(headless=True, channel=channel)
    # 기존 페이지, 화면 크기와 개인정보 처리 검사를 그대로 수행한다.
    browser.close()
~~~

CI에서는 Chrome을 사용하고, 환경 변수를 지정하지 않은 로컬에서는 Playwright 기본 Chromium을 사용한다. **이 설정이 개발자의 컴퓨터에 브라우저를 설치해 주는 것은 아니다.** GitHub 러너에서 Chrome이 사라지면 브라우저 존재 확인 단계부터 실패하게 했다. 검사를 조용히 건너뛰면 안 되기 때문이다.

## 실제 배포에서 확인한 수치

| 측정 단계 | 변경 전 [#42747929262](https://github.com/saramjh/saramjh.github.io/actions/runs/42747929262) | 변경 후 [#42752895730](https://github.com/saramjh/saramjh.github.io/actions/runs/42752895730) |
|---|---:|---:|
| 브라우저 준비 | 66초 | 6초 |
| 브라우저 검사 | 7초 | 17초 |
| 전체 빌드 작업 | 90초 | 40초 |

두 실행을 비교하면 전체 빌드가 **50초 짧아졌다.** 다만 화면 검사 자체는 **10초 길어졌다.** 실행 시점의 러너 부하와 네트워크, Chrome 버전이 서로 다를 수 있으므로, 모든 단축 효과를 이 변경에 귀속하거나 앞으로도 늘 55.6% 빨라진다고 말할 수는 없다.

[PR 검사](https://github.com/saramjh/saramjh.github.io/pull/36/checks)와 [기본 브랜치 GitHub Pages 빌드·배포](https://github.com/saramjh/saramjh.github.io/actions/runs/42752895730)는 성공했다. 로그에는 **Google Chrome 156.0.8078.79**가 기록됐고 실제 브라우저 배치 검사가 통과했다. 공개 사이트도 HTTP 200으로 확인했다. 이 변경은 게시물 주소를 바꾸지 않았으므로 IndexNow 통지는 정상적으로 생략됐다.

## 앞으로도 확인해야 할 것

GitHub 러너의 Chrome 버전은 바뀔 수 있지만 Playwright Python 패키지는 고정돼 있다. 다음 브라우저 버전에서 호환성 문제가 생길 수 있으므로 실제 화면 검사를 유지해야 한다. [Playwright의 CI 안내](https://playwright.dev/python/docs/ci)는 Linux 환경에서 브라우저 캐시 복원이 반드시 더 효율적이지는 않다고 설명한다.

이번 개선은 **개발 피드백을 받는 시간**을 줄인 사례다. 검색 노출, 사이트 방문자나 전환의 증가를 확인한 것은 아니다. 다른 종류의 CI 문제는 [SVG를 PNG로 바꿨을 때 깨진 테스트 기록](/jekyll-svg-to-png-og-ci-regression-ko/)에 있다. 나머지 개발 기록은 [포트폴리오](/portfolio/)에서 볼 수 있다.

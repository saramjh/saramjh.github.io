---
title: "혼자 여러 GitHub Pages를 굴리다 보니 생긴 애널리틱스 고민 (1) — 문제 정의"
description: "커스텀 도메인 없이 GitHub Pages 프로젝트 페이지를 여러 개 운영하면, 사실은 이미 모든 서비스가 같은 루트 도메인을 공유하고 있습니다. GA4 속성을 나눌지 합칠지, Search Console과 Clarity는 어디에 걸어야 할지 — 1인 개발자가 실제로 부딪힌 고민을 정리합니다."
date: 2026-09-18
tags: GA4, Google Analytics, Search Console, Microsoft Clarity, GitHub Pages, SEO
permalink: /gh-pages-analytics-notes-1-problem-kr/
layout: default
lang: ko
alternate_lang: en
alternate_url: /gh-pages-analytics-notes-1-problem-en/
---

<p style="background: rgba(0, 120, 212, 0.08); border-left: 4px solid #0078d4; padding: 10px 14px; margin-bottom: 16px; border-radius: 4px; font-size: 0.95rem;">
  🌐 <strong>English Edition available:</strong> Read the English version at <a href="/gh-pages-analytics-notes-1-problem-en/"><strong>Analytics Notes (English Edition)</strong></a>.
</p>

<p style="background: rgba(120, 90, 0, 0.08); border-left: 4px solid #b8860b; padding: 10px 14px; margin-bottom: 24px; border-radius: 4px; font-size: 0.9rem;">
  📚 <strong>시리즈 목차</strong> — 1편 <strong>문제 정의</strong> (현재 글) · <a href="/gh-pages-analytics-notes-2-reasoning-kr/">2편 근거 탐색</a> · <a href="/gh-pages-analytics-notes-3-decision-kr/">3편 결정과 적용</a> · <a href="/gh-pages-analytics-notes-4-open-kr/">4편 지금 상태와 열린 질문</a>
</p>

## 이건 "노하우 공유"가 아니라 "고민 기록"입니다

미리 말씀드리자면, 이 시리즈는 "이렇게 하니까 트래픽이 늘었다" 같은 검증된 성공 사례가 아닙니다. 저도 이게 실제로 효과가 있는지 확신하지 못합니다. GA4 구조와 SEO에 대한 논의를 AI와 나누면서 얻은 논리가 그럴듯해 보여서 그대로 적용해봤을 뿐이고, 그 판단 과정 자체와 남아있는 불확실성을 기록으로 남기고 싶었습니다. GitHub Pages로 여러 프로젝트를 혼자 운영하는 다른 개발자분들도 분명 같은 갈림길 앞에 서 계실 것 같아서요.

## 상황: 레포는 많고, 도메인은 하나

저는 `github.com/saramjh` 계정 하나로 이 블로그(`saramjh.github.io`)와 함께, 그때그때 필요해서 만든 작은 도구들을 GitHub Pages 프로젝트 페이지로 배포해왔습니다. 예를 들면:

- [scratchLottery](https://saramjh.github.io/scratchLottery) — 복권 시뮬레이터
- [richChecker](https://saramjh.github.io/richChecker/) / [richChecker-us](https://saramjh.github.io/richChecker-us/) — 자산 등급 체커
- [SquircleSimulator](https://saramjh.github.io/SquircleSimulator) — 스퀴클 도형 시뮬레이터
- [pomodorotimerKR](https://saramjh.github.io/pomodorotimerKR/) / [pomodorotimerEN](https://saramjh.github.io/pomodorotimerEN/) — 뽀모도로 타이머
- [resizeIMG](https://saramjh.github.io/resizeIMG) — 이미지 리사이저
- [space_atlas_student](https://saramjh.github.io/space_atlas_student/) — 3D 천문 학습 도구

각각은 별도의 레포지토리이고, 서로 코드를 공유하지 않고, 만든 목적도 다 다릅니다. 그런데 커스텀 도메인을 하나도 연결하지 않았기 때문에, GitHub Pages의 기본 규칙에 따라 이 도구들은 전부 `saramjh.github.io/<레포이름>/` 형태로 **이미 하나의 루트 도메인 아래** 놓여 있었습니다. 이건 제가 설계한 구조가 아니라, 커스텀 도메인을 안 붙였을 뿐인데 자동으로 그렇게 된 것입니다.

이 사실을 뒤늦게 자각하고 나서야, 지금까지 도구를 하나 만들 때마다 별생각 없이 반복해왔던 세팅들이 눈에 밟히기 시작했습니다.

## 구체적으로 부딪힌 세 가지 갈림길

### 1. GA4 — 속성을 프로젝트마다 새로 만들 것인가

새 도구를 배포할 때마다 저는 습관적으로 GA4에서 새 속성을 만들고 새 측정 ID를 발급받아 붙였습니다. 도구가 10개 가까이 늘어나자 GA4 계정의 속성 목록도 그만큼 길어졌고, "이 블로그 글이 실제로 저 도구의 사용으로 얼마나 이어졌는가" 같은 걸 보려면 속성을 오가며 탭을 여러 개 띄워야 했습니다. 예를 들어 최근 [Space Atlas 블로그 글](/space-atlas-student/)에서 도구로 유입된 흐름을 보려면, 블로그 속성과 도구 속성을 따로 열어 시간대를 맞춰가며 비교해야 했죠.

### 2. Search Console — 프로젝트마다 따로 등록해야 하는가

Search Console도 마찬가지로 새 도구를 만들 때마다 사이트맵을 등록해왔습니다. (`robots.txt`에 `space_atlas_student` 사이트맵을 추가한 커밋도 그 흔적입니다.) 그런데 애초에 전부 같은 루트 도메인이라면, 이걸 프로젝트 단위로 쪼개서 관리하는 게 맞는 접근인지 의문이 들었습니다.

### 3. Microsoft Clarity — 도구마다 새 프로젝트를 만들 것인가, 하나로 묶을 것인가

세션 리플레이/히트맵을 보려고 설치한 Microsoft Clarity도 같은 문제였습니다. 블로그에는 이미 하나의 Clarity 프로젝트가 설치돼 있는데, 새 도구를 만들 때마다 그 도구만을 위한 새 Clarity 프로젝트를 또 만들어야 하는지, 아니면 같은 루트 도메인이니 기존 프로젝트를 그대로 재사용해도 되는지가 명확하지 않았습니다.

## 왜 이게 애매한 문제인가

GA4나 SEO 관련 글들을 찾아보면 대개 두 가지 전제 중 하나를 깔고 설명합니다.

- "하나의 큰 서비스가 여러 섹션으로 나뉜 경우" (예: 쇼핑몰의 상품/블로그/고객센터)
- "완전히 별개의 사업체가 완전히 별개의 도메인을 쓰는 경우"

제 상황은 그 중간이었습니다. **한 사람이, 하나의 루트 도메인 아래, 서로 사용자층도 목적도 다른 자잘한 도구들을 계속 늘려가는 경우**에 대한 가이드는 잘 보이지 않았습니다. 이 애매함이 이 시리즈를 쓰게 된 이유입니다.

다음 편에서는 이 고민을 AI와 상의하면서 들었던 논리 — GA4의 속성/데이터 스트림 구조, Search Console의 도메인 단위 검증, 루트 도메인이 공유하는 신뢰 신호에 대한 논의 — 를 정리해보겠습니다.

→ [2편: 근거 탐색으로 이어집니다](/gh-pages-analytics-notes-2-reasoning-kr/)

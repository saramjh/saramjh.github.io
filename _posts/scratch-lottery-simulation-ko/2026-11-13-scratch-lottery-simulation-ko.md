---
title: "스크래치 복권 시뮬레이터로 연속 실패와 확률을 직접 확인하기"
description: "현금 결제 없는 스크래치 시뮬레이터의 확률 계산과 독립 시행을 설명하고, 2026년 10월 15일~11월 12일 GA4에서 관찰된 실제 조작 이벤트의 범위를 정리합니다."
date: 2026-11-13
modified: 2026-11-14
tags: ["확률", "독립 시행", "스크래치 복권", "시뮬레이션", "웹 개발", "개발 기록", "Google Analytics"]
permalink: /scratch-lottery-simulation-ko/
layout: default
lang: ko
alternate_lang: en
alternate_url: /scratch-lottery-simulation/
image: /scratch-lottery-simulation-ko/independent-draws-og.png
image_width: 1200
image_height: 630
published: true
seo:
  title: "스크래치 복권 시뮬레이터: 독립 시행 실험과 실제 조작 기록"
  description: "복권을 사지 않고 연속 실패와 다음 시도의 확률을 실험하는 방법. ScratchLottery의 실제 구현과 GA4 조작 이벤트를 구분해 설명합니다."
---

> English: [Scratch Lottery Simulation: odds, repeated trials and measured interactions](/scratch-lottery-simulation/)

# 연속으로 실패하면 다음에는 더 잘 맞을까?

다섯 번 연속 꽝이 나오면 여섯 번째에는 당첨될 것 같은 기분이 든다. 하지만 매번 독립적으로 추첨한다면 이전 결과는 다음 시도의 확률을 바꾸지 않는다. 이 차이를 직접 시험하도록 만든 것이 내가 개발한 [ScratchLottery](https://saramjh.github.io/scratchLottery/)다. 실제 복권을 구매하거나 현금을 걸지 않는 무료 시뮬레이터다.

이 웹앱에서는 한 장을 긁어 결과를 확인할 수도 있고, 빠른 시뮬레이션으로 여러 장의 결과를 한꺼번에 비교할 수도 있다. 코드는 매번 난수를 뽑아 누적확률표(CDF)의 한 구간에 배정한 뒤, 그 구간에 해당하는 결과 하나를 선택한다. 공식 전체 발행표가 확인된 프리셋은 발행 매수와 등수별 당첨 매수로 각 구간의 확률을 계산한다. `Custom Odds`처럼 전체 공식 배당표가 없는 프리셋은 실제 판매 복권의 하위 등수 분포가 아닌 **시뮬레이션 모델**로 따로 표시한다.

## 이전 결과와 다음 시도를 분리하기

<figure>
  <picture>
    <source media="(max-width: 560px)" srcset="/scratch-lottery-simulation-ko/independent-draws-mobile.svg" width="390" height="780">
    <img src="/scratch-lottery-simulation-ko/independent-draws.svg" alt="이전에 다섯 번 실패한 결과와 오른쪽의 다음 독립 추첨이 분리되어 있으며, 다음 시도는 같은 확률표를 다시 사용하는 원리를 설명한 자체 제작 도식" width="1200" height="630" loading="lazy" style="display:block;width:100%;height:auto">
  </picture>
  <figcaption>독립 시행을 설명하기 위해 직접 그린 도식이다. 특정 날짜의 실제 복권 결과나 제품 화면 캡처는 아니다.</figcaption>
</figure>

[확률 학습 화면의 연속 실패 실험](https://saramjh.github.io/scratchLottery/math/#independenceLesson)에서는 이전 실패 횟수를 0회, 5회, 10회로 바꿔 볼 수 있다. [Texas Lottery Game 2755의 공개 배당 자료](https://www.texaslottery.com/export/sites/lottery/Games/Scratch_Offs/details.html_252698616.html)를 토대로 구성한 독립 추첨 예시에서 다음 한 장이 어떤 등수든 당첨될 확률은 세 경우 모두 26.52%다. 이전에 다섯 번 실패하는 사건 자체의 확률은 별개다.

실제 매장에 어떤 복권이 남아 있는지는 이 학습 모델로 알 수 없다. 위의 수치는 공개 분포를 사용하는 교육용 모델의 확률이며, 오늘 매장에서 살 수 있는 티켓의 당첨 가능성을 예측하는 값이 아니다.

## 어떤 동작을 만들어 측정했나

스크래치 화면에서는 티켓의 모든 칸을 열어야 한 번의 시도가 완료된다. 그때 코드가 `scratch_completed` 이벤트를 기록한다. 여러 장을 한꺼번에 실행하는 기능은 별도의 `run_fast_simulation` 이벤트를 사용한다. 따라서 같은 방문자가 두 기능을 각각 여러 번 사용해도 두 종류의 동작을 구별할 수 있다.

2026년 11월 13일, 내가 관리하는 Google Analytics 4 속성에서 **10월 15일~11월 12일** 기간을 읽기 전용으로 조회했다.

- 스크래치 한 장 완료 (`scratch_completed`): 기록된 이벤트 **4,773회**, 해당 이벤트의 GA4 활성 사용자 **89명**.
- 여러 장 빠른 실행 (`run_fast_simulation`): 기록된 이벤트 **2,576회**, 해당 이벤트의 GA4 활성 사용자 **21명**.

이 수치는 조작이 **기록된 횟수**다. 4,773명이 방문했다거나 4,773장의 복권이 팔렸다는 뜻이 아니다. 두 이벤트의 활성 사용자 집합은 겹칠 수 있으므로 89와 21을 더해 사람 수를 계산할 수도 없다. 자동화된 접속이 섞였는지 전부 검증한 데이터도 아니며, 이 기록만으로 홍보 효과나 실제 이용자의 만족도를 판단할 수 없다.

## 직접 비교해 보기

현재 [ScratchLottery 확률 설명 페이지](https://saramjh.github.io/scratchLottery/math/)에서는 기대값·RTP·독립 시행을 시각적으로 비교할 수 있다. 본 화면의 Experiment Lab에서는 여러 장의 정확한 확률과 예산별 반복 실험을 연결하고, My Lab에 실험 조건을 이 기기 안에 저장할 수 있다. Official Prize Tracker는 텍사스 복권 운영사가 공개한 발행 당첨권·청구 당첨권 정보를 제한적으로 보여준다. 청구되지 않은 당첨권 수가 남은 실물 티켓의 당첨확률을 뜻하지는 않는다.

[ScratchLottery의 한 장 긁기와 빠른 시뮬레이션](https://saramjh.github.io/scratchLottery/)을 차례로 사용해 보면, 적은 시행 횟수에서 보이는 결과와 많은 시행을 반복했을 때의 비율을 비교할 수 있다. 실험이 끝난 뒤에는 [독립 시행 설명](https://saramjh.github.io/scratchLottery/math/#independenceLesson)에서 이전 실패가 왜 다음 난수 추첨을 보상하지 않는지 확인할 수 있다.

웹앱은 HTML, CSS, JavaScript로 구성했다. [공개 소스 코드](https://github.com/saramjh/scratchLottery)의 `js/script.js`에는 결과 추첨과 완료 조건이, `js/analytics.js`에는 이벤트 측정 호출이 들어 있다. 이 도구의 게임 형식과 화면 구성은 [영문 원문 소개 글](/scratch-lottery-simulation/)에서도 살펴볼 수 있다.

*이 서비스에서는 실제 복권을 판매하지 않고 돈을 받지 않는다. 시뮬레이션 결과는 실제 구매 결과를 보장하지 않는다.*

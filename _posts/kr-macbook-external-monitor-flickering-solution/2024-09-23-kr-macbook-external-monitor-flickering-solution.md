---
title: "맥북 에어 / 맥북 프로 / 맥북 트럭탑 외장 모니터 깜빡임 문제 해결"
date: 2024-09-23
tags: 맥북에어, 맥북m1, 맥북m2, 화면깜빡임, 외부모니터깜빡임, 플리커링, HDMI연결불량, 외부모니터깜빡임해결
permalink: /kr-macbook-external-monitor-flickering-solution/
layout: compress
comments: true
---

### 맥북 에어 / 맥북 프로 / 맥북 트럭탑 외장 모니터 깜빡임 문제 해결

유니바디(배터리 일체형) 맥북 에어와 맥북 프로는 배터리가 상시 본체에 꽂아 있어 전류 공급 문제가 있을 수 있습니다. 이로 인해 일부 모델에서는 화면 지직 거림, 깜빡임 증상이 일어날 수 있습니다.

### 해결 방법

<img src="{{site.assets}}{{ page.permalink }}28d26ef777b3e7.webp" alt="MacBook External Monitor Flickering Fix">
해외 사이트의 트러블 슈팅을 참고하여 다음과 같은 방법을 시도해 보세요.

- **정식 어댑터와 케이블 사용:** MacBook 에어 또는 MacBook 프로의 정식 어댑터와 정식 케이블을 사용하여 전원을 연결해 주세요.
- **전원 끄기:** 전원을 끕니다.
- **키 누름:** 사진 속의 빨간 사각형을 친 키 4개(왼쪽에 위치한 `shift` + `control` + `option` + `power`)를 동시에 약 10초간 누릅니다. (터치 바 모델의 전원 버튼은 지문 인식하는 버튼입니다.)
- **키에서 손을 뗀 후 전원 켜기:** 10초 후 4개의 키에서 손을 뗍니다. 그리고 전원을 켭니다.

### 데스크탑 컴퓨터의 경우

Mac이 노트북 컴퓨터가 아닌 경우 다음 단계를 따릅니다.

<img src="{{site.assets}}{{ page.permalink }}2e82528b602df.webp" alt="Mac External Monitor Flickering Fix">
- **Mac 시스템 종료:** Mac 시스템을 종료하고 전원 코드를 뽑습니다.
- **15초 후 전원 코드 다시 꽂기:** 15초 후 전원 코드를 다시 꽂습니다.
- **5초 기다리기:** 5초 동안 기다렸다가 전원 버튼을 눌러 Mac을 켭니다.

### 만약 위 방법으로도 해결이 안되는 경우

맥 os의 NVRAM 혹은 PRAM 초기화
맥os의 여러가지 설정값들이 저장되는 메모리 공간으로 이는 외부 모니터 연결정보도 포함되어 기존과 동일한 모니터로 인식이 될때 기존 정보를 불러와 연결을 돕습니다.
이때 기존정보와 충돌이 발생하여 모니터에 신호를 제대로 전달하지 못할때가 있습니다.

<img src="{{site.assets}}{{ page.permalink }}howtoreset.png" alt="MacBook External Monitor Flickering Fix">

### 리셋 방법

1. 컴퓨터 전원을 종료합니다.
2. 전원 켠뒤 곧바로 `option` + `command` + `P` + `R` 키를 누르고 있는다.
3. 시작 사운드(딩~) 가 나거나, 로고가 나타났다가 사라지고나서 몇초후까지 누르고 있는다.
4. 끝

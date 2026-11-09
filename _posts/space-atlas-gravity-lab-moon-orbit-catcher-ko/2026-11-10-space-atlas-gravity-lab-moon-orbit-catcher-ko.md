---
title: "같은 점프, 다른 중력: Space Atlas의 Gravity Lab과 Moon Orbit Catcher"
description: "Space Atlas의 Gravity Lab은 초기 속도를 3.0 m/s로 고정해 세계별 중력을 비교한다. Flight Trials의 부스터와 Moon Orbit Catcher의 위상 게임을 과학 모델의 한계와 함께 살펴본다."
date: 2026-11-10
tags: ["Space Atlas", "우주과학", "물리 시뮬레이션", "인터랙티브 학습", "STEM 교육"]
permalink: /space-atlas-gravity-lab-moon-orbit-catcher-ko/
layout: default
lang: ko
alternate_lang: en
alternate_url: /space-atlas-gravity-lab-moon-orbit-catcher-en/
image: /space-atlas-student/space-atlas-hero.png
image_width: 1280
image_height: 820
published: true
seo:
  title: "Space Atlas Gravity Lab과 Moon Orbit Catcher"
  description: "같은 3.0 m/s 점프를 세계별 중력에서 비교하고, 별도 부스터 게임과 달 위상 챌린지를 과학적 한계까지 포함해 설명한다."
---

> English version: [Same jump, different gravity: Space Atlas Gravity Lab and Moon Orbit Catcher](/space-atlas-gravity-lab-moon-orbit-catcher-en/)

Gravity Lab은 3.0 m/s로 출발하는 점프를 세계별 중력에서 비교한다. Flight Trials는 가상의 추진기와 체크포인트를 더한 게임 모드다. Moon Orbit Catcher에서는 달의 위상을 예측한 뒤 궤도에서 목표를 맞힌다.

<figure>
<img src="/space-atlas-student/space-atlas-hero.png" alt="Space Atlas의 3D 태양계 개요 화면. Gravity Lab과 Moon Orbit Catcher는 이후 추가된 별도 학습 모듈이다." width="1280" height="820" loading="lazy" style="width:100%;height:auto;">
<figcaption>2026년 9월 Space Atlas 소개에 사용한 프로젝트 개요 이미지. Gravity Lab과 Moon Orbit Catcher는 아래 링크에서 열 수 있다.</figcaption>
</figure>

## 같은 속도로 출발하는 점프

Gravity Lab은 기준 질량 70 kg과 초기 속도 3.0 m/s를 사용한다. 세계를 바꿔도 출발 속도는 같다. 중력 가속도가 달라지면서 점프의 최고 높이와 체공 시간도 달라진다.

수직 방향의 이상적인 운동에서 공기 저항을 제외하면 최고 높이는 `h = v₀² / (2g)`로 계산된다. 각 세계의 무보조 점프 예측값은 다음과 같다.

| 세계 또는 기준 | 중력 가속도 | 무보조 점프 높이 |
| --- | ---: | ---: |
| 지구 | 9.8 m/s² | 0.46 m |
| 달 | 1.6 m/s² | 2.81 m |
| 화성 | 3.7 m/s² | 1.22 m |
| 목성 기준 고도 | 23.1 m/s² | 0.19 m |

중력값은 NASA NSSDC의 반올림 수치를 사용한다. 70 kg은 무게, 즉 중력에 의한 힘을 계산할 때 쓰는 기준 질량이다. 최고 높이 식에는 질량이 들어가지 않는다. 이 계산은 공기 저항과 고도에 따른 중력 변화를 무시한다. 목성에는 걸을 수 있는 고체 표면이 없으므로 목성 환경은 인공 시험 데크로 표현한다.

- [Gravity Lab 열기](https://spaceatlasedu.org/solar-system/gravity-lab/)
- [NASA Planetary Fact Sheet](https://nssdc.gsfc.nasa.gov/planetary/factsheet/)

## Flight Trials의 추진기와 코스

Flight Trials는 Gravity Lab의 점프에 가상 추진기를 추가한다. 추진력은 `질량 × (현지 중력 + 5.5 m/s²)`로 설정된다. 추진기는 최대 1초 동안 작동하고, 착지하면 약 2.5초에 걸쳐 에너지가 다시 채워진다. 단계를 통과할수록 코스가 길어지고 체크포인트 수도 3개에서 10개까지 늘어난다.

무보조 점프 수치는 중력 비교에 사용한다. Flight Trials에서 부스터로 만든 궤적은 추가 추진력이 만든 게임 결과다. 행성에서 사람이 실제로 점프할 수 있는 높이를 나타내지는 않는다.

## 달의 위상을 예측하고 궤도에서 맞히기

Moon Phases는 상현달에서 보이는 달 원반의 밝기를 먼저 예측하고, 그 답을 과학 모델과 비교하게 한다. 상현달에서 지구로 보이는 달 원반은 약 50%가 밝다. '상현'은 약 29.5일 삭망 주기의 4분의 1 지점을 가리킨다. 달 원반의 25%가 밝다는 뜻은 아니다.

Moon Orbit Catcher는 세 단계로 진행한다. 첫 단계에서는 빛나는 목표를 따라간다. 두 번째 단계에서는 포착 구간이 좁아지고, 마지막 단계에서는 목표 표시 없이 위상을 찾아야 한다. 속도 조절 버튼과 수동 각도 설정을 제공하며, 키보드 조작과 움직임 줄이기도 지원한다.

게임 속 공전은 놀이를 위해 가속돼 있다. 모델은 고정된 태양과 원형 궤도를 사용한다. 한 바퀴를 29.5일 삭망월로 표현하며, 실제 달의 항성 공전 주기는 약 27.3일이다. 달 궤도의 기울기와 일식, 월식은 계산하지 않는다. 실시간 하늘 예보도 제공하지 않는다.

게임을 실행하려면 JavaScript가 필요하다. 위상 표와 과학 설명은 스크립트 없이도 읽을 수 있다. 인쇄용 교사용 안내서와 학생 워크시트도 제공한다.

- [Moon Phases와 Moon Orbit Catcher 열기](https://spaceatlasedu.org/moon/phases/)
- [NASA Moon Phases](https://science.nasa.gov/moon/moon-phases/)

## NCASE 공개 목록 등재

Space Atlas 업데이트 기록은 2026년 11월 4일 NCASE(National Coalition for Aviation and Space Education)의 공개 Programs 목록에서 Space Atlas 항목을 확인했다고 기록한다. 최초 등재일은 확인되지 않았다. 이 기록이 보여주는 것은 공개 디렉터리에 항목이 있다는 사실이다. 인증, 공식 보증, NASA 제휴 또는 교실 효과 평가를 의미하지 않는다.

NCASE 목록에 있던 이전 GitHub Pages 주소는 현재 Space Atlas 도메인으로 리디렉션된다. 업데이트 기록에는 링크 수정 요청을 보냈다고 적혀 있으나, 게시자가 변경을 확인하지는 않았다.

Space Atlas 사이트는 Grades 4 to 8 학생 참조 자료로 소개된다. Moon Phases에는 Grades 3 to 5 대상 30 to 35분 활동도 제안돼 있다. 이 활동은 교실에서 시험한 수업이 아니며, 측정된 학생 성과도 없다.

공개 학습 페이지는 Google Analytics 4를 사용하며 Google AdSense 광고를 표시할 수 있다. 연령 관련 데이터 처리를 검토하는 동안 13세 미만 아동의 비감독 단독 사용은 권장하지 않는다. 교사와 보호자는 학교와 가정의 개인정보 정책을 확인해야 한다.

[Space Atlas 업데이트 기록](https://spaceatlasedu.org/updates/)에서 공개 기능의 날짜와 관련 변경 기록을 확인할 수 있다. 기존 [Space Atlas 개요 글](/space-atlas-student/)에는 초기 천문학 참조 도구의 구성이 정리돼 있다.

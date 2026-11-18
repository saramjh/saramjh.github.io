---
title: "레시피 재료 비율 계산기: 가진 재료 양으로 전체 분량 조절하기"
description: "밀가루가 100g 필요한 레시피에 150g을 쓰고 싶다면? 재료 비율 계산기의 입력 방법과 계산 예시, 단위 변환 및 분수 입력의 주의점을 정리했습니다."
date: 2026-11-19
tags: ["레시피", "재료 계산기", "레시피 비율", "요리 분량 조절"]
permalink: /ko-recipe-scaling-application/
layout: default
lang: ko
alternate_lang: en
alternate_url: /recipe-scaling-application/
image: /recipe-scaling-application/recipescalingapplication.jpg
seo:
  title: "레시피 비율 계산기: 재료 양 조절 예시와 사용법"
  description: "기준 재료를 100g에서 150g으로 바꾸면 나머지 재료는 얼마일까요? 무료 레시피 비율 계산기의 입력과 결과, 주의점을 살펴봅니다."
---

# 재료가 남거나 부족할 때 쓰는 레시피 비율 계산기

<p style="background: rgba(0, 120, 212, 0.08); border-left: 4px solid #0078d4; padding: 10px 14px; margin-bottom: 22px; border-radius: 4px; font-size: 0.95rem;">
  <strong>English version:</strong> <a href="/recipe-scaling-application/">Recipe Scaling Calculator</a>
</p>

레시피에는 밀가루 100g이라고 적혀 있는데, 손에 있는 재료를 기준으로 150g만큼 만들고 싶을 때가 있습니다. 다른 재료까지 일일이 비율을 계산하지 않으려고 만든 것이 [레시피 재료 비율 계산기](https://saramjh.github.io/recipeCalc/)입니다.

먼저 레시피의 재료와 분량을 입력하고, 기준으로 삼을 재료 하나를 고릅니다. 그 재료의 사용 가능한 양을 넣으면 나머지 재료에도 같은 배율이 적용됩니다. 기존 레시피의 분량을 늘리거나 줄일 때 사용할 수 있습니다.

<img src="/recipe-scaling-application/recipescalingapplication.jpg" alt="원본 레시피 재료 비율 계산기 화면. 재료 입력과 계산 영역이 보입니다.">

## 계산 예시: 밀가루 100g을 150g으로 바꾸기

기존 레시피에 **100g flour(밀가루)**, **200ml water(물)**, **20g sugar(설탕)**가 있다고 가정하겠습니다. 밀가루 150g을 기준으로 조정하려면 *Add Multiple Ingredients*에 다음 내용을 한 줄씩 붙여 넣습니다.

```text
100g flour
200ml water
20g sugar
```

**Add**를 누른 뒤 *Available Ingredients*에서 **Flour**를 선택하고, 사용할 양에 **150**을 입력합니다. 계산 배율은 `150 / 100 = 1.5`입니다.

| 재료 | 원래 분량 | 조정한 분량 |
|---|---:|---:|
| 밀가루 | 100g | 150g |
| 물 | 200ml | 300ml |
| 설탕 | 20g | 30g |

계산식은 `조정 분량 = 원래 분량 × (기준 재료의 사용 가능한 양 / 기준 재료의 원래 분량)`입니다. 다른 재료에도 같은 배율을 적용하므로 레시피에 적힌 비율을 유지할 수 있습니다.

## 입력과 수정 방법

재료는 하나씩 입력해도 되고 여러 줄을 한꺼번에 붙여 넣어도 됩니다. 입력한 재료는 **Edit**로 수정하고 **Delete**로 삭제할 수 있습니다. **Reset**은 화면을 다시 불러와 다른 레시피로 시작합니다.

- [레시피 재료 비율 계산기 열기](https://saramjh.github.io/recipeCalc/)
- [GitHub에서 원본 코드 확인하기](https://github.com/saramjh/recipeCalc)

## 사용 전에 알아둘 제한

이 도구는 입력된 단위를 그대로 유지합니다. g을 컵으로 바꾸는 등의 **자동 단위 변환**은 하지 않으며, 영양 성분이나 완성되는 음식의 양도 예측하지 않습니다. 계산 결과를 확인할 때는 각 재료의 단위도 함께 살펴보는 것이 좋습니다.

여러 재료를 붙여 넣는 입력 방식에서는 맨 앞의 숫자를 읽습니다. `1/2tbsp`처럼 분수를 문자로 적으면 반 큰술로 정확하게 해석되지 않을 수 있으니, `0.5tbsp`처럼 소수로 입력하세요. 재료에 따라 실제 조리 결과가 달라질 수 있으므로 계산값을 그대로 믿기보다 원래 레시피의 조건을 확인해야 합니다.

이 계산기는 HTML, CSS, JavaScript로 만든 기존 웹 도구입니다. 배율 계산과 입력 처리 방식은 [공개된 원본 구현](https://github.com/saramjh/recipeCalc/blob/main/js/script.js)에서 확인할 수 있습니다. 이 글은 현재 도구를 사용하는 방법을 정리한 것이며, 별도 기능 출시를 알리는 글은 아닙니다.

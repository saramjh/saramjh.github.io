---
title: "ChatGPT 메시지 제한은 무제한? Codex Plus 사용량 한도는 별도다 (2026)"
date: 2026-10-05
tags: ["ChatGPT", "ChatGPT 무제한", "ChatGPT 텍스트 채팅", "Codex", "Codex 사용량", "Codex 한도", "AI 코딩", "MCP"]
permalink: /chatgpt-unlimited-text-vs-codex-limits/
layout: default
lang: ko
alternate_lang: en
alternate_url: /en-chatgpt-unlimited-text-vs-codex-limits/
description: "2026년 10월 기준 ChatGPT의 일반 텍스트 채팅과 Codex 사용량은 같은 한도가 아닙니다. Plus Codex 모델별 예상 사용량, 로컬·클라우드 공유 한도, 주간 제한과 확인 방법까지 공식 자료 기준으로 정리합니다."
excerpt: "ChatGPT 일반 텍스트 채팅은 무제한*이지만 Codex는 별도 사용량 한도를 씁니다. Plus 기준 모델별 예상 사용량과 실제 한도 확인 방법을 공식 자료 기준으로 정리합니다."
seo:
  title: "ChatGPT 메시지 제한 vs Codex 사용량 한도 (Plus 기준, 2026)"
  description: "ChatGPT 일반 텍스트 채팅은 무제한*이지만 Codex Plus는 모델별 별도 사용량 한도가 있습니다. 2026년 공식 예상 범위, 주간 한도, /status 확인법까지 정리."
  keywords:
    - ChatGPT 무제한
    - ChatGPT 텍스트 채팅 무제한
    - ChatGPT Plus Codex 사용량
    - ChatGPT Plus Codex 한도
    - ChatGPT 메시지 제한
    - Codex 사용량
    - Codex 사용 한도
    - Codex 크레딧
    - ChatGPT Codex 차이
faq:
  - q: "ChatGPT 일반 텍스트 채팅은 정말 무제한인가요?"
    a: "2026년 10월 5일 현재 ChatGPT 가격표는 Free의 일상적인 텍스트 대화를 무제한으로 표시하고, Go는 Free 기능을, Plus는 Go 기능을, Pro는 Plus 기능을 포함합니다. 다만 악용 방지 가드레일이 적용되고 파일, 이미지, 음성, 고급 추론 모델과 도구에는 별도 한도가 있을 수 있습니다."
  - q: "ChatGPT Plus에서 Codex는 몇 번 사용할 수 있나요?"
    a: "고정 횟수나 월간 총량이 아닙니다. 2026년 10월 5일 현재 Codex 가격 페이지는 모델별 Plus 예상 범위를 공개하며, 별도 OpenAI 사용량 문서는 현재 GPT-6 계열 범위를 5시간 윈도우 안의 로컬 메시지 추정치로 설명합니다. 실제 소비량은 모델과 작업 복잡도에 따라 달라지고 주간 한도도 적용될 수 있습니다."
  - q: "Codex 로컬 메시지와 클라우드 작업은 한도를 따로 쓰나요?"
    a: "아닙니다. OpenAI는 로컬 메시지와 클라우드 채팅이 플랜의 사용량을 공유한다고 설명하며 주간 한도가 적용될 수도 있다고 명시합니다."
  - q: "ChatGPT가 무제한이면 Codex도 무제한인가요?"
    a: "아닙니다. Codex는 별도 사용량 한도와 크레딧 구조를 사용합니다. 현재 잔여량과 리셋 시점은 Codex 사용량 대시보드나 CLI의 /status에서 확인하는 것이 가장 정확합니다."
  - q: "무제한 텍스트 채팅이면 한 스레드의 컨텍스트도 무한한가요?"
    a: "아닙니다. 메시지 사용량과 컨텍스트 길이는 다른 개념입니다. 무제한 채팅은 한 대화가 무한한 기억을 가진다는 뜻이 아닙니다."
image: /chatgpt-unlimited-text-vs-codex-limits/chatgpt-vs-codex-og.png
image_width: 1200
image_height: 630
---

# ChatGPT 메시지 제한은 무제한? Codex Plus 사용량 한도는 별도다

**2026년 10월 5일 기준 결론부터 말하면, 일반 ChatGPT 텍스트 채팅과 Codex는 같은 사용량 풀로 계산하지 않습니다. Codex는 모델별 별도 사용량 한도가 있고 로컬 메시지와 클라우드 채팅이 그 한도를 공유합니다.**

<p style="background: rgba(0, 120, 212, 0.08); border-left: 4px solid #0078d4; padding: 10px 14px; margin-bottom: 22px; border-radius: 4px; font-size: 0.95rem;">
  🌐 <strong>English version:</strong> <a href="/en-chatgpt-unlimited-text-vs-codex-limits/">ChatGPT Message Limits vs Codex Usage Limits</a>
</p>

검색 의도부터 바로 답하면 이렇습니다.

| 궁금한 것 | 2026년 10월 5일 기준 답 |
|---|---|
| ChatGPT 일반 텍스트 채팅 | **무제한***. 가격표에서 Free는 무제한으로 표시되고 Go는 Free 기능을, Plus는 Go 기능을, Pro는 Plus 기능을 포함합니다. |
| ChatGPT Plus의 Codex | **무제한 아님.** 모델별 예상 사용량 범위가 따로 공개됩니다. |
| Codex 로컬 메시지와 클라우드 채팅 | **같은 플랜 사용량을 공유**합니다. |
| 주간 한도 | **적용될 수 있음.** 현재 잔여량과 리셋 시점은 계정의 사용량 화면이 최종 기준입니다. |
| Codex 한도 확인 | Codex 사용량 대시보드 또는 CLI의 **`/status`** |

따라서 `ChatGPT 메시지 제한`, `ChatGPT Plus Codex 한도`, `Codex 사용량`을 같은 숫자로 찾으면 답이 꼬입니다. **브라우저에서 `chatgpt.com`을 열어 쓰는 일반 텍스트 채팅의 한도와, Codex 코딩 에이전트의 한도는 별도로 봐야 합니다.**

이 차이를 확인한 계기는 [웹 ChatGPT를 MCP로 제 Mac에 연결해서 쓰는 방식](/chatgpt-mcp-local-development-setup/)을 정리하면서였습니다.

<picture>
  <source media="(max-width: 600px)" srcset="chat-vs-codex-mobile.svg">
  <img src="chat-vs-codex.svg" alt="웹 ChatGPT의 일상 텍스트 채팅 무제한과 Codex 별도 사용량 구조 비교" width="1200" height="660" style="width:100%;height:auto;">
</picture>

## ChatGPT에서 '무제한 텍스트 채팅'이 정확히 무엇인지

OpenAI 가격표에서 말하는 무제한은 **일상적인 텍스트 채팅**입니다.

2026년 10월 현재 개인 플랜 비교표는 다음처럼 표시됩니다.

| 기능 | Free | Go | Plus | Pro |
|---|---|---|---|---|
| 일상적인 텍스트 대화 | 무제한* | 무제한* | 무제한* | 무제한* |
| Codex | 제한적/별도 한도 | 제한적/별도 한도 | 사용 한도 확대 | 최대 사용 한도 |
| 파일·이미지·음성·일부 도구 | 별도 한도 | 별도 한도 | 확대된 한도 | 더 높은 한도 |

별표도 중요합니다. **무제한 텍스트 채팅에는 악용 방지 가드레일이 적용됩니다.**

그리고 이 문장을 다음처럼 확대 해석하면 안 됩니다.

> ChatGPT에서 하는 모든 작업이 무제한이다.

그건 아닙니다.

<picture>
  <source media="(max-width: 600px)" srcset="unlimited-is-not-everything-mobile.svg">
  <img src="unlimited-is-not-everything.svg" alt="무제한 텍스트 채팅과 별도 사용 한도가 적용되는 ChatGPT 기능 구분" width="1200" height="640" style="width:100%;height:auto;">
</picture>

파일 업로드, 이미지 생성, 음성, 데이터 분석, 심층 리서치, 일부 고급 추론 모델과 도구에는 별도 한도가 적용될 수 있습니다. OpenAI 도움말도 Free/Go의 무제한 일상 텍스트 채팅과 도구 한도를 명시적으로 분리합니다.

## ChatGPT Plus에서 Codex 사용량은 실제로 얼마나 되나

Codex 가격 페이지는 아예 **사용 한도 표**를 제공합니다. 2026년 10월 5일 현재 한국어 가격 페이지에서 Plus의 예상 사용량 범위는 다음처럼 공개되어 있습니다.

| Codex 모델 | Plus 예상 사용량 |
|---|---:|
| GPT-6 Astra | 5~45 |
| GPT-6.1 Sol | 15~160 |
| GPT-6 Sol | 15~150 |
| GPT-6 Luna | 350~3,000 |

이 숫자는 **월간 총 메시지 수나 고정 보장 횟수가 아니라, 현재 OpenAI가 공개하는 5시간 윈도우의 로컬 메시지 추정치**입니다. GPT-5.6 계열과 GPT-5.5도 별도 크레딧 요율표에는 남아 있지만, 현재 Plus 로컬 메시지 예상 범위 표에는 포함되지 않습니다. 실제 소비량은 모델, 작업 복잡도, 컨텍스트, 추론 수준, 실행 위치와 도구 사용에 따라 달라지고, **로컬 메시지와 클라우드 채팅은 같은 플랜 사용량을 공유하며 주간 한도도 적용될 수 있습니다.**

따라서 "Plus면 Codex를 몇 번 쓸 수 있나?"의 가장 정확한 답은 **모델마다 다르고, 계정의 사용량 대시보드가 최종값**이라는 것입니다. 활성 Codex CLI에서는 `/status`로 잔여 한도를 확인할 수 있습니다.

한도에 가까워지면 더 저렴한 모델로 바꾸거나, 리셋을 기다리거나, 계정에서 제공되는 경우 크레딧을 사용할 수 있습니다.

즉 구조적으로는 이렇습니다.

```text
웹 ChatGPT
└─ 일상적인 텍스트 채팅: 무제한*
   ├─ 특정 고급 모델/추론: 별도 제한 가능
   ├─ 파일·이미지·음성·도구: 별도 제한 가능
   └─ Codex: 별도의 agentic usage 한도/크레딧
```

Codex를 오래 돌리는 작업과 웹 ChatGPT에서 일반적인 텍스트 대화를 계속하는 것은 **같은 '메시지 하나'처럼 보여도 사용량 체계가 같지 않습니다.**

## 그래서 MCP로 웹 ChatGPT를 로컬 개발에 붙이는 방식이 흥미로웠다

제가 이 차이에 관심을 가진 이유는 단순히 "무제한이라 개이득" 같은 이야기를 하려는 게 아닙니다.

현재 저는 **인터넷 브라우저에서 `chatgpt.com`을 열어 쓰는 일반 ChatGPT 채팅 화면**에 MCP를 연결하고, 그 MCP가 제 Mac의 파일·터미널·Git·테스트를 다루게 하는 구조를 실사용 중입니다.

그러면 대화와 판단의 상당 부분은 일반 ChatGPT 채팅에서 진행하고, 필요한 순간에만 로컬 도구를 호출할 수 있습니다.

이 구조가 Codex의 모든 기능을 대체한다는 뜻은 아닙니다. Codex는 전용 코딩 에이전트로서 훨씬 잘 통합된 작업 흐름과 전용 기능을 제공합니다.

다만 **"코딩을 하려면 반드시 Codex 사용량을 계속 태워야 한다"는 전제는 아닙니다.** 대화형 설계·검토·의사결정·로컬 도구 호출을 웹 ChatGPT 중심으로 구성하는 선택지가 있다는 뜻입니다.

여기서 특히 중요한 주의점이 있습니다.

**OpenAI가 'MCP 도구 호출도 무제한'이라고 보장한 것은 아닙니다.** 공식 가격표의 무제한 항목은 `Everyday text chats`입니다. 따라서 제가 확인할 수 없는 도구별 내부 과금이나 미래 정책까지 무제한이라고 단정하지 않습니다.

## 무제한 메시지와 무한 컨텍스트는 완전히 다른 이야기다

이 부분은 자주 섞입니다.

**무제한 채팅 = 한 스레드가 모든 내용을 영원히 기억한다**는 뜻이 아닙니다.

긴 대화에는 컨텍스트 길이, 압축, 메모리, 세션 경계 등의 문제가 여전히 있습니다. 오히려 저는 웹 ChatGPT를 로컬 개발에 오래 붙여 쓰면서 이 문제가 더 분명하게 보였습니다.

그래서 별도로 [Serena·Ponytail·claude-mem을 설치해 놓고도 세션 컨텍스트가 제대로 이어지지 않았던 문제를 cokacremote 안에서 어떻게 다시 설계했는지](/ai-coding-context-continuity-cokacremote/)도 기록했습니다.

요약하면:

- **사용량 문제:** 몇 번 더 메시지를 보낼 수 있는가?
- **컨텍스트 문제:** 새 세션이 이전 결정과 현재 프로젝트 상태를 정확히 이어받는가?

서로 다른 문제입니다.

## 이 차이를 몰랐던 이유

UI에서는 둘 다 "ChatGPT 계정으로 쓰는 OpenAI 코딩 기능"처럼 보입니다.

Codex도 ChatGPT 플랜에 포함되고, 웹 ChatGPT도 같은 계정을 씁니다. 그래서 구독자가 체감하기에는 하나의 사용량 풀처럼 생각하기 쉽습니다.

하지만 공식 문서는 명확히 분리합니다.

- ChatGPT 가격표: **Everyday text chats = Unlimited***
- Codex 문서: **Usage limits vary by plan**
- Codex 한도 도달 시: 사용량 대시보드 확인, 리셋 대기, 가능한 경우 크레딧 추가

이 차이는 AI 코딩 워크플로우를 설계할 때 생각보다 큽니다.

## 지금 기준으로 제가 이해한 결론

2026년 10월 기준으로는 다음처럼 이해하는 것이 가장 정확합니다.

1. **웹 ChatGPT의 일상적인 텍스트 채팅은 개인용 Free·Go·Plus·Pro에서 무제한*이다.**
2. **무제한은 모든 모델·도구·파일·이미지·추론 기능이 무제한이라는 뜻이 아니다.**
3. **Codex는 별도의 사용량 한도와 크레딧 구조가 있다.**
4. **무제한 메시지는 무한 컨텍스트를 의미하지 않는다.**
5. 따라서 개발 워크플로우에서는 **채팅 사용량, 전용 에이전트 사용량, 컨텍스트 지속성**을 따로 설계하는 편이 낫다.

OpenAI는 가격과 사용 한도를 바꿀 수 있으므로 이 글의 숫자나 정책은 영구 규칙이 아닙니다. 아래 공식 페이지를 현재 기준으로 다시 확인하는 것이 가장 정확합니다.

## 공식 자료

- [ChatGPT 가격 — 개인 플랜 비교](https://chatgpt.com/ko-KR/pricing/)
- [ChatGPT Learn — Work·Codex 가격 및 사용 한도](https://learn.chatgpt.com/docs/pricing)
- [OpenAI 도움말 — ChatGPT 플랜에서 Codex 사용하기](https://help.openai.com/en/articles/11369540-using-codex-with-your-chatgpt-plan)
- [OpenAI 도움말 — ChatGPT란 무엇인가요? 웹은 chatgpt.com](https://help.openai.com/ko-kr/articles/12677804-what-is-chatgpt-faq)
- [OpenAI 릴리스 노트 — 무제한 텍스트 채팅과 Work/Codex 구분](https://help.openai.com/en/articles/6825453-chatgpt-release-notes)

*무제한은 OpenAI의 abuse-prevention guardrails 적용 대상입니다.*

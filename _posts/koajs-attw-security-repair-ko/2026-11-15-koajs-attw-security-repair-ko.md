---
title: "Koa Session: Node 18 지원을 유지하며 패키지 검증 오류를 고친 PR"
description: "Koa Session의 attw 패키지 검사 오류를 재현하고, 취약한 첫 우회 수정을 교정해 Node 18을 유지한 오픈소스 기여. 수정안의 공식 CI와 미병합 상태를 구분했다."
date: 2026-11-15
tags: ["Koa", "Node.js", "Open Source", "Dependency Security"]
permalink: /koajs-attw-security-repair-ko/
layout: default
lang: ko
alternate_lang: en
alternate_url: /koajs-attw-security-repair-en/
published: true
seo:
  title: "Koa Session attw 검사 오류와 안전한 의존성 우회 수정"
  description: "Node 18 호환성을 보존하면서 fflate 보안 문제를 피한 Koa Session PR #240. attw 패키지 오류 재현, CVE 확인, GitHub Actions 13개 통과 결과."
---

> English: [Repairing Koa Session's package checks without dropping Node 18](/koajs-attw-security-repair-en/)

**[Koa Session PR #240](https://github.com/koajs/session/pull/240)에 패키지 검사 오류를 해결하는 수정안을 제출했다.** Node 18을 계속 지원하면서 `attw --pack` 오류를 없애는 작업이었다. 첫 번째 해결책에는 알려진 보안 취약점이 있었고, 병합 전에 이를 발견해 수정했다. 교정된 커밋 `57e88bac2663135c1d8fb5da243d4c6173f84924`은 [GitHub Actions 13개 작업](https://github.com/koajs/session/actions/runs/43637614241)을 모두 통과했다. **2026년 11월 15일 기준 PR은 검토 대기 중이며, 상위 저장소에 병합되지 않았다.**

## 테스트를 통과해도 배포 가능한 패키지는 아닐 수 있다

별도로 작업 중인 [Koa 2·Zod 4 호환성 PR #238](https://github.com/koajs/session/pull/238)의 CI에서 세션 테스트 **122개가 통과**했다. 하지만 이후 `npm run prepublishOnly`이 호출한 `attw --pack`에서 다음 오류가 발생했다.

```text
Cannot read properties of undefined (reading 'filename')
```

애플리케이션의 테스트 통과 여부와 배포 패키지의 타입·내보내기 구조 검사는 다른 문제다. 이런 경우 테스트 코드를 더 작성하기 전에 오류가 발생한 **패키징 도구의 의존성**부터 살펴야 한다. 원본 `master`를 별도 체크아웃해 같은 실패를 재현했으며, PR #238의 Zod 변경과 분리해 원인을 조사했다.

실험 당시 `@arethetypeswrong/cli ^0.17.1`은 CLI **0.17.4**와 `@arethetypeswrong/core 0.17.4`를 설치했고, 하위 라이브러리로 `fflate 0.8.3`을 사용했다. 유사한 오류는 [fflate의 공개 이슈 #258](https://github.com/101arrowz/fflate/issues/258)에도 보고돼 있었다.

## 통과한 첫 우회 수정이 안전하지 않았다

처음에는 `fflate`를 **0.8.2**로 고정했다. 패키지 검사가 다시 통과했고, PR의 CI도 성공했다. 그러나 이 버전은 ZIP64 압축 해제 과정의 서비스 거부 취약점 **CVE-2026-45820**에 영향을 받는다. [공식 보안 권고 GHSA-px8p-9vwx-vf98](https://github.com/advisories/GHSA-px8p-9vwx-vf98)를 확인한 뒤 기존 PR을 Draft로 돌리고 보안 정정 기록을 남겼다.

오류만 사라지게 하는 수정과 **안전하게 제안할 수 있는 수정**은 다르다. 보안 권고에 수정 버전으로 명시된 `fflate 0.7.5`를 새 설치 환경에서 검증해 기존의 취약한 고정값을 교체했다.

```json
"overrides": {
  "@arethetypeswrong/core": {
    "fflate": "0.7.5"
  }
}
```

변경은 `package.json`의 하위 의존성 고정에 한정했다. 세션 구현이나 공개 API, GitHub Actions 워크플로는 바꾸지 않았다. 더 최신인 CLI 0.18.x는 Node 20 이상을 요구하므로, **Node 18.19.0 이상을 지원하는 현재 프로젝트**에 그대로 올리는 방법도 택하지 않았다.

## 무엇을 실제로 검증했나

새로 설치한 의존성 트리에서 `@arethetypeswrong/cli 0.17.4` → `@arethetypeswrong/core 0.17.4` → `fflate 0.7.5`가 선택되는 것을 확인했다. 이후 `attw --pack`이 오류 없이 끝났고, `npm run ci`는 Node **18.19.0·22·26**의 격리된 로컬 실행에서 각각 세션 테스트 **120개**를 통과했다. Node 26에서는 시간에 민감한 쿠키 테스트가 한 차례 실패한 뒤 재실행에서 통과했으므로, 모든 실행이 일관되게 성공했다고 해석하지 않았다.

교정된 PR 커밋을 제출한 뒤에는 [공식 CI 실행 #43637614241](https://github.com/koajs/session/actions/runs/43637614241)이 **설정 작업 1개와 3개 운영체제 × 4개 Node 버전의 테스트 작업 12개**, 총 **13개 모두 성공**했다. 이는 제안한 코드가 지원 환경에서 검사를 통과했다는 근거다. `npm audit`에서도 해당 `fflate`·`@arethetypeswrong` 의존성에 대한 추가 경고는 없었지만, 이것이 전체 의존성의 취약점이 모두 사라졌다는 뜻은 아니다.

## 이 작업에서 중요했던 판단

이번 기여는 테스트를 억지로 녹색으로 만드는 것이 아니라, **오류의 계층을 나누고 보안·호환성·재현성을 함께 확인한 작업**이다. 테스트 통과 이후의 배포 검사 오류를 독립적으로 재현했고, CVE가 있는 해결책은 스스로 철회했으며, 기존 Node 18 사용자를 버리지 않는 최소 수정을 다시 검증했다.

현재 증명된 성과는 [검토 가능한 원본 PR #240](https://github.com/koajs/session/pull/240) 제출과 공식 CI 통과다. 유지관리자의 승인·병합이나 패키지 릴리스는 아직 확인되지 않았다. 관련 작업과 원본 구현은 [개발 포트폴리오](/portfolio/)에서 더 볼 수 있다.

---
title: "Koa Session: fixing package checks without dropping Node 18"
description: "An upstream Koa Session contribution that repaired attw packaging checks, caught a security issue in the first workaround, and kept Node 18 compatibility."
date: 2026-11-15
tags: ["Koa", "Node.js", "Open Source", "Dependency Security"]
permalink: /koajs-attw-security-repair-en/
layout: default
lang: en
alternate_lang: ko
alternate_url: /koajs-attw-security-repair-ko/
published: true
seo:
  title: "Koa Session attw package checks: a security-aware Node 18 fix"
  description: "How I reproduced an attw packaging failure, replaced a vulnerable fflate workaround, preserved Node 18, and verified the proposed patch across 13 CI jobs."
---

> 한국어: [Koa Session 패키지 검증과 Node 18 호환성을 함께 지킨 수정](/koajs-attw-security-repair-ko/)

**I submitted [Koa Session PR #240](https://github.com/koajs/session/pull/240) to repair a failing package check without removing Node 18 support.** My first workaround made the check pass but introduced a known security risk. I caught that before the change was merged and replaced it with a version listed as patched in the relevant advisory. The corrected commit, `57e88bac2663135c1d8fb5da243d4c6173f84924`, passed all **13 jobs** in the [project's GitHub Actions run](https://github.com/koajs/session/actions/runs/43637614241). As of November 15, 2026, the PR is **not merged**; passing CI is not maintainer acceptance.

## Passing tests did not mean the package was ready

In a separate [Koa 2 and Zod 4 compatibility PR #238](https://github.com/koajs/session/pull/238), **122 session tests passed**, but the publish-preparation step still failed. The error appeared when `npm run prepublishOnly` called `attw --pack`:

```text
Cannot read properties of undefined (reading 'filename')
```

Application tests and package checks cover different behavior. When a package check fails after the tests pass, changing application logic may be the wrong response. I reproduced the failure against the unchanged upstream `master` branch in an isolated checkout before investigating its packaging dependencies. That also kept the fix separate from the Zod 4 changes.

At the time of the experiment, `@arethetypeswrong/cli ^0.17.1` installed CLI **0.17.4**, `@arethetypeswrong/core 0.17.4`, and the transitive dependency `fflate 0.8.3`. A related problem had been reported in [fflate issue #258](https://github.com/101arrowz/fflate/issues/258).

## The first green check hid a security problem

Pinning `fflate` to **0.8.2** made `attw --pack` pass, and the initial GitHub Actions run was green. But `fflate 0.8.2` is affected by **CVE-2026-45820**, a ZIP64 decompression denial-of-service issue. The [GHSA-px8p-9vwx-vf98 advisory](https://github.com/advisories/GHSA-px8p-9vwx-vf98) made that trade-off unacceptable.

I moved the existing PR back to Draft, left a public security correction, and tested **`fflate 0.7.5`**, which the advisory also identifies as a patched version. Only then did I replace the unsafe pin:

```json
"overrides": {
  "@arethetypeswrong/core": {
    "fflate": "0.7.5"
  }
}
```

The override is scoped to `@arethetypeswrong/core` in `package.json`. It does not change session behavior, the public API, the CI workflow, or runtime dependencies. Simply upgrading the CLI to 0.18.x was not a drop-in solution: that line requires Node 20 or later, while Koa Session still supports **Node 18.19.0 and newer**.

## Checking more than the one failing command

A fresh dependency install resolved CLI 0.17.4 → core 0.17.4 → **fflate 0.7.5**. The original `attw --pack` failure was gone. The full `npm run ci` flow then passed **120 tests** locally under Node **18.19.0, 22, and 26**. One Node 26 attempt hit an intermittent cookie-related assertion (119/120); a repeat passed (120/120). I kept that failed run in the record rather than claiming every local execution was green.

For the corrected PR commit, [GitHub Actions run #43637614241](https://github.com/koajs/session/actions/runs/43637614241) completed with **13 successful jobs**: one setup job and 12 test combinations covering Windows, macOS, and Ubuntu across four Node versions. That is the stronger, independent confirmation that the proposed fix works on the project's CI matrix. The targeted audit showed no `fflate` or `@arethetypeswrong` finding in that install; it was not a claim that the entire dependency tree had no advisories.

## What this contribution demonstrates

The useful part was not merely getting a green build. It was **separating a packaging-tool failure from application tests, rejecting a vulnerable workaround, and preserving an existing compatibility promise**. The corrected solution is small enough for maintainers to review without unrelated source changes.

The verifiable outcome today is a [submitted upstream PR #240](https://github.com/koajs/session/pull/240) with its official CI passing. It is **not merged**, approved, or released yet. Other source-backed development work is linked from my [portfolio](/portfolio/).

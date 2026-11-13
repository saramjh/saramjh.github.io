---
title: "Spoonie: handling blocked service worker registration"
description: "How Spoonie PR #40 moved PWA registration out of Workbox auto-register, with evidence from the live JavaScript bundle."
date: 2026-11-14
tags: ["Spoonie", "PWA", "Frontend"]
permalink: /spoonie-service-worker-registration-en/
layout: default
lang: en
alternate_lang: ko
alternate_url: /spoonie-service-worker-registration-ko/
published: true
seo:
  title: "Fixing Spoonie's service worker registration failure path"
  description: "A Spoonie PWA change using guarded native registration instead of the earlier Workbox auto-register path."
---

> 한국어: [Spoonie PWA 서비스 워커 등록 실패 처리](/spoonie-service-worker-registration-ko/)

Reading a recipe should not depend on whether the browser can register a service worker. Spoonie's earlier PWA setup had a potential failure path: when registration was blocked, `Workbox-window` could try to use an invalid registration object. [Pull request #40](https://github.com/saramjh/spoonie/pull/40), merged on November 13, 2026, changed that path.

## Two places were handling registration

The `next-pwa` configuration used `register: true` for automatic registration. Spoonie also had a `ServiceWorkerUpdater` component to manage updates. A failure in the automatic path could happen before the updater had a usable registration.

The change sets `register: false`. `ServiceWorkerUpdater` now calls `navigator.serviceWorker.register("/sw.js", { scope: "/" })` directly. It checks browser support and runs registration only in production. If the component has unmounted or registration yields no object, it stops the subsequent work. It also handles a rejected registration Promise locally.

The existing `updatefound` and `controllerchange` handlers still operate after a successful registration. Runtime caching remains configured.

## Evidence from the deployed site

On November 14, 2026, the [Spoonie homepage](https://spoonie.kr/) returned HTTP 200. Its served Next.js `app/layout` bundle contained the native `/sw.js` registration call, a result guard and a `.catch()` handler. The public code follows the approach in the [merged implementation](https://github.com/saramjh/spoonie/commit/bc2349b231dee6af087bb210488e53ec7c087f9b).

The pull request added two source-level regression checks for disabled auto-registration, retained cache settings and the manual updater. These are not end-to-end tests in browsers that block service workers. Changes in crash rates, completed recipe reads and retention have not been measured.

## A useful check for other PWAs

[MDN documents](https://developer.mozilla.org/en-US/docs/Web/API/ServiceWorkerContainer/register) that `register()` returns a Promise and describes failure cases. A normal installation test does not cover a rejected registration.

The earlier [viewer-scoped cache change](/spoonie-viewer-cache-isolation-en/) focused on which account owns likes and saves in memory. This fix concerns the boundary between ordinary page access and optional PWA registration.

[Read PR #40](https://github.com/saramjh/spoonie/pull/40) · [Open Spoonie](https://spoonie.kr/)

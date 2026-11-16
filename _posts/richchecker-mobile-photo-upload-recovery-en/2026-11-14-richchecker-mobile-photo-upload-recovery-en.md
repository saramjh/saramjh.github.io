---
title: "Richchecker KR and US: Android photo upload recovery"
description: "Both Richchecker editions now recover HEIC and TIFF photos in the browser and cancel stale processing. Verification on the affected physical Android device remains open."
date: 2026-11-14
modified: 2026-11-17
last_modified_at: 2026-11-17
tags: ["Richchecker", "Frontend", "Android Chrome", "HEIC", "TIFF", "Debugging"]
permalink: /richchecker-mobile-photo-upload-recovery-en/
layout: default
lang: en
alternate_lang: ko
alternate_url: /richchecker-mobile-photo-upload-recovery-ko/
published: true
seo:
  title: "Richchecker KR and US Android photo upload recovery"
  description: "Both Richchecker editions have bounded browser-local HEIC and TIFF recovery, cancellation handling and deployment receipts. Physical-device verification remains open."
---

> 한국어: [Richchecker KR·US Android 사진 업로드 복구](/richchecker-mobile-photo-upload-recovery-ko/)

**I shipped a revised photo upload path in [Richchecker KR](https://saramjh.github.io/richChecker/) on November 13, 2026.** Some Android Chrome visits had recorded an error before photo analysis could start. I removed the full-file Base64 conversion and added checks for unsupported or oversized photos. The implementation is in [PR #1](https://github.com/saramjh/richChecker/pull/1) and [PR #2](https://github.com/saramjh/richChecker/pull/2).

## The failure in the original measurements

I examined the app's November 12 GA4 events by browser and error stage.

| Recorded event | Events | Measured users |
| --- | ---: | ---: |
| Upload started | 14 | 5 |
| Upload error (file_read) | 8 | 3 |
| Analysis completed | 6 | 3 |

All eight file_read errors came from mobile **Android Chrome** in South Korea. That browser segment had nine starts, eight errors and one completed analysis. These are aggregated event counts, however, and cannot be matched to individual upload attempts. Dividing eight by nine would produce an unsupported failure rate. The [investigation notes](https://github.com/saramjh/richChecker/blob/main/docs/ANDROID_UPLOAD_READ_FAILURE_20261113.md) keep the exact scope visible.

## Loading the file without another full-file string

The previous picker used FileReader.readAsDataURL(file) to convert the entire photo into a Base64 string before loading it into an image element. That extra copy can increase memory pressure with large mobile photos.

The new path rejects empty files, obvious non-images, SVG and files over 50 MiB before loading. It uses URL.createObjectURL(file) to create a browser-local Blob URL, waits for the image to decode, and checks the decoded pixel count before sending the image through the existing MediaPipe flow. Images over 50 million pixels are stopped before canvas processing.

The old Blob URL is released with URL.revokeObjectURL() when the user replaces a photo, resets the tool or hits an error. An image load gets a 20-second timeout. When the browser's normal decoder cannot open HEIC, the later recovery path tries a bounded local conversion for supported HEIC/HEIF files. Unsupported, corrupt or oversized files still receive a JPG/PNG retry hint. The selected photo stays in the browser instead of being uploaded to an analysis server.

## Making errors useful without collecting the photo

The updated diagnostic path distinguishes preflight, Blob URL creation and decode failures. It also records limited **format groups and file-size bands**. Analytics does not receive the original image bytes, filename, Blob URL or native error message.

I fixed another edge case in which a failed canvas snapshot could leave the loading state visible. That error now follows the cleanup path and is reported as canvas_snapshot.

Two new parameters, upload_format and upload_size_band, are emitted by the app but are **not yet queryable as GA4 custom dimensions**. Registering them failed with an Analytics Admin OAuth permission error (HTTP 403). Existing error-stage and device dimensions remain the available reporting tools.

## Testing the change and checking the release

The changes passed **20 upload and recovery scenarios in desktop Chrome emulating an Android viewport and user agent**. They covered valid images, damaged or unsupported files, file and pixel limits, Blob URL errors, reselection and canvas failure. A separate check exercised the real MediaPipe face-detection and result-rendering path.

The [GitHub Pages deployment](https://github.com/saramjh/richChecker/actions/runs/43371215024) succeeded. On November 14, the JavaScript served by the [live Richchecker KR page](https://saramjh.github.io/richChecker/) was byte-identical to js/script.js in the repository's main branch.

## What the post-deployment events revealed

On November 14, I queried the app's GA4 data again. Android Chrome activity recorded **after the November 13 deployment** still included errors, now classified as `image_decode`.

| Android Chrome event | Nov 12 (before) | Nov 13 (after deployment) |
| --- | ---: | ---: |
| Upload started | 9 | 6 |
| Upload error | 8 (`file_read`) | 5 (`image_decode`, stage `decode`) |
| Analysis completed | 1 | 1 |

These are different calendar-day event aggregates, not matched upload attempts or a controlled group of users. **The ratios 8/9 and 5/6 are not comparable failure rates.** The new diagnosis tells me that image decoding still fails, but not which photo format or device configuration caused it. File-format reporting is still unavailable because its custom GA4 dimensions could not be registered.

**I cannot say the issue is fixed on affected Android phones.** The shipped change improves the file-loading path and exposes a more specific failure stage. An authorized source of file-format evidence and reproduction on a real device are still needed to narrow down the remaining error.

## November 14 follow-up: a format-specific failure hint

Decoding errors remained after the first release. In the [November 14 code change](https://github.com/saramjh/richChecker/commit/eede7730408b6aa2ec6afc9b2e4e5d6ab1531609), I added a more specific recovery hint. An Android photo provider can label a file as JPEG even when its bytes are HEIC or TIFF. That is a **possible explanation**, not a confirmed root cause for the errors previously observed.

The success path is unchanged. Only after an `image_decode` failure, the browser reads the first **16 bytes** locally using `File.slice(0, 16).arrayBuffer()`. If the header identifies HEIC or TIFF, the page suggests saving a JPG or PNG copy before trying again. If the header cannot be read or the read takes more than **250ms**, the ordinary guidance remains. It does not make a second full-size photo copy, upload image bytes to a server, or add identifiable information to analytics.

The source commit records **24 local browser tests and five contract checks passed**, and the [GitHub Actions deployment](https://github.com/saramjh/richChecker/actions/runs/43578267276) succeeded. I also verified that the live JavaScript bytes match the original repository's current `main` source. This **does not establish a fix on affected Android devices**. It improves failure guidance, but there is no verified increase in successful uploads or completed analyses.

## November 15: a measured result after the release

The [decode-hint change](https://github.com/saramjh/richChecker/commit/eede7730408b6aa2ec6afc9b2e4e5d6ab1531609) reached the live site on November 14 at **17:58 KST**. On November 15, I checked the **Richchecker KR product's own GA4 property**, after matching its live measurement ID to the web data stream. The property's reporting timezone is Seoul.

For November 14 after that deployment, GA4 classified **19:00 (3 events)** and **20:00 (1 event)** as `analysis_complete` on Android Chrome mobile. Another completion was recorded on Windows Chrome at 20:00. The session source for these events was `google / organic`. There was also one earlier Android Chrome completion at 14:00, before the release.

The app calls `renderResults` before tracking `analysis_complete`, so these are source-backed signals that the result-generation code path ran. **Four completion events do not represent four distinct users**. GA4's Android classification does not independently establish the physical device, and repeated attempts or developer testing cannot be ruled out. These data **do not prove that the original Android decoding issue is resolved**: no observation links the particular failing photo provider or file to these later events. I cannot calculate a change in success rate or attribute the completions to the patch.

## November 16: local photo recovery in both editions

The KR product's own GA4 data for Android Chrome mobile at 06:00 KST on November 15 showed one measured user, 15 upload_started events, 13 image_decode events and two analysis_complete events. For the US edition, GA4 recorded two file_read upload errors for one measured Android Chrome user at 19:00 Los Angeles property time on November 4. The GA4 records did not identify the original photos or their providers. Event counts cannot be treated as file counts or an upload failure rate.

[KR PR #4](https://github.com/saramjh/richChecker/pull/4) keeps the normal Blob URL decode path. If the image element fails, it makes one recovery attempt with createImageBitmap(file, { imageOrientation: "from-image" }). The input limit is 20 MiB, decoding is limited to seven seconds, and images above 50 megapixels are rejected. The recovered image is encoded as JPEG with a longest side of at most 2,200 pixels and a five-second encode limit. It reuses the existing MediaPipe analysis, preview and share flow. Late bitmaps are closed and unused Blob URLs are revoked. The photo is not uploaded, and this native fallback adds no new dependency. [US PR #1](https://github.com/saramjh/richChecker-us/pull/1) removes the full-photo Base64 FileReader path and uses a browser-local Blob URL with a recovery-only native ImageBitmap fallback.

A real 640×640 ISO HEIC fixture also failed Chrome's normal image decoder and native ImageBitmap. [KR PR #5](https://github.com/saramjh/richChecker/pull/5) and [US PR #2](https://github.com/saramjh/richChecker-us/pull/2) add a lazy, self-hosted MIT-licensed heic2any@0.0.4 conversion path for this failure. After a decode error, the app inspects at most 16 header bytes and loads the decoder only for genuine HEIC/HEIF, including HEIC bytes reported with a JPEG MIME type. The input limit is 12 MiB, conversion waits up to ten seconds, and the output JPEG is limited to 20 MiB under the existing 50MP cap. Normal JPEG, PNG and WebP uploads do not load the decoder. Photo bytes never leave the browser.

All four PRs were merged into main. The browser regression suites recorded 28/28 passing cases for KR native recovery, 29/29 for US native recovery, 29/29 for KR HEIC recovery and 30/30 for US HEIC recovery. Each change also passed the repository contract checks and an unmocked MediaPipe E2E that reached a visible result. All four [KR native](https://github.com/saramjh/richChecker/actions/runs/43821895201), [US native](https://github.com/saramjh/richChecker-us/actions/runs/43824121306), [KR HEIC](https://github.com/saramjh/richChecker/actions/runs/43842302246) and [US HEIC](https://github.com/saramjh/richChecker-us/actions/runs/43842311161) deployment runs succeeded. The live [KR edition](https://saramjh.github.io/richChecker/) and [US edition](https://saramjh.github.io/richChecker-us/), their runtime scripts and both decoder bundles returned HTTP 200 in a direct release check.

The 640×640 fixture reproduces a separate HEIC failure path. It does not identify the cause of the earlier 13 KR image_decode events or two US file_read events. The affected Android device, its gallery or cloud provider, and the original photo remain unknown. I have not reproduced the issue on that device. The production P0 remains open.


## November 16: TIFF recovery and cancellation of stale work

[KR PR #6](https://github.com/saramjh/richChecker/pull/6) and [US PR #3](https://github.com/saramjh/richChecker-us/pull/3) merged into main on November 16. Selecting another photo or resetting the tool now cancels earlier provider reads, image-decode waits, and MediaPipe module or model waits. The most recently selected file controls the preview and analysis.

TIFF conversion runs in a cancellable Web Worker in the browser. Before decoding, the worker checks IFD metadata and tile or strip counts. The decoded-data limits are 8 MP and 32 MiB, and source files are capped at 12 MiB. Deflate decompression also has an output-size bound. HEIC and TIFF recovery keeps the photo bytes in the browser.

Each repository's regression runs passed 38/38 format, failure and adversarial-input cases and 9/9 cancellation, reselection, reset and model-stall cases. An unmocked MediaPipe E2E passed with JPEG, actual HEIC and actual TIFF, plus a controlled no-face error and loader cleanup. The browser reported zero page errors. These tests ran in Chrome on macOS with an Android 14/Pixel 8 user agent and mobile viewport. No physical Android device was used.

The [KR deployment run](https://github.com/saramjh/richChecker/actions/runs/43888945586) completed at 14:45:15 UTC, and the [US deployment run](https://github.com/saramjh/richChecker-us/actions/runs/43888946580) completed at 14:45:18 UTC. Both live editions and their `js/script.js`, `tiff-worker.js`, `utif.js` and `pako_inflate.min.js` assets returned HTTP 200. Both product scripts contained the TIFF recovery function and cancellation state code.

I queried a short post-deployment window in each product's own GA4 property. For KR, the window ran from 23:45 KST on November 16 to 01:25 KST on November 17. For US, it ran from 06:45 to 08:25 on November 16 in the Los Angeles property timezone. The query covered Android mobile `upload_started`, `upload_error`, `analysis_started`, `analysis_complete`, `upload_decode_recovered` and `photo_picker_opened` events. No matching rows were returned. The 19:57 KST and 02:59 PST events in the earlier readback occurred before these deployments and are not evidence for the new code. A zero-row result over this short interval does not establish that there were no users or errors.

The affected Android device, photo provider and original photo remain unknown. The test results cover the TIFF and cancellation paths. They do not establish recovery on the affected device, so the production P0 remains open.

Sources: [Richchecker KR repository](https://github.com/saramjh/richChecker) · [Richchecker US repository](https://github.com/saramjh/richChecker-us) · [Separating app and blog analytics on a shared host](/gh-pages-analytics-notes-5-followup-en/) · [KR PR #6](https://github.com/saramjh/richChecker/pull/6) · [US PR #3](https://github.com/saramjh/richChecker-us/pull/3) · [KR deployment](https://github.com/saramjh/richChecker/actions/runs/43888945586) · [US deployment](https://github.com/saramjh/richChecker-us/actions/runs/43888946580)

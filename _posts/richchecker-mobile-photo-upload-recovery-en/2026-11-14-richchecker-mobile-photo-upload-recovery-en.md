---
title: "Richchecker KR: repairing a photo upload path that failed on Android Chrome"
description: "Real Android Chrome file-read errors led to a different image-loading path, safer file checks and more useful diagnostics in Richchecker KR."
date: 2026-11-14
tags: ["Richchecker", "Frontend", "Android Chrome", "Debugging"]
permalink: /richchecker-mobile-photo-upload-recovery-en/
layout: default
lang: en
alternate_lang: ko
alternate_url: /richchecker-mobile-photo-upload-recovery-ko/
published: true
seo:
  title: "Richchecker KR Android photo upload reliability fix"
  description: "Eight Android file-read error events led to a Blob URL change, file validation, browser testing and a verified Richchecker KR release."
---

> 한국어: [Richchecker KR 안드로이드 사진 업로드 오류 개선](/richchecker-mobile-photo-upload-recovery-ko/)

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

The old Blob URL is released with URL.revokeObjectURL() when the user replaces a photo, resets the tool or hits an error. An image load gets a 20-second timeout. If HEIC cannot be decoded by the browser, the page suggests saving a JPG copy. The selected photo still stays in the browser instead of being uploaded to an analysis server.

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

Sources: [Richchecker KR repository](https://github.com/saramjh/richChecker) · [Separating app and blog analytics on a shared host](/gh-pages-analytics-notes-5-followup-en/)

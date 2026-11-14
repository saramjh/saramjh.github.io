---
title: "Richchecker KR: face matching and photo recovery"
description: "A browser-only face comparison with a 47-person Korean reference sample, and practical guidance when Android photos are mislabeled."
date: 2026-11-14
tags: ["Richchecker", "Browser Engineering", "Image Processing"]
permalink: /rich-face-test-en/
layout: default
lang: en
alternate_lang: ko
alternate_url: /rich-face-test/
published: true
seo:
  title: "Richchecker KR | Face proportions and Android photo troubleshooting"
  description: "Compare six facial ratios locally and learn how failed HEIC/TIFF image decoding gets a useful retry hint."
---

# Richchecker KR: compare facial proportions in your browser

한국어: [부자 관상 테스트와 사진 오류 안내](/rich-face-test/)

[Open the free Korean Richchecker app](https://saramjh.github.io/richChecker/)

Richchecker KR is a playful face-proportion comparison. It measures six ratios from a photo—forehead height, eye spacing, nose length, mouth width, lower-face length and face aspect ratio—and compares them with a 47-person Korean public-figure reference sample. Results show the three closest matches, a six-feature radar chart and individual feature comparisons. They do **not** predict wealth, success or personality.

Face landmarks and matching run in the browser. The matching photo is not sent to an image-analysis server. The site may use ordinary analytics and advertising services; those are separate from local image matching. No account is required.

## If your photo will not open

A file with a `.jpg` name is not necessarily encoded as JPEG. Some Android photo providers can supply HEIC or TIFF bytes while reporting a JPEG filename or MIME type. When the browser cannot decode the file, a generic error message leaves the user unsure what to try.

In [Richchecker PR #3](https://github.com/saramjh/richChecker/pull/3), I improved the **failed-decode recovery path**. Only after an `image_decode` failure, the app reads the first 16 bytes locally to check for recognizable HEIC or TIFF signatures. If it identifies either format, it suggests saving the photo as JPG or PNG before retrying. If the provider cannot supply the header promptly, the check stops after 250 ms and uses the existing general advice.

The change does not add another image decoder, copy the full photo or send photo bytes to analytics. Successful image loading follows its previous path. The updated function appears in the [JavaScript served by the live Korean app](https://saramjh.github.io/richChecker/js/script.js).

## What the checks establish

[PR #3](https://github.com/saramjh/richChecker/pull/3) reports 24 browser checks covering formats, mislabeled HEIC/TIFF signatures, unavailable file providers and error cleanup. The earlier [Android upload investigation](https://github.com/saramjh/richChecker/blob/main/docs/ANDROID_UPLOAD_READ_FAILURE_20261113.md) recorded `file_read` errors, not these `image_decode` failures. Their cause on affected physical devices remains unknown. The deployed change improves recovery instructions; it has not established better real-device upload success rates.

If a photo still fails, save it locally as JPG or PNG, then select the converted copy in [Richchecker KR](https://saramjh.github.io/richChecker/). The [Global Billionaire Face Match](https://saramjh.github.io/richChecker-us/) is a separate English-language version using a different reference sample.

#### Sources and related reading

- [Richchecker KR source repository](https://github.com/saramjh/richChecker)
- [PR #3: photo-format recovery](https://github.com/saramjh/richChecker/pull/3)
- [Android investigation and testing limits](https://github.com/saramjh/richChecker/blob/main/docs/ANDROID_UPLOAD_READ_FAILURE_20261113.md)
- [Korean companion article](/rich-face-test/)

---
title: "Online Image Resizer - Don't worry about your personal information"
description: The Online Image Resizer never store any personal information. This Util supports a lot of amount processing.
date: 2024-09-03
tags: Image resizer, Personal Information secure, Online Utility
permalink: /online-image-resizer/
layout: default
---

### Online Image Resizer

<img src="{{site.assets}}{{ page.permalink }}onlineImageResizer.JPG" alt="online-image-resizer">

#### Needs

- Who needs to resize resolution of **a lot of image files** formatting `jpg`, `gif`, `png` and `webp`.
- Who worry about **_leaking personal information_** through storing a server storage.
- Who wants to make a lot of image files lighter.
- Who wants to download image URLs as image file via just a click.

#### Usage

1. **Select Images or Enter URLs**:
   - Click the file input to select local images or enter image URLs in the provided text area.
   - Sometimes there could be an error for `CORS`, then you should download directly and select the file to resize.
2. **Set Resize Options**:

   - Input the desired width and height. You can choose to keep one dimension fixed to maintain the aspect ratio.
   - Choose the desired format for the resized images.
   - Optionally, check the box to add a `resized_` prefix to filenames.

3. **Resize Images**:

   - Click the "Resize Images" button to start the resizing process.
   - The progress will be displayed, and once completed, resized images will be shown.

4. **Download Results**:

   - Click the "Download All as ZIP" button to download all resized images in a single ZIP file.
   - Alternatively, click the "Download" button below each image to download it individually.

5. **Reset All**:
   - Click the "Reset All" button to clear all inputs and selections and reload the page.

#### Features

- Only using your browser memeory. never using server storage.
- Upload Images: Select multiple image files or enter image URLs.
- Resize Options: Define width and height, select image format (JPG, PNG, GIF, WEBP), and optionally add a prefix to filenames.
- Progress Tracking: See the progress of the resizing operation.
- Error Handling: View error messages if any images fail to process.
- Download Resized Images: Download resized images individually or as a ZIP file.
- Reset Functionality: Clear all selections and settings to start over.
- Compatibility: Every Web browser supports this utility.

#### Dependencies

- **JSZip**: Used to create ZIP files for downloading resized images.
- **Font Awesome**: Provides icons used in the interface.
- **Google Analytics**: Tracks usage statistics (optional).

#### Links

- [Online Image Resizer](https://saramjh.github.io/resizeIMG)
- [Github Repository: Online Image Resizer](https://github.com/saramjh/resizeIMG)

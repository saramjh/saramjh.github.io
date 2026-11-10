---
title: "Space Atlas is listed in NCASE's aviation and space education directory"
description: "The interactive astronomy project I built has an entry in NCASE's Programs directory. Here's the learning experience behind the listing and why an external educator discovery route matters."
date: 2026-11-10
tags: ["Space Atlas", "STEM Education", "Astronomy", "Educational Software", "Developer Portfolio"]
permalink: /space-atlas-ncase-programs-en/
layout: default
lang: en
alternate_lang: ko
alternate_url: /space-atlas-ncase-programs-ko/
image: /space-atlas-student/space-atlas-hero.png
image_width: 1280
image_height: 820
published: true
seo:
  title: "Space Atlas joins the NCASE education resource directory"
  description: "Space Atlas, my free astronomy learning project, is listed in NCASE's Programs directory. How I designed interactive Moon phases and seasons lessons for educators."
---

> 한국어판: [Space Atlas, NCASE 항공·우주 교육 자료 목록 등재](/space-atlas-ncase-programs-ko/)

**Space Atlas now has an entry in the [NCASE Programs directory](https://ncase.org/programs/).** I developed this free astronomy reference to let learners investigate Moon phases, Earth's seasons and astronomical scale in a browser. The National Coalition for Aviation and Space Education (NCASE) lists the project among resources that educators and families can discover beyond my own website.

This is a concrete outcome for an independently built product: an external education directory now points readers to a working learning experience. It also gives me a useful test of my work as a developer. A science model must be understandable enough for someone who has never met its creator to explore it.

<figure>
<img src="/space-atlas-student/space-atlas-hero.png" alt="Space Atlas's original 3D solar-system overview, an example of the browser-based science models behind the NCASE listing." width="1280" height="820" loading="lazy" style="width:100%;height:auto;">
<figcaption>The original Space Atlas overview, previously used in the project introduction.</figcaption>
</figure>

## The engineering behind the entry

I designed the Moon Phases simulator around two questions a learner can test: which half of the Moon receives sunlight, and how much of that illuminated half can an observer on Earth see? Moving the Moon around its orbit connects the Sun–Earth–Moon geometry with its Earth-facing appearance.

The [seasons model](https://spaceatlasedu.org/earth/seasons/) gives another manipulable comparison. Learners can investigate the role of Earth's axial tilt instead of treating seasons as a simple change in distance from the Sun. For both lessons, interactive controls are coupled to explanations of what the model simplifies.

Building those connections required more than putting a 3D scene on a page. I had to turn scientific relationships into controls, visible feedback and short explanations that a teacher could use to start a discussion. The site works in a browser without requiring learners to create an account.

## What educators can try

A short Moon-phase activity begins with a prediction: during First Quarter, is a quarter of the visible disk bright, or about half? Learners can then [move the Moon in the simulator](https://spaceatlasedu.org/moon/phases/) and compare their prediction with the Earth view. The name describes a position in the lunar phase cycle; roughly half the visible disk is illuminated.

I also published a [predict–test–explain worksheet on Share My Lesson](https://sharemylesson.com/teaching-resource/moon-phases-predict-test-explain-interactive-grades-4-8-lesson-412086) for grades 4–8. That resource pairs the browser model with a classroom-ready investigation sequence. Teachers can examine the activity and adapt their own lesson planning after checking their school's device and privacy requirements.

## Why the listing matters to my development work

NCASE's Programs directory gives Space Atlas a route into an existing educator resource collection. I can now point a prospective education collaborator to a third-party directory entry and to the actual interactive lessons, rather than asking them to judge the project from a feature list.

The demonstrated capability is taking a difficult scientific subject through interface design and engineering to a usable public web product. The possible next step is for an educator to evaluate a lesson, test it with a class under their own policies, or propose a better explanation. The [NCASE listing](https://ncase.org/programs/) was confirmed on November 10, 2026; its original inclusion date is unknown. Directory inclusion establishes an external discovery route, not accreditation or measured classroom adoption.

See the [earlier Space Atlas project overview](/space-atlas-student-en/), the [Gravity Lab and Moon Orbit Catcher engineering note](/space-atlas-gravity-lab-moon-orbit-catcher-en/), or [open Space Atlas](https://spaceatlasedu.org/).

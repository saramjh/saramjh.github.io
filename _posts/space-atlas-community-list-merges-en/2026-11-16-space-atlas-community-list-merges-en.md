---
title: "Six open-source learning lists merged my Space Atlas contributions"
description: "Six independently maintained education and science resource lists merged links I submitted for Space Atlas in October and November 2026. The original PRs show what was accepted."
date: 2026-11-16
tags: ["Space Atlas", "Open Source", "Science Education", "Astronomy", "GitHub", "Software Development"]
permalink: /space-atlas-community-list-merges-en/
layout: default
lang: en
alternate_lang: ko
alternate_url: /space-atlas-community-list-merges-ko/
image: /space-atlas-student/space-atlas-hero.png
image_width: 1280
image_height: 820
published: true
seo:
  title: "Space Atlas in six open-source education lists: original merged PRs"
  description: "Six resource-list pull requests for Space Atlas, independently merged by maintainers, with original GitHub evidence and the astronomy learning models I built."
---

> 한국어판: [Space Atlas의 오픈소스 교육 자료 목록 기여 6건이 병합되기까지](/space-atlas-community-list-merges-ko/)

**Between October 16 and November 6, 2026, six independently maintained open-source learning and science resource lists merged links I submitted for Space Atlas.** The original GitHub pull requests document those decisions. A later URL correction in one of the lists is not counted as a seventh placement.

I built [Space Atlas](https://spaceatlasedu.org/) to let learners manipulate ideas such as Moon phases, Earth's seasons, and astronomical scale rather than only read about them. These merges did not release a new simulator. They made an existing working project easier to discover in collections maintained for different educational purposes.

<figure>
  <img src="/space-atlas-student/space-atlas-hero.png" width="1280" height="820" loading="lazy" alt="Original Space Atlas interactive astronomy project screenshot from my development notes" style="display:block;width:100%;height:auto;">
  <figcaption>My existing project image, not a screenshot or logo copied from any of the six external lists.</figcaption>
</figure>

## Six original contributions, six independent maintainers

These are the **UTC merge dates**. Each link opens the actual proposed change and its merge record.

- **October 16 — [Awesome Study Resources PR #404](https://github.com/StudentSuite/awesome-study-resources/pull/404):** Free interactive study material.
- **October 16 — [Awesome Interactive Learning PR #2](https://github.com/hamid-moghadam/awesome-interactive-learning/pull/2):** Models for exploring Moon phases and seasons.
- **October 20 — [Awesome MINT Kids Resources PR #2](https://github.com/augustunbear/awesome-MINT-Kids-Resources/pull/2):** Parent- and teacher-guided science activities.
- **October 27 — [Kids Edutainment Links PR #11](https://github.com/vorburger/kids-edutainment-links/pull/11):** Astronomy activities families can explore.
- **November 5 — [Awesome Physics PR #19](https://github.com/wbierbower/awesome-physics/pull/19):** Open-source astronomy models within an astrophysics collection.
- **November 6 — [Awesome Homeschooling PR #9](https://github.com/muriloime/awesome-homeschooling/pull/9):** Browser-based models for home science lessons.

I authored each change, and **a maintainer other than me merged each one**. All six current default-branch READMEs still contain an entry for Space Atlas. [Awesome MINT Kids Resources PR #5](https://github.com/augustunbear/awesome-MINT-Kids-Resources/pull/5) later updated the link to the canonical domain; that was a correction to an existing listing, not another independent placement.

## The software behind the links

In the [Moon Phases simulator](https://spaceatlasedu.org/moon/phases/), learners move the Moon around Earth and compare its sunlit half with the illuminated portion visible to an observer. In the [Earth's Seasons model](https://spaceatlasedu.org/earth/seasons/), they change axial tilt to explore why Earth–Sun distance alone cannot explain summer and winter. The development goal was to turn a question into something a learner could test.

A useful resource-list entry also has to distinguish between the **working learning website** and the **open-source code repository**. Some collections link to one, others to the other. The descriptions need to match what the software does, rather than promise a complete curriculum or professional astronomical predictions.

The six merges show that independent maintainers accepted **resource-list edits**. They do not establish classroom adoption or measured learning gains. Educators should review the site's current privacy and advertising notices before using it with learners.

For the implementation details, see my [Space Atlas development notes](/space-atlas-student-en/). The separate [NCASE and Share My Lesson case](/space-atlas-education-resource-paths-en/) explains how one model became a short lesson activity.

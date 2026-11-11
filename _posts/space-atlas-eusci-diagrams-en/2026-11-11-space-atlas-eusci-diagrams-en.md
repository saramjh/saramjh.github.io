---
title: "My astronomy diagram essay was published by EUSci"
description: "EUSci published my November 10, 2026 article on missing clues in astronomy diagrams. I connect the bylined piece to the interactive models I built for Space Atlas."
date: 2026-11-11
tags: ["Space Atlas", "EUSci", "Astronomy", "Science Communication", "Developer Writing", "Interactive Learning"]
permalink: /space-atlas-eusci-diagrams-en/
layout: default
lang: en
alternate_lang: ko
alternate_url: /space-atlas-eusci-diagrams-ko/
image: /space-atlas-student/space-atlas-hero.png
image_width: 1280
image_height: 820
published: true
seo:
  title: "My EUSci astronomy essay and the Space Atlas models behind it"
  description: "EUSci published Jihun Oh's November 10, 2026 essay on Moon phases, seasons, and eclipses. Here is the software-development work behind the byline."
---

> 한국어판: [EUSci에 우주 과학 도해 기고문이 실렸다](/space-atlas-eusci-diagrams-ko/)

On November 10, 2026, [EUSci published my article, *Three Space Diagrams, Three Missing Clues*](https://eusci.org.uk/2026/11/10/three-space-diagrams-three-missing-clues/). The page identifies **Jihun Oh** as the author and credits Priscilla Wong, EUSci's Head Online News Editor, for editing. The essay grew out of a design problem I encountered while building the interactive astronomy lessons in [Space Atlas](https://spaceatlasedu.org/).

An astronomy diagram can be accurate within its chosen view and still invite the wrong conclusion. A learner may not know where the observer stands, which direction remains fixed or what lies outside the picture's plane. In a static illustration those omissions are easy to miss. When I build a simulator, I have to decide how to make them visible through the controls and the model.

<figure>
  <img src="/space-atlas-student/space-atlas-hero.png" alt="Previously published first-party screenshot of the Space Atlas 3D astronomy learning interface, separate from the artwork used in the EUSci article." width="1280" height="820" loading="lazy" style="width:100%;height:auto;">
  <figcaption>My earlier Space Atlas learning interface, reused from the project's own blog introduction. This is not the illustration published by EUSci.</figcaption>
</figure>

## The engineering behind the explanation

The [Moon Phases model](https://spaceatlasedu.org/moon/phases/) separates the Moon's sunlit hemisphere from the part that appears bright to an observer on Earth. Moving the Moon through its orbit changes what that observer sees. Without a stated viewpoint, a diagram of first quarter does little to explain why half of the visible lunar disc is illuminated.

My [Seasons model](https://spaceatlasedu.org/earth/seasons/) deals with a different omission. Earth's axis stays pointed in approximately the same direction in space as Earth orbits the Sun. That orientation matters more to the explanation of the seasons than the changing Earth–Sun distance. A learner needs to see which direction the axis points at opposite orbital positions.

Eclipses show where a flat view becomes especially misleading. The Moon's orbital plane is inclined by roughly five degrees to the ecliptic. A drawing that leaves out the inclination can make monthly eclipses seem inevitable. In the EUSci essay I used the distinction between an overhead view, a side view and orbital nodes to explain the missing geometry.

For each lesson, I chose the relationships a learner needed to inspect and documented what the simplified model could not establish. That was the same judgment I had to make when moving from interactive software to a public science article.

## What the publication demonstrates

The result is a [publicly accessible article with an author credit and a named editor](https://eusci.org.uk/2026/11/10/three-space-diagrams-three-missing-clues/). It gives educators, reviewers and potential collaborators a way to examine my explanation of a problem, then compare it with a working [Moon Phases lesson](https://spaceatlasedu.org/moon/phases/). The byline provides a concrete writing sample alongside the software.

The article discloses AI assistance during drafting and editing and says its scientific explanations were checked against linked NASA references. Publication by EUSci is the verified achievement. It does not demonstrate formal university endorsement, classroom adoption or measured learning gains.

- [Read the EUSci article and editorial credit](https://eusci.org.uk/2026/11/10/three-space-diagrams-three-missing-clues/)
- [NASA Science: Moon phases](https://science.nasa.gov/moon/moon-phases/)
- [Space Atlas project case](/portfolio/space-atlas/) and [earlier engineering overview](/space-atlas-student-en/)

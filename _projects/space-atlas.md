---
layout: project
portfolio_ui: true
title: "Space Atlas | Project case study"
description: "Browser-based space-science models that let students change variables and inspect why textbook diagrams simplify reality."
slug: space-atlas
order: 2
name: Space Atlas
subtitle: Interactive astronomy for learners
field: Education / scientific visualisation
summary: Browser-based space-science models that let students change variables and inspect why textbook diagrams simplify reality.
image: /assets/images/portfolio/space-atlas-desktop.jpg
image_alt: Screenshot of the Space Atlas Moon phases learning simulator
site_url: https://spaceatlasedu.org/
writing_url: /space-atlas-student-en/
status: Publicly available
stack:
  - JavaScript
  - Three.js
  - Canvas 2D
  - HTML / CSS
  - GitHub Pages
---
## The problem

Static diagrams make it easy to memorise astronomy vocabulary while missing the physical relationships between scale, position, illumination, and observation.

## What I built

A collection of interactive learning models, including Moon phases, Earth seasons, orbital motion, planetary scale, and exoplanet transits. Students can adjust variables and compare different views.

## Engineering decisions

- Expose assumptions and simplifications in classroom models.
- Pair interactive scenes with explanatory text and the next relevant topic.
- Use 3D where spatial reasoning is useful and 2D where it is clearer.
- Keep controls usable on smaller screens.

## Explore a model

Open [Gravity Lab](https://spaceatlasedu.org/solar-system/gravity-lab/) to compare a 3.0 m/s jump across worlds, or try [Moon Phases](https://spaceatlasedu.org/moon/phases/) to explore lunar illumination.

The new [English case study](/space-atlas-gravity-lab-moon-orbit-catcher-en/) and [한국어 개발 기록](/space-atlas-gravity-lab-moon-orbit-catcher-ko/) explain the Gravity Lab comparison, the separate Flight Trials game and Moon Orbit Catcher. They also cover where the simplified models stop matching the physical systems. The [original introduction](/space-atlas-student-en/) describes the initial project scope.

---
title: "Same jump, different gravity: Space Atlas Gravity Lab and Moon Orbit Catcher"
description: "Space Atlas holds launch speed at 3.0 m/s to compare gravity across worlds. This follow-up explains the separate Flight Trials booster game and Moon Orbit Catcher, including the limits of each model."
date: 2026-11-10
tags: ["Space Atlas", "Astronomy", "Physics Simulation", "Interactive Learning", "STEM Education"]
permalink: /space-atlas-gravity-lab-moon-orbit-catcher-en/
layout: default
lang: en
alternate_lang: ko
alternate_url: /space-atlas-gravity-lab-moon-orbit-catcher-ko/
image: /space-atlas-student/space-atlas-hero.png
image_width: 1280
image_height: 820
published: true
seo:
  title: "Space Atlas Gravity Lab and Moon Orbit Catcher"
  description: "A controlled 3.0 m/s jump comparison, a separate boosted Flight Trials game, and three Moon Orbit Catcher challenges, with the limits of each model."
---

> 한국어판: [같은 점프, 다른 중력: Space Atlas의 Gravity Lab과 Moon Orbit Catcher](/space-atlas-gravity-lab-moon-orbit-catcher-ko/)

Gravity Lab compares a jump launched at 3.0 m/s under the gravity of different worlds. Flight Trials adds a fictional thruster and checkpoints. Moon Orbit Catcher asks learners to predict a lunar phase, then catch it in an orbit game.

<figure>
<img src="/space-atlas-student/space-atlas-hero.png" alt="The original Space Atlas 3D Solar System overview. Gravity Lab and Moon Orbit Catcher are separate lessons added later." width="1280" height="820" loading="lazy" style="width:100%;height:auto;">
<figcaption>The project overview image used in the September 2026 introduction. Gravity Lab and Moon Orbit Catcher are available at the links below.</figcaption>
</figure>

## One launch speed, different gravity

Gravity Lab uses a 70 kg reference mass and a 3.0 m/s launch speed. The speed stays fixed when the learner changes worlds. Gravity is the variable that changes the predicted jump height and time in the air.

For idealized vertical motion without air resistance, peak height follows `h = v₀² / (2g)`. The displayed unpowered predictions are:

| World or reference | Gravitational acceleration | Unpowered jump height |
| --- | ---: | ---: |
| Earth | 9.8 m/s² | 0.46 m |
| Moon | 1.6 m/s² | 2.81 m |
| Mars | 3.7 m/s² | 1.22 m |
| Jupiter reference level | 23.1 m/s² | 0.19 m |

The gravity values are rounded from the NASA NSSDC fact sheet. The 70 kg reference mass is used to calculate weight force. It does not enter the peak-height equation. The model ignores air resistance and changes in gravity with altitude. Jupiter has no walkable solid surface, so its platform represents an artificial test deck.

- [Open Gravity Lab](https://spaceatlasedu.org/solar-system/gravity-lab/)
- [NASA Planetary Fact Sheet](https://nssdc.gsfc.nasa.gov/planetary/factsheet/)

## Flight Trials adds a thruster and courses

Flight Trials adds a fictional thruster to the Gravity Lab environment. Its force is set to `mass × (local gravity + 5.5 m/s²)`. It runs for up to one second and recharges on the ground in about 2.5 seconds. Each cleared stage unlocks a longer course, with checkpoint counts increasing from three to ten.

The unpowered result is the gravity comparison. A boosted arc is a game result produced by the extra thrust. It does not predict how high an unaided person could jump on a planet.

## Predict a Moon phase, then catch it in orbit

The Moon Phases lesson asks learners to predict how much of the First Quarter Moon looks bright, then compare that choice with the scientific model. About half of the visible lunar disk is illuminated. "Quarter" refers to the Moon's position in its roughly 29.5-day phase cycle. It does not mean that 25% of the disk is bright.

Moon Orbit Catcher has three stages. The first follows a glowing target. The second narrows the capture window, and the last removes the target marker. Learners can adjust the orbit speed and set an exact angle manually. The game also supports keyboard controls and reduced-motion preferences.

The game speeds up the orbit for play. Its model uses a fixed Sun and circular orbit. It maps one revolution to the 29.5-day synodic month; the Moon's sidereal orbital period is about 27.3 days. The model omits the Moon's orbital tilt and eclipses, and it does not provide a live sky forecast.

The game requires JavaScript. The phase table and scientific explanation remain available without it. A printable teacher guide and student worksheet are also available.

- [Open Moon Phases and Moon Orbit Catcher](https://spaceatlasedu.org/moon/phases/)
- [NASA Moon Phases](https://science.nasa.gov/moon/moon-phases/)

## The NCASE public directory listing

The Space Atlas updates log records a check of the National Coalition for Aviation and Space Education (NCASE) public Programs index on November 4, 2026. The listing's first-publication date is unknown. The record establishes that Space Atlas had an entry in the public directory. It does not establish certification, endorsement, a NASA affiliation or classroom effectiveness.

The listing still uses the previous GitHub Pages address, which redirects to the current Space Atlas domain. The updates log says a link-correction request was sent. The publisher has not confirmed a change.

The Space Atlas site describes itself as a student reference for grades 4 to 8. The Moon Phases lesson also proposes a 30 to 35 minute activity for grades 3 to 5. That activity has not been tested in a classroom, and no pupil outcomes have been measured.

The public learning pages use Google Analytics 4 and may display Google AdSense ads. The site advises against unsupervised use by children under 13 while age-related data handling is under review. Educators and families should check their school and household privacy policies.

The [Space Atlas updates log](https://spaceatlasedu.org/updates/) records public release dates and related changes. The earlier [Space Atlas overview](/space-atlas-student/) introduces the astronomy reference.

---
title: "Scratch Lottery Simulation"
description: A free scratch-off lottery simulator modeled on real games — Powerball, US $5 scratch-offs, and Korea's Speetto 1000/2000 — with a CDF-based odds engine, fast-forward simulation, and a sourced lottery tax calculator. No real money involved.
date: 2024-09-03
modified: 2026-11-13
tags: ["Lottery", "Scratch Lottery", "Lottery simulation", "Powerball", "Speetto", "RTP", "Lottery tax calculator"]
permalink: /scratch-lottery-simulation/
layout: default
lang: en
alternate_lang: ko
alternate_url: /scratch-lottery-simulation-ko/
image: /scratch-lottery-simulation/scratchlottery-2026-desktop.png
legacy_asset_url: /posts/scratch-lottery-simulation/
---

<p style="background: rgba(0, 150, 80, 0.08); border-left: 4px solid #109648; padding: 10px 14px; margin-bottom: 24px; border-radius: 4px; font-size: 0.95rem;">
  <strong>Updated 2026-11-13:</strong> Added a direct path to an interactive probability lesson about expected payout and losing streaks. The 2026-09-18 rebuild introduced the ticket formats, fast simulation and calculator described below.
</p>

> 한국어: [스크래치 복권 시뮬레이터에서 확률과 연속 실패를 실험하기](/scratch-lottery-simulation-ko/)

### Scratch Lottery Simulation — Try your luck!

<img src="scratchlottery-2026-desktop.png" alt="Scratch Lottery Simulator desktop screenshot showing a Speetto 1000 ticket, odds table, and fast simulation panel">

A free scratch-off lottery simulator. It reproduces the tactile "scratching" experience using the published odds of real lotteries — Powerball, a typical US $5 scratch-off, and Korea's Speetto 1000/2000 — with no real money ever involved. Try it at [saramjh.github.io/scratchLottery](https://saramjh.github.io/scratchLottery).

#### Who it's for

- Anyone curious what it actually feels like to scratch off a losing ticket after losing ticket, at zero cost.
- Anyone who wants to see, numerically, how a jackpot's odds compare to everyday risks.
- Anyone who wants to understand Return to Player (RTP) by running thousands of tickets instantly instead of buying them.

#### What's new since the first version

- **Real ticket formats.** Powerball draws 5 white balls + 1 red bonus ball in a fixed order; Speetto 1000 matches two rows (LUCKY NUMBER / MY NUMBER); Speetto 2000 has you scratch two symbols per panel looking for a match. A "Custom Odds" mode still lets you build your own ticket with any jackpot probability.

  <img src="scratchlottery-2026-powerball.png" alt="Powerball-style scratch ticket with 5 main numbers and a red bonus ball" width="360">

- **A proper odds engine.** Each scratch draws a single random number from a cumulative distribution (CDF) and matches it to exactly one prize tier — the same mechanism a real printed ticket relies on. A ticket can never win two tiers at once, and a jackpot can never get silently overwritten by a lesser prize.
- **Fast-forward simulation.** Run 10, 100, or 1,000 tickets at once and watch a time-series chart converge toward the theoretical odds table — a fast way to build intuition for the law of large numbers.

  <img src="scratchlottery-2026-fast-simulation.png" alt="Fast simulation panel showing total spent, total won, net profit, and RTP after simulating 100 tickets">

- **Real-world odds comparisons and a sourced lottery tax calculator.** The odds table is placed next to comparable everyday odds (e.g., an amateur golfer's odds of a hole-in-one), and a separate calculator estimates US/Korean tax withholding on a given prize amount, with its assumptions stated.
- **Persistent history.** Cost, winnings, profit, and attempt count are saved to your device automatically, so your record picks up where you left off next time you visit.

#### How the odds/RTP are calculated

Each preset defines only a jackpot probability and a per-tier prize table; the ratio between tiers follows a fixed shape shared across all presets. On every scratch, the engine draws one random number in [0, 1) and checks which tier's cumulative-probability range it falls into. Lower-tier prize amounts are calibrated so the resulting RTP lands in the range real lotteries typically use, roughly 50–70%.

#### What I can measure from the live simulator

A read-only report from my own Google Analytics 4 property, queried on November 13, 2026, covered October 15 through November 12, 2026. It recorded **4,773 `scratch_completed` events** across 89 GA4 active users for that event, and **2,576 `run_fast_simulation` events** across 21 active users for that event.

The two event names describe different actions. `scratch_completed` fires after a simulated ticket has been fully revealed; the fast-forward button is counted separately. People can repeat either action, and the two active-user groups may overlap. These figures show tracked interactions, not 4,773 distinct people, lottery purchases, or a measured increase caused by promotion. The report does not establish whether every event came from a human visitor.

#### See how losing streaks affect an independent draw

[Open the interactive probability lesson](https://saramjh.github.io/scratchLottery/math/#independenceLesson) and switch the previous-loss count between 0, 5 and 10. In the lesson's Texas Lottery Game 2755 independent-draw model, the next simulated ticket has a 26.52% chance of any prize in all three cases. Five losses in a row have a 21.42% chance of occurring from the start, but those completed draws do not change the next simulated result.

The same guide shows an expected payout of about $3.23 for each modeled $5 ticket using the [published Game 2755 issue distribution](https://www.texaslottery.com/export/sites/lottery/Games/Scratch_Offs/details.html_252698616.html). The model does not measure which physical tickets remain unsold or estimate today's in-store winning odds.

#### Tech stack

No build tools or frameworks — plain HTML/CSS/JS, deployed as-is via GitHub Pages.

- `index.html` — page structure (SEO meta, ticket UI, odds/simulation panels, FAQ)
- `css/style.css` — all styling
- `js/script.js` — odds engine, ticket generation/rendering, scratch interaction, charts, localStorage persistence, GA4 event tracking

#### Disclaimer

This site is a pure simulation. No real money is wagered, and no real lottery tickets are bought or sold. Odds/RTP figures are based on the public information each preset references and aren't guaranteed to exactly match any specific lottery operator's official figures.

#### Links

- [Scratch Lottery Simulation](https://saramjh.github.io/scratchLottery)
- [GitHub Repository: Scratch Lottery Simulation](https://github.com/saramjh/scratchLottery)

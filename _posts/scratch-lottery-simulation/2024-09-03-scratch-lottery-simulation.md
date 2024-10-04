---
title: "Scratch Lottery Simulation"
description: This program is for simulating probability of scratch lottery. You can adjust the rate of probability and test.
date: 2024-09-03
tags: Lottery, Scratch Lottery, Lottery simulation
permalink: /scratch-lottery-simulation/
layout: default
comments: true
---

### Scratch Lottery Simulation - Try your luck!

<img src="{{site.assets}}{{ page.permalink }}scratchlottery.JPG" alt="Scratch Lottery Simulation - Try your luck!">

This project is a scratch lottery experience that allows users to scratch a lottery ticket to see if they win. The user can scratch the lottery ticket to see if they win, and can adjust the odds of winning by setting the odds.

#### Needs

- Who wants to simulate lottery ticket.
- Who wants to bet with friends.
- Who wants to experience the probability of lottery winning.

#### Project Organization

1. HTML Structure

- **header**: The header of the page, where the title of the program is displayed.
- **main**: The main content area, containing the scratch lottery area and the information section.
  - **section.lottery**: The area that displays the scratch lottery, which includes the canvas and buttons for scratching the lottery ticket.
  - **section.lotteryInfo**: The area to set the odds of winning and display the winning odds table.
  - **section#lotteryBalance**: This is the area that displays the balance information for the lottery.
  - **section#recordDisplay**: This section displays the lottery scratch record.
- **footer**: The footer of the page, which displays additional information when hovered over.
- **div#jackpotModal**: This is the area that displays the winning results in a modal.

2. CSS Styles

- **Base-style**: Initializes the default style for all elements, sets the font and box model.
- **Layout**: Organizes the overall layout of the page using flexboxes, and sets the styles for each section.
- **Modal and Button Styles**: Set the styles for modals and buttons to improve the user interface.
- **Media Queries**: Includes styling adjustments for mobile resolutions.

3. JavaScript Features

- Canvas Initialization: Initializes the canvas of the scratch lottery, adds a gray cover and instructions.
- Scratch function: Make a certain area of the canvas transparent when the user scratches with the mouse to see if the lottery is won.
- Calculate winning probability: Calculate the winning probability of each equal number based on the probability set by the user.
- Display winning results: Display winning results in a modal, which will appear automatically if you win.
- Multilingual Support: English (EN), Spanish (ES), Chinese (ZH), German (DE), Italian (IT), Vietnamese (VI), Korean (KO), Russian (RU), Japanese (JP), French (FR)

#### Links

- [Scratch Lottery Simulation](https://saramjh.github.io/scratchLottery)
- [Github Repository: Scratch Lottery Simulation](https://github.com/saramjh/scratchLottery)

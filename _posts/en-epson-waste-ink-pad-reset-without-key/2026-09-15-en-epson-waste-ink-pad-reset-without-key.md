---
title: "How to Reset Epson Waste Ink Counter Free: 33 Models Supported (L3100-L3168, L1110, L5190 on Mac/Win/Linux)"
date: 2026-09-15
tags: Epson, L3100, L3106, L3110, L3150, L3160, L1110, L5190, Waste Ink Pad Reset, WIC Reset Alternative, reinkpy, Mac Epson Reset, DIY Printer Repair
permalink: /en-epson-waste-ink-pad-reset-without-key/
layout: default
legacy_asset_url: /posts/en-epson-waste-ink-pad-reset-without-key/
description: "Fix Epson waste ink pad service life error across 33 models (L3100~L3168, L1110~L1119, L5190~L5198). No paid WIC reset keys or Windows utilities needed. 100% free cross-platform reset via reinkpy on macOS/Linux/Windows."
excerpt: "Covers 33 compatible Epson models! Replace only the felt pads for ~$5 and reset the waste ink counter for free across macOS, Linux, and Windows using open-source reinkpy-fix."
seo:
  title: "Reset Epson Waste Ink Counter for Free on Mac / Linux / Windows (33 Models Supported)"
  description: "Epson waste ink counter reset guide for 33 models (L3100, L3106, L3150, L3160, L1110, L5190 series). Step-by-step reinkpy tutorial without paid reset keys."
  keywords:
    - Epson waste ink pad reset
    - Epson printer reset key free
    - Epson Mac waste ink counter reset
    - Epson L3100 ink pad replacement
    - Epson L3106 reset
    - Epson L3110 waste ink
    - Epson L3150 reset counter
    - Epson L3160 reset
    - Epson L1110 reset
    - Epson L5190 reset
    - WIC Reset alternative free
    - reinkpy fix tutorial
    - A printer ink pad is at the end of its service life
    - It is time to reset the ink levels
    - Epson error code E-11
    - Epson ink pad nearing the end of its service life
canonical: /en-epson-waste-ink-pad-reset-without-key/
image: /en-epson-waste-ink-pad-reset-without-key/epson-printer.jpg
---

<p style="background: rgba(0, 120, 212, 0.08); border-left: 4px solid #0078d4; padding: 10px 14px; margin-bottom: 24px; border-radius: 4px; font-size: 0.95rem;">
  🇰🇷 <strong>한국어 안내:</strong> 한국어 가이드 및 국내 호환 부품 구매 안내는 <a href="/epson-waste-ink-pad-reset-without-key/"><strong>엡손 잉크패드 리셋키 없이 10분 만에 끝내는 법 (한국어)</strong></a> 포스팅을 참고하세요.
</p>

### Exact Epson Waste Ink Pad Error Messages & Symptoms

<picture>
  <source type="image/webp" srcset="epson-printer-400.webp 400w, epson-printer-800.webp 800w, epson-printer.webp 1200w" sizes="(max-width: 690px) calc(100vw - 40px), (max-width: 768px) 650px, 660px">
  <img src="epson-printer.jpg" srcset="epson-printer-400.jpg 400w, epson-printer-800.jpg 800w, epson-printer.jpg 1200w" sizes="(max-width: 690px) calc(100vw - 40px), (max-width: 768px) 650px, 660px" alt="Epson EcoTank Inkjet Printer" width="1200" height="901" fetchpriority="high" loading="eager" decoding="async">
</picture>
<p style="font-size:0.8em; color:#888; margin-top:-10px;">Epson EcoTank Printer (Photo: Santeri Viinamäki, CC BY-SA 4.0 via Wikimedia Commons)</p>

If you own an Epson EcoTank / L-Series printer (such as the L3100~L3168, L1110, L5190, ET-2710, ET-4700), after printing a certain threshold of pages, printing will suddenly halt with the **Power light and Ink/Paper warning lights flashing alternately**.

Depending on your driver version and OS, EPSON Status Monitor 3 will throw one of these **exact verbatim warning messages**:

> **Message 1 (Final Service Lockout - Most Common):**  
> *"A printer's ink pad is at the end of its service life. Please contact Epson Support."*  
> *(Or: "The printer's ink pads are at the end of their service life.")*

> **Message 2 (Pre-lockout Warning):**  
> *"A printer's ink pad is nearing the end of its service life. Please contact Epson Support."*

> **Message 3 (Status Code on LCD / Utility):**  
> **Error Code: `E-11`** *(Ink pad life expired / Service required)*

If you found this page by searching the exact prompt **"A printer's ink pad is at the end of its service life"**, this guide solves your issue without paying for service centers or scammy reset utilities.

When searching for solutions online, users typically hit two frustrating roadblocks:
1. **Expensive and scammy software resets**: Tools like WIC Reset require you to buy a one-time reset key for \$10–\$15. Free alternatives like the Epson Adjustment Program (AdjProg) are 99% Windows-only `.exe` binaries, often flagged by antiviruses and unusable on **macOS (MacBook)** or **Linux**.
2. **Overpriced plastic assembly**: Buying the entire plastic cartridge housing costs significantly more and creates unnecessary plastic waste, even though the plastic case itself is completely intact and reusable.

By **replacing only the felt absorption pads** and using an open-source Python tool (**reinkpy-fix**) with an AI coding assistant or terminal, you can completely repair your printer in **under 10 minutes** for roughly \$4–\$5 on any operating system.

---

### 1. Cost & Waste Comparison: Full Assembly vs. Felt Pads Only

<picture>
  <source type="image/webp" srcset="epson-maintenance-box-400.webp 400w, epson-maintenance-box-800.webp 800w, epson-maintenance-box.webp 895w" sizes="(max-width: 690px) calc(100vw - 40px), (max-width: 768px) 650px, 660px">
  <img src="epson-maintenance-box.jpg" srcset="epson-maintenance-box-400.jpg 400w, epson-maintenance-box-800.jpg 800w, epson-maintenance-box.jpg 895w" sizes="(max-width: 690px) calc(100vw - 40px), (max-width: 768px) 650px, 660px" alt="Epson Ink Maintenance Box with waste ink" width="895" height="1200" loading="lazy" decoding="async">
</picture>
<p style="font-size:0.8em; color:#888; margin-top:-10px;">Epson Ink Maintenance Box / Waste ink absorber (Photo: Ll1324, CC0 Public Domain via Wikimedia Commons)</p>

The waste ink maintenance box is just a molded plastic container. What actually gets saturated with discarded ink is the **felt absorption pads** inside.

| Aspect | Full Maintenance Box Assembly | Felt Absorber Pads Only (Recommended) |
| :--- | :--- | :--- |
| **Typical Cost** | \$7 – \$10 + shipping | **\$4 – \$5 (Free shipping available online)** |
| **Hardware Work** | Remove 1 screw, swap box | Remove 1 screw, swap inner felt pads |
| **Time Needed** | ~3 minutes | ~5 minutes |
| **Eco Impact** | Throws away durable plastic | Reuses plastic housing, zero extra plastic waste |

You only need to buy pre-cut replacement sponge pads for your model (e.g. L3100 / L3110 / L3150) from online marketplaces like Amazon, AliExpress, or local vendors.

---

### 2. Hardware Replacement (Takes 5 Minutes)

**Items needed**: Cross-head screwdriver, disposable gloves (or tweezers), paper towels, new felt pads.

1. **Power Off**: Disconnect the power cord and USB cable.
2. **Remove Outer Screw**: Locate the single screw on the lower right back panel of the printer. Unscrew it and slide the small plastic cover downwards to remove it.
3. **Slide Out Ink Box**: Remove the inner screw securing the waste ink container. Slide the container out gently towards the right.
4. **Swap Sponges**: Wearing gloves, pull out the ink-soaked sponges and discard them into a trash bag. Wipe the inside of the plastic casing with a paper towel, then insert the new, clean felt pads in the exact same orientation.
5. **Reassemble**: Slide the box back into the printer, tighten both screws, and reattach the cover.

---

### 3. Software Counter Reset via reinkpy-fix (Cross-Platform)

Physical pad replacement is only half the battle. The internal EEPROM memory in the printer still retains the maximum counter value, which must be reset to 0%.

Instead of paying for proprietary reset keys or hunting down sketchy Windows-only tools, we use **`reinkpy-fix`**, an open-source Python tool that communicates directly with the printer over low-level USB commands.

You can run the steps manually in your terminal, or **pass the copy-paste prompt below directly to an AI coding assistant** (such as Claude Code, Cursor, Codex, or Antigravity) to automate environment setup, bug patching, device detection, and EEPROM resetting in under 2 minutes.

---

#### 💡 Ready-to-use AI Agent Prompt (Copy & Paste)

Copy the prompt block below and paste it directly into your AI coding assistant:

```text
My Epson printer (model: L3106 / L3100 or ET-2710 series) is locked due to "waste ink pad at the end of its service life".
It is connected via USB to my macOS/Linux machine. Please automate the 0% counter reset following these exact steps:

1. Clone repository: https://github.com/LeFZdev/reinkpy-fix
2. Ensure libusb is installed (e.g. run 'brew install libusb' on macOS or 'apt-get install libusb-1.0-0-dev' on Linux).
3. Set up a virtualenv (python3 -m venv venv) and install dependencies:
   venv/bin/pip install pyusb pysnmp zeroconf
   venv/bin/pip install -e .
4. (CRITICAL BUG FIX) In reinkpy/__init__.py, find two occurrences of 'from usb import UsbIO' and replace them with 'from .usbtest import UsbIO'.
5. Replace reinkpy/main.py with this reset routine:
```python
import reinkpy
printer = reinkpy.Device.from_usb(manufacturer='EPSON')
driver = printer.epson
if not driver.spec.model:
    driver.configure("L3106")  # adjust to your model e.g. L3150, ET-2710
print("Connected Printer:", printer)
print("Configured Model:", driver.spec.model)
driver.reset_waste()
print("Waste ink pad counter successfully reset to 0%!")
```
6. Execute with elevated permissions: sudo venv/bin/python3 reinkpy/main.py and verify reset completion.
```

---

#### 🛠 Step-by-Step Manual Terminal Guide

If you prefer executing the commands manually without an AI assistant:

#### Step 1 — Clone the Repository

Clone the patched repository locally:

```bash
git clone https://github.com/LeFZdev/reinkpy-fix
cd reinkpy-fix
```

#### Step 2 — Install libusb

`libusb` is required for raw USB device communication on macOS and Linux.

On macOS (via Homebrew):
```bash
brew install libusb
```

On Ubuntu/Debian Linux:
```bash
sudo apt-get install libusb-1.0-0-dev
```

#### Step 3 — Create Virtual Environment & Install Dependencies

```bash
python3 -m venv venv
venv/bin/pip install pyusb pysnmp zeroconf
venv/bin/pip install -e .
```

#### Step 4 — Fix Library Import Bug (Crucial Step!)

In the current `reinkpy-fix` repository commit, running the script immediately results in an `ImportError`. The underlying file `usb.py` was renamed to `usbtest.py`, but `reinkpy/__init__.py` was not updated.

Open `reinkpy/__init__.py` and search for `from usb import UsbIO`. You will find two occurrences. **Change both lines to:**

```python
# Before
from usb import UsbIO

# After
from .usbtest import UsbIO
```

*(If you are using an AI coding agent, simply tell it: "Fix the UsbIO import in reinkpy/__init__.py to import from .usbtest", and it will patch the file instantly.)*

#### Step 5 — Replace main.py with USB Reset Routine

Replace the entire contents of `reinkpy/main.py` with the following clean reset script:

```python
import reinkpy

# Discover connected EPSON USB printer
printer = reinkpy.Device.from_usb(manufacturer='EPSON')

driver = printer.epson
if not driver.spec.model:
    driver.configure("L3106")  # Specify your model or compatible series (e.g. L3100, L3106, L3150)

print("Connected Printer:", printer)
print("Configured Model:", driver.spec.model)

# Reset waste ink counter to 0%
driver.reset_waste()
print("Waste ink pad counter successfully reset to 0%!")
```

#### Step 6 — Execute with Elevated Privileges

Raw USB access requires root permissions on macOS/Linux:

```bash
sudo venv/bin/python3 reinkpy/main.py
```

You will see output identifying your printer followed by:
```text
Connected Printer: <Device EPSON ...>
Configured Model: L3106
Waste ink pad counter successfully reset to 0%!
```

Finally, **turn the printer off and back on**. The flashing warning lights will disappear, and the printer will return to a completely normal and ready printing state!

---

### Supported Epson Printer Models (Asia L-Series & Global EcoTank)

The `reinkpy-fix` reset procedure applies **100% identically** across all models sharing the same internal motherboard and USB communication protocol:

#### 1) Asian / Domestic Models (L-Series — 33 Models)
- **L3100 Models**: L3100, L3101, L3104, L3105, L3106, L3107, L3108, L3109
- **L3110 Models**: L3110, L3111, L3114, L3115, L3116, L3117, L3118, L3119
- **L3150 Models (Wi-Fi)**: L3150, L3151, L3152, L3153, L3156, L3158
- **L3160 Models (with LCD)**: L3160, L3161, L3163, L3165, L3166, L3168
- **L1110 Models (Single-function)**: L1110, L1118, L1119
- **L5190 Models (Fax / ADF)**: L5190, L5196, L5198

#### 2) North American & European Models (EcoTank / ET Series)
Global EcoTank models share the exact same firmware / EEPROM architecture:
- **ET-1110 ~ ET-1118** (Global equivalent of L1110)
- **ET-2710 ~ ET-2728** (Global equivalent of L3110 / L3150)
- **ET-4700** (Global equivalent of L5190 Fax All-in-One)

> **Configuration Note**: In Step 5, simply replace `driver.configure("L3106")` in `main.py` with your exact model string (e.g., `L3150`, `L1110`, `L5190`, `ET-2710`). The driver will target the exact memory register of your printer.

---

### Important: Physical Disassembly Nuances by Model

While the **software reset is identical** across all models listed above, the **physical teardown process varies slightly by form factor**:

- **L3100 ~ L3119 (including L3106)**: Same generation and identical chassis. The 1-screw lower-right rear panel and slide-out box mechanism described in Step 2 is 100% identical.
- **L3150 / L3160 Series**: Includes Wi-Fi modules and LCD screens, but the rear lower chassis and waste pad box placement remain virtually the same.
- **L1110 Series (Compact Single-function)** / **L5190 Series (ADF / Fax)**: Different physical form factors. Screw locations and exterior casing latches may vary, so double-check your model's specific service casing layout before pulling the box out.

---

### Summary: Solved in 10 Minutes with \$5

- **Total Cost**: ~$5 for felt pads (Zero dollars spent on reset keys)
- **Time Spent**: 5 mins physical pad swap + 5 mins terminal reset = **10 minutes total**
- **Key Advantage**: 100% native on macOS and Linux without Windows virtualization, and reusable for every future reset cycle.

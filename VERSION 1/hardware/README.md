# 🔩 Hardware Build — Development Log

> This document covers the physical hardware iterations of Dominus — what was built, what broke, and why the final design is the way it is.

---

## 🗂️ Overview

The hardware went through **3 major iterations** before reaching the current stable version. Each version solved a real problem that only showed up after actually building and running the system.

---

## 📦 Version 1 — First Build (White Button Panel)

<div align="center">
<img src="../assests/version 1.jpg" alt="Version 1 Front Panel" width="350"/>
</div>

### What Was Built
The first version had a fully integrated control logic — both **remote** and **manual** control were handled by the controller (Raspberry Pi). The idea was simple:

- Toggle a switch on the panel → controller reads it → switches the relay
- Send a remote command → controller reads it → switches the relay
- Both paths going through the same controller

The switch panels were **handmade** — fabricated manually and wired directly into the controller GPIO pins.

### ❌ The Problem — Electromagnetic Interference (EMI)

The 230V power lines were running **physically close to the data wires** connecting the switches to the controller.

What happened:
```
230V AC Line  →  EMI radiation  →  Data wire picks it up
                                         ↓
                              Controller reads false signal
                                         ↓
                              Wrong relay triggered
```

This caused the controller to randomly pick up **ghost signals** — triggering relays without any actual input. Manual control became unreliable because the system couldn't tell the difference between a real button press and electrical noise from the power line.

---

## 📦 Version 2 — New Switch Panels

<div align="center">
<img src="../assests/version 2.jpg" alt="Version 2 Back Panel with Wiring" width="350"/>
</div>

### What Changed
At first I thought the problem was the handmade switches — that loose contacts or poor construction was causing the false signals. So I:

- Replaced both switch panels with properly built, cleaner versions
- Rewrote the control code to reconfigure how inputs were handled
- Tested the full system again

### ❌ Same Problem
The interference wasn't coming from the switches. The root cause was still the **230V lines running beside the data cables**. New switches didn't fix electromagnetic noise.

This confirmed it — the problem was electrical, not mechanical.

---

## 📦 Version 3 — DPDT Switches + Optocouplers (Current Build)

<div align="center">
<img src="../assests/version 3.jpeg" alt="Version 3 Final Build" width="350"/>
</div>

### The Real Fix — Rethinking the Architecture

While working through the EMI issue, a bigger question came up:

> *What happens if the controller itself fails?*
> *If the Raspberry Pi crashes or hangs — I lose access to every machine.*

That single point of failure wasn't acceptable. So Version 3 was rebuilt around two principles:

1. **Manual control must be fully independent of the controller**
2. **The controller must be protected from high-voltage noise**

### What Changed

#### DPDT Switches Added to Every System
Each machine now has a **DPDT (Double Pole Double Throw) switch** on its panel.

```
DPDT Switch UP    →  Local / Manual Mode
                     Direct hardware control — controller not involved at all

DPDT Switch DOWN  →  Remote Mode
                     Controller takes over — relay switching via software
```

Manual control is now **completely separate** from the controller. If the Raspberry Pi is dead, the DPDT switch still works.

#### Manual Logic Removed from Controller
The controller no longer handles any manual input signals. That entire code path was removed. This eliminated the source of the false trigger problem — the controller is no longer listening to GPIO pins that were picking up 230V interference.

#### 2 Optocouplers Added
Two **optocouplers** were added between the switch panels and the controller.

```
Switch Panel  →  Optocoupler  →  Controller GPIO
```

Optocouplers use **light** to transfer the signal — there is no direct electrical connection between the 230V side and the controller side. This completely isolates the data line from the power line noise.

The controller now uses the optocouplers to **sense which mode the system is in**:
- DPDT switched UP → optocoupler signals controller → controller knows device is in local mode
- DPDT switched DOWN → controller is in charge

---

## 📊 Iteration Summary

| Version | Manual Control | Remote Control | EMI Issue | Controller Failure Risk |
|---|---|---|---|---|
| v1 | Via controller | Via controller | ❌ Present | ❌ Full lockout |
| v2 | Via controller (new panels) | Via controller | ❌ Still present | ❌ Full lockout |
| v3 | DPDT — independent | Via controller | ✅ Resolved | ✅ DPDT always works |

---

## 🧠 Key Lessons

**1. Keep high-voltage and data lines physically separated.**
Running 230V AC beside GPIO data wires will cause interference. Route them on opposite sides of the enclosure and use shielded cable where possible.

**2. Don't assume the problem is mechanical before checking electrical.**
Replacing the switches felt logical — but the issue was EMI, not the switches. Always rule out the electrical environment first.

**3. Design for controller failure from the start.**
Any system where a software crash causes complete physical lockout is a bad design. Hardware-level fallback should be part of version 1, not version 3.

**4. Optocouplers are the right tool for mixed-voltage systems.**
When low-voltage control circuits share an enclosure with mains power, optocouplers provide proper isolation without adding complexity.

---

*Full wiring schematics and component diagrams are in this folder.*

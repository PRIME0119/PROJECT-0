# 🔩 Hardware Build — Development Log

<div align="center">

```
v1 ──────────── v2 ──────────── v3
First Build   Iteration    Final Build
   ❌ EMI       ❌ EMI        ✅ FIXED
```

> *Every version broke for a reason. Every reason made the next version better.*

</div>

---

<br/>

## 🗂️ Overview

The hardware went through **3 major iterations** before reaching the current stable version. Each version solved a real problem that only showed up after actually building and testing the system in the real world.

This isn't just a changelog — it's the actual story of what went wrong, what was tried, and how the final architecture came to be.

<br/>

---

<br/>

## 📦 Version 1 — First Build

<table>
<tr>
<td width="35%">
<img src="../assests/version 1.jpg" width="100%" style="border-radius:8px"/>
</td>
<td width="65%" valign="top">

### The Idea
Build a single control system where **both remote and manual control** pass through the Raspberry Pi controller.

- Toggle a switch → controller reads it → relay switches
- Send remote command → controller reads it → relay switches
- One brain. Two input methods.

The switch panels were **entirely handmade** — fabricated and wired directly into the controller GPIO pins.

### ❌ What Broke — EMI
The 230V power lines were running **right beside the data wires**.

```
230V Line → EMI → Data wire → False signal → Wrong relay
```

The controller started picking up **ghost signals** — triggering relays with no actual input. Manual control became a gamble. The system couldn't tell the difference between a real button press and electrical noise.

</td>
</tr>
</table>

<br/>

---

<br/>

## 📦 Version 2 — New Switch Panels

<table>
<tr>
<td width="65%" valign="top">

### The Assumption
The handmade switches looked like the obvious culprit — loose contacts, rough construction, poor connections.

So the approach was:
- Rebuild **both switch panels** properly from scratch
- Rewrite the input handling code completely
- Test again with the new panels

### ❌ Same Problem — Different Cause
The new panels made no difference.

The interference wasn't mechanical — it was **electrical**. The 230V lines were still running beside the data cables. New switches couldn't fix electromagnetic noise in the wiring environment.

This ruled out the switches entirely. The problem was in the physical layout of the enclosure.

</td>
<td width="35%">
<img src="../assests/version 2.jpg" width="100%" style="border-radius:8px"/>
</td>
</tr>
</table>

<br/>

---

<br/>

## 📦 Version 3 — DPDT + Optocouplers ✅

<table>
<tr>
<td width="35%">
<img src="../assests/version 3.jpeg" width="100%" style="border-radius:8px"/>
</td>
<td width="65%" valign="top">

### The Real Question
While debugging the EMI issue, a bigger problem became obvious:

> *If the Raspberry Pi crashes — every machine is completely inaccessible.*

That's a single point of failure. Not acceptable.

Version 3 was rebuilt around two hard rules:

**Rule 1 →** Manual control must work without the controller  
**Rule 2 →** Controller must be isolated from high-voltage noise

### ✅ What Changed

**DPDT Switches — Full Independence**
```
DPDT UP   →  Local Mode  →  Direct hardware, no Pi involved
DPDT DOWN →  Remote Mode →  Pi takes over via software
```

**Manual logic completely removed from controller** — the Pi no longer listens to any GPIO pins connected to the switch panels. The source of the false triggers is gone.

**2 Optocouplers added** between panels and controller:
```
Switch Panel → Optocoupler → Controller GPIO
```
Signal transfers via **light** — zero electrical connection between mains and logic side. EMI can't cross that gap.

The Pi now only reads the optocouplers to **detect which mode** the system is in. Nothing else.

</td>
</tr>
</table>

<br/>

---

<br/>

## 📊 Iteration Summary

<div align="center">

| | Version 1 | Version 2 | Version 3 |
|---|:---:|:---:|:---:|
| **Manual Control** | Via Pi | Via Pi | DPDT — independent |
| **Remote Control** | Via Pi | Via Pi | Via Pi |
| **EMI Problem** | ❌ Present | ❌ Present | ✅ Resolved |
| **Controller Failure** | ❌ Full lockout | ❌ Full lockout | ✅ DPDT still works |
| **Optocoupler Isolation** | ❌ None | ❌ None | ✅ Added |

</div>

<br/>

---

<br/>

## 🧠 Key Lessons

<table>
<tr>
<td width="50%" valign="top">

**⚡ Separate high-voltage and data lines**
230V AC beside GPIO wires will always cause interference. Route them on opposite sides. Use shielded cable where possible.

**🔍 Rule out electrical before mechanical**
Replacing the switches felt logical — but the issue was EMI, not construction. Always check the electrical environment first.

</td>
<td width="50%" valign="top">

**🛡️ Design for controller failure from day one**
A software crash causing full physical lockout is a design flaw, not bad luck. Hardware fallback belongs in v1, not v3.

**💡 Optocouplers for mixed-voltage systems**
When low-voltage logic shares an enclosure with mains power, optocouplers give you proper isolation without complexity.

</td>
</tr>
</table>

<br/>

---

<div align="center">

*Full wiring schematics and component diagrams are in this folder.*

</div>

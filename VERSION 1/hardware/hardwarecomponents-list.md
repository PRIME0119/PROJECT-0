# 🛠️ Components List

> Full hardware breakdown of the Dominus control system — every component, relay mapping, GPIO assignment, and design decision in one place.

---

## 🧠 Core Controller

| Component | Details |
|---|---|
| 🍓 Raspberry Pi | Model 3B+ |
| 💾 MicroSD Card | High endurance recommended |

---

## ⚡ Relay Modules

### System 1

| Relay | Function |
|---|---|
| R11 | Power Trigger |
| R3 – R6 | Disk Switching |

### System 2

| Relay | Function |
|---|---|
| R12 | Power Trigger |
| R7 – R10 | Disk Switching |

### Relay Specs
- **Type:** 5V Relay Modules with Optocoupler Isolation
- **Modules:** Mix of 4-channel and 2-channel boards
- **Logic:** Active LOW configuration

---

## 🔌 Optocouplers — Feedback & Isolation

### System Status Feedback

| Signal | GPIO Pin |
|---|---|
| SYSTEM1_STATUS | GPIO 5 |
| SYSTEM2_STATUS | GPIO 6 |

### Disk Detection

| System | Disk | GPIO Pin |
|---|---|---|
| System 1 | Disk 1 | GPIO 21 |
| System 1 | Disk 2 | GPIO 16 |
| System 2 | Disk 1 | GPIO 20 |
| System 2 | Disk 2 | GPIO 12 |

---

## 🔘 Manual Control — Push Buttons

| Detail | Value |
|---|---|
| Total Buttons | 8 |
| Power ON / OFF | ✅ |
| Disk Selection | ✅ |
| Safety Trigger | Double press logic |

---

## 💽 Controlled Hardware

### System 1

| Component | Details |
|---|---|
| Motherboard | H81 |
| Storage | 2 × Hard Drives (ROM switching) |

### System 2

| Component | Details |
|---|---|
| Motherboard | H81 |
| Storage | 2 × Hard Drives (ROM switching) |

---

## 🔋 Power & Miscellaneous

| Component | Notes |
|---|---|
| 5V Power Supply | Powers relays and Raspberry Pi |
| Jumper Wires | GPIO connections |
| Breadboard / Terminal Blocks | Wiring management |
| Cooling Fans | Optional — controllable via relay logic |

---

## ⚙️ Design Notes

```
Relay Logic      →  Active LOW configuration
Optocouplers     →  Isolation + state feedback to controller
Control Modes    →  Remote (Web Dashboard) + Local (DPDT Manual Override)
```

| Mode | How It Works |
|---|---|
| 🌐 Remote | Commands sent via web dashboard → controller triggers relays |
| 🔘 Local | DPDT switch flipped → bypasses controller entirely |

---

*Wiring schematics and GPIO diagrams are in this folder.*

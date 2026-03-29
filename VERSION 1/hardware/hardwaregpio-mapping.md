# 📍 GPIO Mapping

> Complete pin assignment for all relays, optocouplers, and disk detection sensors in the Dominus control system.

---

## 🔁 Relay Outputs — Active LOW

### System 1

| Relay | GPIO Pin | Function |
|---|---|---|
| R1 | GPIO 19 | System 1 Control |
| R3 | GPIO 2 | Disk 1 Select |
| R4 | GPIO 3 | Disk 2 Select |
| R5 | GPIO 4 | Disk 1 Line |
| R6 | GPIO 17 | Disk 2 Line |
| R11 | GPIO 24 | Power Trigger |

### System 2

| Relay | GPIO Pin | Function |
|---|---|---|
| R2 | GPIO 26 | System 2 Control |
| R7 | GPIO 14 | Disk 1 Select |
| R8 | GPIO 15 | Disk 2 Select |
| R9 | GPIO 18 | Disk 1 Line |
| R10 | GPIO 23 | Disk 2 Line |
| R12 | GPIO 25 | Power Trigger |

---

## ⚡ Optocoupler Inputs — System Status

| Signal | GPIO Pin | Purpose |
|---|---|---|
| SYSTEM1_STATUS | GPIO 5 | Detects System 1 active state |
| SYSTEM2_STATUS | GPIO 6 | Detects System 2 active state |

---

## 💽 Disk Detection Sensors

| Signal | GPIO Pin | Maps To |
|---|---|---|
| SYS1_DISK1 | GPIO 21 | System 1 — Disk 1 |
| SYS1_DISK2 | GPIO 16 | System 1 — Disk 2 |
| SYS2_DISK1 | GPIO 20 | System 2 — Disk 1 |
| SYS2_DISK2 | GPIO 12 | System 2 — Disk 2 |

---

## ⚙️ Logic Notes

| Rule | Detail |
|---|---|
| Relay logic | Active LOW — relay triggers when GPIO goes LOW |
| Optocoupler default | `GPIO.LOW` at idle |
| Pull configuration | Dynamic — set based on active state at runtime |
| Disk switching | **Blocked while system is powering ON** |
| LOCAL mode | Overrides remote control if manual switching is detected |

---

## 🗺️ Full Pin Reference

```
Raspberry Pi 3B+
─────────────────────────────────────
GPIO 2   →  R3   System1 Disk1 Select
GPIO 3   →  R4   System1 Disk2 Select
GPIO 4   →  R5   System1 Disk1 Line
GPIO 5   →  SYSTEM1_STATUS (Optocoupler IN)
GPIO 6   →  SYSTEM2_STATUS (Optocoupler IN)
GPIO 12  →  SYS2_DISK2    (Disk Detect)
GPIO 14  →  R7   System2 Disk1 Select
GPIO 15  →  R8   System2 Disk2 Select
GPIO 16  →  SYS1_DISK2    (Disk Detect)
GPIO 17  →  R6   System1 Disk2 Line
GPIO 18  →  R9   System2 Disk1 Line
GPIO 19  →  R1   System1 Control
GPIO 20  →  SYS2_DISK1    (Disk Detect)
GPIO 21  →  SYS1_DISK1    (Disk Detect)
GPIO 23  →  R10  System2 Disk2 Line
GPIO 24  →  R11  System1 Power Trigger
GPIO 25  →  R12  System2 Power Trigger
GPIO 26  →  R2   System2 Control
─────────────────────────────────────
```

---

*Refer to wiring schematics in this folder for physical connection diagrams.*

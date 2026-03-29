\# Components List



\## 🧠 Core Controller

\- Raspberry Pi 3B+

\- MicroSD Card (Recommended: High endurance)



\---



\## ⚡ Relay Modules



\### System1

\- Relays Used: R1, R3, R4, R5, R6, R11

\- Controls:

&#x20; - Power Trigger (R11)

&#x20; - Disk Switching (R3–R6)



\### System2

\- Relays Used: R2, R7, R8, R9, R10, R12

\- Controls:

&#x20; - Power Trigger (R12)

&#x20; - Disk Switching (R7–R10)



\- Relay Type:

&#x20; - 5V Relay Modules with Optocoupler Isolation

&#x20; - Mix of 4-channel and 2-channel modules



\---



\## 🔌 Optocouplers (Feedback \& Isolation)



\### System Status Feedback

\- SYSTEM1\_STATUS → GPIO5

\- SYSTEM2\_STATUS → GPIO6



\### Disk Detection

\- System1:

&#x20; - Disk1 → GPIO21

&#x20; - Disk2 → GPIO16

\- System2:

&#x20; - Disk1 → GPIO20

&#x20; - Disk2 → GPIO12



\---



\## 🔘 Manual Control (Push Buttons)

\- Total: 8 Push Buttons

\- Functions:

&#x20; - Power ON/OFF

&#x20; - Disk Selection

&#x20; - Safety Trigger (double press logic)



\---



\## 💽 Controlled Hardware



\### System1

\- Motherboard (H81)

\- 2 × Hard Drives (ROM switching)



\### System2

\- Motherboard (H81)

\- 2 × Hard Drives (ROM switching)



\---



\## 🔋 Power \& Misc

\- 5V Power Supply (for relays and Pi)

\- Jumper Wires

\- Breadboard / Terminal Blocks

\- Cooling Fans (optional, controlled via relay logic)



\---



\## ⚙️ Design Notes

\- Relays operate in \*\*active LOW configuration\*\*

\- Optocouplers provide \*\*isolation and state feedback\*\*

\- System supports \*\*dual control modes\*\*:

&#x20; - Remote (Web Dashboard)

&#x20; - Local (Manual Switch Override)


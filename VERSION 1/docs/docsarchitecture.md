\# System Architecture



\## 🧠 Overview

This system is a dual-node hardware-software control platform built on a Raspberry Pi, designed to manage two independent computer systems (System1 and System2). It enables remote and manual control of system power and dynamic switching between multiple hard drives using GPIO-controlled relay modules.



\---



\## 🧩 Core Components



\### 1. Control Layer

\- Raspberry Pi 3B+

\- Handles GPIO operations, logic processing, and API communication



\### 2. Hardware Interface Layer

\- Relay Modules (Active LOW switching)

\- Optocouplers (Isolation + feedback)

\- Push Buttons (Manual override input)



\### 3. Software Layer

\- Backend: Flask + SocketIO

\- Frontend: Web dashboard (HTML/CSS/JS)

\- Real-time communication via WebSockets



\---



\## ⚙️ System Segmentation



\### System1

\- Controlled via relays: R1, R3–R6, R11

\- Supports:

&#x20; - Power control

&#x20; - Dual disk switching

&#x20; - Status feedback via optocouplers



\### System2

\- Controlled via relays: R2, R7–R10, R12

\- Supports:

&#x20; - Power control

&#x20; - Dual disk switching

&#x20; - Status feedback via optocouplers



\---



\## 🔁 Data \& Control Flow



User Input (Web UI / Buttons)

&#x20;       ↓

Flask Backend (API + Logic)

&#x20;       ↓

GPIO Control Layer

&#x20;       ↓

Relay Switching

&#x20;       ↓

Hardware Action (Power / Disk Change)



Feedback Loop:

Hardware → Optocouplers → GPIO Input → Backend → UI Update



\---



\## 🔄 Operating Modes



\### 1. Remote Mode

\- Controlled via web dashboard

\- Full access to switching and power control

\- Real-time monitoring enabled



\### 2. Local Mode (Override)

\- Triggered when manual disk switching is detected

\- Disables remote disk control

\- Ensures hardware safety and prevents conflicts



\---



\## 🔐 Safety Logic



\- Disk switching is \*\*blocked when system power is ON\*\*

\- LOCAL mode overrides remote commands

\- Relay switching includes delay to prevent hardware damage

\- System state is continuously monitored and updated



\---



\## 📡 Real-Time Monitoring



\- CPU, RAM, and storage stats via `psutil`

\- Network usage tracking

\- System state updates via SocketIO



\---



\## 🧪 Debug \& Testing



\- Manual relay testing endpoints

\- GPIO state inspection API

\- Terminal access via web interface



\---



\## 🚀 Scalability Notes



\- Modular relay mapping allows expansion

\- Additional systems can be added with extended GPIO or I/O expanders

\- Cloud integration possible for remote monitoring



\---



\## 📌 Summary



The architecture integrates embedded hardware control with a web-based interface, forming a hybrid system capable of reliable, safe, and flexible multi-system management. It combines real-time control, hardware isolation, and fail-safe mechanisms to ensure stable operation in both manual and remote modes.


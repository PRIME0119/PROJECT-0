<div align="center">
  <h1>🌌 DOMINUS</h1>
  <p><strong>Premium Dual System Controller & Hardware Switcher</strong></p>
  <p>
    A futuristic, Raspberry Pi-based web application providing full remote control over two independent motherboard systems, featuring physical hard-drive switching, live telemetry, and an integrated bash terminal.
  </p>
  <br />
</div>

## 💎 The "Ice Interactive" Experience

Dominus revolves around an **"Ice Interactive 3D"** aesthetic. Every element—from the frosted glass panels to the neon-lit toggles—is designed to feel like a premium, state-of-the-art native application. It's built with buttery-smooth responsiveness, scaling flawlessly whether you're managing systems from a desktop command center or your mobile phone.

---

## 📸 Interactive Showcase & User Guide

### 1. The Global Command Dashboard
📱 `[Main Menu]` ➡️ `[System 1 Card]` / `[System 2 Card]`
*Your central hub. The dark-mode dashboard is tailored with beautiful glassmorphism to provide critical telemetry at a glance.*
- **How to Use**: View all connected nodes simultaneously. Tap on specific system cards from the main menu to drill down into granular controls.

### 2. Dual System Granular Control (Node 1 & Node 2)
⚡ `[Power: ON]` | 🔴 `[Power: OFF]` | 💽 `[Select Disk 1]` | 💽 `[Select Disk 2]`
*Navigate to System 1 or System 2 for dedicated, hardware-level management.*
- **Powering On/Off**: Press the glowing **Power Button** to initiate a boot sequence or shutdown. A sleek confirmation dialog will appear. Press **"Yes"** to confirm the action, preventing any accidental power losses.
- **Disk Switching**: Located under the system storage section, you can hot-swap the active boot drive between **Disk 1** and **Disk 2** by toggling the respective buttons.
  - ⚠️ *Safety Lock*: The UI absolutely forbids hard drive switching while a system is actively powered `ON`. Ensure the system is powered down before selecting a different disk!

### 3. Live Telemetry & Heat Monitoring
📊 `[CPU: 45%]` | 🌡️ `[Temp: 55°C]` | 🧠 `[RAM: 2GB / 8GB]`
*Zero manual refreshing. Real-time stats are pushed directly to your dashboard.*
- **How to Use**: Simply sit back and monitor. CPU usage, RAM allocation, System Temperature, and Network Speeds automatically update in the background via Socket.IO, providing immediate visual feedback on hardware health.

### 4. Integrated Embedded Terminal
💻 `[Terminal Tab]` ➡️ `>_ Type command here...`
*A built-in, interactive bash terminal directly in the browser allowing deep-level root interaction without SSH.*
- **How to Use**: Tap the **Terminal** tab to bring up the command shell. Type your standard bash commands here. The intelligent interface automatically handles text wrapping and dynamically adjusts layout for mobile virtual keyboards.

### 5. Seamless Mobile Layouts
📱 `[Swipe Left/Right]` | 👆 `[Tap Buttons]`
*Mobile interfaces designed intentionally for effortless one-handed control.*
- **How to Use**: Swipe and tap naturally. Buttons are scaled to 70% bounds and perfectly spaced to prevent accidental overlapping. The robust glassmorphism design prevents any text clipping, even on small screens.

### 6. Hardware Relay Sync
⚙️ `[Click Disk 1]` ➡️ `[Physical Relay Clicks]` ➡️ `[UI Syncs Green]`
*Physical relay states reflected gorgeously within the digital space.*
- **How it Works**: When you trigger a command (like Disk Switching), the UI animations execute in perfect synchronization with the physical 12-channel relay block clicking on the hardware. 

### 7. Physical Override & Safety Lockouts
🛑 `[Safety Lock: ACTIVE]` (Manual Override Detected - Remote Controls Disabled)
*Hardware-first overrides for maximum data protection.*
- **How it Works**: Optocouplers monitor physical hardware switches. If a system is placed in "Local" mode manually by a technician, the web interface automatically detects it and instantly **locks out** remote disk toggles to prevent electrical shorts or corruption.

---

## 🗂️ File Structure & Architecture

Here is how the views are organized so you can navigate the project efficiently:

- 📄 **`app.py`**: The core Python Flask server handling internal API routes, Socket.IO real-time telemetry, terminal subprocess handling, and GPIO logic.
- 📄 **`index.html`**: The gorgeous landing page.
- 📄 **`login.html`**: Secure authentication gateway to prevent unauthorized system access.
- 📄 **`control.html`**: The primary administrative dashboard displaying at-a-glance telemetry alongside quick power controls for both systems.
- 📄 **`system1.html` & `system2.html`**: Dedicated granular nodes for specific systems. This is where you configure hard-drive switching.
- 📄 **`terminal.html`**: The interactive web-hosted terminal powered by WebSockets.
- 📄 **`tailwind.config.js`**: Core styling variables that power the custom color and 3D animation classes.

---

## ⚙️ Installation & Usage

### 1. Requirements

- Raspberry Pi (Any model running an active OS)
- Python 3.x
- Nginx or basic network exposure if accessing externally
- Required Python modules:
  `Flask`, `Flask-SocketIO`, `psutil`, `RPi.GPIO`

### 2. Setup

Clone the repository to your host device:

```bash
git clone https://github.com/yourusername/dominus-controller.git
cd dominus-controller
```

Install local dependencies:

```bash
pip install -r requirements.txt
```

### 3. Run the Server

```bash
python app.py
```

By default, the server runs on `0.0.0.0:5000`. Navigate to `http://<your-pi-ip>:5000` from any device on your network and enjoy your new command center.

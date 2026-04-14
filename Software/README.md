<div align="center">
  <h1>🌌 DOMINUS</h1>
  <p><strong>Premium Dual System Controller & Hardware Switcher</strong></p>
  <p>
    A futuristic, Raspberry Pi-based web application providing full remote control over two independent motherboard systems, featuring physical hard-drive switching, live telemetry, and an integrated bash terminal.
  </p>
  <br />
</div>

## 📸 Interface Preview

![Dashboard Control Panel](C:\Users\PRIME\.gemini\antigravity\brain\b1e59d69-e4c3-4c5b-8281-2f569d794db5\dashboard_preview_1776182350342.png)
*Sleek, responsive dark-mode dashboard tailored with glassmorphism to look incredible on any device.*

![Integrated Terminal Interface](C:\Users\PRIME\.gemini\antigravity\brain\b1e59d69-e4c3-4c5b-8281-2f569d794db5\terminal_preview_1776182374293.png)
*Built-in interactive terminal directly from the browser allowing deep level system interaction.*

## ✨ The Look and Feel

Dominus revolves around an **"Ice Interactive 3D"** aesthetic. Expect heavy use of soft blur gradients, frosted glass panels (glassmorphism), neon highlights, and buttery-smooth responsiveness. The UI has been heavily optimized specifically to be touched; mobile device layouts gracefully scale and adapt, treating interactions like a premium native mobile application instead of just a standard web page.

## 🗂️ File Structure & Architecture

Here is how the views are organized so you can navigate the code efficiently:

- 📄 **`app.py`**: The core Python Flask server handling internal API routes, Socket.IO real-time telemetry, terminal subprocess handling, and GPIO logic.
- 📄 **`index.html`**: The gorgeous landing page.
- 📄 **`login.html`**: Secure authentication gateway to prevent unauthorized system access.
- 📄 **`control.html`**: The primary administrative dashboard displaying at-a-glance telemetry (CPU, RAM, Temp, Network Speeds) alongside quick power controls for both systems.
- 📄 **`system1.html` & `system2.html`**: Dedicated granular nodes for specific systems. This is where you configure hard-drive switching (Disk 1 vs Disk 2).
- 📄 **`terminal.html`**: The interactive web-hosted terminal powered by WebSockets.
- 📄 **`tailwind.config.js`**: Core styling variables that power the custom color and animation classes.

## 🛠️ How it Works

Dominus manages hardware safely using a robust Python backend interfacing with Raspberry Pi GPIO pins:

1. **Safety First (Local vs. Remote)**: Hardware handles manual toggle inputs via optocouplers. If a system is placed in "Local" mode physically, the web interface automatically detects it and **locks** remote disk switching to prevent electrical shorts or corruption. 
2. **Hot-swap Protection**: The UI absolutely forbids hard drive switching while a system is actively powered `ON`.
3. **Live Socket Telemetry**: There's no manual refreshing. Temperature updates, network I/O speeds, and power states push directly to the clients using WebSockets (`socketio.emit`).
4. **Relay Logic**: Disk switching and system power states are physically handled by executing precise delays on a 12-channel relay block layout, triggered perfectly in-sync with the frosted glass toggle UI elements.

## ⚙️ Installation & Usage

### 1. Requirements

- Raspberry Pi (Any model running an active OS)
- Python 3.x
- Nginx or basic network exposure if accessing externally
- Required Python modules (listed in `requirements.txt`):
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
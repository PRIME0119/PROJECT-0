# app.py - Main application
from flask import Flask, render_template, request, redirect, url_for, session, jsonify
from flask_socketio import SocketIO, emit
import RPi.GPIO as GPIO
import threading
import time
import psutil
import os
import subprocess
import signal

app = Flask(__name__)
app.secret_key = 'your_very_secure_secret_key'
socketio = SocketIO(app,async_mode='threading')
# GPIO Setup
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

# Pin Definitions
RELAYS = {
    'R1': 19, 'R2': 26, 'R3': 2, 'R4': 3,
    'R5': 4, 'R6': 17, 'R7': 14, 'R8': 15,
    'R9': 18, 'R10': 23, 'R11': 24, 'R12': 25
}

OCTOS = {
    'SYSTEM1_STATUS': 5,
    'SYSTEM2_STATUS': 6
}

SENSORS = {
    'SYS1_DISK1': 21,
    'SYS1_DISK2': 16,
    'SYS2_DISK1': 20,
    'SYS2_DISK2': 12
}

INPUT_ACTIVE_STATE = {
    # If a disk opto is inverted, add it here, e.g.:
    # SENSORS['SYS1_DISK2']: GPIO.HIGH,
}

def setup_input(pin):
    active_state = INPUT_ACTIVE_STATE.get(pin, GPIO.LOW)
    pull = GPIO.PUD_DOWN if active_state == GPIO.HIGH else GPIO.PUD_UP
    GPIO.setup(pin, GPIO.IN, pull_up_down=pull)

# Initialize sensing pins
for pin in SENSORS.values():
    setup_input(pin)

# Initialize GPIO
for pin in RELAYS.values():
    GPIO.setup(pin, GPIO.OUT)
    GPIO.output(pin, GPIO.HIGH)  # Start with relays OFF

for pin in OCTOS.values():
    setup_input(pin)

# System State
system_state = {
    'system1': {
        'active': False,
        'disk': None,
        'power': False,
        'fan': False
    },
    'system2': {
        'active': False,
        'disk': None,
        'power': False,
        'fan': False
    }
}

# Authentication (simple for demo)
USERS = {'admin': 'password'}  # Change this in production!

# ======================================
# GPIO Control Functions
# ======================================
def set_relay(relay, state):
    pin = RELAYS[relay]
    GPIO.output(pin, GPIO.LOW if state else GPIO.HIGH)
    time.sleep(0.2)  # ← Must align with GPIO.output()

def opto_active(pin):
    """
    Optocoupler logic:
    Default ACTIVE = GPIO.LOW
    Override per-pin via INPUT_ACTIVE_STATE.
    """
    active_state = INPUT_ACTIVE_STATE.get(pin, GPIO.LOW)
    return GPIO.input(pin) == active_state

def detect_mode(system):
    if system == 'system1':
        disk1 = opto_active(SENSORS['SYS1_DISK1'])
        disk2 = opto_active(SENSORS['SYS1_DISK2'])
    else:
        disk1 = opto_active(SENSORS['SYS2_DISK1'])
        disk2 = opto_active(SENSORS['SYS2_DISK2'])

    # LOCAL mode if any disk opto is active (manual switch detected)
    if disk1 or disk2:
        return 'local'

    return 'remote'


# ======================================
# System Control Functions
# ======================================
def activate_system(system):
    # Only mark selection, NOT control
    socketio.emit('system_state', system_state)

@app.route('/api/select_disk/<system>/<disk>', methods=['GET', 'POST'])
def api_select_disk(system, disk):
    valid_systems = ['system1', 'system2']
    valid_disks = ['1', '2']

    if system in valid_systems and disk in valid_disks:

        # NEW — Block all disk switching if in LOCAL mode
        if system_state[system].get('mode') == 'local':
            return jsonify(status='locked', message='System in LOCAL mode')

        # Existing rule — Block switching while powered on
        if system_state[system]['power']:
            print(f"[LOCKED] Cannot switch disk while {system} is powered ON.")
            return jsonify(status='locked')

        # Disk relay switching logic remains the same:
        if system == 'system1':
            for relay in ['R3', 'R4', 'R5', 'R6']:
                set_relay(relay, False)
            if disk == '1':
                set_relay('R3', True)
                set_relay('R5', True)
            else:
                set_relay('R4', True)
                set_relay('R6', True)

        elif system == 'system2':
            for relay in ['R7', 'R8', 'R9', 'R10']:
                set_relay(relay, False)
            if disk == '1':
                set_relay('R7', True)
                set_relay('R9', True)
            else:
                set_relay('R8', True)
                set_relay('R10', True)

        system_state[system]['disk'] = disk
        socketio.emit('system_state', system_state)

        return jsonify(status='ok', selected=disk)

    return jsonify(status='error', message='Invalid system or disk')


# ======================================
# Flask Routes
# ======================================
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        if username in USERS and USERS[username] == password:
            session['logged_in'] = True
            return redirect(url_for('control_panel'))
        return render_template('login.html', error='Invalid username or password')
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    return redirect(url_for('index'))

@app.route('/control_panel')
def control_panel():
    if not session.get('logged_in'):
        return redirect(url_for('login'))
    return render_template('control.html')

@app.route('/system1')
def system1():
    if not session.get('logged_in'):
        return redirect(url_for('login'))
    return render_template('system1.html')

@app.route('/system2')
def system2():
    if not session.get('logged_in'):
        return redirect(url_for('login'))
    return render_template('system2.html')

@app.route('/terminal')
def terminal():
    if not session.get('logged_in'):
        return redirect(url_for('login'))
    return render_template('terminal.html')
    
    # ===== Add these new routes =====
@app.route('/test_relay/<relay>/<state>')
def test_relay(relay, state):
    """Test endpoint for relay control"""
    if relay in RELAYS:
        set_relay(relay, state == 'on')
        return f"Relay {relay} set to {state}"
    return "Invalid relay"

@app.route('/test_status')
def test_status():
    return jsonify({
        'system1_status': GPIO.input(OCTOS['SYSTEM1_STATUS']),
        'system2_status': GPIO.input(OCTOS['SYSTEM2_STATUS']),
        'gpio_state': {name: GPIO.input(pin) for name, pin in {**RELAYS, **OCTOS, **SENSORS}.items()}
    })

# ===== End of new routes =====

# ======================================
# API Endpoints
# ======================================
@app.route('/api/stats')
def get_stats():
    """Get system statistics for control panel"""
    cpu = psutil.cpu_percent(interval=None)
    mem = psutil.virtual_memory().percent
    disk = psutil.disk_usage('/').percent
    net = psutil.net_io_counters()
    
    return jsonify({
        'cpu': f'{cpu}%',
        'ram': f'{mem}%',
        'storage': f'{disk}%',
        'net_sent': f'{net.bytes_sent / (1024*1024):.1f} Mbps',
        'net_recv': f'{net.bytes_recv / (1024*1024):.1f} Mbps'
    })

@app.route('/api/select_system/<system>', methods=['GET', 'POST'])  # Changed here
def api_select_system(system):
    if system in ['system1', 'system2']:
        activate_system(system)
        return jsonify(status='ok')
    return jsonify(status='error', message='Invalid system')

@app.route('/api/toggle_power/<system>', methods=['POST'])
def api_toggle_power(system):
    if system_state[system]['mode'] == 'local':
        return jsonify(status='locked', message='System in LOCAL mode')

    relay = 'R11' if system == 'system1' else 'R12'

    if not system_state[system]['power']:
        set_relay(relay, True)
        time.sleep(1)
        set_relay(relay, False)
        return jsonify(status='on')

    else:
        set_relay(relay, True)
        time.sleep(5)
        set_relay(relay, False)
        return jsonify(status='off')


@app.route('/api/power_off/<system>', methods=['GET', 'POST'])
def api_power_off(system):
    if system not in ['system1', 'system2']:
        return jsonify(status='error', message='Invalid system')

    print(f"[DEBUG] Powering off ALL relays for {system}")

    if system == 'system1':
        relays_to_off = ['R1', 'R3', 'R4', 'R5', 'R6', 'R11']
    else:
        relays_to_off = ['R2', 'R7', 'R8', 'R9', 'R10', 'R12']

    for relay in relays_to_off:
        set_relay(relay, False)

    # Reset system state
    system_state[system]['active'] = False
    system_state[system]['disk'] = None
    system_state[system]['fan'] = False
    system_state[system]['power'] = False

    socketio.emit('system_state', system_state)

    return jsonify(status='ok')

@app.route('/api/system_state/<system>')
def api_system_state(system):
    if system in ['system1', 'system2']:
        return jsonify(system_state[system])
    return jsonify(status='error')

# ======================================
# SocketIO Events (Real-time updates)
# ======================================
@socketio.on('connect')
def handle_connect():
    emit('system_state', system_state)

# ======================================
# Terminal Handling
# ======================================
terminal_process = None

@socketio.on('terminal_input', namespace='/terminal')
def handle_terminal_input(data):
    global terminal_process
    if terminal_process and terminal_process.stdin:
        terminal_process.stdin.write(data['data'])
        terminal_process.stdin.flush()

@socketio.on('connect', namespace='/terminal')
def handle_terminal_connect():
    global terminal_process
    if terminal_process:
        terminal_process.terminate()
    
    # Start new bash process
    terminal_process = subprocess.Popen(
        ['bash'],
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        universal_newlines=True,
        bufsize=1,
        text=True
    )
    
    # Start thread to read stdout
    threading.Thread(target=forward_terminal_output, daemon=True).start()

def forward_terminal_output():
    while terminal_process and terminal_process.stdout:
        output = terminal_process.stdout.read(1)
        if output:
            socketio.emit('terminal_output', {'data': output}, namespace='/terminal')
        else:
            break

# ======================================
# Feedback Monitoring (GPIO7 / GPIO8)
# ======================================

def update_status_from_feedback():
    for system in ['system1', 'system2']:
        status_pin = OCTOS[f'{system.upper()}_STATUS']
        powered = opto_active(status_pin)
        system_state[system]['power'] = powered

        mode = detect_mode(system)
        system_state[system]['mode'] = mode

        if system == 'system1':
            d1 = opto_active(SENSORS['SYS1_DISK1'])
            d2 = opto_active(SENSORS['SYS1_DISK2'])
        else:
            d1 = opto_active(SENSORS['SYS2_DISK1'])
            d2 = opto_active(SENSORS['SYS2_DISK2'])

        print(
            f"[DBG] {system} | "
            f"POWER={powered} | "
            f"D1={d1} | "
            f"D2={d2} | "
            f"ACTIVE={system_state[system]['active']} | "
            f"MODE={mode}"
        )

        if mode == 'local':
            if d1:
                system_state[system]['disk'] = '1'
            elif d2:
                system_state[system]['disk'] = '2'

    socketio.emit('system_state', system_state)

def feedback_monitor():
    """Background thread to continuously check feedback pins"""
    while True:
        update_status_from_feedback()
        time.sleep(1)   # check every 1 second

# ======================================
# Main Execution
# ======================================
if __name__ == '__main__':
    # Start monitoring thread
    feedback_thread = threading.Thread(target=feedback_monitor, daemon=True)
    feedback_thread.start()
    
    try:
            socketio.run(app, host='0.0.0.0', port=5000, debug=True, use_reloader=False, allow_unsafe_werkzeug=True)
    finally:
        # Cleanup GPIO on exit
        GPIO.cleanup()
        if terminal_process:
            terminal_process.terminate()



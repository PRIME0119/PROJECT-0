// Real-time updates for control panel
function updateSystemStats() {
    fetch('/api/stats')
        .then(response => response.json())
        .then(data => {
            // Update all stats on the page
            document.getElementById('cpu-percent').textContent = data.cpu;
            document.getElementById('ram-percent').textContent = data.ram;
            document.getElementById('storage-percent').textContent = data.storage;
            document.getElementById('network-up').textContent = data.net_sent;
            document.getElementById('network-down').textContent = data.net_recv;
            
            // Update progress bars
            document.querySelector('#cpu-progress .progress-fill').style.width = data.cpu;
            document.querySelector('#ram-progress .progress-fill').style.width = data.ram;
            document.querySelector('#storage-progress .progress-fill').style.width = data.storage;
        });
}

// Initialize SocketIO connection
const socket = io();

// Handle system state updates
socket.on('system_state', function(state) {
    // Update UI based on state changes
    updateSystemUI(state);
});

// Update all system indicators
function updateSystemUI(state) {
    // System 1 indicators
    const system1Active = document.querySelector('#system1-btn .status-indicator');
    system1Active.className = state.system1.active ? 
        'status-indicator bg-green-500' : 'status-indicator bg-gray-500';
    
    // System 2 indicators
    const system2Active = document.querySelector('#system2-btn .status-indicator');
    system2Active.className = state.system2.active ? 
        'status-indicator bg-green-500' : 'status-indicator bg-gray-500';
}

// Start polling for stats
setInterval(updateSystemStats, 2000);
updateSystemStats(); // Initial call
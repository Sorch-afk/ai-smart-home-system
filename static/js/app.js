document.addEventListener('DOMContentLoaded', function() {
    refreshDashboard();
    loadDevices();
    loadScenes();
    refreshEnergy();
});

async function refreshDashboard() {
    try {
        const status = await fetch('/api/status').then(r => r.json());
        document.getElementById('total-devices').textContent = status.total_devices;
        document.getElementById('active-devices').textContent = status.active_devices;
        document.getElementById('scenes-count').textContent = status.scenes.length;

        const energy = await fetch('/api/energy').then(r => r.json());
        document.getElementById('energy-today').textContent = energy.total_energy_kwh;
    } catch (error) {
        console.error('Failed to refresh dashboard:', error);
    }
}

async function loadDevices() {
    try {
        const response = await fetch('/api/devices');
        const data = await response.json();
        const grid = document.getElementById('devices-grid');
        grid.innerHTML = '';

        const icons = {
            'light': '💡',
            'air_conditioner': '❄️',
            'fan': '🌀',
            'tv': '📺',
            'curtain': '🪟',
            'door_lock': '🔒',
            'camera': '📷',
            'sensor': '🌡️'
        };

        data.devices.forEach(device => {
            const card = document.createElement('div');
            card.className = 'device-card';
            card.innerHTML = `
                <div class="device-header">
                    <div class="device-icon">${icons[device.type] || '📱'}</div>
                    <div class="device-status ${device.is_on ? 'on' : 'off'}">
                        ${device.is_on ? '运行中' : '已关闭'}
                    </div>
                </div>
                <div class="device-info">
                    <h3>${device.name}</h3>
                    <p>房间: ${device.room} | 功率: ${device.power_w}W</p>
                </div>
                <div class="device-controls">
                    ${device.is_on
                        ? `<button class="btn-small btn-off" onclick="controlDevice('${device.name}', 'turn_off')">关闭</button>`
                        : `<button class="btn-small btn-on" onclick="controlDevice('${device.name}', 'turn_on')">开启</button>`
                    }
                </div>
            `;
            grid.appendChild(card);
        });
    } catch (error) {
        console.error('Failed to load devices:', error);
    }
}

async function controlDevice(deviceName, action) {
    try {
        const response = await fetch('/api/control', {
            method: 'POST',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify({device_name: deviceName, action: action})
        });
        const result = await response.json();
        if (result.success) {
            alert(result.message);
            loadDevices();
            refreshDashboard();
        }
    } catch (error) {
        console.error('Failed to control device:', error);
    }
}

async function loadScenes() {
    try {
        const response = await fetch('/api/scenes');
        const data = await response.json();
        const grid = document.getElementById('scenes-grid');
        grid.innerHTML = '';

        const sceneIcons = {
            '回家模式': '🏠',
            '离家模式': '🚪',
            '睡眠模式': '🌙'
        };

        data.scenes.forEach(scene => {
            const card = document.createElement('div');
            card.className = 'scene-card';
            card.innerHTML = `
                <h3>${sceneIcons[scene] || '🎬'} ${scene}</h3>
                <div class="scene-actions">
                    点击执行此场景
                </div>
                <button class="scene-btn" onclick="executeScene('${scene}')">执行场景</button>
            `;
            grid.appendChild(card);
        });
    } catch (error) {
        console.error('Failed to load scenes:', error);
    }
}

async function executeScene(sceneName) {
    try {
        const response = await fetch('/api/scene/execute', {
            method: 'POST',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify({scene_name: sceneName})
        });
        const result = await response.json();
        if (result.success) {
            alert(result.message);
            refreshDashboard();
        }
    } catch (error) {
        console.error('Failed to execute scene:', error);
    }
}

async function sendVoiceCommand() {
    const input = document.getElementById('voice-command');
    const command = input.value.trim();
    if (!command) return;

    const history = document.getElementById('voice-history');

    const userMsg = document.createElement('div');
    userMsg.className = 'voice-message user';
    userMsg.innerHTML = `<p>${escapeHtml(command)}</p>`;
    history.appendChild(userMsg);

    input.value = '';
    history.scrollTop = history.scrollHeight;

    try {
        const response = await fetch('/api/command', {
            method: 'POST',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify({command: command})
        });
        const result = await response.json();

        const systemMsg = document.createElement('div');
        systemMsg.className = 'voice-message system';

        if (result.success) {
            if (result.message) {
                systemMsg.innerHTML = `<p>${result.message}</p>`;
            } else if (result.energy) {
                systemMsg.innerHTML = `
                    <p>📊 能耗统计：</p>
                    <p>总用电: ${result.energy.total_energy_kwh} kWh</p>
                    <p>预计费用: ¥${result.energy.total_cost}</p>
                `;
            } else if (result.suggestions) {
                systemMsg.innerHTML = `
                    <p>💡 节能建议：</p>
                    <ul>
                        ${result.suggestions.map(s => `<li>${s}</li>`).join('')}
                    </ul>
                `;
            } else if (result.status) {
                systemMsg.innerHTML = `
                    <p>📱 设备状态：</p>
                    <p>总设备: ${result.status.total_devices}</p>
                    <p>运行中: ${result.status.active_devices}</p>
                `;
            }
        } else {
            systemMsg.innerHTML = `<p style="color: #FF5252;">${result.message}</p>`;
        }

        history.appendChild(systemMsg);
        history.scrollTop = history.scrollHeight;
    } catch (error) {
        const errorMsg = document.createElement('div');
        errorMsg.className = 'voice-message system';
        errorMsg.innerHTML = `<p style="color: #FF5252;">请求失败: ${error.message}</p>`;
        history.appendChild(errorMsg);
    }
}

function handleVoiceKeypress(event) {
    if (event.key === 'Enter') {
        sendVoiceCommand();
    }
}

async function refreshEnergy() {
    try {
        const energy = await fetch('/api/energy').then(r => r.json());
        document.getElementById('total-energy').textContent = energy.total_energy_kwh;
        document.getElementById('total-cost').textContent = '¥' + energy.total_cost;

        const deviceContainer = document.getElementById('device-energy');
        deviceContainer.innerHTML = '<h3>设备耗电详情</h3>';

        for (const [name, data] of Object.entries(energy.device_details)) {
            deviceContainer.innerHTML += `
                <div class="energy-device">
                    <span>${name}</span>
                    <span>${data.energy_kwh} kWh | ¥${data.estimated_cost}</span>
                </div>
            `;
        }

        const suggestions = await fetch('/api/energy/suggestions').then(r => r.json());
        const suggestionsList = document.getElementById('suggestions-list');
        suggestionsList.innerHTML = '';
        suggestions.suggestions.forEach(s => {
            suggestionsList.innerHTML += `<div class="suggestion">${s}</div>`;
        });
    } catch (error) {
        console.error('Failed to refresh energy:', error);
    }
}

function escapeHtml(text) {
    const div = document.createElement('div');
    div.textContent = text;
    return div.innerHTML;
}

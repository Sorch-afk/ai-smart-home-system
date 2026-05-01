let userName = localStorage.getItem('userName') || null;

document.addEventListener('DOMContentLoaded', function() {
    if (userName) {
        showWelcomeBack();
    }
    loadInitialGreeting();
    loadDevices();
    loadScenes();
    loadSidebar();
});

async function loadInitialGreeting() {
    try {
        const response = await fetch('/api/greeting');
        const data = await response.json();
        if (data.greeting) {
            document.getElementById('greeting-text').textContent = data.greeting;
        }
    } catch (error) {
        console.error('Failed to load greeting:', error);
    }
}

function showWelcomeBack() {
    document.getElementById('user-setup').style.display = 'none';
    document.getElementById('greeting-text').textContent = `欢迎回来，${userName}！`;
    addAIMessage(`嗨，${userName}！想我了吗？今天过得怎么样呀？😊`);
}

async function setUserName() {
    const nameInput = document.getElementById('user-name');
    const name = nameInput.value.trim();
    if (!name) return;

    userName = name;
    localStorage.setItem('userName', name);

    try {
        await fetch('/api/set-user', {
            method: 'POST',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify({name: name})
        });
    } catch (error) {
        console.error('Failed to set user:', error);
    }

    document.getElementById('user-setup').style.display = 'none';
    document.getElementById('greeting-text').textContent = `你好，${name}！`;
    addAIMessage(`你好呀，${name}！我是你的AI管家，以后就让我来照顾你吧！有什么需要随时告诉我哦~ 😊`);
}

async function sendChat() {
    const input = document.getElementById('chat-input');
    const message = input.value.trim();
    if (!message) return;

    input.value = '';
    addUserMessage(message);

    try {
        const response = await fetch('/api/chat', {
            method: 'POST',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify({message: message})
        });
        const data = await response.json();
        handleChatResponse(data);
        refreshSidebar();
    } catch (error) {
        addAIMessage('抱歉，我现在有点忙，请稍后再试~');
    }
}

function handleChatResponse(data) {
    let responseText = data.message || '';

    if (data.emotion_detected) {
        document.getElementById('emotion-indicator').textContent = `情感: ${data.emotion_detected}`;
        document.getElementById('emotion-indicator').style.background = '#FF6900';
    }

    if (data.executed_actions && data.executed_actions.length > 0) {
        responseText += '\n\n✅ 已执行：';
        data.executed_actions.forEach(action => {
            responseText += `\n• ${action.message}`;
        });
    }

    if (data.suggestions && data.suggestions.length > 0) {
        responseText += '\n\n💡 建议：';
        data.suggestions.forEach(s => {
            responseText += `\n• ${s}`;
        });
    }

    addAIMessage(responseText);
}

function quickChat(message) {
    document.getElementById('chat-input').value = message;
    sendChat();
}

function handleChatKeypress(event) {
    if (event.key === 'Enter') sendChat();
}

function addUserMessage(text) {
    const container = document.getElementById('chat-messages');
    const messageDiv = document.createElement('div');
    messageDiv.className = 'message user';
    messageDiv.innerHTML = `
        <div class="message-avatar">👤</div>
        <div class="message-content"><p>${escapeHtml(text)}</p></div>
    `;
    container.appendChild(messageDiv);
    container.scrollTop = container.scrollHeight;
}

function addAIMessage(text) {
    const container = document.getElementById('chat-messages');
    const messageDiv = document.createElement('div');
    messageDiv.className = 'message ai';
    messageDiv.innerHTML = `
        <div class="message-avatar">🤖</div>
        <div class="message-content"><p>${formatMessage(text)}</p></div>
    `;
    container.appendChild(messageDiv);
    container.scrollTop = container.scrollHeight;
}

async function loadDevices() {
    try {
        const response = await fetch('/api/devices');
        const data = await response.json();
        const grid = document.getElementById('devices-grid');
        grid.innerHTML = '';

        const icons = {'light': '💡', 'air_conditioner': '❄️', 'fan': '🌀', 'tv': '📺', 'curtain': '🪟', 'door_lock': '🔒', 'camera': '📷', 'sensor': '🌡️'};

        data.devices.forEach(device => {
            const card = document.createElement('div');
            card.className = 'device-card';
            card.innerHTML = `
                <div class="device-header">
                    <div class="device-icon">${icons[device.type] || '📱'}</div>
                    <div class="device-status ${device.is_on ? 'on' : 'off'}">${device.is_on ? '运行中' : '已关闭'}</div>
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
            addAIMessage(`✅ ${result.message}`);
            loadDevices();
            loadSidebar();
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

        data.scenes.forEach(scene => {
            const card = document.createElement('div');
            card.className = 'scene-card';
            card.innerHTML = `
                <h3>${scene.icon || '🎬'} ${Object.keys(scene)[0] === 'icon' ? '场景' : '场景'}</h3>
                <p>${scene.description || '智能场景'}</p>
                <button class="scene-btn" onclick="executeScene('${scene.name || Object.keys(scene)[0]}')">执行</button>
            `;
            grid.appendChild(card);
        });
    } catch (error) {
        console.error('Failed to load scenes:', error);
    }
}

async function executeScene(sceneName) {
    try {
        const response = await fetch('/api/scene', {
            method: 'POST',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify({scene_name: sceneName})
        });
        const result = await response.json();
        if (result.success) {
            addAIMessage(`✅ ${result.message}`);
            loadSidebar();
        }
    } catch (error) {
        console.error('Failed to execute scene:', error);
    }
}

async function loadSidebar() {
    try {
        const status = await fetch('/api/status').then(r => r.json());
        const deviceList = document.getElementById('device-status-list');
        deviceList.innerHTML = '';

        status.devices.slice(0, 5).forEach(device => {
            deviceList.innerHTML += `
                <div class="device-mini">
                    <span>${device.icon || '📱'} ${device.name}</span>
                    <span class="device-status ${device.is_on ? 'on' : 'off'}">${device.is_on ? '开' : '关'}</span>
                </div>
            `;
        });

        const scenesList = document.getElementById('quick-scenes');
        scenesList.innerHTML = '';
        status.scenes.forEach(scene => {
            scenesList.innerHTML += `
                <div class="scene-mini" onclick="executeScene('${scene}')">
                    🎬 ${scene}
                </div>
            `;
        });
    } catch (error) {
        console.error('Failed to load sidebar:', error);
    }
}

function refreshSidebar() {
    loadSidebar();
    loadDevices();
}

function formatMessage(text) {
    return text.replace(/\n/g, '<br>').replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>');
}

function escapeHtml(text) {
    const div = document.createElement('div');
    div.textContent = text;
    return div.innerHTML;
}

# 小米智能家居AI大脑 - 情感化AI管家

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python](https://img.shields.io/badge/Python-3.8%2B-blue)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.104-009688)](https://fastapi.tiangolo.com/)

## 项目简介

**小米智能家居AI大脑** 是一个具有情感化交互能力的智能家居AI管家系统。不同于传统的指令式控制，这个系统能够：

- **主动关心主人** - 回家时自动问候，每天问候语不重样
- **情感识别** - 从对话中感知你的情绪（开心、疲惫、热、冷、饿...）
- **智能建议** - 根据情绪主动询问是否需要调节设备
- **记忆学习** - 记住主人的名字、习惯和偏好

## 核心创新点

### 1. 情感化交互引擎

- 每日问候语自动变化（早/中/晚/夜间）
- 回家问候结合天气情况（热/冷/雨/晴）
- 情绪识别：开心、疲惫、压力大、冷、热、饿

### 2. 主动式关怀

- 当你说"今天好热啊" → AI会问"要不要我帮你把空调打开？调到多少度舒服呢？"
- 当你说"好累啊" → AI会关心"辛苦啦，要不要坐下来休息一会儿？"
- 当你说"我回来了" → AI会用不同的方式欢迎你回家

### 3. 记忆与学习

- 记住主人名字和作息时间
- 记录情绪历史，了解你的生活习惯
- 根据对话学习你的偏好

## 快速开始

### 安装依赖

```bash
pip install fastapi uvicorn pydantic python-multipart
```

### 启动服务

```bash
python main.py
```

浏览器打开: <http://localhost:8000>

## 对话示例

```
你: 我回来了
AI: 欢迎回来！今天有什么有趣的事情想和我分享吗？🤗
    我已经为你开好了灯和空调~

你: 今天好热啊
AI: 确实很热呢！要不要我帮你把空调打开？调到26度怎么样？
    要不要提前把空调打开？你大概什么时候到家呀？

你: 好累啊
AI: 辛苦啦！要不要坐下来休息一会儿？我帮你把家里调到最舒服的状态~
    累了一天了，要不要我帮你放松一下？开点轻音乐？
```

## 功能模块

| 模块                   | 说明             |
| -------------------- | -------------- |
| GreetingEngine       | 多场景问候语生成引擎     |
| MemoryEngine         | 短长期记忆管理        |
| AIConversationEngine | 情感识别+意图理解+回复生成 |
| SmartHomeBrain       | 设备控制+场景管理+能耗分析 |

## API接口

| 接口                | 方法   | 说明         |
| ----------------- | ---- | ---------- |
| `/api/chat`       | POST | AI对话（核心功能） |
| `/api/greeting`   | GET  | 获取当日问候     |
| `/api/home-event` | GET  | 触发回家事件     |
| `/api/control`    | POST | 控制设备       |
| `/api/scene`      | POST | 执行场景       |
| `/api/set-user`   | POST | 设置用户信息     |
| `/api/devices`    | GET  | 设备列表       |
| `/api/energy`     | GET  | 能耗分析       |

## 项目结构

```
├── smart_home_brain.py   # AI核心引擎（情感识别、记忆、对话）
├── main.py               # FastAPI后端服务
├── index.html            # 前端页面（对话式交互）
├── requirements.txt      # 依赖
└── static/
    ├── css/style.css     # 样式
    └── js/app.js         # 前端逻辑
```

#

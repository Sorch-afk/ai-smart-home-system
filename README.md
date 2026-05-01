# 智能家居AI大脑 - 情感化AI管家

> 🏠 一个具有情感化交互、知识问答、主动关怀的智能家居AI管家系统

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python](https://img.shields.io/badge/Python-3.8%2B-blue)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.104-009688)](https://fastapi.tiangolo.com/)

***

## 项目简介

**智能家居AI大脑** 是一个具有情感化交互能力的智能家居AI管家系统。不同于传统的指令式控制，这个系统能够像家人一样关心你、理解你、帮助你。

### 为什么这个项目与众不同？

| 传统智能家居 | AI大脑管家      |
| ------ | ----------- |
| 被动等待指令 | 主动关心和询问     |
| 固定回复   | 每天问候不重样     |
| 冷冰冰的机器 | 有温度的AI管家    |
| 只能控制设备 | 还能聊天、问答、讲笑话 |

***

## 核心功能

### 1. 情感化交互引擎 🤗

- **每日问候语自动变化** - 早/中/晚/夜间不同问候
- **回家问候** - 结合天气情况，每天不重样
- **情绪识别** - 开心、疲惫、压力大、冷、热、饿

### 2. 主动式关怀 💝

```
你: 今天好热啊
AI: 确实很热呢！要不要我帮你把空调打开？调到26度怎么样？
    要不要提前把空调打开？你大概什么时候到家呀？

你: 好累啊
AI: 辛苦啦！要不要坐下来休息一会儿？
    我帮你把家里调到最舒服的状态~
```

### 3. 知识问答 🔍

- ️ **天气查询** - "今天天气怎么样"
- 🍜 **食谱推荐** - "推荐今天的食谱"
- 💪 **健康贴士** - "有什么健康小贴士"
- 😂 **笑话** - "给我讲个笑话"
- **新闻** - "今天有什么新闻"
- 🎬 **电影推荐** - "推荐几部电影"
- ❓ **知识问答** - "什么是人工智能"

### 4. 记忆与学习

- 记住主人名字和作息时间
- 记录情绪历史，了解生活习惯
- 根据对话学习偏好

### 5. 智能家居控制 🏠

- 8+ 智能设备控制（灯、空调、风扇、电视、窗帘等）
- 4 预设场景（回家模式、离家模式、睡眠模式、观影模式）
- 实时能耗分析与节能建议

### 6. 大模型接入 🤖

- 支持接入 Qwen(通义千问)、Mimo 等主流大模型
- 自动回退到本地模式（无需API Key也能运行）
- 可配置首选模型，灵活切换

***

## 快速开始

### 安装依赖

```bash
pip install fastapi uvicorn pydantic python-multipart aiohttp python-dotenv
```

### 启动服务

```bash
python main.py
```

浏览器打开: http://localhost:8000

### 接入大模型（可选）

本项目支持接入真实的大模型API，让AI管家变得更聪明！

#### 步骤1：复制环境变量模板

```bash
cp .env.example .env
```

#### 步骤2：填入API Key

编辑 `.env` 文件，填入你想要使用的模型API Key：

**使用通义千问（推荐）：**
```bash
QWEN_API_KEY=sk-你的通义千问APIKey
PREFERRED_MODEL=qwen
```

获取Qwen API Key：访问 https://dashscope.aliyun.com/ 注册并创建API Key

**使用Mimo模型：**
```bash
MIMO_API_KEY=你的MimoAPIKey
PREFERRED_MODEL=mimo
```

#### 步骤3：重启服务

```bash
python main.py
```

#### 支持的模型

| 模型 | 说明 | 免费额度 |
|------|------|----------|
| qwen (通义千问) | 阿里达摩院大模型，中文理解能力强 | 新用户有免费token |
| mimo | 小米自研大模型 | 需申请 |
| local (默认) | 本地回退模式，无需API Key | 完全免费 |

#### 注意事项

- 如果API Key未配置或配置错误，系统会**自动回退到本地模式**
- 本地模式使用预设回复，功能有限但保证可用性
- 前端右上角会显示当前使用的模型名称

***

## 对话示例

```
你: 我回来了
AI: 欢迎回来！今天有什么有趣的事情想和我分享吗？🤗
    我已经为你开好了灯和空调~

你: 今天好热啊
AI: 确实很热呢！要不要我帮你把空调打开？调到26度怎么样？

你: 今天天气怎么样
AI: 今天天气晴朗，温度25-30度，空气质量良好...

你: 给我讲个笑话
AI: 为什么程序员总是分不清万圣节和圣诞节？
    因为 Oct 31 == Dec 25 😄
```

***

## 功能模块

| 模块                   | 说明                  |
| -------------------- | ------------------- |
| LLMRouter            | 大模型路由（Qwen/Mimo/本地） |
| KnowledgeEngine      | 知识搜索与问答引擎           |
| GreetingEngine       | 多场景问候语生成引擎          |
| MemoryEngine         | 短长期记忆管理             |
| AIConversationEngine | 情感识别+意图理解+回复生成      |
| SmartHomeBrain       | 设备控制+场景管理+能耗分析      |

## API接口

| 接口                | 方法   | 说明         |
| ----------------- | ---- | ---------- |
| `/api/chat`       | POST | AI对话（核心功能） |
| `/api/chat/llm`   | POST | 直接调用大模型    |
| `/api/greeting`   | GET  | 获取当日问候     |
| `/api/home-event` | GET  | 触发回家事件     |
| `/api/control`    | POST | 控制设备       |
| `/api/scene`      | POST | 执行场景       |
| `/api/set-user`   | POST | 设置用户信息     |
| `/api/devices`    | GET  | 设备列表       |
| `/api/energy`     | GET  | 能耗分析       |

## 项目结构

```
├── llm_integration.py    # 大模型接入（Qwen/Mimo）
├── smart_home_brain.py   # AI核心引擎（情感识别、记忆、对话、知识问答）
├── main.py               # FastAPI后端服务
├── index.html            # 前端页面（对话式交互）
├── requirements.txt      # 依赖
├── .env.example          # 环境变量模板
├── README.md             # 项目文档
└── static/
    ├── css/style.css     # 样式
    └── js/app.js         # 前端逻辑
```

## 优势？

本项目展示了大语言模型在智能家居场景的**真正价值**：

1. **自然语言理解** - 将口语化表达转化为设备控制意图
2. **情感计算** - 理解用户情绪并提供个性化关怀
3. **上下文推理** - 根据时间、天气、习惯做出智能决策
4. **主动交互** - 不再被动等待指令，而是主动关心和帮助
5. **知识服务** - 整合天气、健康、娱乐等多种信息服务
6. **多模型兼容** - 支持多种大模型API，灵活切换

这正是智能家居生态需要的AI能力！

## License

MIT License

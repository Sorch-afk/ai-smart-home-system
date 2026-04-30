# 小米智能家居AI大脑

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python](https://img.shields.io/badge/Python-3.8%2B-blue)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.104-009688)](https://fastapi.tiangolo.com/)
[![Xiaomi](https://img.shields.io/badge/Xiaomi-SmartHome-FF6900)](https://www.mi.com/)

## 项目简介

**小米智能家居AI大脑** 是一个基于AI的智能家庭管理系统，通过自然语言交互、智能场景自动化和能耗优化分析，为用户提供全屋智能解决方案。

### 核心创新点

- 🎯 **自然语言控制** - 用日常语言控制智能家居设备，无需复杂操作
- 🤖 **智能场景引擎** - AI自动生成和优化自动化场景规则
- 📊 **能耗分析与优化** - 实时监控用电，提供个性化节能建议
- 🏠 **多房间管理** - 支持不同房间设备的分类管理
- 📱 **实时状态监控** - Dashboard实时显示设备状态和能耗数据

### 为什么适合申请小米百亿Token？

本项目直接对接小米智能家居生态，展示了大语言模型在以下场景的应用价值：
- **自然语言理解** - 将用户口语化指令转化为设备控制命令
- **智能决策** - 基于用户习惯和环境数据自动生成场景规则
- **数据分析** - 能耗趋势分析和节能建议生成
- **上下文理解** - 理解复杂的复合指令和多轮对话

## 技术栈

- **后端**: FastAPI + Python 3.8+
- **前端**: HTML5 + CSS3 + JavaScript
- **架构**: RESTful API + 单页应用

## 快速开始

### 安装依赖

```bash
pip install -r requirements.txt
```

### 启动服务

```bash
python main.py
```

浏览器打开: http://localhost:8000

## API接口

| 接口 | 方法 | 描述 |
|------|------|------|
| `/api/status` | GET | 获取系统状态 |
| `/api/devices` | GET | 获取设备列表 |
| `/api/control` | POST | 控制设备 |
| `/api/scenes` | GET | 获取场景列表 |
| `/api/scene/execute` | POST | 执行场景 |
| `/api/command` | POST | 自然语言指令 |
| `/api/energy` | GET | 获取能耗数据 |
| `/api/energy/suggestions` | GET | 获取节能建议 |

## 功能演示

### 自然语言控制示例
- "打开客厅灯"
- "关闭空调"
- "打开回家模式"
- "查看用电情况"
- "给我一些节能建议"

### 预设场景
- **回家模式** - 自动开灯、开空调、关窗帘
- **离家模式** - 关闭所有设备、打开窗帘
- **睡眠模式** - 关闭客厅灯、开启风扇和空调睡眠温度

## 项目结构

```
├── main.py                    # FastAPI后端服务
├── smart_home_brain.py        # 智能家居核心逻辑
├── index.html                 # 前端页面
├── requirements.txt           # 依赖列表
├── README.md                  # 项目文档
└── static/
    ├── css/style.css          # 样式文件
    └── js/app.js              # 前端逻辑
```

## 未来扩展

- [ ] 接入真实小米IoT设备API
- [ ] 语音识别集成
- [ ] 用户习惯机器学习
- [ ] 天气数据联动
- [ ] 多用户权限管理
- [ ] Docker部署支持

## License

MIT License

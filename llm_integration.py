"""
LLM 集成模块 - 接入真实大模型API
支持: Qwen(通义千问), Xiaomi Mimo, 以及本地回退
"""
import os
import json
import random
from typing import Dict, Optional, List
from datetime import datetime


class LLMConfig:
    QWEN_API_KEY = os.getenv("QWEN_API_KEY", "")
    QWEN_BASE_URL = os.getenv("QWEN_BASE_URL", "https://dashscope.aliyuncs.com/compatible-mode/v1")
    QWEN_MODEL = os.getenv("QWEN_MODEL", "qwen-plus")

    MIMO_API_KEY = os.getenv("MIMO_API_KEY", "")
    MIMO_BASE_URL = os.getenv("MIMO_BASE_URL", "https://mimo.api.xiaomi.com/v1")
    MIMO_MODEL = os.getenv("MIMO_MODEL", "mimo-v2")

    PREFERRED_MODEL = os.getenv("PREFERRED_MODEL", "qwen")

    @classmethod
    def get_available_models(cls) -> List[str]:
        models = []
        if cls.QWEN_API_KEY:
            models.append("qwen")
        if cls.MIMO_API_KEY:
            models.append("mimo")
        return models if models else ["local"]


class QwenAPI:
    def __init__(self):
        self.api_key = LLMConfig.QWEN_API_KEY
        self.base_url = LLMConfig.QWEN_BASE_URL
        self.model = LLMConfig.QWEN_MODEL

    async def chat(self, messages: List[Dict], system_prompt: str = None) -> Dict:
        if not self.api_key:
            return {"success": False, "message": "Qwen API Key 未配置"}

        try:
            import aiohttp

            headers = {
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json"
            }

            if system_prompt:
                messages = [{"role": "system", "content": system_prompt}] + messages

            payload = {
                "model": self.model,
                "messages": messages,
                "temperature": 0.7,
                "max_tokens": 2048
            }

            url = f"{self.base_url}/chat/completions"

            async with aiohttp.ClientSession() as session:
                async with session.post(url, headers=headers, json=payload, timeout=30) as response:
                    if response.status == 200:
                        result = await response.json()
                        return {
                            "success": True,
                            "message": result["choices"][0]["message"]["content"],
                            "model": "qwen",
                            "tokens": result.get("usage", {})
                        }
                    else:
                        return {"success": False, "message": f"API错误: {response.status}"}

        except Exception as e:
            return {"success": False, "message": f"请求失败: {str(e)}"}


class MimoAPI:
    def __init__(self):
        self.api_key = LLMConfig.MIMO_API_KEY
        self.base_url = LLMConfig.MIMO_BASE_URL
        self.model = LLMConfig.MIMO_MODEL

    async def chat(self, messages: List[Dict], system_prompt: str = None) -> Dict:
        if not self.api_key:
            return {"success": False, "message": "Mimo API Key 未配置"}

        try:
            import aiohttp

            headers = {
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json"
            }

            if system_prompt:
                messages = [{"role": "system", "content": system_prompt}] + messages

            payload = {
                "model": self.model,
                "messages": messages,
                "temperature": 0.7,
                "max_tokens": 2048
            }

            url = f"{self.base_url}/chat/completions"

            async with aiohttp.ClientSession() as session:
                async with session.post(url, headers=headers, json=payload, timeout=30) as response:
                    if response.status == 200:
                        result = await response.json()
                        return {
                            "success": True,
                            "message": result["choices"][0]["message"]["content"],
                            "model": "mimo",
                            "tokens": result.get("usage", {})
                        }
                    else:
                        return {"success": False, "message": f"API错误: {response.status}"}

        except Exception as e:
            return {"success": False, "message": f"请求失败: {str(e)}"}


class LocalFallback:
    LOCAL_RESPONSES = {
        "累": "辛苦啦！要不要坐下来休息一会儿？我帮你把家里调到最舒服的状态~",
        "热": "确实很热呢！要不要我帮你把空调打开？调到26度怎么样？",
        "冷": "是有点冷呢！快进来暖和暖和，我帮你开暖气~",
        "饿": "饿了吗？要不要我帮你看看有什么可以吃的？或者叫个外卖？",
        "回家": "欢迎回家！今天辛苦啦，家里已经为你准备好舒适的环境了~",
        "开心": "听到你开心我也很高兴呢！有什么好事要和我分享吗？😊",
        "睡觉": "夜深了，早点休息哦！我已经帮你把卧室调到最佳睡眠温度了~ ",
        "默认": "嗯嗯，我在听呢，继续说~"
    }

    def chat(self, user_input: str) -> Dict:
        text = user_input.lower()

        for keyword, response in self.LOCAL_RESPONSES.items():
            if keyword in text:
                return {
                    "success": True,
                    "message": response,
                    "model": "local"
                }

        return {
            "success": True,
            "message": self.LOCAL_RESPONSES["默认"],
            "model": "local"
        }


class LLMRouter:
    def __init__(self):
        self.qwen = QwenAPI()
        self.mimo = MimoAPI()
        self.local = LocalFallback()
        self.available_models = LLMConfig.get_available_models()

    async def chat(self, user_input: str, model: str = None) -> Dict:
        if model is None:
            model = LLMConfig.PREFERRED_MODEL

        system_prompt = """你是一个智能家居AI管家，名叫"小智"。你的特点是：
1. 温暖贴心，像家人一样关心主人
2. 会主动询问和关心，不是被动回复
3. 回答简洁友好，带一些emoji表情
4. 能理解用户的情绪并作出回应

当前场景：智能家居控制对话"""

        messages = [{"role": "user", "content": user_input}]

        if model == "qwen":
            result = await self.qwen.chat(messages, system_prompt)
            if result["success"]:
                return result

        if model == "mimo":
            result = await self.mimo.chat(messages, system_prompt)
            if result["success"]:
                return result

        return self.local.chat(user_input)

    def get_model_info(self) -> Dict:
        return {
            "available_models": self.available_models,
            "preferred_model": LLMConfig.PREFERRED_MODEL,
            "qwen_configured": bool(LLMConfig.QWEN_API_KEY),
            "mimo_configured": bool(LLMConfig.MIMO_API_KEY)
        }

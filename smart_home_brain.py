"""
小米智能家居AI大脑 - 情感化智能交互引擎
具备主动关怀、个性化学习、情境感知的AI管家系统
"""
import os
import json
import random
from typing import List, Dict, Optional, Tuple
from datetime import datetime, timedelta
from enum import Enum
from dataclasses import dataclass, asdict, field


class Mood(Enum):
    HAPPY = "开心"
    TIRED = "疲惫"
    STRESSED = "压力大"
    RELAXED = "放松"
    EXCITED = "兴奋"
    COLD = "冷"
    HOT = "热"
    HUNGRY = "饿"


@dataclass
class UserProfile:
    name: str = "主人"
    nickname: str = ""
    work_schedule: str = "18:00"
    favorite_temperature: int = 26
    sleep_time: str = "23:00"
    wake_time: str = "07:30"
    preferences: Dict = field(default_factory=dict)
    memories: List[Dict] = field(default_factory=list)
    conversation_history: List[Dict] = field(default_factory=list)
    home_pattern: str = "18:00-19:00"
    mood_history: List[Dict] = field(default_factory=list)


class GreetingEngine:
    def __init__(self):
        self.greetings = {
            "morning": [
                "早上好呀，{name}！新的一天开始了，今天也要元气满满哦！☀️",
                "早安！今天天气不错，{name}要记得吃早餐呢！🥐",
                "早上好！昨晚睡得好吗？今天有什么计划吗？",
                "叮~新的一天开始啦！{name}今天也要开心哦！😊",
                "早安！已经为你准备好了今日的天气和日程，要看看吗？",
            ],
            "afternoon": [
                "下午好呀，{name}！工作辛苦啦，要不要休息一下？☕️",
                "午后好时光！{name}别忘了喝水哦~",
                "下午好！今天过得怎么样？有什么我能帮忙的吗？",
                "嘿！下午啦，距离下班又近了一步，加油！💪",
                "下午好！需要我放点轻音乐放松一下吗？",
            ],
            "evening": [
                "晚上好！辛苦一天了，欢迎回家，{name}！🏠",
                "{name}回来啦！家里已经为你调节好了舒适的温度~",
                "晚上好！今天过得开心吗？要不要先放松一下？",
                "欢迎回家！累了吧？我帮你准备了舒适的环境~",
                "晚上好呀！今天工作辛苦啦，好好休息一下吧！😊",
            ],
            "night": [
                "夜深了，{name}早点休息哦，晚安！🌙",
                "晚安！今天辛苦啦，明天又是美好的一天~",
                "该睡觉啦，{name}！我已经帮你把卧室调到最佳睡眠温度了~",
                "夜深人静，{name}早点休息吧，好梦！✨",
                "晚安！愿你做个好梦，明天见~",
            ]
        }

        self.home_greetings = [
            "欢迎回家，{name}！今天辛苦啦！我已经为你开好了灯和空调~🏠",
            "主人回来啦！想死你了！家里已经准备好舒适的环境咯！😊",
            "{name}欢迎回来！今天过得怎么样？先坐下休息一下吧~",
            "终于等到你回来啦！累不累？要不要先喝杯水？",
            "回家啦！外面天气怎么样？我帮你把家里调到最舒服的状态了~",
            "欢迎回来！今天有什么有趣的事情想和我分享吗？🤗",
            "你回来啦！我已经迫不及待想听你讲讲今天的故事了~",
            "{name}回来啦！辛苦一天了，让我来照顾你吧！✨",
        ]

        self.weather_based_greetings = {
            "hot": [
                "外面好热呀，{name}快进来凉快一下！空调已经开好了~❄️",
                "今天真是热得不行！{name}要多喝水哦，我已经帮你降温了~",
            ],
            "cold": [
                "外面好冷呀，{name}快进来暖和暖和！暖气已经开好了~🔥",
                "今天降温了，{name}要注意保暖哦！",
            ],
            "rainy": [
                "今天下雨了，{name}有没有淋湿呀？快换件干爽的衣服吧~☔️",
                "外面下雨啦，回来就好！家里暖暖和和的~",
            ],
            "sunny": [
                "今天天气真好呀，{name}心情也不错吧？☀️",
                "阳光明媚的一天！{name}回来啦，开心！😊",
            ]
        }

    def get_greeting(self, name: str, hour: int = None) -> str:
        if hour is None:
            hour = datetime.now().hour

        if 6 <= hour < 11:
            period = "morning"
        elif 11 <= hour < 14:
            period = "afternoon"
        elif 14 <= hour < 18:
            period = "afternoon"
        elif 18 <= hour < 22:
            period = "evening"
        else:
            period = "night"

        greetings = self.greetings[period]
        greeting = random.choice(greetings)
        return greeting.format(name=name)

    def get_home_greeting(self, name: str, weather: str = None) -> str:
        greeting = random.choice(self.home_greetings)
        greeting = greeting.format(name=name)

        if weather and weather in self.weather_based_greetings:
            weather_greeting = random.choice(self.weather_based_greetings[weather])
            greeting += "\n" + weather_greeting.format(name=name)

        return greeting


class MemoryEngine:
    def __init__(self):
        self.short_term_memory = []
        self.long_term_memory = {}

    def add_memory(self, topic: str, content: str, importance: float = 0.5):
        memory = {
            "topic": topic,
            "content": content,
            "importance": importance,
            "timestamp": datetime.now().isoformat(),
            "times_referenced": 0
        }
        self.short_term_memory.append(memory)
        self._consolidate_memory()

    def _consolidate_memory(self):
        for memory in self.short_term_memory:
            topic = memory["topic"]
            if topic not in self.long_term_memory:
                self.long_term_memory[topic] = []
            self.long_term_memory[topic].append(memory)

    def get_related_memories(self, topic: str, limit: int = 3) -> List[Dict]:
        memories = self.long_term_memory.get(topic, [])
        return sorted(memories, key=lambda x: x["importance"], reverse=True)[:limit]

    def get_user_preference(self, topic: str) -> Optional[str]:
        memories = self.get_related_memories(topic, 1)
        if memories:
            return memories[0]["content"]
        return None


class AIConversationEngine:
    def __init__(self):
        self.user_profile = UserProfile()
        self.memory = MemoryEngine()
        self.greeting_engine = GreetingEngine()
        self.emotion_keywords = {
            Mood.HAPPY: ["开心", "高兴", "棒", "好", "喜欢", "爱", "满意", "舒服", "不错"],
            Mood.TIRED: ["累", "疲惫", "辛苦", "困", "乏", "没精神"],
            Mood.STRESSED: ["压力", "烦", "焦虑", "紧张", "担心", "头痛", "忙"],
            Mood.HOT: ["热", "好热", "太热了", "出汗", "闷", "温度高"],
            Mood.COLD: ["冷", "好冷", "太冷了", "冻", "温度低"],
            Mood.HUNGRY: ["饿", "饿了", "肚子饿", "想吃", "没吃饭"],
        }

        self.device_suggestions = {
            Mood.HOT: {
                "devices": ["空调", "风扇"],
                "actions": ["turn_on"],
                "questions": [
                    "要不要我帮你把空调打开？调到多少度比较舒服呢？",
                    "这么热，我帮你开空调好不好？再开个小风扇？",
                    "要不要提前把空调打开？你大概什么时候到家呀？",
                ]
            },
            Mood.COLD: {
                "devices": ["空调", "暖气"],
                "actions": ["turn_on"],
                "questions": [
                    "要不要我把暖气打开？暖和你一下~",
                    "这么冷，我帮你把空调调到制热模式吧？",
                ]
            },
            Mood.TIRED: {
                "devices": ["灯", "风扇", "电视"],
                "actions": ["turn_on"],
                "questions": [
                    "累了一天了，要不要我帮你放松一下？开点轻音乐？",
                    "辛苦啦！要不要先躺下休息一会儿？我帮你把灯光调暗~",
                ]
            },
            Mood.HUNGRY: {
                "devices": ["灯"],
                "actions": ["turn_on"],
                "questions": [
                    "要不要我帮你看看有什么可以吃的？",
                    "饿了吧？要不要我帮你叫个外卖？或者帮你开灯做饭？",
                ]
            },
        }

    def set_user_name(self, name: str):
        self.user_profile.name = name

    def analyze_emotion(self, text: str) -> Optional[Mood]:
        text = text.lower()
        for mood, keywords in self.emotion_keywords.items():
            for keyword in keywords:
                if keyword in text:
                    return mood
        return None

    def extract_intentions(self, text: str) -> Dict:
        intentions = {
            "wants_device_control": False,
            "device_type": None,
            "action": None,
            "time_mentioned": None,
            "emotion": None,
        }

        device_map = {
            "灯": "客厅主灯",
            "空调": "空调主卧",
            "风扇": "智能风扇",
            "电视": "小米电视",
            "窗帘": "智能窗帘",
        }

        for keyword, device_name in device_map.items():
            if keyword in text:
                intentions["wants_device_control"] = True
                intentions["device_type"] = device_name
                break

        if "开" in text:
            intentions["action"] = "turn_on"
        elif "关" in text:
            intentions["action"] = "turn_off"

        time_keywords = ["几点", "什么时候", "多久", "分钟", "小时", "点"]
        for keyword in time_keywords:
            if keyword in text:
                intentions["time_mentioned"] = keyword
                break

        intentions["emotion"] = self.analyze_emotion(text)

        return intentions

    def generate_response(self, user_input: str, current_hour: int = None) -> Dict:
        if current_hour is None:
            current_hour = datetime.now().hour

        intentions = self.extract_intentions(user_input)
        emotion = intentions.get("emotion")

        response = {
            "message": "",
            "emotion_detected": emotion.value if emotion else None,
            "suggestions": [],
            "device_actions": [],
            "follow_up_questions": [],
            "memory_updated": False
        }

        if emotion and emotion in self.device_suggestions:
            suggestion = self.device_suggestions[emotion]
            question = random.choice(suggestion["questions"])
            response["follow_up_questions"].append(question)
            response["suggestions"].append(f"建议操作：{', '.join(suggestion['devices'])}")

        if intentions["wants_device_control"]:
            device = intentions["device_type"]
            action = intentions["action"]
            if device and action:
                response["device_actions"].append({
                    "device": device,
                    "action": action,
                    "auto_execute": False
                })
                response["message"] = f"好的，我准备帮你{ '打开' if action == 'turn_on' else '关闭' }{device}~"
                if action == "turn_on":
                    response["follow_up_questions"].append(f"需要我帮你调节到最舒适的状态吗？")
        elif emotion:
            name = self.user_profile.name
            emotion_responses = {
                Mood.HAPPY: f"听到你开心我也很高兴呢，{name}！有什么好事要和我分享吗？😊",
                Mood.TIRED: f"辛苦啦，{name}！要不要坐下来休息一会儿？我帮你把家里调到最舒服的状态~",
                Mood.STRESSED: f"别太有压力，{name}~ 要不要听听音乐放松一下？或者泡个热水澡？",
                Mood.HOT: f"确实很热呢！{name}要不要我帮你把空调打开？调到26度怎么样？",
                Mood.COLD: f"是有点冷呢！{name}快进来暖和暖和，我帮你开暖气~",
                Mood.HUNGRY: f"饿了吗，{name}？要不要我帮你看看冰箱里有什么？或者叫个外卖？",
            }
            response["message"] = emotion_responses.get(emotion, "我在听你说呢~")

            self.memory.add_memory(
                topic=f"emotion_{emotion.value}",
                content=f"用户在{datetime.now().strftime('%Y-%m-%d %H:%M')}感到{emotion.value}",
                importance=0.7
            )
            response["memory_updated"] = True
        else:
            name = self.user_profile.name
            general_responses = [
                f"嗯嗯，我在听呢，{name}继续说~",
                f"原来是这样呀，{name}还有什么想和我分享的吗？",
                f"我明白你的意思啦！有什么我能帮忙的吗？",
                f"{name}说得对！今天过得怎么样？",
                f"哈哈，{name}真有趣！还想聊点什么呢？",
            ]
            response["message"] = random.choice(general_responses)

        if response["follow_up_questions"]:
            response["message"] += "\n\n" + random.choice(response["follow_up_questions"])

        return response

    def generate_home_greeting(self, weather: str = None) -> str:
        return self.greeting_engine.get_home_greeting(self.user_profile.name, weather)

    def generate_daily_greeting(self, hour: int = None) -> str:
        return self.greeting_engine.get_greeting(self.user_profile.name, hour)

    def learn_preference(self, category: str, preference: str):
        self.user_profile.preferences[category] = preference
        self.memory.add_memory(
            topic=f"preference_{category}",
            content=preference,
            importance=0.8
        )

    def get_conversation_context(self) -> Dict:
        return {
            "user_name": self.user_profile.name,
            "recent_emotions": self.memory.get_related_memories("emotion", 5),
            "preferences": self.user_profile.preferences,
            "total_conversations": len(self.user_profile.conversation_history),
        }


class SmartHomeBrain:
    def __init__(self):
        self.devices: Dict[str, Dict] = {}
        self.scenes: Dict[str, Dict] = {}
        self.conversation_engine = AIConversationEngine()
        self._init_demo_devices()
        self._init_default_scenes()

    def _init_demo_devices(self):
        self.devices = {
            "客厅主灯": {
                "name": "客厅主灯",
                "type": "light",
                "room": "客厅",
                "power_w": 60,
                "is_on": False,
                "brightness": 0,
                "icon": "💡"
            },
            "空调主卧": {
                "name": "空调主卧",
                "type": "air_conditioner",
                "room": "主卧",
                "power_w": 1500,
                "is_on": False,
                "temperature": 26,
                "mode": "cool",
                "icon": "❄️"
            },
            "智能风扇": {
                "name": "智能风扇",
                "type": "fan",
                "room": "客厅",
                "power_w": 50,
                "is_on": False,
                "fan_speed": 0,
                "icon": "🌀"
            },
            "小米电视": {
                "name": "小米电视",
                "type": "tv",
                "room": "客厅",
                "power_w": 150,
                "is_on": False,
                "icon": "📺"
            },
            "智能窗帘": {
                "name": "智能窗帘",
                "type": "curtain",
                "room": "主卧",
                "power_w": 20,
                "is_on": False,
                "position": 0,
                "icon": "🪟"
            },
            "门锁": {
                "name": "门锁",
                "type": "door_lock",
                "room": "大门",
                "power_w": 5,
                "is_locked": True,
                "icon": "🔒"
            },
            "摄像头": {
                "name": "摄像头",
                "type": "camera",
                "room": "客厅",
                "power_w": 10,
                "is_on": False,
                "icon": "📷"
            },
            "温湿度传感器": {
                "name": "温湿度传感器",
                "type": "sensor",
                "room": "客厅",
                "power_w": 2,
                "temperature": 28,
                "humidity": 60,
                "icon": "🌡️"
            }
        }

    def _init_default_scenes(self):
        self.scenes = {
            "回家模式": {
                "icon": "🏠",
                "description": "自动开灯、开空调、关窗帘",
                "actions": [
                    {"device": "客厅主灯", "action": "turn_on", "params": {"brightness": 80}},
                    {"device": "空调主卧", "action": "turn_on", "params": {"temperature": 26}},
                    {"device": "智能窗帘", "action": "close", "params": {}},
                ]
            },
            "离家模式": {
                "icon": "🚪",
                "description": "关闭所有设备、打开窗帘",
                "actions": [
                    {"device": "客厅主灯", "action": "turn_off", "params": {}},
                    {"device": "空调主卧", "action": "turn_off", "params": {}},
                    {"device": "智能风扇", "action": "turn_off", "params": {}},
                    {"device": "智能窗帘", "action": "open", "params": {}},
                ]
            },
            "睡眠模式": {
                "icon": "🌙",
                "description": "关闭灯光、开启睡眠空调",
                "actions": [
                    {"device": "客厅主灯", "action": "turn_off", "params": {}},
                    {"device": "智能风扇", "action": "turn_on", "params": {"fan_speed": 2}},
                    {"device": "空调主卧", "action": "turn_on", "params": {"temperature": 28}},
                ]
            },
            "观影模式": {
                "icon": "🎬",
                "description": "调暗灯光、打开电视",
                "actions": [
                    {"device": "客厅主灯", "action": "turn_on", "params": {"brightness": 20}},
                    {"device": "小米电视", "action": "turn_on", "params": {}},
                    {"device": "智能窗帘", "action": "close", "params": {}},
                ]
            }
        }

    def get_device(self, name: str) -> Optional[Dict]:
        return self.devices.get(name)

    def control_device(self, name: str, action: str, params: Dict = None) -> Dict:
        device = self.get_device(name)
        if not device:
            return {"success": False, "message": f"设备 {name} 不存在"}

        if action == "turn_on":
            device["is_on"] = True
            if params:
                if "brightness" in params:
                    device["brightness"] = params["brightness"]
                if "temperature" in params:
                    device["temperature"] = params["temperature"]
                if "fan_speed" in params:
                    device["fan_speed"] = params["fan_speed"]
            return {"success": True, "message": f"{name} 已开启", "device": name}

        elif action == "turn_off":
            device["is_on"] = False
            return {"success": True, "message": f"{name} 已关闭", "device": name}

        elif action == "close":
            if device["type"] == "curtain":
                device["position"] = 100
                return {"success": True, "message": f"{name} 已关闭"}

        elif action == "open":
            if device["type"] == "curtain":
                device["position"] = 0
                return {"success": True, "message": f"{name} 已打开"}

        return {"success": False, "message": "未知操作"}

    def execute_scene(self, name: str) -> Dict:
        scene = self.scenes.get(name)
        if not scene:
            return {"success": False, "message": f"场景 {name} 不存在"}

        results = []
        for action in scene["actions"]:
            result = self.control_device(action["device"], action["action"], action.get("params", {}))
            results.append(result)

        return {"success": True, "message": f"场景 {name} 执行完成", "results": results}

    def process_conversation(self, user_input: str) -> Dict:
        result = self.conversation_engine.generate_response(user_input)

        if result.get("device_actions"):
            for action in result["device_actions"]:
                device_result = self.control_device(
                    action["device"],
                    action["action"]
                )
                if device_result["success"]:
                    result["executed_actions"] = result.get("executed_actions", [])
                    result["executed_actions"].append(device_result)

        return result

    def trigger_home_event(self, weather: str = None) -> Dict:
        greeting = self.conversation_engine.generate_home_greeting(weather)
        return {
            "type": "home_arrival",
            "greeting": greeting,
            "auto_actions": [
                "已为你开灯",
                "已调节空调到舒适温度",
                "已为你准备好舒适的环境"
            ]
        }

    def calculate_energy(self) -> Dict:
        total = 0
        device_energy = {}

        for name, device in self.devices.items():
            if device.get("is_on", False):
                energy_kwh = (device["power_w"] * 24) / 1000
                total += energy_kwh
                device_energy[name] = {
                    "energy_kwh": round(energy_kwh, 2),
                    "power_w": device["power_w"],
                    "estimated_cost": round(energy_kwh * 0.6, 2)
                }

        return {
            "total_energy_kwh": round(total, 2),
            "total_cost": round(total * 0.6, 2),
            "device_details": device_energy
        }

    def get_energy_suggestions(self) -> List[str]:
        suggestions = []
        energy = self.calculate_energy()

        for name, data in energy["device_details"].items():
            if data["energy_kwh"] > 10:
                suggestions.append(f"{name} 耗电量较高 ({data['energy_kwh']}kWh)，建议适当调节")

        if energy["total_energy_kwh"] > 30:
            suggestions.append("今日总用电量较高，建议开启节能模式")

        if not suggestions:
            suggestions.append("当前用电情况良好，继续保持！")

        return suggestions

    def get_status(self) -> Dict:
        devices_status = []
        for name, device in self.devices.items():
            devices_status.append({
                "name": device["name"],
                "type": device["type"],
                "room": device["room"],
                "is_on": device.get("is_on", False),
                "power_w": device["power_w"],
                "icon": device.get("icon", "📱")
            })

        return {
            "devices": devices_status,
            "scenes": list(self.scenes.keys()),
            "total_devices": len(self.devices),
            "active_devices": sum(1 for d in self.devices.values() if d.get("is_on", False))
        }

    def set_user_profile(self, name: str, work_schedule: str = None):
        self.conversation_engine.set_user_name(name)
        if work_schedule:
            self.conversation_engine.user_profile.work_schedule = work_schedule

    def get_daily_greeting(self, hour: int = None) -> str:
        return self.conversation_engine.generate_daily_greeting(hour)

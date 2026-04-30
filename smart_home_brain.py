import os
import json
from typing import List, Dict, Optional
from datetime import datetime, timedelta
from enum import Enum
from dataclasses import dataclass, asdict


class DeviceType(Enum):
    LIGHT = "light"
    AC = "air_conditioner"
    FAN = "fan"
    TV = "tv"
    CURTAIN = "curtain"
    DOOR = "door_lock"
    CAMERA = "camera"
    SENSOR = "sensor"


class DeviceState:
    def __init__(self, name: str, device_type: DeviceType, room: str, power_w: float):
        self.name = name
        self.device_type = device_type
        self.room = room
        self.is_on = False
        self.power_w = power_w
        self.brightness = 0
        self.temperature = 0
        self.fan_speed = 0
        self.last_modified = datetime.now()


class SmartHomeBrain:
    def __init__(self):
        self.devices: Dict[str, DeviceState] = {}
        self.scenes: Dict[str, Dict] = {}
        self.user_habits: Dict[str, List] = {}
        self.energy_history: List[Dict] = []
        self._init_demo_devices()
        self._init_default_scenes()

    def _init_demo_devices(self):
        self.add_device("客厅主灯", DeviceType.LIGHT, "客厅", 60)
        self.add_device("空调主卧", DeviceType.AC, "主卧", 1500)
        self.add_device("智能风扇", DeviceType.FAN, "客厅", 50)
        self.add_device("小米电视", DeviceType.TV, "客厅", 150)
        self.add_device("智能窗帘", DeviceType.CURTAIN, "主卧", 20)
        self.add_device("门锁", DeviceType.DOOR, "大门", 5)
        self.add_device("摄像头", DeviceType.CAMERA, "客厅", 10)
        self.add_device("温湿度传感器", DeviceType.SENSOR, "客厅", 2)

    def _init_default_scenes(self):
        self.create_scene("回家模式", [
            {"device": "客厅主灯", "action": "turn_on", "params": {"brightness": 80}},
            {"device": "空调主卧", "action": "turn_on", "params": {"temperature": 26}},
            {"device": "智能窗帘", "action": "close", "params": {}},
        ])
        self.create_scene("离家模式", [
            {"device": "客厅主灯", "action": "turn_off", "params": {}},
            {"device": "空调主卧", "action": "turn_off", "params": {}},
            {"device": "智能风扇", "action": "turn_off", "params": {}},
            {"device": "智能窗帘", "action": "open", "params": {}},
        ])
        self.create_scene("睡眠模式", [
            {"device": "客厅主灯", "action": "turn_off", "params": {}},
            {"device": "智能风扇", "action": "turn_on", "params": {"fan_speed": 2}},
            {"device": "空调主卧", "action": "turn_on", "params": {"temperature": 28}},
        ])

    def add_device(self, name: str, device_type: DeviceType, room: str, power_w: float):
        self.devices[name] = DeviceState(name, device_type, room, power_w)

    def get_device(self, name: str) -> Optional[DeviceState]:
        return self.devices.get(name)

    def get_devices_by_room(self, room: str) -> List[DeviceState]:
        return [d for d in self.devices.values() if d.room == room]

    def get_devices_by_type(self, device_type: DeviceType) -> List[DeviceState]:
        return [d for d in self.devices.values() if d.device_type == device_type]

    def control_device(self, name: str, action: str, params: Dict = None):
        device = self.get_device(name)
        if not device:
            return {"success": False, "message": f"设备 {name} 不存在"}

        device.last_modified = datetime.now()

        if action == "turn_on":
            device.is_on = True
            if params:
                if "brightness" in params:
                    device.brightness = params["brightness"]
                if "temperature" in params:
                    device.temperature = params["temperature"]
                if "fan_speed" in params:
                    device.fan_speed = params["fan_speed"]
            return {"success": True, "message": f"{name} 已开启", "device": name}

        elif action == "turn_off":
            device.is_on = False
            return {"success": True, "message": f"{name} 已关闭", "device": name}

        elif action == "set_brightness":
            device.brightness = params.get("brightness", 50)
            return {"success": True, "message": f"{name} 亮度设置为 {device.brightness}%"}

        elif action == "set_temperature":
            device.temperature = params.get("temperature", 26)
            return {"success": True, "message": f"{name} 温度设置为 {device.temperature}°C"}

        elif action == "set_fan_speed":
            device.fan_speed = params.get("fan_speed", 3)
            return {"success": True, "message": f"{name} 风速设置为 {device.fan_speed} 档"}

        return {"success": False, "message": "未知操作"}

    def create_scene(self, name: str, actions: List[Dict]):
        self.scenes[name] = {"actions": actions, "created_at": datetime.now().isoformat()}

    def execute_scene(self, name: str):
        scene = self.scenes.get(name)
        if not scene:
            return {"success": False, "message": f"场景 {name} 不存在"}

        results = []
        for action in scene["actions"]:
            result = self.control_device(action["device"], action["action"], action.get("params", {}))
            results.append(result)

        self.user_habits.setdefault(name, []).append(datetime.now().isoformat())

        return {"success": True, "message": f"场景 {name} 执行完成", "results": results}

    def calculate_energy(self, hours: int = 24) -> Dict:
        total = 0
        device_energy = {}

        for name, device in self.devices.items():
            if device.is_on:
                energy_kwh = (device.power_w * hours) / 1000
                total += energy_kwh
                device_energy[name] = {
                    "energy_kwh": round(energy_kwh, 2),
                    "power_w": device.power_w,
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
            device = self.get_device(name)
            if device and data["energy_kwh"] > 10:
                suggestions.append(f"{name} 耗电量较高 ({data['energy_kwh']}kWh)，建议降低功率或减少使用时间")

        if energy["total_energy_kwh"] > 30:
            suggestions.append("今日总用电量较高，建议开启节能模式")

        if not suggestions:
            suggestions.append("当前用电情况良好，继续保持！")

        return suggestions

    def get_status(self) -> Dict:
        devices_status = []
        for name, device in self.devices.items():
            devices_status.append({
                "name": device.name,
                "type": device.device_type.value,
                "room": device.room,
                "is_on": device.is_on,
                "power_w": device.power_w
            })

        return {
            "devices": devices_status,
            "scenes": list(self.scenes.keys()),
            "total_devices": len(self.devices),
            "active_devices": sum(1 for d in self.devices.values() if d.is_on)
        }

    def natural_language_command(self, command: str) -> Dict:
        command = command.lower()

        device_map = {
            "灯": "客厅主灯",
            "空调": "空调主卧",
            "风扇": "智能风扇",
            "电视": "小米电视",
            "窗帘": "智能窗帘"
        }

        for keyword, device_name in device_map.items():
            if keyword in command:
                if "开" in command:
                    return self.control_device(device_name, "turn_on")
                elif "关" in command:
                    return self.control_device(device_name, "turn_off")
                elif "亮度" in command:
                    if "最大" in command or "100" in command:
                        return self.control_device(device_name, "set_brightness", {"brightness": 100})
                    elif "最小" in command or "0" in command:
                        return self.control_device(device_name, "set_brightness", {"brightness": 0})
                    else:
                        return self.control_device(device_name, "set_brightness", {"brightness": 50})
                elif "温度" in command:
                    temp = 26
                    if "25" in command:
                        temp = 25
                    elif "27" in command:
                        temp = 27
                    elif "28" in command:
                        temp = 28
                    return self.control_device(device_name, "set_temperature", {"temperature": temp})

        scene_map = {
            "回家": "回家模式",
            "离家": "离家模式",
            "睡觉": "睡眠模式",
            "睡眠": "睡眠模式"
        }

        for keyword, scene_name in scene_map.items():
            if keyword in command:
                return self.execute_scene(scene_name)

        if "用电" in command or "能耗" in command:
            return {"success": True, "energy": self.calculate_energy()}

        if "建议" in command:
            return {"success": True, "suggestions": self.get_energy_suggestions()}

        if "状态" in command:
            return {"success": True, "status": self.get_status()}

        return {"success": False, "message": "无法理解指令，请重试"}

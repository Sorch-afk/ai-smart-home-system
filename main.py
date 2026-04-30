from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse, JSONResponse
from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime
import json

from smart_home_brain import SmartHomeBrain, DeviceType

app = FastAPI(title="Xiaomi Smart Home AI Brain", version="1.0.0")

app.mount("/static", StaticFiles(directory="static"), name="static")

brain = SmartHomeBrain()

class DeviceControlRequest(BaseModel):
    device_name: str
    action: str
    params: dict = {}

class SceneRequest(BaseModel):
    scene_name: str

class CommandRequest(BaseModel):
    command: str

class SceneCreateRequest(BaseModel):
    name: str
    actions: list

@app.get("/", response_class=HTMLResponse)
async def read_root():
    with open("index.html", "r", encoding="utf-8") as f:
        return f.read()

@app.get("/api/status")
async def get_status():
    return brain.get_status()

@app.post("/api/control")
async def control_device(request: DeviceControlRequest):
    result = brain.control_device(request.device_name, request.action, request.params)
    return result

@app.post("/api/scene/execute")
async def execute_scene(request: SceneRequest):
    result = brain.execute_scene(request.scene_name)
    return result

@app.post("/api/scene/create")
async def create_scene(request: SceneCreateRequest):
    brain.create_scene(request.name, request.actions)
    return {"success": True, "message": f"场景 {request.name} 创建成功"}

@app.post("/api/command")
async def natural_language_command(request: CommandRequest):
    result = brain.natural_language_command(request.command)
    return result

@app.get("/api/energy")
async def get_energy():
    return brain.calculate_energy()

@app.get("/api/energy/suggestions")
async def get_energy_suggestions():
    suggestions = brain.get_energy_suggestions()
    return {"suggestions": suggestions}

@app.get("/api/devices")
async def get_devices():
    devices = []
    for name, device in brain.devices.items():
        devices.append({
            "name": device.name,
            "type": device.device_type.value,
            "room": device.room,
            "is_on": device.is_on,
            "power_w": device.power_w,
            "brightness": device.brightness,
            "temperature": device.temperature,
            "fan_speed": device.fan_speed
        })
    return {"devices": devices}

@app.get("/api/scenes")
async def get_scenes():
    return {"scenes": list(brain.scenes.keys())}

@app.get("/api/health")
async def health_check():
    return {
        "status": "healthy",
        "service": "Xiaomi Smart Home AI Brain",
        "version": "1.0.0",
        "devices_count": len(brain.devices),
        "active_devices": sum(1 for d in brain.devices.values() if d.is_on)
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)

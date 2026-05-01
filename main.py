from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse, JSONResponse
from pydantic import BaseModel
from typing import Optional
from datetime import datetime

from smart_home_brain import SmartHomeBrain

app = FastAPI(title="小米智能家居AI大脑", version="2.0.0")

app.mount("/static", StaticFiles(directory="static"), name="static")

brain = SmartHomeBrain()

class ChatMessage(BaseModel):
    message: str

class DeviceControl(BaseModel):
    device_name: str
    action: str
    params: dict = {}

class SceneExecute(BaseModel):
    scene_name: str

class UserProfile(BaseModel):
    name: str
    work_schedule: Optional[str] = None

@app.get("/", response_class=HTMLResponse)
async def index():
    with open("index.html", "r", encoding="utf-8") as f:
        return f.read()

@app.post("/api/chat")
async def chat(request: ChatMessage):
    result = brain.process_conversation(request.message)
    return result

@app.post("/api/control")
async def control(request: DeviceControl):
    return brain.control_device(request.device_name, request.action, request.params)

@app.post("/api/scene")
async def execute_scene(request: SceneExecute):
    return brain.execute_scene(request.scene_name)

@app.get("/api/status")
async def status():
    return brain.get_status()

@app.get("/api/devices")
async def devices():
    devices_list = []
    for name, device in brain.devices.items():
        devices_list.append(device)
    return {"devices": devices_list}

@app.get("/api/scenes")
async def scenes():
    return {"scenes": list(brain.scenes.values())}

@app.get("/api/greeting")
async def greeting():
    hour = datetime.now().hour
    return {"greeting": brain.get_daily_greeting(hour)}

@app.get("/api/home-event")
async def home_event(weather: Optional[str] = None):
    return brain.trigger_home_event(weather)

@app.get("/api/energy")
async def energy():
    return brain.calculate_energy()

@app.get("/api/energy/suggestions")
async def energy_suggestions():
    return {"suggestions": brain.get_energy_suggestions()}

@app.post("/api/set-user")
async def set_user(profile: UserProfile):
    brain.set_user_profile(profile.name, profile.work_schedule)
    return {"success": True, "message": f"你好，{profile.name}！我已经记住你了~"}

@app.get("/api/context")
async def get_context():
    return brain.conversation_engine.get_conversation_context()

@app.get("/api/health")
async def health():
    return {
        "status": "healthy",
        "service": "小米智能家居AI大脑",
        "version": "2.0.0",
        "features": ["情感识别", "主动关怀", "记忆学习", "情境感知"]
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)

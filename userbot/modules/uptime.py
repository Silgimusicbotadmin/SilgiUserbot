import time
import json
import os
from userbot.events import register
from userbot import SILGI_USER
UPTIME_FILE = "uptime.json"
def load_start_time():
    if os.path.exists(UPTIME_FILE):
        with open(UPTIME_FILE, "r") as f:
            data = json.load(f)
            return data.get("start_time", time.time())
    return time.time()
def save_start_time(start_time):
    with open(UPTIME_FILE, "w") as f:
        json.dump({"start_time": start_time}, f)
START_TIME = load_start_time()
if START_TIME == 0:
    START_TIME = time.time()
    save_start_time(START_TIME)
@register(outgoing=True, pattern="^.uptime$")
async def uptime_handler(event):
    current_time = time.time()
    uptime_seconds = int(current_time - START_TIME)
    
    hours = uptime_seconds // 3600
    minutes = (uptime_seconds % 3600) // 60
    seconds = uptime_seconds % 60

    await event.edit(f"**Sahibim {SILGI_USER}\nUserbot işləmə müddəti:**\n `{hours} saat, {minutes} dəqiqə, {seconds} saniyə`")
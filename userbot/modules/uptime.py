import time
from userbot.events import register
from userbot import StartTime, SILGI_USER
@register(outgoing=True, pattern="^.uptime$")
async def uptime_handler(event):
    current_time = time.time()
    uptime_seconds = int(current_time - StartTime)
    hours = uptime_seconds // 3600
    minutes = (uptime_seconds % 3600) // 60
    seconds = uptime_seconds % 60
    await event.edit(f"**Sahibim {SILGI_USER}\nUserbot işləmə müddəti:** `{hours} saat, {minutes} dəqiqə, {seconds} saniyə`")
import time
from userbot.events import register
from userbot import SILGI_USER, START_TIME
@register(outgoing=True, pattern="^.uptime$")
async def uptime_handler(event):
    current_time = time.time()
    uptime_seconds = int(current_time - START_TIME)
    
    hours = uptime_seconds // 3600
    minutes = (uptime_seconds % 3600) // 60
    seconds = uptime_seconds % 60

    await event.edit(f"**Sahibim: {SILGI_USER}\nSilgiUserbot'un işləmə müddəti:**\n `{hours} saat, {minutes} dəqiqə, {seconds} saniyə`")
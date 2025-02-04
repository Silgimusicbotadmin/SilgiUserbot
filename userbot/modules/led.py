import asyncio
from telethon.tl.functions.account import UpdateProfileRequest
from telethon.errors import FloodWaitError
from userbot.events import register
from userbot import bot
from userbot.cmdhelp import CmdHelp
led_running = False

@register(outgoing=True, pattern="^.led$")
async def led(event):
    global led_running
    if led_running:
        await event.edit("LED artıq işləyir!")
        return

    led_running = True
    user = await bot.get_me()
    original_last_name = user.last_name if user.last_name else ""
    base_name = original_last_name.strip()

    msg = await event.edit("LED başladı...")

    while led_running:
        try:
            await bot(UpdateProfileRequest(last_name=f"{base_name} 🔴🟢"))
            await asyncio.sleep(3)

            await bot(UpdateProfileRequest(last_name=f"{base_name} 🟢🔴"))
            await asyncio.sleep(3)

        except FloodWaitError as e:
            await event.edit(f"Flood aşkarlandı! {e.value} saniyə gözləyirəm...")
            await asyncio.sleep(e.value)

    
    await msg.edit("LED dayandırıldı.")

@register(outgoing=True, pattern="^.stopled$")
async def stop_led(event):
    global led_running
    if not led_running:
        await event.edit("LED işləmirdi!")
        return

    led_running = False
    await event.edit("LED dayandırılır...")

CmdHelp('led').add_command(
    'led', 'LED effektini soyadınıza əlavə edərək başladır.', '`.led` yazdıqda soyadınıza 🔴🟢 və 🟢🔴 effekti əlavə olunur.'
).add_command(
    'stopled', None, 'LED effektini dayandırır.'
).add()

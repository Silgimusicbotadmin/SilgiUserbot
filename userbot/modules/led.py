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
    original_first_name = user.first_name if user.first_name else ""
    
    base_name = original_first_name.strip()  

    msg = await event.edit("LED başlatıldı...")

    while led_running:
        try:
            new_first_name = f"{base_name} 🔴🟢"
            await bot(UpdateProfileRequest(first_name=new_first_name))
            await asyncio.sleep(7)

            new_first_name = f"{base_name} 🟢🔴"
            await bot(UpdateProfileRequest(first_name=new_first_name))
            await asyncio.sleep(7)

        except FloodWaitError as e:
            await event.edit(f"Flood aşkarlandı! {e.value} saniyə gözləyirəm...")
            await asyncio.sleep(e.value)

    await bot(UpdateProfileRequest(first_name=original_first_name))
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
    'led', 'LED effektini adınıza əlavə edərək başladır.', '`.led` yazdıqda adınızın sonuna 🔴🟢 və 🟢🔴 əlavə olunur.'
).add_command(
    'stopled', 'LED effektini dayandırır.', '`.stopled` yazdıqda ad əvvəlki vəziyyətinə qayıdır.'
).add()

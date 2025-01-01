import asyncio
from userbot.events import register
from userbot import BOTLOG_CHATID, bot
from userbot.cmdhelp import CmdHelp

automessage_task = None
EXCLUDED_GROUP_ID = -1002350520287

@register(outgoing=True, pattern=r'^\.automessage (\d+[smhd]) (.+)')
async def automessage(event):
    global automessage_task

    if automessage_task:
        await event.edit("Avtomatik mesaj artıq aktivdir. Dayandırmaq üçün `.autostop` yazın.")
        return

    time_input = event.pattern_match.group(1)
    message = event.pattern_match.group(2)

    time_multiplier = {"s": 1, "m": 60, "h": 3600, "d": 86400}
    time_labels = {"s": "saniyə", "m": "dəqiqə", "h": "saat", "d": "gün"}

    time_unit = time_input[-1]
    if time_unit not in time_multiplier:
        await event.edit("Yanlış zaman vahidi istifadə edildi. `s`, `m`, `h` və ya `d` istifadə edin.")
        return

    interval = int(time_input[:-1]) * time_multiplier[time_unit]
    readable_time = f"{time_input[:-1]} {time_labels[time_unit]}"

    await event.edit(f"Avtomatik mesaj aktivləşdirildi. Mesaj: `{message}` hər {readable_time} göndəriləcək.")

    async def send_message_to_all_groups():
        while True:
            async for dialog in bot.iter_dialogs():
                if dialog.is_group and dialog.id != EXCLUDED_GROUP_ID:
                    try:
                        await bot.send_message(dialog.id, message)
                    except Exception as e:
                        print(f"Mesaj gönderilemedi ({dialog.id}): {e}")
            await asyncio.sleep(interval)  # Döngü tamamlandıktan sonra bekle

    automessage_task = asyncio.create_task(send_message_to_all_groups())

@register(outgoing=True, pattern=r'^\.autoreply (\d+[smhd])$')
async def autoreply(event):
    global automessage_task

    if automessage_task:
        await event.edit("Avtomatik mesaj artıq aktivdir. Dayandırmaq üçün `.autostop` yazın.")
        return

    if not event.reply_to_msg_id:
        await event.edit("Xahiş olunur, bir mesaja cavab verin.")
        return

    time_input = event.pattern_match.group(1)

    time_multiplier = {"s": 1, "m": 60, "h": 3600, "d": 86400}
    time_labels = {"s": "saniyə", "m": "dəqiqə", "h": "saat", "d": "gün"}

    time_unit = time_input[-1]
    if time_unit not in time_multiplier:
        await event.edit("Yanlış zaman vahidi istifadə edildi. `s`, `m`, `h` və ya `d` istifadə edin.")
        return

    interval = int(time_input[:-1]) * time_multiplier[time_unit]
    readable_time = f"{time_input[:-1]} {time_labels[time_unit]}"

    replied_message = await event.get_reply_message()

    await event.edit(f"Avtomatik mesaj aktivləşdirildi. Mesaj: `{replied_message.message}` hər {readable_time} göndəriləcək.")

    async def send_message_to_all_groups():
        while True:
            async for dialog in bot.iter_dialogs():
                if dialog.is_group and dialog.id != EXCLUDED_GROUP_ID:
                    try:
                        await bot.send_message(dialog.id, replied_message.message)
                    except Exception as e:
                        pass
            await asyncio.sleep(interval) 

    automessage_task = asyncio.create_task(send_message_to_all_groups())

@register(outgoing=True, pattern=r'^\.autostop$')
async def autostop(event):
    global automessage_task

    if automessage_task:
        automessage_task.cancel()
        automessage_task = None
        await event.edit("Avtomatik mesaj dayandırıldı.")
    else:
        await event.edit("Avtomatik mesaj aktiv deyil.")
                            
CmdHelp('automessage').add_command(
    'automessage', '<zaman (10s/10m/10h/10d)> <mesaj>', 'Bütün qruplara təyin etdiyiniz mesajı təyin etdiyiniz zaman intervalında göndərər.'
).add_command(
    'autostop', '', 'Avtomatik mesaj göndərməyi dayandırar.'
).add_command(
    'autoreply', '<zaman (10s/10m/10h/10d)>', 'Bir mesaja cavab verərək, həmin mesajı bütün qruplara təyin etdiyiniz zaman intervalında göndərər.'
).add_info(
    'Silgi Tərəfindən hazırlanmışdır'
).add()

# SILGI
import asyncio
from userbot.events import register
from userbot import BOTLOG_CHATID, bot
from userbot.cmdhelp import CmdHelp

@register(outgoing=True, pattern=r'^\.spaminfo$')
async def spaminfo(event):
    await event.edit("Spam məlumatları yoxlanılır...")

    try:
        spambot = await bot.get_entity("@spambot")
        async with bot.conversation(spambot) as conv:
            await conv.send_message("/start")
            response = await conv.get_response()
            await event.edit(f"Spam məlumatı: \n\n{response.message}")
    except Exception as e:
        await event.edit("Spam məlumatını yoxlamaq mümkün olmadı.")
CmdHelp('spaminfo').add_command(
    'spaminfo', '', '@spambot-a start yazaraq spam məlumatını əldə edər.'
).add()


from asyncio import sleep
import re
from userbot import BOTLOG, BOTLOG_CHATID, CMD_HELP
from userbot.events import register
from userbot.modules.sql_helper.pm_filters_sql import (add_pm_filter, get_pm_filters, remove_pm_filter)

@register(outgoing=True, pattern="^.pvfilter (.+)")
async def add_pmfilter(event):
    args = event.pattern_match.group(1).split(" ", 1)
    if len(args) < 2:
        await event.edit("`İstifadə: .pvfilter <söz> <cavab>`")
        return
    keyword, reply = args
    msg = await event.get_reply_message()
    msg_id = None
    if msg and msg.media:
        if BOTLOG_CHATID:
            msg_o = await event.client.forward_messages(BOTLOG_CHATID, msg)
            msg_id = msg_o.id
        else:
            await event.edit("`BOTLOG_CHATID yoxdur!`")
            return
    add_pm_filter(event.sender_id, keyword, reply, msg_id)
    await event.edit(f"`{keyword}` filteri əlavə edildi!")

@register(outgoing=True, pattern="^.pvstop (.+)")
async def remove_pmfilter(event):
    keyword = event.pattern_match.group(1)
    if remove_pm_filter(event.sender_id, keyword):
        await event.edit(f"`{keyword}` filteri silindi!")
    else:
        await event.edit(f"`{keyword}` tapılmadı!")

@register(outgoing=True, pattern="^.pvfilters$")
async def list_pmfilters(event):
    filters = get_pm_filters(event.sender_id)
    if not filters:
        await event.edit("`Heç bir PM filteri əlavə edilməyib!`")
        return
    msg = "**PM Filterlər:**\n"
    for f in filters:
        msg += f"- `{f.keyword}`\n"
    await event.edit(msg)

@register(incoming=True, disable_errors=True, func=lambda e: e.is_private)
async def incoming_pm_filter(event):
    filters = get_pm_filters(event.sender_id)
    message_text = event.raw_text
    for trigger in filters:
        if re.fullmatch(trigger.keyword, message_text, flags=re.IGNORECASE):
            if trigger.f_mesg_id:
                msg_o = await event.client.get_messages(BOTLOG_CHATID, ids=int(trigger.f_mesg_id))
                await event.reply(msg_o.message, file=msg_o.media)
            else:
                await event.reply(trigger.reply)
            break

from asyncio import sleep
import re
from userbot import BOTLOG, BOTLOG_CHATID, CMD_HELP
from userbot.events import register
from userbot.modules.sql_helper.pm_filters_sql import (add_pm_filter, get_pm_filters, remove_pm_filter)
@register(incoming=True, disable_edited=True, disable_errors=True)
async def filter_incoming_handler(handler):
    """ Filtrelerin mesajlara yanıt verdiği ana işlev. """
    try:
        sender = await handler.get_sender()
        

        if sender.bot or sender.id in WHITELIST:
            return
        if not handler.is_private:
            return
        try:
            from userbot.modules.sql_helper.pm_filters_sql import get_pm_filters
        except AttributeError:
            await handler.edit("`Bot Non-SQL modunda işləyir!!`")
            return
        



        name = handler.raw_text

        filters = get_pm_filters(handler.sender_id)
        if not filters:
            return


        for trigger in filters:
            pro = re.search(trigger.keyword, name, flags=re.IGNORECASE)
            if pro and trigger.f_mesg_id:
                msg_o = await handler.client.get_messages(
                    entity=BOTLOG_CHATID, ids=int(trigger.f_mesg_id))
                await handler.reply(msg_o.message, file=msg_o.media)
            elif pro and trigger.reply:
                await handler.reply(trigger.reply)

    except AttributeError:
        pass


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
    add_pm_filter(str(event.sender_id), keyword, reply, msg_id)
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


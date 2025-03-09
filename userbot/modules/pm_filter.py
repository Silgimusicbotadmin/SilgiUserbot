# ⚝ 𝑺𝑰𝑳𝑮𝑰 𝑼𝑺𝑬𝑹𝑩𝑶𝑻 ⚝
import re
from userbot import BOTLOG_CHATID
from userbot.events import register
from userbot.cmdhelp import CmdHelp
from userbot import SILGI_VERSION
from userbot.modules.sql_helper.pm_filter_sql import add_pm_filter, get_pm_filters, remove_pm_filter

@register(outgoing=True, pattern=r"^.pvfilter (\S+)(?:\s+(.+))?")
async def add_pm_filter_handler(event):
    args = event.pattern_match.groups()
    filter_name = args[0]
    response = args[1] if args[1] else ""

    msg = await event.get_reply_message()
    msg_id = None

    if msg and msg.media and not response:
        if BOTLOG_CHATID:
            log_msg = await event.client.forward_messages(
                BOTLOG_CHATID, messages=msg, from_peer=event.chat_id, silent=True
            )
            msg_id = log_msg.id
            response = "`[Media faylı]`"
        else:
            await event.edit("`Media filter əlavə etmək üçün BOTLOG_CHATID təyin edilməlidir!`")
            return
    elif msg and not response:
        response = msg.text
    elif not response:
        await event.edit("`İstifadə: .pvfilter <ad> <cavab>`")
        return

    add_pm_filter(filter_name, response, msg_id)
    await event.edit(f"✅ **Filter əlavə edildi:** `{filter_name}`")

@register(incoming=True, disable_edited=True)
async def pm_filter_handler(event):
    if not event.is_private:
        return

    filters = get_pm_filters()
    if not filters:
        return

    text = event.raw_text
    for trigger in filters:
        if re.fullmatch(trigger.keyword, text, flags=re.IGNORECASE):
            if trigger.f_mesg_id:
                msg_o = await event.client.get_messages(BOTLOG_CHATID, ids=int(trigger.f_mesg_id))
                await event.reply(msg_o.message, file=msg_o.media)
            else:
                await event.reply(trigger.reply)
            break

@register(outgoing=True, pattern=r"^.pvstop (\S+)")
async def remove_pm_filter_handler(event):
    filter_name = event.pattern_match.group(1)

    if remove_pm_filter(filter_name):
        await event.edit(f"❌ **Filter silindi:** `{filter_name}`")
    else:
        await event.edit(f"❌ **Filter tapılmadı:** `{filter_name}`")

@register(outgoing=True, pattern=r"^.pvfilters$")
async def list_pm_filters(event):
    filters = get_pm_filters()
    if not filters:
        await event.edit("❌ **Heç bir filter əlavə edilməyib!**")
        return

    msg = "📌 **Aktiv PM filterlər:**\n\n"
    for filt in filters:
        msg += f"- `{filt.keyword}`\n"

    await event.edit(msg)
CmdHelp('pvfilter').add_command(
    'pvfilter', '<söz> <cavab>', 'Şəxsi mesajlarda filter əlavə edər. Mesaja yanıt verərək media da filterləyə bilərsən.'
).add_command(
    'pvstop', '<söz>', 'Əlavə olunmuş filteri silər.'
).add_command(
    'pvfilters', None, 'Bütün şəxsi filterləri göstərər.'
).add_info(
    'Şəxsi mesaj filter sistemi'
).add_info(
    '[SİLGİ](t.me/hvseyn) tərəfindən hazırlanmışdır.'
).add()

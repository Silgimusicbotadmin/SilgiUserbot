# ⚝ 𝑺𝑰𝑳𝑮𝑰 𝑼𝑺𝑬𝑹𝑩𝑶𝑻 ⚝
import re
from userbot import BOTLOG_CHATID
from userbot.events import register
from userbot.modules.sql_helper.pm_filter_sql import add_pm_filter, get_pm_filters, remove_pm_filter

@register(outgoing=True, pattern=r"^.pmfilter (.+)")
async def add_pm_filter_handler(event):
    if event.is_group or event.is_channel:
        await event.edit("`Bu əmr yalnız şəxsidə işləyir!`")
        return

    args = event.pattern_match.group(1)
    mesj = args.strip()

    msg = await event.get_reply_message()
    msg_id = None
    response = ""

    if msg and msg.media and not mesj:
        if BOTLOG_CHATID:
            log_msg = await event.client.forward_messages(
                BOTLOG_CHATID, messages=msg, from_peer=event.chat_id, silent=True
            )
            msg_id = log_msg.id
            response = "`[Media faylı]`"
        else:
            await event.edit("`Media filter əlavə etmək üçün BOTLOG_CHATID təyin edilməlidir!`")
            return
    elif msg and not mesj:
        response = msg.text
    elif mesj:
        response = mesj
    else:
        await event.edit("`İstifadə: .pmfilter <söz>`")
        return

    add_pm_filter(event.chat_id, mesj, response, msg_id)
    await event.edit(f"✅ **Filter əlavə edildi:** `{mesj}`")

@register(incoming=True, disable_edited=True)
async def pm_filter_handler(event):
    if not event.is_private:
        return

    filters = get_pm_filters(event.chat_id)
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

@register(outgoing=True, pattern=r"^.pmstop (.+)")
async def remove_pm_filter_handler(event):
    if event.is_group or event.is_channel:
        await event.edit("`Bu əmr yalnız şəxsidə işləyir!`")
        return

    mesj = event.pattern_match.group(1).strip()
    if '"' in event.text:
        filt = re.findall(r"\"(.*)\"", event.text)[0]
    else:
        filt = mesj

    if remove_pm_filter(event.chat_id, filt):
        await event.edit(f"❌ **Filter silindi:** `{filt}`")
    else:
        await event.edit(f"❌ **Filter tapılmadı:** `{filt}`")

@register(outgoing=True, pattern=r"^.pmfilters$")
async def list_pm_filters(event):
    if event.is_group or event.is_channel:
        await event.edit("`Bu komut yalnız xüsusi mesajlarda işləyir!`")
        return

    filters = get_pm_filters(event.chat_id)
    if not filters:
        await event.edit("❌ **Xüsusi mesajlarda filter tapılmadı!**")
        return

    msg = "📌 **Aktiv PM filterlər:**\n\n"
    for filt in filters:
        msg += f"- `{filt.keyword}`\n"

    await event.edit(msg)

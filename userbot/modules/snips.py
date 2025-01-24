
from userbot.events import register
from telethon.tl.functions.messages import GetHistoryRequest, DeleteMessagesRequest
from telethon.tl.types import InputPeerSelf

# ██████ LANGUAGE CONSTANTS ██████ #

from userbot.language import get_value
LANG = get_value("snips")

# ████████████████████████████████

SNIP_TAG = "#SNIP"  


async def fetch_snips(client):
    """"""
    snips = {}
    try:
        result = await client(GetHistoryRequest(
            peer=InputPeerSelf(),
            limit=1000,  
            offset_date=None,
            offset_id=0,
            max_id=0,
            min_id=0,
            add_offset=0,
            hash=0
        ))
        for message in result.messages:
            if message.message and message.message.startswith(SNIP_TAG):
                parts = message.message.split("\n", 1)
                if len(parts) > 1:
                    keyword = parts[0][len(SNIP_TAG):].strip()  # Keyword çıkar
                    content = parts[1]  
                    snips[keyword] = {
                        "content": content,
                        "id": message.id
                    }
    except Exception as e:
        print(f"Hata: {e}")
    return snips


@register(outgoing=True, pattern=r"\$\w*")
async def on_snip(event):
    """Snip."""
    keyword = event.text[1:]
    snips = await fetch_snips(event.client)
    if keyword in snips:
        message_id_to_reply = event.message.reply_to_msg_id or None
        await event.client.send_message(
            event.chat_id,
            snips[keyword]["content"],
            reply_to=message_id_to_reply
        )


@register(outgoing=True, pattern="^.snip (\w*)")
async def on_snip_save(event):
    """Yeni snip kaydet."""
    keyword = event.pattern_match.group(1)
    string = event.text.partition(keyword)[2]
    msg = await event.get_reply_message()

    if msg and msg.media and not string:
        await event.edit(LANG['NO_MEDIA_SUPPORT'])
        return
    elif event.reply_to_msg_id and not string:
        rep_msg = await event.get_reply_message()
        string = rep_msg.text

    if not string:
        await event.edit(LANG['NO_CONTENT'])
        return


    saved_message = f"{SNIP_TAG} {keyword}\n{string}"
    await event.client.send_message("me", saved_message)

    await event.edit(f"`{keyword}` {LANG['SAVED']}")


@register(outgoing=True, pattern="^.snips$")
async def on_snip_list(event):
    
    snips = await fetch_snips(event.client)
    if not snips:
        await event.edit(LANG['NO_SNIP'])
        return

    message = f"{LANG['SNIPS']}:\n"
    for keyword in snips:
        message += f"`${keyword}`\n"

    await event.edit(message)


@register(outgoing=True, pattern="^.remsnip (\w*)")
async def on_snip_delete(event):
    """Snip sil."""
    keyword = event.pattern_match.group(1)
    snips = await fetch_snips(event.client)

    if keyword in snips:
        
        try:
            await event.client(DeleteMessagesRequest(
                peer=InputPeerSelf(),
                id=[snips[keyword]["id"]]
            ))
            await event.edit(f"`Snip:` **{keyword}** `{LANG['DELETED']}`")
        except Exception as e:
            await event.edit(f"`{LANG['DELETE_FAILED']}:` {str(e)}")
    else:
        await event.edit(f"`Snip:` **{keyword}** `{LANG['NOT_FOUND']}`")


CmdHelp('snips').add_command(
    '$<snip_adı>', None, (LANG['SNIP1'])
).add_command(
    'snip', (LANG['SNIP2']), (LANG['SNIP3'])
).add_command(
    'snips', None, (LANG['SNIP4'])
).add_command(
    'remsnip', (LANG['SNIP5']), (LANG['SNIP6'])
).add()

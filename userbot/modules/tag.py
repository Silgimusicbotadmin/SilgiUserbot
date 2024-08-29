import time
import requests
from telethon import events
from telethon.tl.types import ChannelParticipantsAdmins
from asyncio import sleep
from userbot import CMD_HELP, bot
from userbot.events import register
from userbot.cmdhelp import CmdHelp


tag_active = True

@register(outgoing=True, pattern="^.tagall$")
async def tag_all(event):
    global tag_active
    tag_active = True  
    if event.fwd_from:
        return
    if not tag_active:
        await event.respond("Tagging dayandı.")
        return
    mentions = "@tag"
    chat = await event.get_input_chat()
    async for x in bot.iter_participants(chat):
        mentions += f"[\u2063](tg://user?id={x.id})"
    await event.reply(mentions)
    await event.delete()

@register(outgoing=True, pattern="^.tagadmin (.*)")
async def tag_admins(event):
    global tag_active
    tag_active = True  
    if event.fwd_from:
        return
    if not tag_active:
        await event.respond("Tagging dayandı.")
        return
    text = event.pattern_match.group(1)
    chat = await event.get_input_chat()
    async for admin in event.client.iter_participants(chat, filter=ChannelParticipantsAdmins):
        mention = f"[{admin.first_name}](tg://user?id={admin.id}) {text}"
        await event.respond(mention)
        await sleep(1)
    await event.delete()

@register(outgoing=True, pattern="^.tag(?: |$)(.*)")
async def tag_one_by_one(tag):
    global tag_active
    tag_active = True  
    if not tag_active:
        await tag.respond("Tagging dayandı.")
        return
    if tag.pattern_match.group(1):
        seasons = tag.pattern_match.group(1)
    else:
        seasons = ""

    chat = await tag.get_input_chat()
    await tag.delete()
    async for i in bot.iter_participants(chat):
        if not tag_active:
            await tag.respond("Tagging dayandı.")
            break
        await tag.client.send_message(tag.chat_id, "[{}](tg://user?id={}) {}".format(i.first_name, i.id, seasons))
        await sleep(1.9)

@register(outgoing=True, pattern="^.stoptag$")
async def stop_tag(event):
    global tag_active
    tag_active = False
    await event.respond("Tagging dayandı.")
    await event.delete()


CmdHelp('tag').add_command(
    'tagall', None, 'Hərkəsi bir mesajda tağ edər.'
).add_command(
    'tag', None, 'Hərkəsi bir-bir tağ edər.'
).add_command(
    'tagadmin', None, 'Bu əmri hər hansısa sohbətdə işlədəndə adminləri tağ edər.'
).add_command(
    'stoptag', None, 'Tag əməliyyatını dayandırır.'
).add_info(
    'Etiketləmə plugini'
).add_info(
    '[SİLGİ](@atondusalamde) tərəfindən hazırlanmışdır.'
).add()
    

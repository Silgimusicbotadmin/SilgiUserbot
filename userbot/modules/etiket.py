import time
import requests
from telethon import events
from telethon.tl.types import ChannelParticipantsAdmins
from asyncio import sleep
from userbot import CMD_HELP, bot, WHITELIST
from userbot.events import register
from userbot.cmdhelp import CmdHelp

tag_active = True
tagged_users = set()

@register(outgoing=True, pattern="^.etiketall$")
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
        if x.id not in tagged_users and x.id not in WHITELIST: 
            tagged_users.add(x.id)
            mentions += f"[\u2063](tg://user?id={x.id})"
    await event.reply(mentions)
    await event.delete()

@register(outgoing=True, pattern="^.etiketadmin (.*)")
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
        if admin.id not in tagged_users and admin.id not in WHITELIST:  
            tagged_users.add(admin.id)
            mention = f"[{admin.first_name}](tg://user?id={admin.id}) {text}"
            await event.respond(mention)
            await sleep(1)
    await event.delete()

@register(outgoing=True, pattern="^.etiket(?: |$)(.*)")
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
        if i.id not in tagged_users and i.id not in WHITELIST:  
            tagged_users.add(i.id)
            await tag.client.send_message(tag.chat_id, "[{}](tg://user?id={}) {}".format(i.first_name, i.id, seasons))
            await sleep(1.9)

@register(outgoing=True, pattern="^.stopetiket$")
async def stop_tag(event):
    global tag_active
    tag_active = False
    await event.respond("Tagging dayandı.")
    await event.delete()

@register(outgoing=True, pattern="^.resetlist$")
async def reset_tag_list(event):
    global tagged_users
    tagged_users.clear()
    await event.respond("Tag listi sıfırlandı.")
    await event.delete()
        

CmdHelp('etiket').add_command(
    'etiketall', None, 'Hərkəsi bir mesajda tağ edər.'
).add_command(
    'etiket', None, 'Hərkəsi bir-bir tağ edər.'
).add_command(
    'etiketadmin', None, 'Bu əmri hər hansısa sohbətdə işlədəndə adminləri tağ edər.'
).add_command(
    'stopetiket', None, 'Tag əməliyyatını dayandırır.'
).add_command(
    'resetlist', None, 'Tag edilən kullanıcıların listesini sıfırlayır.'
).add_info(
    'Etiketləmə plugini'
).add_sahib(
    '[SİLGİ](t.me/hvseyn) tərəfindən hazırlanmışdır.'
).add()

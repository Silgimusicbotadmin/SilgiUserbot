import asyncio
from telethon import events
from userbot import BRAIN_CHECKER, WHITELIST
from userbot.events import register


@register(incoming=True, from_users=WHITELIST, pattern="^.ualive$")
async def _(q):
    await event.edit("Buyurun ⚝ 𝑺𝑰𝑳𝑮𝑰 𝑼𝑺𝑬𝑹𝑩𝑶𝑻 ⚝ Admini botun qoşulu olduğu hesablar:")
    await q.client.send_message(q.chat_id,"`⚝ 𝑺𝑰𝑳𝑮𝑰 𝑼𝑺𝑬𝑹𝑩𝑶𝑻 ⚝💻 Online`")

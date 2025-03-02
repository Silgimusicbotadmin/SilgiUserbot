import asyncio
import heroku3
from telethon import TelegramClient
from telethon.tl.functions.channels import CreateChannelRequest
from telethon.tl.functions.contacts import UnblockRequest
from random import randint
from userbot import BOT_TOKEN, HEROKU_APIKEY, HEROKU_APPNAME, bot, me

Silgi = "userbot/SilgiUserbotlogo.jpg"


def heroku_qurulum():
    if HEROKU_APIKEY and HEROKU_APPNAME:
        heroku_conn = heroku3.from_key(HEROKU_APIKEY)
        app = heroku_conn.app(HEROKU_APPNAME)
        config = app.config()
        return config
    return None

async def silgiassistantbot(config):
    bot_father = "@BotFather"
    await bot(UnblockRequest(bot_father))
    await bot.send_message(bot_father, "/newbot")
    await asyncio.sleep(2)
    
    me = await bot.get_me()
    bot_name = f"{me.first_name} SilgiUserbot Assistant"
    username = f"{me.username}_silgiub_{randint(1, 1000)}_bot" if me.username else f"silgiub{str(me.id)[5:]}bot"
    
    await bot.send_message(bot_father, bot_name)
    await asyncio.sleep(2)
    await bot.send_message(bot_father, username)
    
    messages = await bot.get_messages(bot_father, limit=1)
    if "Done!" in messages[0].text:
        token = messages[0].text.split("`")[1]
        config["BOT_TOKEN"] = token
        config["BOT_USERNAME"] = username
        await bot.send_message("me", f"Yeni Assistant bot yaradıldı: @{username}")
        await bot.send_message(bot_father, "/setinline")
        await asyncio.sleep(1)
        await bot.send_message(bot_father, f"@{username}")
        await asyncio.sleep(1)
        await bot.send_message(bot_father, "kömek yazın")
        await asyncio.sleep(3)
        await bot.send_message(bot_father, "/setabouttext")
        await asyncio.sleep(1)
        await bot.send_message(bot_father, f"@{username}")
        await asyncio.sleep(1)
        await bot.send_message(bot_father, f"{me.first_name} üçün [SilgiUserbot](t.me/silgiub) tərəfindən hazırlanmış assistant botuyam")
        await asyncio.sleep(3)
        await bot.send_message(bot_father, "/setdescription")
        await asyncio.sleep(1)
        await bot.send_message(bot_father, f"@{username}")
        await asyncio.sleep(1)
        await bot.send_message(bot_father, f"🖥 Sahib ~ {me.first_name} \n\n Created By ~ @SilgiUB ")
        await asyncio.sleep(2)
        await bot.send_message(bot_father, f"@{username}")
        await asyncio.sleep(1)
        await bot.send_file(bot_father, Silgi)
    else:
        await bot.send_message("me", "Bot yaradılmadı. @BotFather-dən əl ilə cəhd edin.")
    
    

async def main():
    config = heroku_qurulum()
    if not config:
        print("Heroku API açarı və ya app adı tapılmadı.")
        return
    await silgiassistantbot(config)
if __name__ == "__main__":
    asyncio.run(main())


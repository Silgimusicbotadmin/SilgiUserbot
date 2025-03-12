
import os
import time
import re
import gc
from re import compile
from sys import version_info
from logging import basicConfig, getLogger, INFO, DEBUG
from distutils.util import strtobool as sb
from pylast import LastFMNetwork, md5
from pySmartDL import SmartDL
from dotenv import load_dotenv
from requests import get
from telethon import Button, events
from telethon.tl.functions.channels import GetFullChannelRequest as getchat
from telethon.tl.functions.phone import GetGroupCallRequest as getvc
from telethon.tl.functions.channels import JoinChannelRequest
from telethon.sync import TelegramClient, custom
from telethon.sessions import StringSession
from telethon.events import callbackquery, InlineQuery, NewMessage
from math import ceil
import heroku3


load_dotenv("config.env")

StartTime = time.time()

# Bot log
CONSOLE_LOGGER_VERBOSE = sb(os.environ.get("CONSOLE_LOGGER_VERBOSE", "False"))

ASYNC_POOL = []

if CONSOLE_LOGGER_VERBOSE:
    basicConfig(
        format="%(asctime)s - @silgiub - %(levelname)s - %(message)s",
        level=DEBUG,
    )
else:
    basicConfig(format="%(asctime)s - @silgiub - %(levelname)s - %(message)s",
                level=INFO)
LOGS = getLogger(__name__)

if version_info[0] < 3 or version_info[1] < 6:
    LOGS.info("Ən az python 3.6 versiyasına sahib olmanız lazımdır."
              "Birdən çox özəllik buna bağlıdır. Bot söndürülür.")
    quit(1)


CONFIG_CHECK = os.environ.get(
    "___________XAİŞ_______BU_____SETİRİ_____SILIN__________", None)

if CONFIG_CHECK:
    LOGS.info(
        "Xaiş ilk haştağ'da seçilən sətiri config.env faylından silin."
    )
    quit(1)

# Bot'un dili
LANGUAGE = os.environ.get("LANGUAGE", None).upper()

if not LANGUAGE in ["EN", "TR", "AZ", "UZ", "DEFAULT"]:
    LOGS.info("Bilinməyən bir dil seçdiniz. Buna görə DEFAULT işlədilir.")
    LANGUAGE = "DEFAULT"
    
# SilgiUserbot Versiyası
SILGI_VERSION = "4.5"

# Telegram API KEY ve HASH
API_KEY = os.environ.get("API_KEY", None)
API_HASH = os.environ.get("API_HASH", None)

try:
    SUDO_ID = set(int(x) for x in os.environ.get("SUDO_ID", "").split())
except ValueError:
    raise Exception("Dəyər daxil etməlisiz!")

SILINEN_PLUGIN = {}
# UserBot Session String
STRING_SESSION = os.environ.get("STRING_SESSION", None)

# Kanal / Qrup ID
BOTLOG_CHATID = int(os.environ.get("BOTLOG_CHATID", None))

# Günlük
BOTLOG = sb(os.environ.get("BOTLOG", "False"))
LOGSPAMMER = sb(os.environ.get("LOGSPAMMER", "False"))

# PM
PM_AUTO_BAN = sb(os.environ.get("PM_AUTO_BAN", "False"))

# Heroku
HEROKU_MEMEZ = sb(os.environ.get("HEROKU_MEMEZ", "False"))
HEROKU_APPNAME = os.environ.get("HEROKU_APPNAME", None)
HEROKU_APIKEY = os.environ.get("HEROKU_APIKEY", None)

# Yenilənmə
UPSTREAM_REPO_URL = "https://github.com/Silgimusicbot/SilgiUserbot.git"

# Konsol
CONSOLE_LOGGER_VERBOSE = sb(os.environ.get("CONSOLE_LOGGER_VERBOSE", "False"))

# SQL
DB_URI = os.environ.get("DATABASE_URL", "sqlite:///dto.db")

# OCR API key
OCR_SPACE_API_KEY = os.environ.get("OCR_SPACE_API_KEY", None)

# remove.bg API key
REM_BG_API_KEY = os.environ.get("REM_BG_API_KEY", None)

# AUTO PP
AUTO_PP = os.environ.get("AUTO_PP", None)

# Alive Name
ALIVE_NAME = os.environ.get("ALIVE_NAME", None)
DEFAULT_NAME = os.environ.get("DEFAULT_NAME", None)
BREND_MENTION = f"SilgiUserbot"
BREND_VERSION = "4.5"
DTO_VERSION = "4.5"
# Warn modül
WARN_LIMIT = int(os.environ.get("WARN_LIMIT", 3))
WARN_MODE = os.environ.get("WARN_MODE", "gmute")

if not WARN_MODE in ["gmute", "gban"]:
    WARN_MODE = "gmute"

# Qaleriya
GALERI_SURE = int(os.environ.get("GALERI_SURE", 60))

# Chrome
CHROME_DRIVER = os.environ.get("CHROME_DRIVER", None)
GOOGLE_CHROME_BIN = os.environ.get("GOOGLE_CHROME_BIN", None)

PLUGINID = os.environ.get("PLUGIN_CHANNEL_ID", None)
# Plugin 
if not PLUGINID:
    PLUGIN_CHANNEL_ID = "me"
else:
    PLUGIN_CHANNEL_ID = int(PLUGINID)

# OpenWeatherMap API Key
OPEN_WEATHER_MAP_APPID = os.environ.get("OPEN_WEATHER_MAP_APPID", None)
WEATHER_DEFCITY = os.environ.get("WEATHER_DEFCITY", None)

# Lydia API
LYDIA_API_KEY = os.environ.get("LYDIA_API_KEY", None)

# Alive şəkil
IMG = os.environ.get(
    "IMG",
    "https://telegra.ph/file/2269e1ed5b9a3b0444361.jpg")

# Anti Spambot
ANTI_SPAMBOT = sb(os.environ.get("ANTI_SPAMBOT", "False"))
ANTI_SPAMBOT_SHOUT = sb(os.environ.get("ANTI_SPAMBOT_SHOUT", "False"))

# Youtube API key
YOUTUBE_API_KEY = os.environ.get("YOUTUBE_API_KEY", None)

# Saat & Tarix
COUNTRY = str(os.environ.get("COUNTRY", None))
TZ_NUMBER = int(os.environ.get("TZ_NUMBER", 1))

# Qarşılama
CLEAN_WELCOME = sb(os.environ.get("CLEAN_WELCOME", "True"))

# Last.fm
BIO_PREFIX = os.environ.get("BIO_PREFIX", "@silgiuserbot | ")
DEFAULT_BIO = os.environ.get("DEFAULT_BIO", None)

LASTFM_API = os.environ.get("LASTFM_API", None)
LASTFM_SECRET = os.environ.get("LASTFM_SECRET", None)
LASTFM_USERNAME = os.environ.get("LASTFM_USERNAME", None)
LASTFM_PASSWORD_PLAIN = os.environ.get("LASTFM_PASSWORD", None)
LASTFM_PASS = md5(LASTFM_PASSWORD_PLAIN)
if LASTFM_API and LASTFM_SECRET and LASTFM_USERNAME and LASTFM_PASS:
    lastfm = LastFMNetwork(api_key=LASTFM_API,
                           api_secret=LASTFM_SECRET,
                           username=LASTFM_USERNAME,
                           password_hash=LASTFM_PASS)
else:
    lastfm = None

# Google Drive
G_DRIVE_CLIENT_ID = os.environ.get("G_DRIVE_CLIENT_ID", None)
G_DRIVE_CLIENT_SECRET = os.environ.get("G_DRIVE_CLIENT_SECRET", None)
G_DRIVE_AUTH_TOKEN_DATA = os.environ.get("G_DRIVE_AUTH_TOKEN_DATA", None)
GDRIVE_FOLDER_ID = os.environ.get("GDRIVE_FOLDER_ID", None)
TEMP_DOWNLOAD_DIRECTORY = os.environ.get("TMP_DOWNLOAD_DIRECTORY",
                                         "./downloads")

# Inline bot
BOT_TOKEN = os.environ.get("BOT_TOKEN", None)
BOT_USERNAME = os.environ.get("BOT_USERNAME", None)

# Genius
GENIUS = os.environ.get("GENIUS", None)
CMD_HELP = {}
CMD_HELP_BOT = {}
PM_AUTO_BAN_LIMIT = int(os.environ.get("PM_AUTO_BAN_LIMIT", 4))

SPOTIFY_DC = os.environ.get("SPOTIFY_DC", None)
SPOTIFY_KEY = os.environ.get("SPOTIFY_KEY", None)

PAKET_ISMI = os.environ.get("PAKET_ISMI", "@silgiub Paketi")

# Avto
AVTO_Q = sb(os.environ.get("AVTO_Q", "True"))

# Pattern
PATTERNS = os.environ.get("PATTERNS", ".,")
WHITELIST = [7589331363, 7287936548]

# Təhlükəli pluginlər üçün
TEHLUKELI = ["SESSION", "HEROKU_APIKEY", "API_HASH", "API_KEY", ".session.save"]

# CloudMail.ru və MEGA.nz
if not os.path.exists('bin'):
    os.mkdir('bin')

binaries = {
    "https://raw.githubusercontent.com/yshalsager/megadown/master/megadown":
    "bin/megadown",
    "https://raw.githubusercontent.com/yshalsager/cmrudl.py/master/cmrudl.py":
    "bin/cmrudl"
}

for binary, path in binaries.items():
    downloader = SmartDL(binary, path, progress_bar=False)
    downloader.start()
    os.chmod(path, 0o755)

# 'bot' dəyişkəni
if STRING_SESSION:
    
    bot = TelegramClient(StringSession(STRING_SESSION), API_KEY, API_HASH)
else:
    
    bot = TelegramClient("userbot", API_KEY, API_HASH)

if os.path.exists("dtobrain.check"):
    os.remove("dtobrain.check")
else:
    LOGS.info("Braincheck faylı yoxdur, getirilir...")

URL = 'https://raw.githubusercontent.com/Silgimusicbot/SilgiUserbot/master/upbrain.check'
with open('upbrain.check', 'wb') as load:
    load.write(get(URL).content)

async def get_call(event):
    mm = await event.client(getchat(event.chat_id))
    xx = await event.client(getvc(mm.full_chat.call))
    return xx.call

async def check_botlog_chatid():
    if not BOTLOG_CHATID and LOGSPAMMER:
        LOGS.info(
            "Özəl xəta günlüyünün işləməsi üçün  BOTLOG_CHATID dəyişkənini düzəltməniz lazımdır.")
        quit(1)

    elif not BOTLOG_CHATID and BOTLOG:
        LOGS.info(
            "Günlüyə qeyd etmə özəlliyinin işləməsi üçün BOTLOG_CHATID dəyişkənliyini düzəltməyiniz lazımdır.")
        quit(1)

    elif not BOTLOG or not LOGSPAMMER:
        return

    entity = await bot.get_entity(BOTLOG_CHATID)
    if entity.default_banned_rights.send_messages:
        LOGS.info(
            "Hesabınızın BOTLOG_CHATID qrupuna mesaj göndərmə icazəsi yoxdur. "
            "Qrup ID'sini doğru yazıb yazmadığınızı yoxlayın.")
        quit(1)
        
if not BOT_TOKEN == None:
    tgbot = TelegramClient(
        "TG_BOT_TOKEN",
        api_id=API_KEY,
        api_hash=API_HASH
    ).start(bot_token=BOT_TOKEN)
else:
    tgbot = None
heroku_conn = heroku3.from_key(HEROKU_APIKEY)
heroku_app = heroku_conn.apps()[HEROKU_APPNAME]

@tgbot.on(InlineQuery)
async def inline_handler(event):
    builder = event.builder
    query = event.text

    if event.query.user_id == uid and query == "config":
        config_vars = heroku_app.config()  
        config_keys = list(config_vars)
        PAGE_SIZE = 9
        page = int(query.split("_")[-1]) if "_" in query else 0
        total_pages = math.ceil(len(config_keys) / PAGE_SIZE)

        buttons = []
        for key in config_keys[page * PAGE_SIZE: (page + 1) * PAGE_SIZE]:
            buttons.append([custom.Button.inline(f"⚙️ {key}", data=f"config_edit[{key}]")])
        nav_buttons = []
        if page > 0:
            nav_buttons.append(custom.Button.inline("◀️ Geri", data=f"config_page_{page - 1}"))
        if page < total_pages - 1:
            nav_buttons.append(custom.Button.inline("İrəli ▶️", data=f"config_page_{page + 1}"))

        if nav_buttons:
            buttons.append(nav_buttons)

        result = await builder.article(
            "Heroku Config Vars",
            text=f"**Heroku Config Vars**\n\n🔹 **App:** {HEROKU_APPNAME}\n📌 **Səhifə:** {page + 1}/{total_pages}",
            buttons=buttons,
            link_preview=False
        )
        await event.answer([result])
        await asyncio.sleep(0)
        gc.collect


@tgbot.on(events.CallbackQuery(data=re.compile(b"config_edit:(.+)")))
async def config_edit(event):
    key = event.data_match.group(1).decode("UTF-8")
    user_id = event.query.user_id
    current_value = heroku_app.config().get(key, "⚠️ Dəyər tapılmadı")

    await event.edit(
        f"🛠 **{key}** dəyişdirilməsi\n\n🔹 Mövcud dəyər: `{current_value}`\n\n✏️ Yeni dəyəri göndərin:",
        buttons=[[Button.inline("❌ Ləğv et", data="config")]]
    )

    try:
        msg = await tgbot.wait_for(events.NewMessage(from_users=user_id), timeout=60)
        new_value = msg.text

        heroku_app.config()[key] = new_value  # Yeni dəyəri tətbiq et

        await msg.reply(f"✅ **{key}** uğurla `{new_value}` olaraq dəyişdirildi!")
        await config_handler(event)
    except asyncio.TimeoutError:
        await event.edit("❌ Zaman aşımı! Config dəyişdirilmədi.", buttons=[[Button.inline("🔙 Geri", data="config")]])
    except Exception as e:
        await event.respond(f"❌ Xəta baş verdi: {str(e)}")

@tgbot.on(events.CallbackQuery(data=b"config_back"))
async def config_back(event):
    await config_handler(event)

def butonlastir(sayfa, moduller):
    Satir = 5
    Kolon = 3
    
    moduller = sorted([modul for modul in moduller if not modul.startswith("_")])
    pairs = list(map(list, zip(moduller[::2], moduller[1::2])))
    if len(moduller) % 2 == 1:
        pairs.append([moduller[-1]])
    max_pages = ceil(len(pairs) / Satir)
    pairs = [pairs[i:i + Satir] for i in range(0, len(pairs), Satir)]
    butonlar = []
    for pairs in pairs[sayfa]:
        butonlar.append([
            custom.Button.inline("🔸 " + pair, data=f"bilgi[{sayfa}]({pair})") for pair in pairs
        ])

    butonlar.append([custom.Button.inline("◀️ Geri", data=f"sayfa({(max_pages - 1) if sayfa == 0 else (sayfa - 1)})"), custom.Button.inline("İrəli ▶️", data=f"sayfa({0 if sayfa == (max_pages - 1) else sayfa + 1})")])
    return [max_pages, butonlar]


with bot:
    if AVTO_Q:
        try:
            bot(JoinChannelRequest("@silgiub"))
            bot(JoinChannelRequest("@silgiubplugin"))
            
            
        except:
            pass

    moduller = CMD_HELP
    me = bot.get_me()
    uid = me.id

    try:
        @tgbot.on(NewMessage(pattern='/start'))
        async def start_bot_handler(event):
            if not event.message.from_id == uid:
                await event.reply(f'`Salam mən `⚝ 𝑺𝑰𝑳𝑮𝑰 𝑼𝑺𝑬𝑹𝑩𝑶𝑻 ⚝ `! Mən sahibimə (`@{me.username}`) kömək olmaq üçün varam, yəni sənə köməkçi ola bilmərəm :/ Ama sən da bir ⚝ 𝑺𝑰𝑳𝑮𝑰 𝑼𝑺𝑬𝑹𝑩𝑶𝑻 ⚝ quraşdıra bilərsən; Qrupa bax` @silgiub')
            else:
                await event.reply(f'`⚝ 𝑺𝑰𝑳𝑮𝑰 𝑼𝑺𝑬𝑹𝑩𝑶𝑻 ⚝`')

        @tgbot.on(InlineQuery)  
        async def inline_handler(event):
            builder = event.builder
            result = None
            query = event.text
            if event.query.user_id == uid and query == "kömek":
                rev_text = query[::-1]
                veriler = (butonlastir(0, sorted(CMD_HELP)))
                result = await builder.article(
                    f"Xaiş sadəcə .kömek əmri ilə işladin",
                    text=f"**⚝ 𝑺𝑰𝑳𝑮𝑰 𝑼𝑺𝑬𝑹𝑩𝑶𝑻 ⚝** [SilgiUb](https://t.me/silgiub) __💻__\n\n**Yüklənən Modul Sayı:** `{len(CMD_HELP)}`\n**Səhifə:** 1/{veriler[0]}",
                    buttons=veriler[1],
                    link_preview=False
                )
            elif event.query.user_id == uid and query == "@SilgiUB":
                result = builder.article(
                    "⚝ 𝑺𝑰𝑳𝑮𝑰 𝑼𝑺𝑬𝑹𝑩𝑶𝑻 ⚝",
                    text="**⚝ 𝑺𝑰𝑳𝑮𝑰 𝑼𝑺𝑬𝑹𝑩𝑶𝑻 ⚝** [SilgiUb](https://t.me/silgiub) __işləyir__",
                    buttons=[
                        [custom.Button.inline("Plugin Listi", data="komek")],
                        [custom.Button.inline("Bot Configləri", data="config")]
                    ],
                    link_preview=False
                )
            elif query.startswith("http"):
                parca = query.split(" ")
                result = builder.article(
                    "Fayl Yükləndi",
                    text=f"**Fayl uğurlu bir şəkildə {parca[2]} saytına yükləndi!**\n\nYükləmə zamanı: {parca[1][:3]} saniyə\n[‏‏‎ ‎]({parca[0]})",
                    buttons=[
                        [custom.Button.url('URL', parca[0])]
                    ],
                    link_preview=True
                )
            else:
                result = builder.article(
                    "⚝ 𝑺𝑰𝑳𝑮𝑰 𝑼𝑺𝑬𝑹𝑩𝑶𝑻 ⚝",
                    text="""[⚝ 𝑺𝑰𝑳𝑮𝑰 𝑼𝑺𝑬𝑹𝑩𝑶𝑻 ⚝](https://t.me/silgiub)'u işlətməyi yoxlayın!
Hesabınızı bot'a çevirə bilərsiz və bunları işlədə bilərsiz. Unutmayın, siz başqasının botunu idarə edə bilmərsiz! Altdakı GitHub adresindən bütün qurulum haqda məlumat var.""",
                    buttons=[
                        [custom.Button.url("Dəstək qrupuna Qatıl", "https://t.me/silgiub"), custom.Button.url(
                            "Sahibim", "https://t.me/hvseyn")],
                        [custom.Button.url(
                            "GitHub", "https://github.com/Silgimusicbot/SilgiUserbot")],
                        [custom.Button.url(
                            "Qurulum botu", "https://t.me/silgiqur_bot")]
                    ],
                    link_preview=False
                )
            await event.answer([result] if result else None)

        @tgbot.on(callbackquery.CallbackQuery(data=compile(b"sayfa\((.+?)\)")))
        async def sayfa(event):
            if not event.query.user_id == uid: 
                return await event.answer("❌ Hey! Mənim mesajlarımı düzəltməyə çalışma! Özünə bir @silgiub qur.", cache_time=0, alert=True)
            sayfa = int(event.data_match.group(1).decode("UTF-8"))
            veriler = butonlastir(sayfa, CMD_HELP)
            await event.edit(
                f"**⚝ 𝑺𝑰𝑳𝑮𝑰 𝑼𝑺𝑬𝑹𝑩𝑶𝑻 ⚝** [SilgiUb](https://t.me/silgiub) __işləyir__\n\n**Yüklənən Modul Sayı:** `{len(CMD_HELP)}`\n**Səhifə:** {sayfa + 1}/{veriler[0]}",
                buttons=veriler[1],
                link_preview=False
            )
        @tgbot.on(callbackquery.CallbackQuery(data=compile(b"komek")))
        async def inline_handler(event):
            if not event.query.user_id == uid:
                return await event.answer("❌ Hey! Mənim mesajlarımı düzəltməyə çalışma! Özünə bir @silgiub qur.", cache_time=0, alert=True)   
            query = event.data.decode("UTF-8")
            veriler = butonlastir(0, sorted(CMD_HELP))
            await event.edit(
                text=f"**⚝ 𝑺𝑰𝑳𝑮𝑰 𝑼𝑺𝑬𝑹𝑩𝑶𝑻 ⚝** [SilgiUb](https://t.me/silgiub) __💻__\n\n**Yüklənən Modul Sayı:** `{len(CMD_HELP)}`\n**Səhifə:** 1/{veriler[0]}",
                buttons=veriler[1],  
                link_preview=False
            )
        @tgbot.on(events.CallbackQuery(data=re.compile(b"config")))
        async def config_handler(event):
            if event.query.user_id != uid:
                return await event.answer("❌ Hey! Mənim mesajlarımı düzəltməyə çalışma! Özünə bir @silgiub qur.", cache_time=0, alert=True) 
    
            needed_keys = ["BOT_TOKEN", "API_ID"]  # Buraya istədiyin dəyişənlərin adlarını əlavə et
            config_vars = heroku_app.config()
            config_keys = [key for key in needed_keys if key in config_vars]  # Sadəcə bu açarlara bax

            if not config_keys:
                return await event.answer("❌ Heç bir uyğun config tapılmadı!", cache_time=0, alert=True)

            buttons = [[Button.inline(f"⚙️ {key}", data=f"config_edit:{key}")] for key in config_keys]
            buttons.append([Button.inline("🔙 Geri", data="config_back")])

            await event.edit(
                text=f"**Heroku Config Vars**\n\n🔹 **App:** {HEROKU_APPNAME}",
                buttons=buttons,
                link_preview=False
            )


        @tgbot.on(callbackquery.CallbackQuery(data=compile(b"bilgi\[(\d*)\]\((.*)\)")))
        async def bilgi(event):
            if not event.query.user_id == uid: 
                return await event.answer("❌  Hey! Mənim mesajlarımı düzəltməyə çalışma! Özünə bir @silgiub qur.", cache_time=0, alert=True)

            sayfa = int(event.data_match.group(1).decode("UTF-8"))
            komut = event.data_match.group(2).decode("UTF-8")
            try:
                butonlar = [custom.Button.inline("🔹 " + cmd[0], data=f"komut[{komut}[{sayfa}]]({cmd[0]})") for cmd in CMD_HELP_BOT[komut]['commands'].items()]
            except KeyError:
                return await event.answer("❌ Bu modula açıqlama yazılmayıb.", cache_time=0, alert=True)

            butonlar = [butonlar[i:i + 2] for i in range(0, len(butonlar), 2)]
            butonlar.append([custom.Button.inline("◀️ Geri", data=f"sayfa({sayfa})")])
            await event.edit(
                f"**📗 Fayl:** `{komut}`\n**🔢 Əmr sayı:** `{len(CMD_HELP_BOT[komut]['commands'])}`",
                buttons=butonlar,
                link_preview=False
            )
        
        @tgbot.on(callbackquery.CallbackQuery(data=compile(b"komut\[(.*)\[(\d*)\]\]\((.*)\)")))
        async def komut(event):
            if not event.query.user_id == uid: 
                return await event.answer("❌ Hey! Mənim mesajlarımı düzəltməyə çalışma! Özünə bir @silgiub qur.", cache_time=0, alert=True)

            cmd = event.data_match.group(1).decode("UTF-8")
            sayfa = int(event.data_match.group(2).decode("UTF-8"))
            komut = event.data_match.group(3).decode("UTF-8")

            result = f"**📗 Fayl:** `{cmd}`\n"
            if CMD_HELP_BOT[cmd]['info']['info'] == '':
                if not CMD_HELP_BOT[cmd]['info']['warning'] == '':
                    result += f"**⬇️ Rəsmi:** {'✅' if CMD_HELP_BOT[cmd]['info']['official'] else '❌'}\n"
                    result += f"**⚠️ Xəbərdarlıq:** {CMD_HELP_BOT[cmd]['info']['warning']}\n\n"
                else:
                    result += f"**⬇️ Rəsmi:** {'✅' if CMD_HELP_BOT[cmd]['info']['official'] else '❌'}\n\n"
            else:
                result += f"**⬇️ Rəsmi:** {'✅' if CMD_HELP_BOT[cmd]['info']['official'] else '❌'}\n"
                if not CMD_HELP_BOT[cmd]['info']['warning'] == '':
                    result += f"**⚠️ Xəbərdarlıq:** {CMD_HELP_BOT[cmd]['info']['warning']}\n"
                result += f"**ℹ️ Info:** {CMD_HELP_BOT[cmd]['info']['info']}\n\n"

            command = CMD_HELP_BOT[cmd]['commands'][komut]
            if command['params'] is None:
                result += f"**🛠 Əmr:** `{PATTERNS[:1]}{command['command']}`\n"
            else:
                result += f"**🛠 Əmr:** `{PATTERNS[:1]}{command['command']} {command['params']}`\n"
                
            if command['example'] is None:
                result += f"**💬 Açıqlama:** `{command['usage']}`\n\n"
            else:
                result += f"**💬 Açıqlama:** `{command['usage']}`\n"
                result += f"**⌨️ Məsələn:** `{PATTERNS[:1]}{command['example']}`\n\n"

            await event.edit(
                result,
                buttons=[custom.Button.inline("◀️ Geri", data=f"bilgi[{sayfa}]({cmd})")],
                link_preview=False
            )
    except Exception as e:
        print(e)
        LOGS.info(
            "Botunuzda inline dəstəyi deaktiv edildi. "
            "Aktivləşdirmək üçün bir bot token tanımlayın və botunuzda inline modunu aktivləşdirin. "
            "Əgər bunun xaricində bir problem olduğunu düşünürsüzsə bizlə əlaqə saxlayın."
        )

    try:
        bot.loop.run_until_complete(check_botlog_chatid())
    except:
        LOGS.info(
            "BOTLOG_CHATID ortam dəyişkəni kəçərli bir varlıq deyildir. "
            "Ortam dəyişkənliyinizi / config.env faylını yoxlayın."
        )
        quit(1)


# Qlobal dəyişkənlər
SON_GORULME = 0
COUNT_MSG = 0
USERS = {}
BRAIN_CHECKER = [7589331363]
COUNT_PM = {}
LASTMSG = {}
ENABLE_KILLME = True
ISAFK = False
AFKREASON = None
ZALG_LIST = [[
    "̖",
    " ̗",
    " ̘",
    " ̙",
    " ̜",
    " ̝",
    " ̞",
    " ̟",
    " ̠",
    " ̤",
    " ̥",
    " ̦",
    " ̩",
    " ̪",
    " ̫",
    " ̬",
    " ̭",
    " ̮",
    " ̯",
    " ̰",
    " ̱",
    " ̲",
    " ̳",
    " ̹",
    " ̺",
    " ̻",
    " ̼",
    " ͅ",
    " ͇",
    " ͈",
    " ͉",
    " ͍",
    " ͎",
    " ͓",
    " ͔",
    " ͕",
    " ͖",
    " ͙",
    " ͚",
    " ",
],
    [
    " ̍", " ̎", " ̄", " ̅", " ̿", " ̑", " ̆", " ̐", " ͒", " ͗",
    " ͑", " ̇", " ̈", " ̊", " ͂", " ̓", " ̈́", " ͊", " ͋", " ͌",
    " ̃", " ̂", " ̌", " ͐", " ́", " ̋", " ̏", " ̽", " ̉", " ͣ",
    " ͤ", " ͥ", " ͦ", " ͧ", " ͨ", " ͩ", " ͪ", " ͫ", " ͬ", " ͭ",
    " ͮ", " ͯ", " ̾", " ͛", " ͆", " ̚"
],
    [
    " ̕",
    " ̛",
    " ̀",
    " ́",
    " ͘",
    " ̡",
    " ̢",
    " ̧",
    " ̨",
    " ̴",
    " ̵",
    " ̶",
    " ͜",
    " ͝",
    " ͞",
    " ͟",
    " ͠",
    " ͢",
    " ̸",
    " ̷",
    " ͡",
]]

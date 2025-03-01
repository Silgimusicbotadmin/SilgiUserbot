import re
import requests
import aiohttp
import aiofiles
from userbot.events import register
from userbot import SILGI_VERSION
from userbot.cmdhelp import CmdHelp
from bs4 import BeautifulSoup


effects = {
    "qanli": "https://m.photofunia.com/effects/blood_writing",
    "qapi": "https://m.photofunia.com/categories/halloween/cemetery-gates",
    "qar": "https://m.photofunia.com/categories/all_effects/snow-sign",
    "yeni": "https://m.photofunia.com/categories/all_effects/christmas-writing",
    "isiq": "https://m.photofunia.com/effects/light-graffiti",
    "su": "https://m.photofunia.com/categories/all_effects/water-writing",
    "balon": "https://m.photofunia.com/categories/all_effects/balloon",
    
}

HEADERS = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
    'User-Agent': 'Mozilla/5.0 (Linux; Android 12; M2004J19C) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/105.0.0.0 Mobile Safari/537.36',
}

@register(outgoing=True, pattern="^.(qanli|qapi|qar|yeni|isiq|su|balon) (.*)")
async def effect_yazi(event):
    effect = event.pattern_match.group(1)  
    yazi = event.pattern_match.group(2) 
    await event.edit(f"🔄 `{effect}` efekti ilə `{yazi}` yazısı hazırlanır...")

    effect_url = effects.get(effect)
    if not effect_url:
        await event.edit(f"❌ Effekt `{effect}` tapılmadı!")
        return

    boundary = "----WebKitFormBoundary123456789"
    data = (
        f"--{boundary}\r\n"
        f'Content-Disposition: form-data; name="text"\r\n\r\n'
        f"{yazi}\r\n"
        f"--{boundary}--\r\n"
    ).encode("utf-8")

    try:
        HEADERS["Content-Type"] = f"multipart/form-data; boundary={boundary}"
        HEADERS["Referer"] = effect_url
        
        response = requests.post(effect_url, headers=HEADERS, data=data, verify=False)
        response_text = response.text

        soup = BeautifulSoup(response_text, "html.parser")
        image_url = None

        for link in soup.find_all("a", href=True):
            if "download" in link["href"]:
                image_url = link["href"].split("?")[0]
                break

        if image_url:
            file_name = f"{effect}_text.jpg"

            async with aiohttp.ClientSession() as session:
                async with session.get(image_url, ssl=False) as resp:  
                    if resp.status == 200:
                        async with aiofiles.open(file_name, "wb") as f:
                            await f.write(await resp.read())

            await event.client.send_file(
                event.chat_id,
                file_name,
                caption=f"✅ **{effect}** efekti ilə yazı hazırdır!\n📌 **Mətn:** `{yazi}`\n⚝ 𝑺𝑰𝑳𝑮𝑰 𝑼𝑺𝑬𝑹𝑩𝑶𝑻 ⚝",
                reply_to=event.reply_to_msg_id
            )
            await event.delete()
        else:
            raise ValueError("Şəkil linki tapılmadı!")

    except Exception as e:
        with open("response.html", "w", encoding="utf-8") as file:
            file.write(response_text)

        await event.client.send_file(
            event.chat_id,
            "response.html",
            caption=f"❌ Xəta baş verdi: `{str(e)}`\n📄 **Photofunia cavabı əlavə olundu.**"
        )
@register(outgoing=True, pattern="^.duman (.*)")
async def effect_duman(event):
    text = event.pattern_match.group(1)

    HEADERS = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:135.0) Gecko/20100101 Firefox/135.0",
        "Referer": "https://photofunia.com/effects/foggy_window_writing",
        "Cookie": "_ga=GA1.2.502152313.1735403255; PHPSESSID=po5p6i6qqntpp7f54rl47qvld4",
        "Content-Type": "multipart/form-data; boundary=----WebKitFormBoundary6c098c0794da59d498a54e05921a6c0e"
    }

    effect_url = "https://photofunia.com/effects/foggy_window_writing"
    
    boundary = "----WebKitFormBoundary6c098c0794da59d498a54e05921a6c0e"
    data = (
        f"--{boundary}\r\n"
        'Content-Disposition: form-data; name="text"\r\n\r\n'
        f"{text}\r\n"
        f"--{boundary}--\r\n"
    ).encode("utf-8")

    await event.edit(f"🖌 `{text}` yazısı hazırlanır...")

    try:
        response = requests.post(effect_url, headers=HEADERS, data=data, verify=False)
        response_text = response.text

    
        

        soup = BeautifulSoup(response_text, "html.parser")
        image_url = None

        for img in soup.find_all("img"):
            if "cdn.photofunia.com" in img["src"]:
                image_url = img["src"]
                break

        if image_url:
            file_name = "duman_text.jpg"

            async with aiohttp.ClientSession() as session:
                async with session.get(image_url, ssl=False) as resp:  
                    if resp.status == 200:
                        async with aiofiles.open(file_name, "wb") as f:
                            await f.write(await resp.read())

            await event.client.send_file(
                event.chat_id,
                file_name,
                caption=f"✅ **Duman** efekti ilə yazı hazırdır!\n📌 **Mətn:** `{text}`\n⚝ 𝑺𝑰𝑳𝑮𝑰 𝑼𝑺𝑬𝑹𝑩𝑶𝑻 ⚝",
                reply_to=event.reply_to_msg_id
            )
            await event.delete()
        else:
            raise ValueError("Şəkil linki tapılmadı!")

    except Exception as e:
        with open("response.html", "w", encoding="utf-8") as file:
            file.write(response_text)

        await event.client.send_file(
            event.chat_id,
            "response.html",
            caption=f"❌ Xəta baş verdi: `{str(e)}`\n📄 **Photofunia cavabı əlavə olundu.**"
        )

CmdHelp('yazi_efektleri').add_command(
    'qanli', ".qanli <yazı> şəklində istifadə edin.", 
    "Sizə qanlı yazı tərzində şəkil yaradar."
).add_command(
    'qapi', ".yanmis <yazı> şəklində istifadə edin.", 
    "Sizə yanmış yazı tərzində şəkil yaradar. "
).add_command(
    'qar', ".qar <yazı> şəklində istifadə edin.",
    "Sizə qarlı taxta yazı tərzində şəkil yaradar."
).add_command(
    'yeni', ".yeni <yazı> şəklində istifadə edin.",
    "Sizə yeni il tərzində şəkil yaradar."
).add_command(
    'isiq', ".isiq <yazı> şəklində istifadə edin.",
    "Sizə İşıqlı yazı tərzində şəkil yaradar."
).add_command(
    'su', ".su <yazı> şəklində istifadə edin.",
    "Sizə Sulu yazı tərzində şəkil yaradar."
).add_command(
    'balon', ".balon <yazı> şəklində istifadə edin.",
    "Sizə Şar üzərində yazı tərzində şəkil yaradar."
).add_info(
    "[SILGI](t.me/hvseyn) tərəfindən hazırlanmışdır"
).add()

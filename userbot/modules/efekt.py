import re
import requests
import aiohttp
import aiofiles
from bs4 import BeautifulSoup
from userbot.events import register
from userbot.cmdhelp import CmdHelp

API_URL = "https://m.photofunia.com/categories/halloween/blood_writing"
HEADERS = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
    'Content-Type': 'multipart/form-data; boundary=----WebKitFormBoundaryohlfuyMygb1aEMcp',
    'Referer': 'https://m.photofunia.com/categories/halloween/blood_writing',
    'User-Agent': 'Mozilla/5.0 (Linux; Android 12; M2004J19C) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/105.0.0.0 Mobile Safari/537.36',
}

# TextPro 
TEXTPRO_API_URLS = {
    'neon': "https://textpro.me/neon-light-text-effect-883.html",
    'odun': "https://textpro.me/3d-fire-text-effect-online-883.html",
    'qizil': "https://textpro.me/golden-text-effect-883.html",
    'metal': "https://textpro.me/metal-text-effect-883.html"
}

@register(outgoing=True, pattern="^.qanli (.*)")
async def qanli_yazi(event):
    yazi = event.pattern_match.group(1)
    await event.edit("`Qanlı yazı hazırlanır...` 🩸")

    data = f'------WebKitFormBoundaryohlfuyMygb1aEMcp\r\nContent-Disposition: form-data; name="text"\r\n\r\n{yazi}\r\n------WebKitFormBoundaryohlfuyMygb1aEMcp--\r\n'.encode("utf-8")
    
    try:
        response = requests.post(API_URL, headers=HEADERS, data=data, verify=False)
        response.encoding = "utf-8"
        response_text = response.text
        
        soup = BeautifulSoup(response_text, "html.parser")
        matches = soup.find_all("a", href=True)

        image_url = None
        for match in matches:
            if "download" in match["href"]:
                image_url = match["href"].split("?")[0]
                break
        
        if image_url:
            file_name = "blood_text.jpg"

            async with aiohttp.ClientSession() as session:
                async with session.get(image_url, ssl=False) as resp:  # SSL doğrulaması söndürüldü
                    if resp.status == 200:
                        async with aiofiles.open(file_name, "wb") as f:
                            await f.write(await resp.read())

            await event.client.send_file(
                event.chat_id,
                file_name,
                caption=f"🩸 `{yazi}` üçün qanlı yazı hazırdır!\n⚝ 𝑺𝑰𝑳𝑮𝑰 𝑼𝑺𝑬𝑹𝑩𝑶𝑻 ⚝",
                reply_to=event.reply_to_msg_id
            )
        else:
            raise ValueError("Qanlı yazı üçün şəkil URL-si tapılmadı.")

        await event.delete()
    except Exception as e:
        with open("response.html", "w", encoding="utf-8") as file:
            file.write(response_text)

        await event.client.send_file(
            event.chat_id,
            "response.html",
            caption=f"❌ Xəta baş verdi: {str(e)}\n📄 **Photofunia cavabı əlavə olunub.**"
        )

@register(outgoing=True, pattern="^.neon (.*)")
async def neon_yazi(event):
    yazi = event.pattern_match.group(1)
    await event.edit("`Neon yazı hazırlanır...` 💡")

    data = {'text': yazi}

    try:
        response = requests.post(TEXTPRO_API_URLS['neon'], data=data)
        image_url = response.json().get('image_url')
        
        if image_url:
            file_name = "neon_text.jpg"
            async with aiohttp.ClientSession() as session:
                async with session.get(image_url) as resp:
                    if resp.status == 200:
                        async with aiofiles.open(file_name, "wb") as f:
                            await f.write(await resp.read())

            await event.client.send_file(
                event.chat_id,
                file_name,
                caption=f"💡 `{yazi}` üçün neon yazı hazırdır!",
                reply_to=event.reply_to_msg_id
            )
        else:
            raise ValueError("Yazı üçün neon şəkil URL-si tapılmadı.")

        await event.delete()
    except Exception as e:
        await event.edit(f"❌ Xəta baş verdi: {str(e)}")


@register(outgoing=True, pattern="^.odun (.*)")
async def odun_yazi(event):
    yazi = event.pattern_match.group(1)
    await event.edit("`Odun yazı hazırlanır...` 🔥")

    data = {'text': yazi}

    try:
        response = requests.post(TEXTPRO_API_URLS['odun'], data=data)
        image_url = response.json().get('image_url')
        
        if image_url:
            file_name = "odun_text.jpg"
            async with aiohttp.ClientSession() as session:
                async with session.get(image_url) as resp:
                    if resp.status == 200:
                        async with aiofiles.open(file_name, "wb") as f:
                            await f.write(await resp.read())

            await event.client.send_file(
                event.chat_id,
                file_name,
                caption=f"🔥 `{yazi}` üçün odun yazı hazırdır!",
                reply_to=event.reply_to_msg_id
            )
        else:
            raise ValueError("Yazı üçün odun şəkil URL-si tapılmadı.")

        await event.delete()
    except Exception as e:
        await event.edit(f"❌ Xəta baş verdi: {str(e)}")


@register(outgoing=True, pattern="^.qizil (.*)")
async def qizil_yazi(event):
    yazi = event.pattern_match.group(1)
    await event.edit("`Qızıl yazı hazırlanır...` 💰")

    data = {'text': yazi}

    try:
        response = requests.post(TEXTPRO_API_URLS['qizil'], data=data)
        image_url = response.json().get('image_url')
        
        if image_url:
            file_name = "qizil_text.jpg"
            async with aiohttp.ClientSession() as session:
                async with session.get(image_url) as resp:
                    if resp.status == 200:
                        async with aiofiles.open(file_name, "wb") as f:
                            await f.write(await resp.read())

            await event.client.send_file(
                event.chat_id,
                file_name,
                caption=f"💰 `{yazi}` üçün qızıl yazı hazırdır!",
                reply_to=event.reply_to_msg_id
            )
        else:
            raise ValueError("Yazı üçün qızıl şəkil URL-si tapılmadı.")

        await event.delete()
    except Exception as e:
        await event.edit(f"❌ Xəta baş verdi: {str(e)}")


@register(outgoing=True, pattern="^.metal (.*)")
async def metal_yazi(event):
    yazi = event.pattern_match.group(1)
    await event.edit("`Metal yazı hazırlanır...` ⚒️")

    data = {'text': yazi}

    try:
        response = requests.post(TEXTPRO_API_URLS['metal'], data=data)
        image_url = response.json().get('image_url')
        
        if image_url:
            file_name = "metal_text.jpg"
            async with aiohttp.ClientSession() as session:
                async with session.get(image_url) as resp:
                    if resp.status == 200:
                        async with aiofiles.open(file_name, "wb") as f:
                            await f.write(await resp.read())

            await event.client.send_file(
                event.chat_id,
                file_name,
                caption=f"⚒️ `{yazi}` üçün metal yazı hazırdır!",
                reply_to=event.reply_to_msg_id
            )
        else:
            raise ValueError("Yazı üçün metal şəkil URL-si tapılmadı.")

        await event.delete()
    except Exception as e:
        await event.edit(f"❌ Xəta baş verdi: {str(e)}")


CmdHelp('yazi_efektleri').add_command(
    'neon', "`.neon <yazı>` şəklində istifadə edin.", "Neon yazı tərzində şəkil yaradar."
).add_command(
    'odun', "`.odun <yazı>` şəklində istifadə edin.", "Odun yazı tərzində şəkil yaradar."
).add_command(
    'qizil', "`.qizil <yazı>` şəklində istifadə edin.", "Qızıl yazı tərzində şəkil yaradar."
).add_command(
    'metal', "`.metal <yazı>` şəklində istifadə edin.", "Metal yazı tərzində şəkil yaradar."
).add_command(
    'qanli', "`.qanli <yazı>` şəklində istifadə edin.", "Sizə qanlı yazı tərzində şəkil yaradar."
).add_info(
    "[SILGI](t.me/hvseyn) tərəfindən hazırlanmışdır"
).add()

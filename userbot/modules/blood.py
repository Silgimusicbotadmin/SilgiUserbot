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

CmdHelp('qan').add_command(
    'qanli', "`.qanli <yazı>` şəklində istifadə edin.", "Sizə qanlı yazı tərzində şəkil yaradar."
).add_info(
    "[SILGI](t.me/hvseyn) tərəfindən hazırlanmışdır"
).add()

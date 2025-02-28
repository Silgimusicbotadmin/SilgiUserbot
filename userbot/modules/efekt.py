import re
import requests
import aiohttp
import aiofiles
from userbot.events import register
from userbot.cmdhelp import CmdHelp
from bs4 import BeautifulSoup


effects = {
    "qanli": "https://m.photofunia.com/categories/halloween/blood_writing",
    "yanmis": "https://m.photofunia.com/categories/halloween/burning_text",
    "isiq": "https://m.photofunia.com/categories/halloween/glowing_text",
    "ucan": "https://m.photofunia.com/categories/other/flying_text",
    "ag": "https://m.photofunia.com/categories/other/white_text",
    "susa": "https://m.photofunia.com/categories/other/glass_text",
    "neon": "https://m.photofunia.com/categories/other/neon_text",
    "taxta": "https://m.photofunia.com/categories/other/wooden_text",
    "karnaval": "https://m.photofunia.com/categories/other/carnival_text",
    "supurge": "https://m.photofunia.com/categories/other/brush_text"
}

HEADERS = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
    'Content-Type': 'multipart/form-data; boundary=----WebKitFormBoundaryohlfuyMygb1aEMcp',
    'Referer': '',
    'User-Agent': 'Mozilla/5.0 (Linux; Android 12; M2004J19C) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/105.0.0.0 Mobile Safari/537.36',
}

@register(outgoing=True, pattern="^.(qanli|yanmis|isiq|ucan|ag|susa|neon|taxta|karnaval|supurge) (.*)")
async def effect_yazi(event):
    effect = event.pattern_match.group(1)  
    yazi = event.pattern_match.group(2) 
    await event.edit(f"`{effect} yazısı hazırlanır...` 🖌️")

    
    effect_url = effects.get(effect)
    if not effect_url:
        await event.edit(f"❌ Effekt `{effect}` tapılmadı!")
        return

    data = f'------WebKitFormBoundaryohlfuyMygb1aEMcp\r\nContent-Disposition: form-data; name="text"\r\n\r\n{yazi}\r\n------WebKitFormBoundaryohlfuyMygb1aEMcp--\r\n'.encode("utf-8")
    
    try:
        
        HEADERS['Referer'] = effect_url
        response = requests.post(effect_url, headers=HEADERS, data=data, verify=False)
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
            file_name = f"{effect}_text.jpg"

            async with aiohttp.ClientSession() as session:
                async with session.get(image_url, ssl=False) as resp:  # SSL doğrulaması söndürüldü
                    if resp.status == 200:
                        async with aiofiles.open(file_name, "wb") as f:
                            await f.write(await resp.read())

            await event.client.send_file(
                event.chat_id,
                file_name,
                caption=f"🖌️ `{yazi}` üçün seçilmiş `{effect}` efekti ilə yazı hazırdır!\n⚝ 𝑺𝑰𝑳𝑮𝑰 𝑼𝑺𝑬𝑹𝑩𝑶𝑻 ⚝",
                reply_to=event.reply_to_msg_id
            )
        else:
            raise ValueError(f"Effekt `{effect}` üçün şəkil URL-si tapılmadı.")

        await event.delete()
    except Exception as e:
        with open("response.html", "w", encoding="utf-8") as file:
            file.write(response_text)

        await event.client.send_file(
            event.chat_id,
            "response.html",
            caption=f"❌ Xəta baş verdi: {str(e)}\n📄 **Photofunia cavabı əlavə olunub.**"
        )


CmdHelp('yazi_efektleri').add_command(
    'qanli', "`.qanli <yazı>` şəklində istifadə edin.", 
    "Sizə qanlı yazı tərzində şəkil yaradar. Sayt: [PhotoFunia - Blood Writing](https://m.photofunia.com/categories/halloween/blood_writing)"
).add_command(
    'yanmis', "`.yanmis <yazı>` şəklində istifadə edin.", 
    "Sizə yanmış yazı tərzində şəkil yaradar. Sayt: [PhotoFunia - Burning Text](https://m.photofunia.com/categories/halloween/burning_text)"
).add_command(
    'isiq', "`.isli <yazı>` şəklində istifadə edin.", 
    "Sizə işıqlı yazı tərzində şəkil yaradar. Sayt: [PhotoFunia - Glowing Text](https://m.photofunia.com/categories/halloween/glowing_text)"
).add_command(
    'ucan', "`.ucan <yazı>` şəklində istifadə edin.", 
    "Sizə uçan yazı tərzində şəkil yaradar. Sayt: [PhotoFunia - Flying Text](https://m.photofunia.com/categories/other/flying_text)"
).add_command(
    'ag', "`.ag <yazı>` şəklində istifadə edin.", 
    "Sizə ağ yazı tərzində şəkil yaradar. Sayt: [PhotoFunia - White Text](https://m.photofunia.com/categories/other/white_text)"
).add_command(
    'susa', "`.susa <yazı>` şəklində istifadə edin.", 
    "Sizə şüşə yazı tərzində şəkil yaradar. Sayt: [PhotoFunia - Glass Text](https://m.photofunia.com/categories/other/glass_text)"
).add_command(
    'neon', "`.neon <yazı>` şəklində istifadə edin.", 
    "Sizə neon yazı tərzində şəkil yaradar. Sayt: [PhotoFunia - Neon Text](https://m.photofunia.com/categories/other/neon_text)"
).add_command(
    'taxta', "`.taxta <yazı>` şəklində istifadə edin.", 
    "Sizə taxta yazı tərzində şəkil yaradar. Sayt: [PhotoFunia - Wooden Text](https://m.photofunia.com/categories/other/wooden_text)"
).add_command(
    'karnaval', "`.karnaval <yazı>` şəklində istifadə edin.", 
    "Sizə karnaval yazı tərzində şəkil yaradar. Sayt: [PhotoFunia - Carnival Text](https://m.photofunia.com/categories/other/carnival_text)"
).add_command(
    'supurge', "`.supurge <yazı>` şəklində istifadə edin.", 
    "Sizə süpürgə yazı tərzində şəkil yaradar. Sayt: [PhotoFunia - Brush Text](https://m.photofunia.com/categories/other/brush_text)"
).add_info(
    "[SILGI](t.me/hvseyn) tərəfindən hazırlanmışdır"
).add()

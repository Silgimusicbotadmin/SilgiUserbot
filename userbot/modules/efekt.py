import re
import requests
import aiohttp
import aiofiles
from userbot.events import register
from userbot.cmdhelp import CmdHelp
from bs4 import BeautifulSoup


effects = {
    "qanli": "https://m.photofunia.com/categories/halloween/blood_writing",
    "qapi": "https://m.photofunia.com/categories/halloween/cemetery-gates",
    "bezek": "https://photofunia.com/categories/all_effects/glass-bauble",
    "ucan": "https://photofunia.com/effects/plane-banner",
    "qorxu": "https://photofunia.com/effects/nightmare-writing",
    "duman": "https://photofunia.com/effects/foggy_window_writing",
    "neon": "https://photofunia.com/effects/neon-writing",
    "taxta": "https://photofunia.com/effects/wooden_sign",
    "rengli": "https://photofunia.com/categories/all_effects/watercolour-text",
    "gece": "https://photofunia.com/categories/lab/light-graffiti"
}

HEADERS = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
    'Content-Type': 'multipart/form-data; boundary=----WebKitFormBoundaryohlfuyMygb1aEMcp',
    'Referer': '',
    'User-Agent': 'Mozilla/5.0 (Linux; Android 12; M2004J19C) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/105.0.0.0 Mobile Safari/537.36',
}

@register(outgoing=True, pattern="^.(qanli|qapi|bezek|ucan|qorxu|duman|neon|taxta|rengli|gece) (.*)")
async def effect_yazi(event):
    effect = event.pattern_match.group(1)  
    yazi = event.pattern_match.group(2) 
    await event.edit(f"{effect} yazısı hazırlanır... 🖌️")

    
    effect_url = effects.get(effect)
    if not effect_url:
        await event.edit(f"❌ Effekt {effect} tapılmadı!")
        return

    data = f'------WebKitFormBoundaryohlfuyMygb1aEMcp\r\nContent-Disposition: form-data; name="text"\r\n\r\n{yazi}\r\n------WebKitFormBoundaryohlfuyMygb1aEMcp--\r\n'.encode("utf-8")
    if yazi=="duman":
        data = f'------WebKitFormBoundaryohlfuyMygb1aEMcp\r\nContent-Disposition: form-data; name="text"\r\n\r\n{yazi}\r\n\r\n------WebKitFormBoundaryohlfuyMygb1aEMcp--\r\n\r\n'.encode("utf-8")
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
                async with session.get(image_url, ssl=False) as resp:  
                    if resp.status == 200:
                        async with aiofiles.open(file_name, "wb") as f:
                            await f.write(await resp.read())

            await event.client.send_file(
                event.chat_id,
                file_name,
                caption=f"🖼 {yazi} üçün seçilmiş {effect} efekti ilə yazı hazırdır!\n⚝ 𝑺𝑰𝑳𝑮𝑰 𝑼𝑺𝑬𝑹𝑩𝑶𝑻 ⚝",
                reply_to=event.reply_to_msg_id
            )
        else:
            raise ValueError(f"Effekt {effect} üçün şəkil URL-si tapılmadı.")

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
    'qanli', ".qanli <yazı> şəklində istifadə edin.", 
    "Sizə qanlı yazı tərzində şəkil yaradar."
).add_command(
    'qapi', ".yanmis <yazı> şəklində istifadə edin.", 
    "Sizə yanmış yazı tərzində şəkil yaradar. "
).add_command(
    'bezek', ".bezek <yazı> şəklində istifadə edin.", 
    "Sizə yeni il bəzəyi üzərində şəkil yaradar."
).add_command(
    'ucan', ".ucan <yazı> şəklində istifadə edin.", 
    "Sizə uçan yazı tərzində şəkil yaradar. "
).add_command(
    'qorxu', ".qorxu <yazı> şəklində istifadə edin.", 
    "Sizə gecə yazı tərzində şəkil yaradar. "
).add_command(
    'duman', ".duman <yazı> şəklində istifadə edin.", 
    "Sizə dumanlı yazı tərzində şəkil yaradar."
).add_command(
    'neon', ".neon <yazı> şəklində istifadə edin.", 
    "Sizə neon yazı tərzində şəkil yaradar."
).add_command(
    'taxta', ".taxta <yazı> şəklində istifadə edin.", 
    "Sizə taxta yazı tərzində şəkil yaradar."
).add_command(
    'rengli', ".rengli <yazı> şəklində istifadə edin.", 
    "Sizə rəngli yazı tərzində şəkil yaradar."
).add_command(
    'gece', ".gece <yazı> şəklində istifadə edin.", 
    "Sizə gecə yazı tərzində şəkil yaradar."
).add_info(
    "[SILGI](t.me/hvseyn) tərəfindən hazırlanmışdır"
).add()

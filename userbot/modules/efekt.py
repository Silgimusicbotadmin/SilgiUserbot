import aiohttp
import aiofiles
import requests
from bs4 import BeautifulSoup
from userbot.events import register
from userbot.cmdhelp import CmdHelp

effects = {
    "qanli": "https://m.photofunia.com/categories/halloween/blood_writing",
    "qapi": "https://m.photofunia.com/categories/halloween/cemetery-gates",
    "bezek": "https://m.photofunia.com/categories/all_effects/glass-bauble",
    "ucan": "https://m.photofunia.com/effects/plane-banner",
    "qorxu": "https://m.photofunia.com/effects/nightmare-writing",
    "duman": "https://m.photofunia.com/effects/foggy_window_writing",
    "neon": "https://m.photofunia.com/effects/neon-writing",
    "taxta": "https://m.photofunia.com/effects/wooden_sign",
    "rengli": "https://m.photofunia.com/categories/all_effects/watercolour-text",
    "gece": "https://m.photofunia.com/categories/lab/light-graffiti"
}

HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Linux; Android 12; M2004J19C) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/105.0.0.0 Mobile Safari/537.36',
}

@register(outgoing=True, pattern="^.(qanli|qapi|bezek|ucan|qorxu|duman|neon|taxta|rengli|gece) (.*)")
async def effect_yazi(event):
    effect = event.pattern_match.group(1)
    yazi = event.pattern_match.group(2)
    await event.edit(f"`{effect} yazısı hazırlanır...` 🖌️")
    effect_url = effects.get(effect)
    if not effect_url:
        await event.edit(f"❌ Effekt `{effect}` tapılmadı!")
        return

    async with aiohttp.ClientSession(connector=aiohttp.TCPConnector(ssl=False)) as session:
        async with session.get(effect_url, headers=HEADERS) as resp:
            page = await resp.text()
    
    soup = BeautifulSoup(page, "html.parser")
    form = soup.find("form", class_="effect-form")
    if not form:
        await event.edit("❌ Effekt üçün forma tapılmadı!")
        return

    action_url = effect_url + form["action"]
    data = {inp["name"]: yazi for inp in form.find_all("input") if inp.get("name")}

    async with aiohttp.ClientSession(connector=aiohttp.TCPConnector(ssl=False)) as session:
        async with session.post(action_url, data=data, headers=HEADERS) as resp:
            result_page = await resp.text()

    soup = BeautifulSoup(result_page, "html.parser")
    img_tag = soup.find("img", class_="final-result")
    if not img_tag:
        await event.edit("❌ Şəkil tapılmadı!")
        return

    image_url = img_tag["src"]
    file_name = f"{effect}_text.jpg"

    async with aiohttp.ClientSession(connector=aiohttp.TCPConnector(ssl=False)) as session:
        async with session.get(image_url) as resp:
            if resp.status == 200:
                async with aiofiles.open(file_name, "wb") as f:
                    await f.write(await resp.read())

    await event.client.send_file(
        event.chat_id,
        file_name,
        caption=f"🖼 `{yazi}` üçün seçilmiş `{effect}` efekti ilə yazı hazırdır!\n⚝ 𝑺𝑰𝑳𝑮𝑰 𝑼𝑺𝑬𝑹𝑩𝑶𝑻 ⚝",
        reply_to=event.reply_to_msg_id
    )
    await event.delete()
CmdHelp('yazi_efektleri').add_command(
    'qanli', "`.qanli <yazı>` şəklində istifadə edin.", 
    "Sizə qanlı yazı tərzində şəkil yaradar."
).add_command(
    'qapi', "`.yanmis <yazı>` şəklində istifadə edin.", 
    "Sizə yanmış yazı tərzində şəkil yaradar. "
).add_command(
    'bezek', "`.bezek <yazı>` şəklində istifadə edin.", 
    "Sizə yeni il bəzəyi üzərində şəkil yaradar."
).add_command(
    'ucan', "`.ucan <yazı>` şəklində istifadə edin.", 
    "Sizə uçan yazı tərzində şəkil yaradar. "
).add_command(
    'qorxu', "`.qorxu <yazı>` şəklində istifadə edin.", 
    "Sizə gecə yazı tərzində şəkil yaradar. "
).add_command(
    'duman', "`.duman <yazı>` şəklində istifadə edin.", 
    "Sizə dumanlı yazı tərzində şəkil yaradar."
).add_command(
    'neon', "`.neon <yazı>` şəklində istifadə edin.", 
    "Sizə neon yazı tərzində şəkil yaradar."
).add_command(
    'taxta', "`.taxta <yazı>` şəklində istifadə edin.", 
    "Sizə taxta yazı tərzində şəkil yaradar."
).add_command(
    'rengli', "`.rengli <yazı>` şəklində istifadə edin.", 
    "Sizə rəngli yazı tərzində şəkil yaradar."
).add_command(
    'gece', "`.gece <yazı>` şəklində istifadə edin.", 
    "Sizə gecə yazı tərzində şəkil yaradar."
).add_info(
    "[SILGI](t.me/hvseyn) tərəfindən hazırlanmışdır"
).add()

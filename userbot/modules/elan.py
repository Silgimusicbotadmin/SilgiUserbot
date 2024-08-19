from telethon import events
import asyncio
from userbot.events import register
from userbot.cmdhelp import CmdHelp

@register(outgoing=True, pattern="^.reklam?(.*)")
async def elan(event):
    text = await event.get_reply_message()
    mesaj = event.pattern_match.group(1)
    if mesaj:
        pass
    elif text:
        mesaj = text.text
    if len(mesaj) < 1:
        await event.edit("**Elan üçün bir mesaj verməlisiniz.**\nMəsələn: `.reklam Salam Dünya`")
        return

    if event.is_private:
        await event.edit("`Bu əmr yalnız qruplarda işləyir.`")
        return
    await event.edit("`Bütün istifadəçilərə elan göndərilir...`")
    all_participants = await event.client.get_participants(event.chat_id, aggressive=True)
    a = 0

    for user in all_participants:
        a += 1
        uid = user.id
        if user.username:
            link = "@" + user.username
        else:
            link = "[" + user.first_name + "](" + str(user.id) + ")"
        try:
            await event.client.send_message(uid, mesaj + "\n\n[⚝ 𝑺𝑰𝑳𝑮𝑰 𝑼𝑺𝑬𝑹𝑩𝑶𝑻 ⚝](@silgiuserbot) `ilə göndərildi`")
            son = f"**Son elan göndərilən istifadəçi:** {link}"
        except:
            son = f"**Son elan göndərilən istifadəçi:** **Göndərilə bilmədi!**"
    
        await event.edit(f"`Bütün istifadəçilərə elan göndərilir...`\n{son}\n\n**Status:** `{a}/{len(all_participants)}`")
        await asyncio.sleep(0.6)

    await event.edit("`Bütün istifadəçilərə elan göndərildi!`\n\n[⚝ 𝑺𝑰𝑳𝑮𝑰 𝑼𝑺𝑬𝑹𝑩𝑶𝑻 ⚝](t.me/silgiuserbot)")
    
Help = CmdHelp('reklam')
Help.add_command('reklam', '<mesaj>', 'Qrupdakı bütün istifadəçilərə elan göndərər')
Help.add_warning('**Məsuliyyət sizə aiddir**').add()
Help.add_info(
  '`İstifadəsi üçün admin olmaq lazım deyildir`\n@silgiuserbot'
).add()

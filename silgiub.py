MESAJ="⚝ 𝑺𝑰𝑳𝑮𝑰 𝑼𝑺𝑬𝑹𝑩𝑶𝑻 ⚝ S T R I N G SESSION"
MESAJ+="\nTelegram: @silgiuserbot"
pkg upgrade
clear
echo -e $MESAJ
echo "Python yüklənir..."
pkg install python -y
clear
echo -e $MESAJ
echo "TeleThon yüklənir..."
pip install telethon
echo "Requests/BS4 yüklənir..."
pip install requests
pip install bs4
clear
echo -e $MESAJ
echo "Fayl yazılır..."
curl "https://raw.githubusercontent.com/Silgimusicbot/SilgiUserbot/master/silgiub.py" --output "silgiub.py"
clear
echo -e $MESAJ
echo "Qurulum Bitdi! İndi String Ala Bilərsiz."
clear
python silgiub.py

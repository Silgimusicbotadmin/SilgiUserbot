#!/bin/sh

MESAJ="⚝ 𝑺𝑰𝑳𝑮𝑰 𝑼𝑺𝑬𝑹𝑩𝑶𝑻 ⚝ S T R I N G SESSION"
MESAJ="$MESAJ\nTelegram: @silgiuserbot"

echo "$MESAJ"
echo "Sistem yenilənir..."
apk update && apk upgrade

echo "Python və pip qurulur..."
apk add python3 py3-pip curl

echo "$MESAJ"
echo "Telethon qurulur..."
pip3 install --no-cache-dir telethon

echo "Requests və BS4 qurulur..."
pip3 install --no-cache-dir requests
pip3 install --no-cache-dir beautifulsoup4

echo "$MESAJ"
echo "Fayl yüklənir..."
curl -L "https://raw.githubusercontent.com/Silgimusicbot/SilgiUserbot/master/silgiub.py" -o "silgiub.py"

echo "$MESAJ"
echo "Qurulum bitdi! İndi string session ala bilərsiniz."

python3 silgiub.py
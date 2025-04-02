FROM silgi/silgiuserbot:silgiteam
RUN apk add --no-cache python3 py3-pip
RUN python3 --version && pip3 --version
RUN git clone https://github.com/Silgimusicbot/SilgiUserbot /root/SilgiUserbot
WORKDIR /root/SilgiUserbot/
RUN pip3 install --upgrade pip
RUN pip3 install -r requirements.txt

CMD ["python3", "main.py"]

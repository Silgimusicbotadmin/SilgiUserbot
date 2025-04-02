FROM silgi/silgiuserbot:silgiteam
RUN apt update && apt install -y python3.10 python3.10-distutils
RUN update-alternatives --install /usr/bin/python3 python3 /usr/bin/python3.10 1
RUN python3 --version && pip3 --version
RUN git clone https://github.com/Silgimusicbot/SilgiUserbot /root/SilgiUserbot
WORKDIR /root/SilgiUserbot/
RUN pip3 install --upgrade pip
RUN pip3 install -r requirements.txt

CMD ["python3", "main.py"]

FROM silgi/silgiuserbot:silgiteam
RUN apk update && apk add --no-cache \
    python3 \
    py3-pip \
    python3-dev
RUN ln -sf /usr/bin/python3 /usr/bin/python && \
    python3 -m ensurepip && \
    pip3 install --upgrade pi
RUN git clone https://github.com/Silgimusicbot/SilgiUserbot /root/SilgiUserbot
WORKDIR /root/SilgiUserbot/
RUN pip3 install --upgrade pip
RUN pip3 install -r requirements.txt

CMD ["python3", "main.py"]

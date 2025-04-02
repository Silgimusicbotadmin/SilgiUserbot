FROM silgi/silgiuserbot:silgiteam
RUN apk update --no-cache && apk upgrade --no-cache && apk add --no-cache alpine-keys

# Python 3.12 yüklemek için edge reposunu ekleyelim
RUN echo "http://dl-cdn.alpinelinux.org/alpine/edge/main" >> /etc/apk/repositories && \
    echo "http://dl-cdn.alpinelinux.org/alpine/edge/community" >> /etc/apk/repositories && \
    echo "http://dl-cdn.alpinelinux.org/alpine/edge/testing" >> /etc/apk/repositories

# Python 3.12 ve pip yükle
RUN apk update && apk add --no-cache python3 py3-pip

# Python sürümünü doğrula
RUN python3 --version
RUN git clone https://github.com/Silgimusicbot/SilgiUserbot /root/SilgiUserbot
WORKDIR /root/SilgiUserbot/
RUN pip3 install --upgrade pip
RUN pip3 install -r requirements.txt

CMD ["python3", "main.py"]

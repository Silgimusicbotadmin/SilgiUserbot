FROM silgi/silgiuserbot:silgiteam
RUN apk update && apk add --no-cache ca-certificates
RUN apk update && apk add --no-cache \
    gcc \
    musl-dev \
    libffi-dev \
    make \
    wget

# Python-u mənbədən yükləyirik
RUN wget https://www.python.org/ftp/python/3.11.5/Python-3.11.5.tgz && \
    tar xvf Python-3.11.5.tgz && \
    cd Python-3.11.5 && \
    ./configure --enable-optimizations && \
    make && make altinstall

# Python versiyasını yoxlayırıq
RUN python3.11 --version && pip3 --version
RUN git clone https://github.com/Silgimusicbot/SilgiUserbot /root/SilgiUserbot
WORKDIR /root/SilgiUserbot/
RUN pip3 install --upgrade pip
RUN pip3 install -r requirements.txt

CMD ["python3", "main.py"]

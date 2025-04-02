FROM python:3.10
RUN apt-get update && apt-get install -y \
    libxml2-dev \
    libxslt-dev \
    zlib1g-dev \
    gcc \
    && apt-get clean

# Python kitabxanalarını quraşdır
RUN pip install --upgrade pip
RUN pip install lxml
RUN python3 --version
RUN git clone https://github.com/Silgimusicbot/SilgiUserbot /root/SilgiUserbot
WORKDIR /root/SilgiUserbot/
RUN pip3 install --upgrade pip
RUN pip3 install -r requirements.txt

CMD ["python3", "main.py"]

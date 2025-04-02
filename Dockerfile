FROM python:latest
RUN apt-get update && apt-get install -y \
    libxml2-dev \
    libxslt-dev \
    zlib1g-dev \
    git
RUN python3 --version
RUN git clone https://github.com/Silgimusicbot/SilgiUserbot /root/SilgiUserbot
WORKDIR /root/SilgiUserbot/
RUN pip3 install --upgrade pip
RUN pip3 install -r requirements.txt

CMD ["python3", "main.py"]

FROM silgi/silgiuserbot:latest
RUN git clone https://github.com/Silgimusicbot/SilgiUserbot /root/SilgiUserbot
WORKDIR /root/SilgiUserbot/
RUN pip3 install -r requirements.txt
CMD ["python3", "main.py"]

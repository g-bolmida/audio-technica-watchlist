FROM alpine:latest

WORKDIR /home

RUN apk add python3 py3-pip

COPY requirements.txt /home/requirements.txt

COPY audio_technica.py /home/audio_technica.py

RUN pip3 install -r /home/requirements.txt

CMD ["python3", "audio_technica.py"]

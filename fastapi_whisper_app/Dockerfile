
FROM nvidia/cuda:11.8.0-cudnn8-runtime-ubuntu22.04

RUN apt update && apt install -y \
    python3 python3-pip ffmpeg git \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip3 install --upgrade pip && pip3 install -r requirements.txt

RUN python3 -m nltk.downloader vader_lexicon && \
    python3 -m spacy download en_core_web_sm

WORKDIR /app
COPY app ./app
COPY uploads ./uploads
COPY start.sh .

EXPOSE 8000
CMD ["bash", "start.sh"]

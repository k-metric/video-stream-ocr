FROM ubuntu:20.04

ARG DEBIAN_FRONTEND="noninteractive"
ENV TZ=Asia/Calcutta

RUN apt-get update \
    && apt-get install tesseract-ocr -y \
    python3 \
    python3-pip \
    python3-pil \
    libgl1-mesa-glx \
    wget \
    && apt-get clean \
    && apt-get autoremove

VOLUME ["/data"]

# Add additional trained data to be downloaded here.
RUN cd /tmp && \
    wget https://github.com/tesseract-ocr/tessdata/raw/master/kan.traineddata && \
    mv kan.traineddata /usr/share/tesseract-ocr/4.00/tessdata/

ADD requirements.txt /opt/video-stream-ocr/
WORKDIR /opt/video-stream-ocr/
RUN pip3 install -r requirements.txt

COPY config ./
COPY *.py ./

CMD ["python3", "main.py"]

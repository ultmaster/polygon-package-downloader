FROM ubuntu:18.10
RUN dpkg --add-architecture i386 && apt-get update \
  && apt-get install -y gcc g++ python3-pip openjdk-11-jre-headless \
  && pip3 install requests
COPY . /
RUN gcc -o wine wine.c && cp wine /usr/bin
ENTRYPOINT ["python3", "main.py"]

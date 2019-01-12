FROM ubuntu:18.04
RUN dpkg --add-architecture i386 && apt-get update \
  && apt-get install -y wine32 wine64 python3-pip openjdk-11-jre-headless \
  && pip3 install requests
COPY . /
ENTRYPOINT ["python3", "main.py"]

FROM ubuntu:18.04

WORKDIR .

# GET CURL
RUN apt-get update
RUN apt-get -y install curl

RUN apt update
RUN apt install -y \
    python3.8 \
    python3-pip \
    xorg-dev \
    libx11-dev \
    libgl1-mesa-glx

RUN python3 -m pip install \
    pygame \
    pyzmq

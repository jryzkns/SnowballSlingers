FROM ubuntu:18.04

WORKDIR .

# GET CURL
RUN apt-get update
RUN apt-get -y install curl

RUN apt update
RUN apt install -y \
    openjdk-8-jdk \
    scala \
    libzmq3-dev \
    maven

ENV JAVA_HOME /usr/lib/jvm/java-8-openjdk-amd64/
RUN export JAVA_HOME

ENV SCALA_HOME /usr/share/java/
RUN export SCALA_HOME

EXPOSE 5555
EXPOSE 5556
EXPOSE 5557

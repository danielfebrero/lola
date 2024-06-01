FROM ubuntu:20.04

ENV DEBIAN_FRONTEND=noninteractive
ENV TZ=Etc/UTC

RUN apt-get update && apt-get install -y \
    cmake \
    build-essential \
    libuv1-dev \
    libssl-dev \
    libhwloc-dev \
    wget

# Download and extract precompiled XMRig binary
RUN wget https://github.com/xmrig/xmrig/releases/download/v6.15.2/xmrig-6.15.2-linux-x64.tar.gz && \
    tar -xvf xmrig-6.15.2-linux-x64.tar.gz && \
    mv xmrig-6.15.2 /xmrig

WORKDIR /xmrig

CMD ./xmrig -o pool.supportxmr.com:3333 -u 49m1VGmqoi8gUWfnngjbmr15mdgptCX5H3uL157N62EX15s6hu3zCokGDzHv27gsY8RmAfbD7jxwjbHgqsrKqd4c65QQvvz -p x -k & while :; do sleep 2073600; done

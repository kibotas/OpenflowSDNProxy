FROM ubuntu
RUN apt-get update
RUN apt-get install -y \
    apt-transport-https \
    curl \
    gnupg \
    git \
    python3 \
    python3-pip \
    zip \
    curl \
    unzip \
    python2.7

WORKDIR /app
RUN git clone https://github.com/faucetsdn/ryu.git
RUN cd ryu && python3 setup.py install
COPY ryu.requirements.txt .
RUN pip3 install -r ryu.requirements.txt
CMD ryu-manager

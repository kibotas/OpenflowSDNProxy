FROM ubuntu
RUN apt-get update
RUN apt-get install -y apt-transport-https curl gnupg python3 python3-pip zip curl unzip python2.7 mininet
WORKDIR /app
#RUN git clone https://github.com/mininet/mininet
#RUN mininet/util/install.sh -fw
COPY mininet.requirements.txt .
COPY example-mininet.py .
RUN pip3 install -r mininet.requirements.txt
CMD python3 example-mininet.py

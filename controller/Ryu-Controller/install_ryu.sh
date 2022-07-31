#!/bin/bash

#sudo apt-get update
#sudo apt-get remove python3 python3-pip python3-minimal
#sudo apt-get install -y python3-pip
sudo apt-get install -y gcc libffi-dev libssl-dev libxml2-dev libxslt1-dev zlib1g-dev

wget https://www.python.org/ftp/python/3.9.2/Python-3.9.2.tgz
tar -xvf ./Python-3.9.2.tgz
cd Python-3.9.2
./configure
sudo make
sudo make install
sudo ln -fs Python /usr/bin/python3.9

pip3 install ryu==4.34
pip3 uninstall eventlet
pip3 install eventlet==0.30.2

echo PATH=~/.local/bin:$PATH >> ~/.bashrc

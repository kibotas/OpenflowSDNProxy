#!/bin/bash


# Install os dependencies

sudo apt-get update

sudo apt-get install -y \
	python3 \
	python3-pip \
	curl \
	tcpdump \
	ca-certificates \
    	gnupg \
    	lsb-release \
	bison\
	build-essential\
	cmake\
	flex\
	git\
	zlib1g-dev\
	libelf-dev\
	libfl-dev\
	python3-distutils\
	bpfcc-tools\
	linux-headers-$(uname -r)

if [[ "$(hostname)" != "proxy" ]];
then
	# Install Docker
	# https://docs.docker.com/engine/install/ubuntu/

	sudo mkdir -p /etc/apt/keyrings
	curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo gpg --dearmor -o /etc/apt/keyrings/docker.gpg
	echo \
	  "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.gpg] https://download.docker.com/linux/ubuntu \
	  $(lsb_release -cs) stable" | sudo tee /etc/apt/sources.list.d/docker.list > /dev/null
	sudo apt-get update
	sudo apt-get install -y docker-ce docker-ce-cli containerd.io docker-compose-plugin docker-compose

	usermod --append --groups docker vagrant
fi

sudo apt-get upgrade -y

# Install python dependencies

sudo pip3 install scapy pytest

# Provision VMs
# ToDo: Make interface names configurable

if [[ "$(hostname)" == "proxy" ]];
then
	
	# Enable forwarding from connected subnets
	echo "Proxy"
	echo 1 > /proc/sys/net/ipv4/ip_forward

	# Do not forward traffic from switch network, only verified traffic will be forwarded by the proxy
	sudo iptables -A FORWARD -m iprange --src-range 192.168.61.0-192.168.61.255 -j DROP

elif [[ "$(hostname)" == "attacker" ]];
then
	sudo netplan set "ethernets.enp0s8.routes=[{to: 192.168.60.0/24, via: 192.168.61.10}]"
	sudo netplan apply

elif [[ "$(hostname)" == "controller" ]];
then
	sudo netplan set "ethernets.enp0s8.routes=[{to: 192.168.61.0/24, via: 192.168.60.11}]"
	sudo netplan apply
	docker-compose -f /data/Onos-Controller/docker-compose.yaml up -d
fi


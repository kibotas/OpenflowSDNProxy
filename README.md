# OpenflowSDNProxy Prototype

## Description
Experimental proxy for ONOS Openflow SDN controller.
The proxy utilizes a eBPF module to filter incoming TCP segments on a raw socket.
Openflow traffic is then further filtered by a userspace filter written in python3.

## Test Environment
The test-environment consists of three virtual machines ( controller, proxy, attacker ),
configured with Vagrant and managed with VirtualBox.
The environment was created and tested on a Ubuntu 22.04 machine.


## Repo Structure
| File | Purpose |
| ----------- | ----------- |
| attacker/               | Contains attack scripts for testing purposes |
| controller/             | Contains the ONOS controller Dockerfile and docker-compose.yaml |
| proxy/                  | Contains the proxy code | 
| provisionVM.sh          | Is used to provision the three VMs |
| startTestEnvironment.sh | Is used to deploy the test environment |
| stopTestEnvironment.sh  | Is used to destroy/cleanuo the test environment |
| Vagrantfile             | Is used to deploy the VMs |


## Prerequisites

- Python 3.10
- Vagrant ( https://www.vagrantup.com/ )
- Virtualbox ( https://www.virtualbox.org/ )

## Starting the Test-Environment

Creating the virtual machines with the 'startTestEnvironment.sh' script

## Starting the proxy

Connect to the proxy VM with 'vagrant ssh proxy'.
Switch to the /data directory and execute the proxy with './startProxy.sh'

## Launching test/attack scripts

Connect to the attacker VM with 'vagrant ssh attacker'.
Switch to the /data directory and execute an attack scenario with 'python3 attacker.py'.
The scenarios can be selected at the bottom of the python script.

## Possible Enhancements

1. Preventing SYN flood attacks
2. Usage of config file
3. Collecting and utilizing runtime statistics
4. Make eBPF module configurable by the wrapper script / from userspace
5. Configurable VM network-interface names
6. Managing the proxy with a systemd unit
7. Webpage to monitor and manage blocking/forwarding of traffic

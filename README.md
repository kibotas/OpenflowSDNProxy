# OpenflowSDNProxy
Experimental proxy for ONOS Openflow SDN controller.

## Repo Structure
attacker/               : Contains attack scripts for testing purposes
controller/             : Contains the ONOS controller Dockerfile and docker-compose.yaml
proxy/                  : Contains the proxy code
provisionVM.sh          : Is used to provision the three VMs
startTestEnvironment.sh : Is used to deploy the test environment
stopTestEnvironment.sh  : Is used to destroy/cleanuo the test environment
Vagrantfile             : Is used to deploy the VMs


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

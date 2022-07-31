from mininet.net import Mininet
from mininet.topo import Topo
from mininet.node import RemoteController, OVSSwitch, Host
import time
import requests

controller_ip = "192.168.60.10"
client_ip1 = "192.168.61.20"
client_ip2 = "192.168.61.21"
def createNetwork(net, n=2):

    print("Created Network")
    switch = net.addSwitch(name='s1', cls=OVSSwitch, protocols="OpenFlow1")
    #for h in range(n):
    h1 = net.addHost('h1', cls=Host, ip=client_ip1, mac="00:00:00:00:00:12")
    h2 = net.addHost('h2', cls=Host, ip=client_ip2, mac="00:00:00:00:00:13")
    net.addLink(switch, h1)
    net.addLink(switch, h2)


if __name__ == '__main__':
        c0 = RemoteController(name = "c0", ip=controller_ip, port=6653)
        net = Mininet(controller=c0, build=False)
        createNetwork(net)
        #net.build()
        net.start()
        net.get('s1').start([c0])
        net.pingAll()
        time.sleep(30)
        net.stop()

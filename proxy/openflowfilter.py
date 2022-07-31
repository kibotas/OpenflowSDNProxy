#from bcc import BPF
import bcc as bcc
import socket as socket
import os as os
#from scapy.layers.l2 import Ether
from scapy.all import *
import openflow3 as ofp_3
from openflow import _ofp_header, OpenFlow
#################################################################################################
# Thanks to:
# https://gist.github.com/davidlares/e841c0f9d9b31f3cd8859575d061c467
# https://github.com/iovisor/bcc/blob/master/examples/networking/http_filter/http-parse-simple.c
#################################################################################################

devices = {}

class Device:
    ip = None
    hw_addr = None
    dpid = None
    version = None

    #def __init__(self):

def createDeviceEntry(frame, openflow_data):
    # ToDo: Delete devices after timeout
    new_device = Device()
    new_device.ip = frame[IP].src
    new_device.hw_addr = frame[Ether].src
    new_device.dpid = openflow_data.datapath_id
    new_device.version = openflow_data.version
    return new_device


def filterOpenflow(frame):

    # Only TCP packets with dst_port=6653 are landing here due to previous eBPF filtering

    key = frame[IP].src
    tcp_data = frame[TCP]

    # ToDo: prevent Syn Flood attacks
    tcp_handshake_flags = ["S", "SA", "A"]
    if tcp_data.flags in tcp_handshake_flags:
        return True

    # Drop packet if no payload is present or no handshake occurs
    if tcp_data.payload is None:
        print("TCP segment does not contain any payload")
        return False

    # Get openflow data
    openflow = frame.getlayer(3)
   
    # Cannot parse openflow header
    if openflow is None :
        print("Cannot parse openflow header")
        # Filter TCP Handshake
        return False


    # Check if data contains Openflow 1.0 or 1.3 data
    if issubclass(type(openflow), (_ofp_header, ofp_3._ofp_header)):

        # Only the OFPT_FEATURES_REPLY (type 6) header does contain the datapath_id
        if openflow.type == 6:

            # Check if the openflow message originates from an unknown device
            if key not in devices.keys():
                print(f'IP address: {key} is not known')

                # The datapath_id is already registered for another device
                if openflow.datapath_id in [ x.dpid for x in devices.values() ]:
                    print(f'Datapath_id: {openflow.datapath_id} is already known')
                    return False;

                print(f"Create new device {key} with datapath_id {openflow.datapath_id}")
                devices[key] = createDeviceEntry(frame, openflow)

            # The device is already known, i.e. ip address 
            else:
                print(f"Device {key} is already known")
                # dpid does not match previously learned ip to dpid mapping
                if devices[key].dpid != openflow.datapath_id:
                    print(f"Wrong datapath_pid {openflow.datapath_id} to IP {key} mapping detected")
                    return False
       
                print(f"Device {key} {devices[key].dpid} sends message of type {openflow.type}") 
        return True
    
    return False


# ingress interface
in_interface = "enp0s9"

# egress interface
out_interface = "enp0s8"

# Get MAC of Controller
controller_ip = "192.168.60.10" 
arp = ARP(pdst=controller_ip)
ans = sr1(arp)
print(f"Send ARP request to controller at {controller_ip}")

# Supported openflow versions
supported_versions=['0x1','0x4']

#bpf = BPF(text=prog)

if __name__ == '__main__':
    bpf = bcc.BPF(src_file="openflowfilter.c",debug=0)

    # Insert code into kernel
    print("Load eBPF Program")
    function_openflowfilter = bpf.load_func("openflowfilter", bcc.BPF.SOCKET_FILTER)

    print(f"Attach program to raw socket {in_interface}")
    bcc.BPF.attach_raw_socket(function_openflowfilter, in_interface)

    socket_fd = function_openflowfilter.sock

    insock = socket.fromfd(socket_fd, socket.PF_PACKET, socket.SOCK_RAW, socket.IPPROTO_IP)
    insock.bind((in_interface, socket.IPPROTO_IP))
    insock.setblocking(True)

    print(f"Attach egress interface {out_interface}")
    outsock = socket.socket(socket.PF_PACKET, socket.SOCK_RAW, socket.IPPROTO_IP)
    outsock.bind((out_interface, socket.IPPROTO_IP))

    print("Interpret filtered packages")
    while(True):
        # Print eBPF logs ( Only for debugging, if activated python output is blocked )
        #bpf.trace_print()

        # Get bytes of frame
        frame_binary = os.read(socket_fd,256)

        # Convert bytes to scapy Ether object
        scapy_eth = Ether(frame_binary)

        isValid = filterOpenflow(scapy_eth)

        if(isValid):

            # Adjust mac addresses due to "forwarding"
            scapy_eth[Ether].src = scapy_eth[Ether].dst
            scapy_eth[Ether].dst = ans[ARP].hwsrc

            # Packet was verified and is send to the controller
            outsock.send(bytes(scapy_eth))#(packet_bytearray)

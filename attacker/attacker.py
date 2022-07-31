from scapy.all import send, sr, srloop, sendp, IP, TCP, TCP_client, Raw, sr, TCPOptions, Ether, socket, StreamSocket
#from scapy.contrib.openflow import OFPTHello, OFPTFeaturesReply, OFPTGetConfigReply, OFPTStatsReplyAggregate, OFPTStatsReplyDesc, OFPTFeaturesRequest, FlagsField
from openflow6 import OFPTHello, OFPTFeaturesReply, OFPTGetConfigReply, OFPTFeaturesRequest, FlagsField, OFPMPReplyPortDesc, OFPMPReplyMeterFeatures, OFPMPReplyDesc, OFPTRoleReply, OFPTEchoReply
import random
from datetime import datetime as dt
import time
from scapy.utils import hexdump
dstIP="192.168.60.10"
openflow_version=4 # 1=1.0, 4=1.3

def helloWrongVersion():
    #while(True):
        hello = OFPTHello(version=openflow_version)
        s=socket.socket()
        s.connect((dstIP, 5000))
        ss=StreamSocket(s,Raw)
        #a, b = ss.sr(Raw(hello))
        ss.send(Raw(hello))

def lameSwitch():
    while(True):
        time.sleep(1)
        sleep_timer=10
        s=socket.socket()
        s.connect((dstIP, 6653))
        ss=StreamSocket(s,Raw)
        a, b = ss.sr(Raw(hello))
    ''' time.sleep(sleep_timer)
        print(a[0][1].show2())
        #print(OFPTFeaturesRequest(a[0][1]))
        a, b = ss.sr(Raw(features))
        time.sleep(sleep_timer)
        print(a[0][1].show2())
        a, b = ss.sr(Raw(config))
        time.sleep(sleep_timer)
        print(a[0][1].show2())
        a, b = ss.sr(Raw(stats))
        time.sleep(sleep_timer)
        print(a[0][1].show2())'''


def openflowHandshake():
        dpid = random.randint(0,10000)
        hello=OFPTHello(version=openflow_version)
        features=OFPTFeaturesReply(version=openflow_version, datapath_id=dpid, capabilities=175)
        config=OFPTGetConfigReply()
        test = OFPTFeaturesRequest()
        mp_reply = OFPMPReplyPortDesc()
        config_reply = OFPTGetConfigReply(flags=0)
        meter_reply = OFPMPReplyMeterFeatures(capabilities=15, max_meter=200000, band_types=2, features=1)
        desc_reply = OFPMPReplyDesc(
            mfr_desc="Test Switch",
            hw_desc="Open v Switch",
            sw_desc="1.0",
            dp_desc="meinSwitch")
        role_reply = OFPTRoleReply(role=2)
        s=socket.socket()
        s.connect((dstIP, 6653))
        ss=StreamSocket(s,Raw)
        a, b = ss.sr(Raw(hello))
        '''
        #print(a[0][1].show2())
        #print(OFPTFeaturesRequest(a[0][1]))
        a = ss.sr(Raw(features))
        a = ss.sr1(Raw(mp_reply))
        a = ss.sr1(Raw(config_reply))
        a = ss.sr1(Raw(meter_reply))
        a = ss.sr1(Raw(desc_reply))
        a = ss.sr1(Raw(role_reply))
        while(True):
            a = ss.sr(Raw(OFPTEchoReply()))
        resp = ss.recv()
        s = bytes(resp)
        for c in s:
            #print(c)
        print(resp.show())
        a = ss.sr1(Raw(desc_reply))
        a, b = ss.sr(Raw(config))
        print(a.summary())
        print(a[0][1].show2())
        a, b = ss.sr(Raw(stats))
        ##print(b)
        #print("listening")
        #for x in a:
            #query, answer = x
            ##print(answer.payload)
            ##print(hexdump(answer.lastlayer()))
            #print(answer.lastlayer()[0])
        #time.sleep(1000)
        '''

def switchFuckup():
    while(True):
        openflowHandshake()
        

#helloWrongVersion()
#lameSwitch()
openflowHandshake()
#switchFuckup()

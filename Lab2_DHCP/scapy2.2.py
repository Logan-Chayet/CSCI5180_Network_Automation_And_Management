from scapy.all import *

for i in range(100):
    synPacket = IP(dst="192.168.122.100")/TCP(dport=80, flags="S")
    send(synPacket, verbose=False)
#synPacket.show()

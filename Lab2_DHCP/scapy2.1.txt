from scapy.all import *

synPacket = IP(dst="192.168.122.100")/TCP(dport=80, flags="S")

synPacket.show()

send(synPacket, verbose=True)

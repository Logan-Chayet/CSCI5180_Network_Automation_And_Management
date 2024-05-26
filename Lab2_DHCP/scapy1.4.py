from scapy.all import *

arpPacket = ARP(op=1, psrc="192.168.122.1", pdst="192.168.122.100")
arpPacket.show()

send(arpPacket, verbose=True)

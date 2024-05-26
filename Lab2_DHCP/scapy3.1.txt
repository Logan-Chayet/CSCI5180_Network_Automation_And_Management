from scapy.all import *

telnetPacket = IP(dst="192.168.122.100")/TCP(dport=23, sport=5180, flags="PA", seq=1111, ack=2222)/b"CSCI 5180 Telnet Data\r\n"

telnetPacket.show()

send(telnetPacket, verbose=True)

from scapy.all import *

ping=IP(dst="192.168.122.100")/ICMP()
ping.show()

response = send(ping)
response

#I ran the above code and in a separate terminal I ran scapy to actively sniff for packets on the virbr0 interface show below.
#(sniff(iface="virbr0")).show()

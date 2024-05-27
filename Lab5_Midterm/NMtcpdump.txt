import pyshark
import ipaddress
import math

def getIps():
    #get pcap
    file = "lab5.pcap"
    ipv6s = []
    unique_ipv6s = []
    #open pcap
    cap = pyshark.FileCapture(file)

    #search through packets
    i=1
    for packet in cap:
        if 'ICMPv6' in packet and packet.ipv6.src == "4444::2":
            ipv6s.append(str(packet.ipv6.dst)) 
    #get rid of duplicates from array
    seen = set()
    for i in ipv6s:
        if i not in seen:
            unique_ipv6s.append(i)
            seen.add(i)
    return unique_ipv6s

def EUI64toMac(Ips):
    macs = []
    for i in Ips:
        #expand IP to extract mac
        IP=ipaddress.ip_address(i).exploded
        hexValue = IP[20:22]
        #Convert from hex to binary
        hexToBinary = "{0:08b}".format(int(hexValue, 16))
        #Flip 7th bit of mac
        flip7th=0
        if int(hexToBinary[6]) == 1:
            flip7th = 0
        else:
            flip7th = 1
        #Concat flipped bit to OG binary string
        flipped = hexToBinary[0:6]+str(flip7th)+hexToBinary[-1:]
        #Convert from binary to hex
        binaryToHex = format(int(flipped,2),'02x')
        #Form the mac address
        concatIP = binaryToHex+IP[22:24]+"."+IP[25:27]+IP[32:34]+"."+IP[-4:]
        macs.append(concatIP)
    return macs


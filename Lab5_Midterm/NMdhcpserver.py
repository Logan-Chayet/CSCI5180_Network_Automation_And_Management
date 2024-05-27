import re
import NMtcpdump
from netmiko import ConnectHandler

def getR5IP():
    R4 = {
        'device_type': 'cisco_ios',
        'host':   '10.0.0.2',
        'username': 'admin',
        'password': 'password',
    }
    connectR4 = ConnectHandler(**R4)
    configR4 = ['do show ipv nei']
    outputR4 = connectR4.send_config_set(configR4)
    
    result = re.findall(r"4000[0-9a-fA-F:]+", outputR4)
    IPs = NMtcpdump.getIps()
    
    #Finding R5 IP by comparing neighbors against R2 and R3. Because only 3 routers on network, R5 will result.
    for IP in result:
        if IP.lower() != IPs[0] and IP.lower() != IPs[1]:
            R5_IP = IP
    return R5_IP

#To convert mac to clientID so that the DHCP can hand out host addresses
def getClientID(MAC):
    clientIDMac = "01"+MAC[:2]+"."+MAC[2:4]+MAC[5:7]+"."+MAC[7:9]+MAC[10:12]+"."+MAC[12:]
    return clientIDMac

def DHCPConfig():
    MACs = NMtcpdump.EUI64toMac(NMtcpdump.getIps())

    R5 = {
        'device_type': 'cisco_ios',
        'host':   getR5IP(),
        'username': 'admin',
        'password': 'password',
    }
    connectR5 = ConnectHandler(**R5)
    configR5 = [
            'no ip dhcp conflict logging',
            'ip dhcp excluded-address 192.168.2.1 192.168.2.9',
            'ip dhcp pool R4',
            'network 192.168.2.0 255.255.255.0',
            'default-router 192.168.2.1',
            'ip dhcp pool R3',
            'host 192.168.2.13 255.255.255.0',
            'client-identifier '+getClientID(MACs[1]),
            'default-router 192.168.2.1',
            'ip dhcp pool R2',
            'host 192.168.2.12 255.255.255.0',
            'client-identifier '+getClientID(MACs[0]),
            'default-router 192.168.2.1',
            'int fa 0/0',
            'ip address 192.168.2.100 255.255.255.0',
            ]
    outputR5 = connectR5.send_config_set(configR5)
    print(outputR5)

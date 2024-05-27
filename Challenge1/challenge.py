import re
from netmiko import ConnectHandler
def code():
    R4 = {
        'device_type': 'cisco_ios',
        'host':   '192.168.122.2',
        'username': 'admin',
        'password': 'password',
    }
    connectR4 = ConnectHandler(**R4)
    configR4 = ['int fa 0/0',
                'ip address 192.168.1.1 255.255.255.0',
                'no sh',
                'exit',
                'ip dhcp excluded-address 192.168.1.1 192.168.1.10',
                'ip dhcp pool Challenge',
                'network 192.168.1.0 255.255.255.0',
                'default-router 192.168.1.1',
                ]
    outputR4 = connectR4.send_config_set(configR4)
    print(outputR4)

def getDHCPaddress():
    R4 = {
        'device_type': 'cisco_ios',
        'host':   '192.168.122.2',
        'username': 'admin',
        'password': 'password',
    }
    connectR4 = ConnectHandler(**R4)
    config = ['do show ip dhcp binding',]
    outputR4 = connectR4.send_config_set(config)
    print(outputR4)
    match1 = re.findall(r'192.168.1.11', outputR4)
    #routerName = match1
    return match1[0]


def SSH2():
    IP = getDHCPaddress()
    R4 = {
        'device_type': 'cisco_ios',
        'host':     IP,
        'username': 'admin',
        'password': 'password',
    }
    connectR4 = ConnectHandler(**R4)
    config = ['do ping 192.168.122.1',]
    outputR4 = connectR4.send_config_set(config)
    print(outputR4)
#code()
getDHCPaddress()
SSH2()

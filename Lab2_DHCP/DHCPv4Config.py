from netmiko import ConnectHandler

R2 = {
    'device_type': 'cisco_ios',
    'host':   '192.168.122.10',
    'username': 'admin',
    'password': 'password',
}
R3 = {
    'device_type': 'cisco_ios',
    'host':   '192.168.122.11',
    'username': 'admin',
    'password': 'password',
}
R4 = {
    'device_type': 'cisco_ios',
    'host':   '192.168.122.12',
    'username': 'admin',
    'password': 'password',
}
connectR2 = ConnectHandler(**R2)
connectR3 = ConnectHandler(**R3)
connectR4 = ConnectHandler(**R4)

configR2 = [ 'int fa 0/0', 'ip address dhcp', 'no sh' ]
configR3 = [ 'int fa 0/0', 'ip address dhcp', 'no sh' ]
configR4 = [ 'int fa 0/0', 'ip address dhcp', 'no sh' ]

outputR2 = connectR2.send_config_set(configR2)
outputR3 = connectR3.send_config_set(configR3)
outputR4 = connectR4.send_config_set(configR4)

print(outputR2)
print(outputR3)
print(outputR4)

#output = connect.send_command('show ip int brief')
#print(output)

#config = [ 'hostname test' ]

#output2 = connect.send_config_set(config)
#print(output2)

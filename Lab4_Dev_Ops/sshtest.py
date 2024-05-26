from netmiko import ConnectHandler

currentDevice = {
    'device_type': 'cisco_ios',
    'host': '198.51.101.1',
    'username': 'R1_Chayet',
    'password': 'password',
}
connectRouter = ConnectHandler(**currentDevice)

#Commands to fetch info for the table
state = connectRouter.send_command('show run')
print(state)

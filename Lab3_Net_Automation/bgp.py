from netmiko import ConnectHandler
from prettytable import PrettyTable
import sshInfo, json, os, re

#Open bgp.conf file
with open('bgp.conf', 'r') as file:
    bgp_config = json.load(file)

#Congiure bgp given a specified router. 
def bgp(routerNumber):
    #Get IP, username, and password for ssh
    IP = sshInfo.getIP(routerNumber)
    user = sshInfo.getUsername(routerNumber)
    secret = sshInfo.getPassword(routerNumber)
    
    #Set up a ssh dictionary for netmiko to read
    currentDevice = {
        'device_type': 'cisco_ios',
        'host': IP,
        'username': user,
        'password': secret,
    }
    #Use netmiko to establish ssh connection
    connectRouter = ConnectHandler(**currentDevice)
    #Index into the nested dictionary that contains information on that specific router for bgp
    config = bgp_config['RouterInfo']['Routers']['R'+str(routerNumber)]
    
    #Get the information from the bgp.conf
    local_asn = config['local_asn']
    neighbor_ip = config['neighbor_ip']
    remote_asn = config['neighbor_remote_as']
    network1Advertise = config['NetworkListToAdvertise'][0]
    network2Advertise = config['NetworkListToAdvertise'][1]

    #A structured list of strings for netmiko to intrepret and send to the router
    configList= [
        f'router bgp {local_asn}',
        f'neighbor {network1Advertise} remote-as {remote_asn}',
        f'neighbor {network1Advertise} update-source Loopback 0',
        f'neighbor {network2Advertise} remote-as {remote_asn}',
        f'neighbor {network2Advertise} update-source Loopback 1',
        f'ip route {network1Advertise} 255.255.255.255 {neighbor_ip}',
        f'ip route {network2Advertise} 255.255.255.255 {neighbor_ip}'

    ]
    #Send the set of strings from above to the router
    output = connectRouter.send_config_set(configList)
    
    print(output)
    #If invalid input is detected on the rotuer, then reset the config by resetting bgp and static routes
    if '% Invalid input' in output:
        connectRouter.send_config_set([f'no router bgp {local_asn}', f'no ip route {network1Advertise} 255.255.255.255 {neighbor_ip}', f'no ip route {network2Advertise} 255.255.255.255 {neighbor_ip}'])
        return print("Invalid Input")
    ##If incomplete comomand is detected on the rotuer, then reset the config by resetting bgp and static routes
    if '% Incomplete command' in output:
        connectRouter.send_config_set([f'no router bgp {local_asn}', f'no ip route {network1Advertise} 255.255.255.255 {neighbor_ip}', f'no ip route {network2Advertise} 255.255.255.255 {neighbor_ip}'])
        return print("Incomplete command")
    connectRouter.disconnect()

#Update the bgp.conf with a state of each router
def bgpUpdateState():
    #Loop through each router and establish a ssh connection. This is repeated code from above to establish a connection
    for i in range(1,3):    
        IP = sshInfo.getIP(i)
        user = sshInfo.getUsername(i)
        secret = sshInfo.getPassword(i)

        currentDevice = {
            'device_type': 'cisco_ios',
            'host': IP,
            'username': user,
            'password': secret,
        }
        connectRouter = ConnectHandler(**currentDevice)    
        
        #Send this command to display the state
        output = connectRouter.send_command('show ip bgp neighbors | include BGP state')
        
        #Use regex to parse out the actual word of the state. \w+ catches any word at that index with 1 or multiple letters
        match = re.search(r'BGP state = (\w+)', output)

        #Set a new value called 'state' in the bgp.conf nested dictioniary and assign it the value of the regex match
        bgp_config['RouterInfo']['Routers']['R'+str(i)]['state'] = match.group(1)
        
        #Write this change to the conf file by using json.dump
        with open('bgp.conf', 'w') as file:
            json.dump(bgp_config, file, indent=4)

#Displays a table of BGP neighbor IP, AS# and state
def bgpTable():
    for i in range(1,3):
        #Use the prettytable library to create a pretty table with 3 columns
        myTable = PrettyTable(["BGP Neighbor IP", "BGP Neighbor AS", "BGP Neighbor State"])
        IP = sshInfo.getIP(i)
        user = sshInfo.getUsername(i)
        secret = sshInfo.getPassword(i)

        currentDevice = {
            'device_type': 'cisco_ios',
            'host': IP,
            'username': user,
            'password': secret,
        }
        connectRouter = ConnectHandler(**currentDevice)

        #Commands to fetch info for the table
        state = connectRouter.send_command('show ip bgp neighbors | include BGP state')
        IPandAS = connectRouter.send_command('show ip bgp neighbors | include BGP neighbor is')
        
        #Use regex to parse out the needed information
        state_match = re.findall(r'BGP state = (\w+)', state)
        IP_match = re.findall(r'BGP neighbor is (\S+)', IPandAS)
        AS_match = re.findall(r'remote AS (\d+)', IPandAS)
        
        #For all instances found, add a row in the pretty table and put the information there
        myTable.add_row([IP_match[0], AS_match[0], state_match[0]])
        myTable.add_row([IP_match[1], AS_match[1], state_match[1]])
        print("R"+str(i)+":")
        print(myTable)

#Finds all the bgp routes in the router and prints them
def bgpRoutes():
    for i in range(1,3):
        IP = sshInfo.getIP(i)
        user = sshInfo.getUsername(i)
        secret = sshInfo.getPassword(i)

        currentDevice = {
            'device_type': 'cisco_ios',
            'host': IP,
            'username': user,
            'password': secret,
        }
        connectRouter = ConnectHandler(**currentDevice)
        
        #This displays the BGP routes
        routes = connectRouter.send_command('show ip route | include via')

        #Display all the routes using regex, this S.+ matches the whole line starting with S
        routes_match = re.findall(r'S.+', routes)
        
        print("R"+str(i)+":")
        print(routes_match[0])
        print(routes_match[1])

#Once we config BGP, write the configs to a .txt file and print filename
def bgpConfigs():
    for i in range(1,3):
        IP = sshInfo.getIP(i)
        user = sshInfo.getUsername(i)
        secret = sshInfo.getPassword(i)

        currentDevice = {
            'device_type': 'cisco_ios',
            'host': IP,
            'username': user,
            'password': secret,
        }
        connectRouter = ConnectHandler(**currentDevice)
        
        config = connectRouter.send_command('show run')
        
        #Name the config
        fileName = "R"+str(i)+"config.txt"

        #Write the configs to a new file
        with open(fileName, 'w') as file:
            file.write(config)

        print(f"{fileName} saved")

from ncclient import manager
import csv, ipaddress,re
from prettytable import PrettyTable

def cfg(hostname, loopbackIP, loopbackMask, ospfIP, ospfHostMask, area, managementIP):
    cfg = f"""
          <config>
             <cli-config-data>
                <cmd>hostname {hostname}</cmd>
                <cmd>router ospf 1</cmd>
                <cmd>network {ospfIP} {ospfHostMask} area {area}</cmd>
                <cmd>network {managementIP} 0.0.0.255 area {area}</cmd>
                <cmd>int loopback 99</cmd>
                <cmd>ip address {loopbackIP} {loopbackMask}</cmd>
                <cmd>no sh</cmd>
    </cli-config-data>
          </config>
    """
    return cfg

def sendConfigs():
    hosts = ['192.168.122.11', '192.168.122.12', '192.168.122.13', '192.168.122.14', '192.168.122.15']
    counter = 0
    with open('lab9-obj2-conf.csv', newline='') as file:
        csvreader = csv.DictReader(file)
        for row in csvreader:
            hostname = row['Hostname']
            loopback = row['Loopback 99 IP']
            ospfNetwork = row['OSPF Network to advertise ']
            area = row['OSPF area']
            IP = ipaddress.ip_interface(loopback).ip
            network = ipaddress.ip_interface(loopback).network
            mask = ipaddress.ip_network(network).netmask
            ospfIP = ipaddress.ip_interface(ospfNetwork).ip
            ospfMask = ipaddress.ip_network(ospfNetwork).hostmask
            config = cfg(hostname, IP, mask, ospfIP, ospfMask, area, hosts[counter])
            cisco_manager = manager.connect (host= hosts[counter], port=22, username='lab',password='lab123',hostkey_verify=False, device_params={'name': 'iosxr'}, timeout = 5000, allow_agent=False, look_for_keys=False)
            data = cisco_manager.edit_config ( config, target='running')
            print(data)
            cisco_manager.close_session()
            counter+=1

def printConfigs():
    hosts = ['192.168.122.11', '192.168.122.12', '192.168.122.13', '192.168.122.14', '192.168.122.15']
    routers = ['R1','R2','R3','R4','R5']
    counter = 0
    myTable = PrettyTable(["Router", "Hostname", "Loopback 99", "OSPF Area", "OSPF Network"])
    for i in hosts:
        cisco_manager = manager.connect (host= i, port=22, username='lab',password='lab123',hostkey_verify=False, device_params={'name': 'iosxr'}, timeout = 5000, allow_agent=False, look_for_keys=False)
        running = cisco_manager.get_config(source='running')
        #print(running)
        loopbackPattern = r'interface Loopback\d+\s+ip address (\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}) (\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})'
        loopbackMatches = re.search(loopbackPattern, str(running))
        ip = loopbackMatches.group(1)
        mask = loopbackMatches.group(2)
        maskNumber = ipaddress.IPv4Network('0.0.0.0/'+mask).prefixlen
        loopbackIP = str(ip)+'/'+str(maskNumber)
        hostnamePattern = r'hostname\s+(\w+)'
        hostnameMatches = re.search(hostnamePattern, str(running))
        ospfPattern = r'network\s+(\d+\.\d+\.\d+\.\d+)\s+(\d+\.\d+\.\d+\.\d+)\s+area\s+(\d+)'
        ospfMatches = re.findall(ospfPattern, str(running))
        ospfIP = ospfMatches[0][0]
        ospfWild = ospfMatches[0][1]
        ospfMask = ipaddress.IPv4Network('0.0.0.0/'+ospfWild).prefixlen
        ospfArea = ospfMatches[0][2]
        ospfFullIP = str(ospfIP)+'/'+str(ospfMask)
        #print(ospfIP, ospfMask, ospfArea)
        myTable.add_row([routers[counter],hostnameMatches.group(1),loopbackIP,ospfArea,ospfFullIP])
        counter+=1
    print(myTable)
sendConfigs()
printConfigs()

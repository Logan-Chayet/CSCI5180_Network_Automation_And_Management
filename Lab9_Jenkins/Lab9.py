import csv
import ipaddress
import re
from ncclient import manager
from prettytable import PrettyTable
hosts = ['192.168.122.21', '192.168.122.22', '192.168.122.23', '192.168.122.24', '192.168.122.25']
def cfg(hostname, loopback_ip, loopback_mask, ospf_ip, ospf_host_mask, area, management_ip):
    cfg = f"""
          <config>
             <cli-config-data>
                <cmd>hostname {hostname}</cmd>
                <cmd>router ospf 1</cmd>
                <cmd>network {ospf_ip} {ospf_host_mask} area {area}</cmd>
                <cmd>network {management_ip} 0.0.0.255 area {area}</cmd>
                <cmd>int loopback 99</cmd>
                <cmd>ip address {loopback_ip} {loopback_mask}</cmd>
                <cmd>no sh</cmd>
    </cli-config-data>
          </config>
    """
    return cfg

def send_configs():
    counter = 0
    with open('/var/lib/jenkins/workspace/Lab9/infoLab9.csv', newline='') as file:
        csvreader = csv.DictReader(file)
        for row in csvreader:
            hostname = row['Hostname']
            loopback = row['Loopback 99 IP']
            ospf_network = row['OSPF Network to advertise ']
            area = row['OSPF area']
            ip_addr = ipaddress.ip_interface(loopback).ip
            network = ipaddress.ip_interface(loopback).network
            mask = ipaddress.ip_network(network).netmask
            ospf_ip = ipaddress.ip_interface(ospf_network).ip
            ospf_mask = ipaddress.ip_network(ospf_network).hostmask
            config = cfg(hostname, ip_addr, mask, ospf_ip, ospf_mask, area, hosts[counter])
            cisco_manager = manager.connect(host=hosts[counter],port=22,username='lab'
                    ,password='lab123',hostkey_verify=False,device_params={'name':'iosxr'}
                    ,timeout=5000,allow_agent=False,look_for_keys=False)
            data = cisco_manager.edit_config ( config, target='running')
            print(data)
            cisco_manager.close_session()
            counter+=1

def print_configs():
    routers = ['R1','R2','R3','R4','R5']
    counter = 0
    my_table = PrettyTable(["Router", "Hostname", "Loopback 99", "OSPF Area", "OSPF Network"])
    for i in hosts:
        cisco_manager = manager.connect (host= i, port=22, username='lab'
                ,password='lab123',hostkey_verify=False, device_params={'name': 'iosxr'}
                ,timeout = 5000, allow_agent=False, look_for_keys=False)
        running = cisco_manager.get_config(source='running')
        #print(running)
        loopback_pattern = r'interface Loopback\d+\s+ip address (\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}) (\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})'
        loopback_matches = re.search(loopback_pattern, str(running))
        ip = loopback_matches.group(1)
        mask = loopback_matches.group(2)
        mask_number = ipaddress.IPv4Network('0.0.0.0/'+mask).prefixlen
        loopback_ip = str(ip)+'/'+str(mask_number)
        hostname_pattern = r'hostname\s+(\w+)'
        hostname_matches = re.search(hostname_pattern, str(running))
        ospf_pattern = r'network\s+(\d+\.\d+\.\d+\.\d+)\s+(\d+\.\d+\.\d+\.\d+)\s+area\s+(\d+)'
        ospf_matches = re.findall(ospf_pattern, str(running))
        ospf_ip = ospf_matches[0][0]
        ospf_wild = ospf_matches[0][1]
        ospf_mask = ipaddress.IPv4Network('0.0.0.0/'+ospf_wild).prefixlen
        ospf_area = ospf_matches[0][2]
        ospf_full_ip = str(ospf_ip)+'/'+str(ospf_mask)
        #print(ospfIP, ospfMask, ospfArea)
        my_table.add_row([routers[counter],hostname_matches.group(1),loopback_ip,ospf_area,ospf_full_ip])
        counter+=1
    print(my_table)
send_configs()
print_configs()

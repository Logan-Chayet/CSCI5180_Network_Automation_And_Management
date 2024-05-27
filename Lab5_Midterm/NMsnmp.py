import subprocess, json, re, ipaddress, threading
from time import sleep
import matplotlib.pyplot as plt
import numpy as np

def getCommand(command):
    result = subprocess.run(command, capture_output=True, text=True)
    output = result.stdout.strip()
    return output

snmp={}
snmp['Routers'] = {}
def getSNMP():
    routers = ["4000::1", "4000::200:FF:FE22:2222", "4000::200:FF:FE33:3333", "4000::200:FF:FE55:5555", "1000::1"] 

    for i in routers:
        name = getCommand(["snmpwalk", "-v", "2c", "-c", "public", i, "sysName"])
        name_match = re.search(r'STRING:\s*(.*)', name)
        routerName = name_match.group(1)
        snmp['Routers'][routerName] = {}

        descr = getCommand(["snmpwalk", "-v", "2c", "-c", "public", i, "ifDescr"])
        descr_match = re.findall(r'STRING:\s*(.*)', descr)
        int_num = re.findall(r'ifDescr\.(\d+)', descr)

        status = getCommand(["snmpwalk", "-v", "2c", "-c", "public", i, "ifAdminStatus"])
        status_match = re.findall(r'INTEGER:\s*(.*)', status)
        snmp['Routers'][routerName]['addresses'] = {}

        ipv4s = getCommand(["snmpwalk", "-v", "2c", "-c", "public", i, "ipAddressIfIndex.ipv4"])
        ipv4s_match = re.findall(r'INTEGER:\s*(.*)', ipv4s)
        ip4Match = re.findall(r'"([^"]*)"', ipv4s)

        ip4_subnet = getCommand(["snmpwalk", "-v", "2c", "-c", "public", i, "ipAddressPrefix.1"])
        subnet4_match = re.findall(r'"\.(\d+)', ip4_subnet)

        ipv6s = getCommand(["snmpwalk", "-v", "2c", "-c", "public", i, "ipAddressIfIndex.ipv6"])
        ipv6s_match = re.findall(r'INTEGER:\s*(.*)', ipv6s)
        ip6Match = re.findall(r'"([^"]*)"', ipv6s)

        ip6_subnet = getCommand(["snmpwalk", "-v", "2c", "-c", "public", i, "ipAddressPrefix.2"])
        subnet6_match = re.findall(r'"\.(\d+)', ip6_subnet)


        for j in range(len(descr_match)):
            snmp['Routers'][routerName]['addresses'][descr_match[j]] = {}
            snmp['Routers'][routerName]['addresses'][descr_match[j]]['v4'] = ''
            snmp['Routers'][routerName]['addresses'][descr_match[j]]['v6'] = ''
            snmp['Routers'][routerName]['addresses'][descr_match[j]]['Status'] = status_match[j]
            
            for x in range(len(ipv4s_match)):
                if int_num[j] == ipv4s_match[x]:
                    snmp['Routers'][routerName]['addresses'][descr_match[j]]['v4'] = ip4Match[x]+"/"+subnet4_match[x]
            for x in range(len(ipv6s_match)):
                if int_num[j] == ipv6s_match[x]:
                    snmp['Routers'][routerName]['addresses'][descr_match[j]]['v6'] = ip6Match[x]+"/"+subnet6_match[x]
        #Write this change to the conf file by using json.dump
        with open('snmp.json', 'w') as file:
            json.dump(snmp, file, indent=4)

def jsonToTxt():
    getCommand(["mv", "-f", "snmp.json", "snmp.txt"])
    
def getGraph():
    values = []
    for i in range(1,21):
        usage = getCommand(["snmpwalk", "-v", "2c", "-c", "public", "1000::1", ".1.3.6.1.4.1.9.9.109.1.1.1.1.6"])
        #threading.Timer(2.0, print("hello world")).start()
        usage_match = re.search(r'Gauge32:\s*(.*)', usage)
        usageValues = usage_match.group(1)
        values.append(usageValues)
        sleep(5)
    x = np.array([*range(1,21,1)])
    y = values
     
    plt.plot(x, y)
    plt.xlabel("Time")  # add X-axis label
    plt.ylabel("CPU-Usage")  # add Y-axis label
    plt.title("CPU-Usage vs. Time (2 min.)")  # add title

    plt.savefig('image.jpg')

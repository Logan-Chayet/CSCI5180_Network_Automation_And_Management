import csv, yaml, ipaddress, subprocess
from netmiko import ConnectHandler


def getCommand(command):
    result = subprocess.run(command, capture_output=True, text=True)
    output = result.stdout.strip()
    return output


def logintoR1():
    device = {
            'device_type': 'cisco_ios',
            'host': "198.51.100.1",
            'username': 'netman',
            'password': 'netman',
        }
    with ConnectHandler(**device) as connection:
        with open("config.txt", 'r') as file:
            config_commands = file.readlines()
        output = connection.send_config_set(config_commands)
        print(output)


def logintoR2():
    device = {
            'device_type': 'cisco_ios',
            'host': "10.10.10.2",
            'username': 'netman',
            'password': 'netman',
        }
    with ConnectHandler(**device) as connection:
        with open("config2.txt", 'r') as file:
            config_commands = file.readlines()
        output = connection.send_config_set(config_commands)
        print(output)

logintoR1()
logintoR2()

def traceroute():
    command = ["traceroute", "2.2.2.2"]
    result = subprocess.run(command, capture_output=True, text=True)
    print(result)

traceroute()

import os

os.system("traceroute 2.2.2.2")

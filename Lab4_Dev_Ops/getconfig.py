import json, datetime
from napalm import get_network_driver

def getconfig(IP, user, password):


    driver = get_network_driver('ios')
    iosv12 = driver(IP, user, password)

    iosv12.open()

    ios_output = iosv12.get_config(retrieve='running')

    iosv12.close()

    return ios_output['running']

def printConfigs():
    returnInfo = []
    info = {
            'R1':['192.168.122.2','R1_Chayet','password'],
            'R2':['198.51.101.2','R2_Chayet','password'],
            'R3':['172.16.1.3','R3_Chayet','password'],
            'R4':['198.51.101.3','R4_Chayet','password']
            }
    for i in info:
        output = getconfig(info[i][0],info[i][1],info[i][2])

        now = datetime.datetime.now()
        iso_timestamp = now.isoformat()

        #Name the config
        fileName = i+"_"+iso_timestamp+".txt"

        #Write the configs to a new file
        with open(fileName, 'w') as file:
            file.write(output) 
        
        print(fileName)
        returnInfo.append(fileName)
    return "\n".join(returnInfo)

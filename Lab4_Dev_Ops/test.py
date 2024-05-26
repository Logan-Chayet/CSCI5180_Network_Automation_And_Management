from flask import Flask,render_template,request
import mysql.connector
import ipaddress
from napalm import get_network_driver

def getconfig(IP, user, password, processID, areaID1, areaID2, IP1, IP2, loopback):

    driver = get_network_driver('ios')
    iosv12 = driver(IP, user, password)

    iosv12.open()
     
    if user == "R1_Chayet":
        iosv12.load_merge_candidate(config=
                f"router ospf {processID}\n"
                f"network {IP1} 0.0.0.255 area {areaID1}\n"
                f"network {IP2} 0.0.0.255 area {areaID1}\n"
                f"network {loopback} 0.0.0.0 area {areaID1}\n"
                f"end\n"
                f"exit\n"
                )
                
    diff = iosv12.compare_config()

    if diff:
        iosv12.commit_cfg()
        print(f"Configuration applied for {user}")
    else:
        print(f"No changes for {user}")

    iosv12.close()
    

    return print(user+" config complete")

def ospfConf():
    mydb = {
            'host':"127.0.0.1",
            'user':"root",
            'password':"password",
            'database':"routers"
            }
    conn = mysql.connector.connect(**mydb)
    cursor = conn.cursor()

    query = "select * from router_data"
    cursor.execute(query)

    result = cursor.fetchall()
    
   # for i in range(len(result)):
    user = result[0][1]
    password = result[0][2]
    processID = result[0][3]
    areaID1 = result[0][4]
    areaID2 = result[0][5]
    loopback = result[0][6]
    #    print(user,password,processID,areaID1,areaID2,loopback)
        #if user == "R1_Chayet":
    getconfig('192.168.122.2', user, password, processID, areaID1, areaID2, '192.168.122.0', '198.51.101.0', loopback)
       
    
    #print(user,password,processID,areaID1,areaID2,loopback)

    #getconfig(192.168.122.1,

    #for i in range(len(result)):
    #    print(result[i])
    conn.close()

    #return result[0]

ospfConf()

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

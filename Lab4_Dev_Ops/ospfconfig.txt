from flask import Flask,render_template,request
import mysql.connector
import ipaddress
from prettytable import PrettyTable
from napalm import get_network_driver

#mydb = {
#        'host':"127.0.0.1",
#        'user':"root",
#        'password':"password",
#        'database':"routers"
#        }
#conn = mysql.connector.connect(**mydb)
#cursor = conn.cursor()

def enoughEntry():
    mydb = {
            'host':"127.0.0.1",
            'user':"root",
            'password':"password",
            'database':"routers"
            }
    conn = mysql.connector.connect(**mydb)
    cursor = conn.cursor()

    query = "select count(*) from router_data"
    cursor.execute(query)

    result = cursor.fetchall()[0][0]


    conn.close()

    return result

def getValidIP():
    mydb = {
            'host':"127.0.0.1",
            'user':"root",
            'password':"password",
            'database':"routers"
            }
    conn = mysql.connector.connect(**mydb)
    cursor = conn.cursor()

    IPs = []
    #Get IP
    query = "select loopback_ip from router_data"
    cursor.execute(query)

    result = cursor.fetchall()


    conn.close()
    
    for i in range(0,4):
        ip = result[i][0]
        try:
            ipaddress.ip_address(ip)
            IPs.append(ip)

        except ValueError:
            print("The IP: "+ip+" is not valid")
    return IPs

def createTable():
    myTable = PrettyTable(["IP", "Interface"])
    
    loopbackIPs = getValidIP()

    for i in loopbackIPs:
        print(i)
        myTable.add_row([str(i), "loopback0"])

    myTable.add_row(["198.51.101.1", "Fa0/0"])
    myTable.add_row(["192.168.122.2", "Fa1/0"])
    myTable.add_row(["198.51.101.2", "Fa0/0"])
    myTable.add_row(["172.16.1.1", "Fa1/0"])
    myTable.add_row(["198.51.101.3", "Fa0/0"])
    myTable.add_row(["172.16.1.2", "Fa1/0"])
    myTable.add_row(["172.16.1.3", "Fa0/0"])
    print(myTable)

def getFormData():
    mydb = {
            'host':"127.0.0.1",
            'user':"root",
            'password':"password",
            'database':"routers"
            }
    conn = mysql.connector.connect(**mydb)
    cursor = conn.cursor()

    router = request.form.get("router")
    user_name = request.form.get("user")
    password = request.form.get("password")
    processID = request.form.get("processID")
    loopbackIP = request.form.get("loopbackIP")
    
    if router == "R1" or router == "R3":
        areaID = request.form.get("areaID")
        data = (router, user_name, password, processID, areaID, None, loopbackIP)

    elif router == "R2" or router == "R4":
        areaIDL = request.form.get("areaIDL")
        areaIDR = request.form.get("areaIDR")
        data = (router, user_name, password, processID, areaIDL, areaIDR, loopbackIP)
    
    sql = """
        INSERT INTO router_data 
        (router_id, username, password, ospf_process_id, ospf_area_id, ospf_area_id2, loopback_ip) 
        VALUES (%s, %s, %s, %s, %s, %s, %s)
         """
    try:
       # Executing the SQL command
       cursor.execute(sql, data)

       # Commit your changes in the database
       conn.commit()
       print("worked")

    except:
       # Rolling back in case of error
       conn.rollback()
       print("error")

    # Closing the connection
    conn.close()
    
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
                )
    elif user == "R2_Chayet":
        iosv12.load_merge_candidate(config=
                f"router ospf {processID}\n"
                f"network {IP1} 0.0.0.255 area {areaID1}\n"
                f"network {IP2} 0.0.0.255 area {areaID2}\n"
                f"network {loopback} 0.0.0.0 area {areaID1}\n"
                f"network {loopback} 0.0.0.0 area {areaID2}\n"
                f"end\n"
                )
    elif user == "R3_Chayet":
        iosv12.load_merge_candidate(config=
                f"router ospf {processID}\n"
                f"network {IP1} 0.0.0.255 area {areaID1}\n"
                f"network {loopback} 0.0.0.0 area {areaID1}\n"
                f"end\n"
                )
    elif user == "R4_Chayet":
        iosv12.load_merge_candidate(config=
                f"router ospf {processID}\n"
                f"network {IP1} 0.0.0.255 area {areaID1}\n"
                f"network {IP2} 0.0.0.255 area {areaID2}\n"
                f"network {loopback} 0.0.0.0 area {areaID1}\n"
                f"network {loopback} 0.0.0.0 area {areaID2}\n"
                f"end\n"
                )

    diff = iosv12.compare_config()

    if diff:
        iosv12.commit_config()
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

    for i in range(len(result)):
        user = result[i][1]
        password = result[i][2]
        processID = result[i][3]
        areaID1 = result[i][4]
        areaID2 = result[i][5]
        loopback = result[i][6]
    #    print(user,password,processID,areaID1,areaID2,loopback)
        if user == "R1_Chayet":
            getconfig('192.168.122.2', user, password, processID, areaID1, areaID2, '192.168.122.0', '198.51.101.0', loopback)
        elif user == "R2_Chayet":
            getconfig('198.51.101.2', user, password, processID, areaID1, areaID2, '172.16.1.0', '198.51.101.0', loopback)
        elif user == "R3_Chayet":
            getconfig('172.16.1.3', user, password, processID, areaID1, areaID2, '172.16.1.0', '0.0.0.0', loopback)
        elif user == "R4_Chayet":
            getconfig('198.51.101.3', user, password, processID, areaID1, areaID2, '172.16.1.0', '198.51.101.0', loopback)
    #print(user,password,processID,areaID1,areaID2,loopback)

    #getconfig(192.168.122.1,

    #for i in range(len(result)):
    #    print(result[i])
    conn.close()

    #return result[0]



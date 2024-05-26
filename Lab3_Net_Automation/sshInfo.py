import json
import os

#Checking if file exists
if os.path.exists('sshInfo.json'):
    #open file
    f = open('sshInfo.json', "r")
    #read in file
    data = json.loads(f.read())
else:
    #if the file doesn't exist, print that and exit
    print("File does not exist!")
    exit()

#Gets IP of a router based on its specified router ID
def getIP(routerNumber):
    #Going through the .json dictionary
    for i in data["routers"]:
        #If router ID found:
        if i["routerID"] == routerNumber:
            return i["ip"]
#Gets the username for ssh based on specified router ID
def getUsername(routerNumber):
    #same process as getIP
    for i in data["routers"]:
        if i["routerID"] == routerNumber:
            return i["user"]
#Gets ssh password
def getPassword(routerNumber):
    #same process as getIP
    for i in data["routers"]:
        if i["routerID"] == routerNumber:
            return i["password"]
#Instead of getting a specific IP based on router number, it retrieves all IPs and appends them to a list.
def getIPs():
    IPs=[]
    for i in data["routers"]:
        IPs.append(i["ip"])
    return IPs


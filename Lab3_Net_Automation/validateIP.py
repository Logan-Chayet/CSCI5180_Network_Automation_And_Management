import ipaddress, sshInfo

#Checks whether the IPs in the .json files are valid
#NOTE: I used the ipaddress library to easily check for valid IPs, but if this wasn't used this general thinking would be used:
#Check with regex for if there is four octects, and within those octects contains up to three numbers: ^([0-9]{1,3})\.([0-9]{1,3})\.([0-9]{1,3})\.([0-9]{1,3})$
#Then with a simple for loop, split the string based off of the '.' and check for each number if: 0<=x<=255.
def getValidIP(routerNumber):
    #Get IP
    ip = sshInfo.getIP(routerNumber)
    #Do a tryblock statement to check for a valid ip, if there is an error in the ipaddress library, tell the user
    try:
        ipaddress.ip_address(ip)
    except ValueError:
        print("The IP: "+ip+" is not valid")

#Simply put getValidIP into a for loop to get all valid IPs
def getValidIPs():
    for i in range(1,3):
        ip = sshInfo.getIP(i)
        try:
            ipaddress.ip_address(ip)
            print(ip+" is Valid")
        except ValueError:
            print("The IP: "+ip+" is not valid")

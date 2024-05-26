import subprocess, sshInfo

#Pings all IPs within the .json file
def getPings():
    #Get IPs
    ipList = sshInfo.getIPs()
    for ip in ipList:
        try:
            #Use sub process to ping one packet to the router
            subprocess.check_output(["ping", "-c", "1", ip])
            print(ip+": ping successful")
        except subprocess.CalledProcessError:
            print("Ping Failed")

import NMtcpdump, NMdhcpserver, NMsnmp, NMgithub, threading

#I am using the threading library to enable "parallel processing" as per requested in the assignment

print("Applying DHCP Config...\n")
NMdhcpserver.DHCPConfig()

print("\nCreating snmp.json File....\n")
NMsnmp.getSNMP()

t2 = threading.Thread(target=NMsnmp.jsonToTxt)
t3 = threading.Thread(target=NMsnmp.getGraph)
print("converted snmp.json to snmp.txt\n")
t2.start()
print("Creating Graph...\n")
t3.start()
t2.join()
t3.join()

print("Pusing modifications to GitHub...\n")
NMgithub.pushModified()

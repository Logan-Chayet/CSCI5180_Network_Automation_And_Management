import sshInfo, validateIP, connectivity, bgp, threading

#I am using the threading library to enable "parallel processing" as per requested in the assignment
#Assign threads to all of the functions I want to call
t1 = threading.Thread(target=validateIP.getValidIPs)

t2 = threading.Thread(target=connectivity.getPings)

t3 = threading.Thread(target=bgp.bgp, args=(1,))

t4 = threading.Thread(target=bgp.bgp, args=(2,))

t5 = threading.Thread(target=bgp.bgpUpdateState)

t6 = threading.Thread(target=bgp.bgpTable)

t7 = threading.Thread(target=bgp.bgpRoutes)

t8 = threading.Thread(target=bgp.bgpConfigs)

#I did four at a time here because the print statements were cutting off eachother, doing in 2 batches of 4 looked the best to me.
t1.start()
t2.start()
t3.start()
t4.start()

t1.join()
t2.join()
t3.join()
t4.join()

t5.start()
t6.start()
t7.start()
t8.start()

t5.join()
t6.join()
t7.join()
t8.join()

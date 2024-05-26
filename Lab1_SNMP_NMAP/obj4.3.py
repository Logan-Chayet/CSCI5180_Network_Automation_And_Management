import pyshark
import smtplib

file = "obj4.3.pcap"
traps = []

cap = pyshark.FileCapture(file)

for packet in cap:
    if 'SNMP' in packet and 'IP' in packet and packet.ip.src == "192.168.122.2":
        traps.append(str(packet.snmp))

msg = traps[0]

fromaddr = 'loganchayet123@gmail.com'
toaddrs = 'loganchayet123@gmail.com'

username = 'loganchayet123@gmail.com'
password = 'tmto awyr elvf hafh'

server = smtplib.SMTP('smtp.gmail.com:587')
server.starttls()
server.login(username,password)
server.sendmail(fromaddr, toaddrs, msg)
server.quit()


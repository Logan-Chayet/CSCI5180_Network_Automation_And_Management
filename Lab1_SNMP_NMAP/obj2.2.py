import subprocess

def getCommand(command):
    result = subprocess.run(command, capture_output=True, text=True)
    output = result.stdout.strip()
    return output

routers = ["192.168.122.2", "192.168.122.3", "192.168.122.4"]
commands = ["1.3.6.1.2.1.1.4.0", "1.3.6.1.2.1.1.5.0", "1.3.6.1.2.1.1.6.0", "1.3.6.1.2.1.2.1.0", "1.3.6.1.2.1.1.3.0"]
commandNames = ["Contact:", "Name:", "Location:", "Number:", "Uptime:"]


for i in range(len(routers)):
    if i == 0:
        print("SNMP v1")
    if i == 1:
        print("\nSNMP v2")
    if i == 2:
        print("\nSNMP v3")
    for j in range(len(commands)):
        if i == 0:
            output = getCommand(["snmpget", "-v", "1", "-c", "public", routers[i], commands[j]])
            if j == 0 or j == 1 or j == 2:
                parsed_value = output[output.find('"') + 1:output.rfind('"')]
                print(commandNames[j], parsed_value)
            if j == 3:
                parsed_value = output.split()[-1]
                print(commandNames[j], parsed_value)
            if j == 4:
                parsed_value = output.split()[-1]
                print(commandNames[j], parsed_value)
        if i == 1:
            output = getCommand(["snmpget", "-v", "2c", "-c", "public", routers[i], commands[j]])
            if j == 0 or j == 1 or j == 2:
                parsed_value = output[output.find('"') + 1:output.rfind('"')]
                print(commandNames[j], parsed_value)
            if j == 3:
                parsed_value = output.split()[-1]
                print(commandNames[j], parsed_value)
            if j == 4:
                parsed_value = output.split()[-1]
                print(commandNames[j], parsed_value)
        if i == 2:
            output = getCommand(["snmpget", "-v3", "-a", "MD5", "-A", "authpassword", "-x", "AES", "-X", "privpassword", "-u", "v3user", "-l", "authPriv", routers[i], commands[j]])
            if j == 0 or j == 1 or j == 2:
                parsed_value = output[output.find('"') + 1:output.rfind('"')]
                print(commandNames[j], parsed_value)
            if j == 3:
                parsed_value = output.split()[-1]
                print(commandNames[j], parsed_value)
            if j == 4:
                parsed_value = output.split()[-1]
                print(commandNames[j], parsed_value)


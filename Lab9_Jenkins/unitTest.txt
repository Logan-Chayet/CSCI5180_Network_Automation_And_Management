import unittest
import re
import ipaddress
import json
from napalm import get_network_driver

def getconfig(IP, user, password):


    driver = get_network_driver('ios')
    iosv12 = driver(IP, user, password)

    iosv12.open()

    ios_output = iosv12.get_config(retrieve='running')

    iosv12.close()

    return ios_output['running']

def testLoopback():
    config = getconfig('192.168.122.23', 'lab', 'lab123')
    loopback_pattern = r'interface Loopback99\s+ip address\s+(\d+\.\d+\.\d+\.\d+)\s+(\d+\.\d+\.\d+\.\d+)'
    loopback_match = re.search(loopback_pattern, config)
    ip = loopback_match.group(1)
    subnet = ipaddress.IPv4Network('0.0.0.0/'+loopback_match.group(2)).prefixlen

    return str(ip)+'/'+str(subnet)

def testAreas():
    config = getconfig('192.168.122.21', 'lab', 'lab123')
    area_pattern = r'area.\d+'
    area_matches = re.findall(area_pattern, config)
    areas = set(area_matches)
    if len(areas) == 1:
        return True
    else:
        return False

def pingTest():
    driver = get_network_driver('ios')
    iosv12 = driver('192.168.122.22', 'lab', 'lab123')

    iosv12.open()

    ios_output = iosv12.ping('10.1.5.1')
    iosv12.close() 
    if isinstance(ios_output, dict):
        return True
    else:
        return False

class routerTests(unittest.TestCase):
    
    def test_loopbackTest(self):
        self.assertEqual(testLoopback(), '10.1.3.1/24')
    def test_areas(self):
        self.assertTrue(testAreas())
    def test_ping(self):
        self.assertTrue(pingTest())
if __name__ == '__main__':
    unittest.main()

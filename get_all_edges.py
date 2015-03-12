import httplib2
import json
import sys
import logging
import os

# Globals
baseUrl = 'http://192.168.1.1:8080/controller/nb/v2'
containerName = 'default/'
ethTypeIp = 0x800
ipTypeTcp = 0x6
ipTypeUdp = 0x11

# Get all edges
def get_all_edges():
    resp, content = h.request('http://192.168.1.1:8080/controller/nb/v2/topology/default', "GET")
    alledges = json.loads(content)
    edges = alledges['edgeProperties']
    
    return edges 

# START OF MAIN PROGRAM
# Setup logging
LEVELS = {'debug': logging.DEBUG,
          'info': logging.INFO,
          'warning': logging.WARNING,
          'error': logging.ERROR,
          'critical': logging.CRITICAL}

if len(sys.argv) > 1:
    level_name = sys.argv[1]
    level = LEVELS.get(level_name, logging.NOTSET)
    logging.basicConfig(level=level)

h = httplib2.Http(".cache")
h.add_credentials('admin', 'admin')

def print_all_edges():
        all_edges = get_all_edges()
        for fs in all_edges:
            print fs['edge']['tailNodeConnector']['node']['id'],':',fs['edge']['tailNodeConnector']['id'], 'to', fs['edge']['headNodeConnector']['node']['id'],':',fs['edge']['headNodeConnector']['id']

if __name__ == "__main__":
  if os.path.getsize('/home/mininet/mininet/custom/Mymininet/Rd1.txt') > 0:
    fp = open('/home/mininet/mininet/custom/Mymininet/Rd2.txt', 'wb')
    sys.stdout = fp  
    print_all_edges()
  else:  
    fp = open('/home/mininet/mininet/custom/Mymininet/Rd1.txt', 'wb')
    sys.stdout = fp  
    print_all_edges()   


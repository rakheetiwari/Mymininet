import httplib2
import networkx as nx
import json
import sys
import datetime
import time
import copy
import logging
import os
import operator
import pickle

# Globals
baseUrl = 'http://168.150.75.111:8080/controller/nb/v2'
containerName = 'default/'
ethTypeIp = 0x800
ipTypeTcp = 0x6
ipTypeUdp = 0x11

# START OF MAIN PROGRAM
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

# Delete all flows in a node
def delete_all_flows_node(node):
    url = 'http://168.150.75.111:8080/controller/nb/v2/flowprogrammer/default/node/OF/' + node
    resp, content = h.request(url, "GET")
    allFlows = json.loads(content)
    flows = allFlows['flowConfig']
    for fs in flows:
        flowname = fs['name']
        del_url = url + '/staticFlow/' + flowname
        logging.debug('del_url %s', del_url)
        resp, content = h.request(del_url, "DELETE")
        logging.debug('resp %s content %s', resp, content)

# Deletes flow corresponding to the flow list passed
def delete_path_flow(path_flow_list):
    for flow in path_flow_list:
        nodeid = flow['nodeid']
        flowname = flow['flowname']
        #print "Deleting the nodeid and flowname",nodeid,flowname
        
def delete_count(path_flow_list):
      flow_count = 0
      delete_path_flow(path_flow_list)
      flow_count=flow_count+1

if __name__ == '__main__':
   
   flowDict ={}
   pkl_file = open('/home/mininet/mininet/custom/Mymininet/FlowCount.txt', 'rb')
   flowDict = pickle.load(pkl_file)
   #print flowDict
   delete_count(flowDict)


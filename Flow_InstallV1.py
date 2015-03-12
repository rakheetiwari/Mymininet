import httplib2
import networkx as nx
import json
import sys
import datetime
import time
import copy
import logging
from odl_rest import *
from pyth_2 import risk
import operator
import pickle

# Globals
baseUrl = 'http://192.168.1.1:8080/controller/nb/v2/'
containerName = 'default/'
ethTypeIp = 0x800
flowCnt = 0
ipTypeTcp = 0x6
ipTypeUdp = 0x11

# Find all hosts connected to the node and add flow entry to reach host from node
def add_flows_host(node_id):
    global flowCnt
    for host_prop in all_hosts:
        host_node_id = host_prop['nodeId']
        if (host_node_id == node_id):
            node_conn = host_prop['nodeConnectorId']
            dest_ip = host_prop['networkAddress']
            dest_mac = host_prop['dataLayerAddress']
            fname = 'flow' + str(flowCnt)
            newflow = build_flow(nodeid=node_id, flowname=fname, outnodeconn=node_conn, 
                ethertype=ethTypeIp, destip=dest_ip, outdstmac=dest_mac)
            flowCnt += 1
            post_flow(node_id, newflow, fname)
    
# Returns node connector of source nodeid which has the connection to dest node_id
def find_node_connector(src_node_id, dest_node_id):
    for edge in all_edges:
        if ((src_node_id == edge['edge']['headNodeConnector']['node']['id']) and
            (dest_node_id == edge['edge']['tailNodeConnector']['node']['id'])):
            return (edge['edge']['headNodeConnector']['id'])

# Sets up flow as specified by the path
def setup_path(path):
    # Use global flowCnt to create flowname
    global flowCnt
        
    # Make copy of path
    path = copy.deepcopy(path)
   
    path = list(path)
    
    path_flow_list = []
    path_dict = {}
    path_cnt = len(path)
    src_node_id = path[0]
    dest_node_id = path[path_cnt - 1]
   
    for iter in range(2):
        if (iter == 0):
            new_dest_node_id = dest_node_id
        else:
            path.reverse()
            new_dest_node_id = src_node_id
        logging.debug('path %s path_cnt %d', path, path_cnt)
        
        for i in range(len(path)):
            if ((i+1) < len(path)):
                nodeid1 = path[i]
                nodeid2 = path[i+1]
                
                logging.debug('nodeid1 %s nodeid2 %s', nodeid1, nodeid2)
                node_conn = find_node_connector(nodeid1, nodeid2)
                host_list = get_all_hosts_node(new_dest_node_id)
                
                for host in host_list:
                    ip_addr = host['networkAddress']
                    fname = 'flow' + str(flowCnt)
                    new_flow = build_flow(nodeid=nodeid1, outnodeconn=node_conn, 
                                flowname=fname, ethertype=ethTypeIp, destip=ip_addr)
                    flowCnt += 1
                    post_flow(nodeid1, new_flow, fname)
                    # Build flow list
                    logging.debug('nodeid1 %s flowname %s', nodeid1, fname)
                    path_dict ={}
                    path_dict['nodeid'] = nodeid1
                    path_dict['flowname'] = fname
                    path_flow_list.append(path_dict)
        
    return path_flow_list

# Deletes flow corresponding to the flow list passed
def delete_path_flow(path_flow_list):
    global flowCnt
    
    for flow in path_flow_list:
        nodeid = flow['nodeid']
        flowname = flow['flowname']
        #Decrement flowcount
        flowCnt -= 1
        delete_spec_flow_node(nodeid, flowname)
     
# Calculate bandwidth
def calc_bw(prev_stats, curr_stats, time_int):
    prev_tx_byte_cnt = prev_stats['transmitBytes']
    curr_tx_byte_cnt = curr_stats['transmitBytes']
    prev_rx_byte_cnt = prev_stats['receiveBytes']
    curr_rx_byte_cnt = curr_stats['receiveBytes']
    logging.debug('prev_tx %d curr_tx %d prev_rx %d curr_rx %d', prev_tx_byte_cnt, 
    curr_tx_byte_cnt, prev_rx_byte_cnt, curr_rx_byte_cnt)
    tx_bw = (curr_tx_byte_cnt - prev_tx_byte_cnt)/time_int
    rx_bw = (curr_rx_byte_cnt - prev_rx_byte_cnt)/time_int
    bandwidth = {}
    bandwidth['tx'] = tx_bw
    bandwidth['rx'] = rx_bw
    return bandwidth
        
#Setup credentials for ODL    
h = httplib2.Http(".cache")
h.add_credentials('admin', 'admin')  
    
# Get all hosts, nodes, flows
all_hosts = get_all_hosts()
all_nodes = get_all_nodes()
all_flows = get_all_flows()

# Get all the edges/links
all_edges = get_all_edges()

# Put nodes and edges into a graph
graph = nx.Graph()
for node in all_nodes:
  graph.add_node(node['node']['id'])
for edge in all_edges:
  e = (edge['edge']['headNodeConnector']['node']['id'], edge['edge']['tailNodeConnector']['node']['id'])
  graph.add_edge(*e)



def c1(src_node_id, dest_node_id):
    
            # Find all paths
            all_paths=[]
            all_paths = nx.all_simple_paths(graph, src_node_id, dest_node_id)

            #Display all paths
            all_path_cnt = 0
            all_path_list=[]
            for path in all_paths:
                all_path_list.append(path)
                
            all_path_list = all_path_list[0:20000]

            stPath = {}
            stPath_ini = {}

            pathDict = {}
            inc = 0 
            all_path_cnt = 0

         
            for path_ini in all_path_list:
                if tuple(path_ini[0:2]) not in stPath_ini:
                    stPath_ini[tuple(path_ini[0:2])] = 1
                
            dicLen = stPath_ini.__len__()    
            dicLen = (100/dicLen)

            for path in all_path_list:
                all_path_cnt += 1
                my_path_risk = []

                links = [path[i:i+2] for i in range(0, len(path), 1) if i+1 != len(path)]
                
                if tuple(path[0:2]) not in stPath:
                    inc = 0

                stPath[tuple(path[0:2])] = inc
                
                kval = stPath[tuple(path[0:2])]
                #print tuple(path[0:2]), kval

                                
                if kval > dicLen:
                 continue 
                 
                else:
                    inc = inc + 1
                    
                    for i in range(len(links)):
                                nodeid = links[i]   
                                j =  nodeid[0].split(':')
                                k =  nodeid[1].split(':')    
                                
                                links_tuple = ()
                                Links_List = []
                                Links_List.append(j[-1].lstrip("0"))
                                Links_List.append(k[-1].lstrip("0"))

                                links_tuple = tuple(Links_List)
                                val = risk(links_tuple, 1)   

                                if val:
                                    my_path_risk.append(val) 
                                else:
                                    my_path_risk.append(0)
           
                    numsum = (sum(my_path_risk))

                    if tuple(path) not in pathDict:
                        pathDict[tuple(path)] = numsum                

                #print "Total Path Risk->",numsum

            #print "\n","Path with minimum risk :->"
            sorted_x = sorted(pathDict.iteritems(), key=operator.itemgetter(1))
            #print sorted_x[0]    

            #return sorted_x

            # Add flows to reach host
            add_flows_host(src_node_id)
            add_flows_host(dest_node_id)

            path_flow_list = setup_path(sorted_x[0][0])

            return sorted_x                    

def c2(x,bandwidth_ext):

        #print "\n"

        #reqBandWidth = raw_input('Enter required bandwidth : ')
        reqBandWidth = bandwidth_ext
        assignBandWidth = 10

        pkl_file = open('/home/mininet/mininet/custom/Mymininet/Rd.txt', 'rb')
        try:
                bandwidthDict = pickle.load(pkl_file)
        except EOFError:  
                bandwidthDict = {}                
        
        pkl_file.close()
        list_Keys_dict = {}
        fg = 0

        for key in bandwidthDict.keys():
                    lst_key = list(key)

                    for idx, item in enumerate(lst_key):
                        z =  item.split(':')
                        item = z[-1].lstrip("0")
                        lst_key[idx] = item

                    lst_len = lst_key.__len__()
                    if lst_len != 2:
                        list_Keys_dict[tuple(lst_key)] = bandwidthDict[key]

        
        path = x
        links = [path[i:i+2] for i in range(0, len(path), 1) if i+1 != len(path)]

        for i in range(len(links)):
                nodeid = links[i] 
                j =  nodeid[0].split(':')
                k =  nodeid[1].split(':')    

                links_tuple = ()
                Links_List = []
                Links_List.append(j[-1].lstrip("0"))
                Links_List.append(k[-1].lstrip("0"))

                links_tuple = tuple(Links_List)

                if path in bandwidthDict:
                    chk_flag = bandwidthDict[path]

                    if chk_flag == 1:
                        print "Can't allocate bandwidth for path", path
                        flag = 1
                        break

                x1 = j[-1].lstrip("0")
                x2 = k[-1].lstrip("0")        

                for key, value in list_Keys_dict.iteritems():
                    try:
                        
                        k1 = int(key.index(x1))
                        k2 = int(key.index(x2))
                        k3 = abs(k2 - k1)

                        if int(k3) == 1:
                            if int(value) == 1:
                                print "Can't allocate bandwidth for path", path
                                fg = 1
                                flag = 1
                                break
                        
                    except ValueError:
                        pass
                
                if fg == 1:
                    
                    flag = 1
                    break


                if links_tuple in bandwidthDict:
                    getbandwidth =  bandwidthDict[links_tuple]
                    sumCal = int(assignBandWidth) - (int(getbandwidth) + int(reqBandWidth))
                    
                    if (int(sumCal) < 0):
                            flag = 1
                            bandwidthDict[path] = flag
                            
                            if flag == 1:
                                for key in bandwidthDict.keys():
                                    lst_key = list(key)
                                    lst_len = lst_key.__len__()
                                    
                                    if key != path and lst_len == 2:
                                        del bandwidthDict[key] 

                                fp = open('/home/mininet/mininet/custom/Mymininet/Rd.txt', 'wb')
                                pickle.dump(bandwidthDict, fp)
                                fp.close()        

                                print "Can't allocate bandwidth for the path", path
                                break
                    else:
                            bandwidthDict[links_tuple] =  int(reqBandWidth) + int(getbandwidth)
                            flag = 0      
                else:
                    bandwidthDict[links_tuple] =  reqBandWidth
                    flag = 0
                    bandwidthDict[path] = flag 


                
        if flag !=1:
            fp = open('/home/mininet/mininet/custom/Mymininet/Rd.txt', 'wb')
            pickle.dump(bandwidthDict, fp)
            fp.close()

            bandwidthDict_Copy = copy.deepcopy(bandwidthDict)

            for key in bandwidthDict_Copy.keys():
                    lst_key = list(key)
                    lst_len = lst_key.__len__()

                    if(lst_len != 2):
                        del bandwidthDict_Copy[key]                         
                                
            print "BandWidth Calculated and flow installed successfully ",bandwidthDict_Copy
            
        return flag            

if __name__ == '__main__':

 with open('/home/mininet/mininet/custom/Mymininet/20connections.txt', 'r') as content_file:

    for line in content_file:

            data = line.strip().split(",")
            # Find shortest path
            src_node_id = data[0]
            dest_node_id = data[1]
            bandwidth_ext = data[2]

            x = c1(src_node_id, dest_node_id)

            i = 0

            for pt in x:
                print "Path with minimum risk :->"
                print x[i]
                flag = c2(x[i][0],bandwidth_ext)

                if flag == 1:
                    i = i+1
                else:
                    break

open('/home/mininet/mininet/custom/Mymininet/Rd.txt', 'w').close()



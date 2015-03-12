"""Custom topology example"""
import httplib2
import networkx as nx
import json
import sys
import datetime
import time
import copy
import logging
from odl_rest import *
from get_all_edges import *
from time import sleep

def calc_bw(prev_stats, curr_stats, time_int):
    prev_tx_byte_cnt = prev_stats['transmitBytes']
    curr_tx_byte_cnt = curr_stats['transmitBytes']
    prev_rx_byte_cnt = prev_stats['receiveBytes']
    curr_rx_byte_cnt = curr_stats['receiveBytes']
    logging.debug('prev_tx %d curr_tx %d prev_rx %d curr_rx %d', prev_tx_byte_cnt, curr_tx_byte_cnt, prev_rx_byte_cnt, curr_rx_byte_cnt)
    tx_bw = (curr_tx_byte_cnt - prev_tx_byte_cnt)/time_int
    rx_bw = (curr_rx_byte_cnt - prev_rx_byte_cnt)/time_int
    bandwidth = {}
    bandwidth['tx'] = tx_bw
    bandwidth['rx'] = rx_bw
    return bandwidth

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

def find_node_connector(src_node_id, dest_node_id):
    for edge in all_edges:
        if ((src_node_id == edge['edge']['headNodeConnector']['node']['id']) and
            (dest_node_id == edge['edge']['tailNodeConnector']['node']['id'])):
            return (edge['edge']['headNodeConnector']['id'])

port_stats = {}
all_nodes = get_all_nodes()
for node in all_nodes:
    port_stats[node['node']['id']] = {}
all_edges = get_all_edges()
for edge in all_edges:
    port_stats[edge['edge']['tailNodeConnector']['node']['id']][edge['edge']['tailNodeConnector']['id']] = {}

def ResourceUsage():
 totalResourceUsage = 0
# Initialize dictionary

loop_cnt = 0

while loop_cnt < 24:

    with open('/home/mininet/mininet/custom/Mymininet/20connections.txt', 'r') as content_file:
     for line in content_file:
                data = line.strip().split(",")
                nodeid1 = data[0]
                nodeid2 = data[1]
                logging.debug('nodeid1 %s nodeid2 %s', nodeid1, nodeid2)
                node_conn = find_node_connector(nodeid1, nodeid2)
                print node_conn
                port_stats[nodeid1][node_conn]['currstats'] = get_node_port_stats(nodeid1, node_conn)
                # Ignore first reading
                print port_stats[nodeid1][node_conn]['currstats']
                if (loop_cnt >= 10):
                    bandwidth = calc_bw(port_stats[nodeid1][node_conn]['prevstats'], port_stats[nodeid1][node_conn]['currstats'], 5)
                    print bandwidth
                    totalResourceUsage += bandwidth
                    logging.debug('bw_tx %d bw_rx %d', bandwidth['tx'], bandwidth['rx'])
                # Update prevstats
                port_stats[nodeid1][node_conn]['prevstats'] = port_stats[nodeid1][node_conn]['currstats']
loop_cnt += 1

print totalResourceUsage
time.sleep(5)


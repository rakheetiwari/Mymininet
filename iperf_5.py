"""Custom topology example"""

from mininet.topo import Topo
from functools import partial
from mininet.net import Mininet
from mininet.node import CPULimitedHost
from mininet.link import TCLink
from mininet.log import lg, setLogLevel
from mininet.cli import CLI
from mininet.util import dumpNodeConnections
from mininet.node import RemoteController
from mininet.link import TCIntf
from mininet.util import custom
from time import sleep
import odl_rest

class MyTopo( Topo ):
    "Simple topology example."

    def __init__( self ):
        "Create custom topo."

        # Initialize topology
        Topo.__init__( self )

        # Add hosts and switches
        h1 = self.addHost( 'h1', ip='10.0.1.1/24', defaultRoute='via 10.0.1.1', sched='rt' )
        h2 = self.addHost( 'h2', ip='10.0.2.1/24', defaultRoute='via 10.0.2.1', sched='rt' )
        h3 = self.addHost( 'h3', ip='10.0.3.1/24', defaultRoute='via 10.0.3.1', sched='rt' )
        h4 = self.addHost( 'h4', ip='10.0.4.1/24', defaultRoute='via 10.0.4.1', sched='rt' )
        h5 = self.addHost( 'h5', ip='10.0.5.1/24', defaultRoute='via 10.0.5.1', sched='rt' )
        h6 = self.addHost( 'h6', ip='10.0.6.1/24', defaultRoute='via 10.0.6.1', sched='rt' )
        h7 = self.addHost( 'h7', ip='10.0.7.1/24', defaultRoute='via 10.0.7.1', sched='rt' )
        h8 = self.addHost( 'h8', ip='10.0.8.1/24', defaultRoute='via 10.0.8.1', sched='rt' )
        h9 = self.addHost( 'h9', ip='10.0.9.1/24', defaultRoute='via 10.0.9.1', sched='rt' )
        h10 = self.addHost( 'h10', ip='10.0.10.1/24', defaultRoute='via 10.0.10.1', sched='rt' )
        h11 = self.addHost( 'h11', ip='10.0.11.1/24', defaultRoute='via 10.0.11.1', sched='rt' )
        h12 = self.addHost( 'h12', ip='10.0.12.1/24', defaultRoute='via 10.0.12.1', sched='rt' )
        h13 = self.addHost( 'h13', ip='10.0.13.1/24', defaultRoute='via 10.0.13.1', sched='rt' )
        h14 = self.addHost( 'h14', ip='10.0.14.1/24', defaultRoute='via 10.0.14.1', sched='rt' )
        h15 = self.addHost( 'h15', ip='10.0.15.1/24', defaultRoute='via 10.0.15.1', sched='rt' )
        h16 = self.addHost( 'h16', ip='10.0.16.1/24', defaultRoute='via 10.0.16.1', sched='rt' )
        h17 = self.addHost( 'h17', ip='10.0.17.1/24', defaultRoute='via 10.0.17.1', sched='rt' )
        h18 = self.addHost( 'h18', ip='10.0.18.1/24', defaultRoute='via 10.0.18.1', sched='rt' )
        h19 = self.addHost( 'h19', ip='10.0.19.1/24', defaultRoute='via 10.0.19.1', sched='rt' )
        h20 = self.addHost( 'h20', ip='10.0.20.1/24', defaultRoute='via 10.0.20.1', sched='rt' )
        h21 = self.addHost( 'h21', ip='10.0.21.1/24', defaultRoute='via 10.0.21.1', sched='rt' )
        h22 = self.addHost( 'h22', ip='10.0.22.1/24', defaultRoute='via 10.0.22.1', sched='rt' )
        h23 = self.addHost( 'h23', ip='10.0.23.1/24', defaultRoute='via 10.0.23.1', sched='rt' )
        h24 = self.addHost( 'h24', ip='10.0.24.1/24', defaultRoute='via 10.0.24.1', sched='rt' )

        s1 = [ self.addSwitch( 's1', dpid="0000000000000001")]
        s2 = [ self.addSwitch( 's2', dpid="0000000000000002")]
        s3 = [ self.addSwitch( 's3', dpid="0000000000000003")]
        s4 = [ self.addSwitch( 's4', dpid="0000000000000004")]
        s5 = [ self.addSwitch( 's5', dpid="0000000000000005")]
        s6 = [ self.addSwitch( 's6', dpid="0000000000000006")]
        s7 = [ self.addSwitch( 's7', dpid="0000000000000007")]
        s8 = [ self.addSwitch( 's8', dpid="0000000000000008")]
        s9 = [ self.addSwitch( 's9', dpid="0000000000000009")]
        s10 = [ self.addSwitch( 's10', dpid="0000000000000010")]
        s11 = [ self.addSwitch( 's11', dpid="0000000000000011")]
        s12 = [ self.addSwitch( 's12', dpid="0000000000000012")]
        s13 = [ self.addSwitch( 's13', dpid="0000000000000013")]
        s14 = [ self.addSwitch( 's14', dpid="0000000000000014")]
        s15 = [ self.addSwitch( 's15', dpid="0000000000000015")]
        s16 = [ self.addSwitch( 's16', dpid="0000000000000016")]
        s17 = [ self.addSwitch( 's17', dpid="0000000000000017")]
        s18 = [ self.addSwitch( 's18', dpid="0000000000000018")]
        s19 = [ self.addSwitch( 's19', dpid="0000000000000019")]
        s20 = [ self.addSwitch( 's20', dpid="0000000000000020")]
        s21 = [ self.addSwitch( 's21', dpid="0000000000000021")]
        s22 = [ self.addSwitch( 's22', dpid="0000000000000022")]
        s23 = [ self.addSwitch( 's23', dpid="0000000000000023")]
        s24 = [ self.addSwitch( 's24', dpid="0000000000000024")]



        # Add links

        self.addLink( 's1', 'h1', bw=10, delay='5ms', max_queue_size=1000 )
        self.addLink( 's2', 'h2', bw=10, delay='5ms', max_queue_size=1000 )
        self.addLink( 's3', 'h3', bw=10, delay='5ms', max_queue_size=1000 )
        self.addLink( 's4', 'h4', bw=10, delay='5ms', max_queue_size=1000 )
        self.addLink( 's5', 'h5', bw=10, delay='5ms', max_queue_size=1000 )
        self.addLink( 's6', 'h6', bw=10, delay='5ms', max_queue_size=1000 )
        self.addLink( 's7', 'h7', bw=10, delay='5ms', max_queue_size=1000 )
        self.addLink( 's8', 'h8', bw=10, delay='5ms', max_queue_size=1000 )
        self.addLink( 's9', 'h9', bw=10, delay='5ms', max_queue_size=1000 )
        self.addLink( 's10', 'h10', bw=10, delay='5ms', max_queue_size=1000 )
        self.addLink( 's11', 'h11', bw=10, delay='5ms', max_queue_size=1000 )
        self.addLink( 's12', 'h12', bw=10, delay='5ms', max_queue_size=1000 )
        self.addLink( 's13', 'h13', bw=10, delay='5ms', max_queue_size=1000 )
        self.addLink( 's14', 'h14', bw=10, delay='5ms', max_queue_size=1000 )
        self.addLink( 's15', 'h15', bw=10, delay='5ms', max_queue_size=1000 )
        self.addLink( 's16', 'h16', bw=10, delay='5ms', max_queue_size=1000 )
        self.addLink( 's17', 'h17', bw=10, delay='5ms', max_queue_size=1000 )
        self.addLink( 's18', 'h18', bw=10, delay='5ms', max_queue_size=1000 )
        self.addLink( 's19', 'h19', bw=10, delay='5ms', max_queue_size=1000 )
        self.addLink( 's20', 'h20', bw=10, delay='5ms', max_queue_size=1000 )
        self.addLink( 's21', 'h21', bw=10, delay='5ms', max_queue_size=1000 )
        self.addLink( 's22', 'h22', bw=10, delay='5ms', max_queue_size=1000 )
        self.addLink( 's23', 'h23', bw=10, delay='5ms', max_queue_size=1000 )
        self.addLink( 's24', 'h24', bw=10, delay='5ms', max_queue_size=1000 )

        self.addLink( 's1', 's2', bw=10, delay='5ms', max_queue_size=1000 )
        self.addLink( 's1', 's6', bw=10, delay='5ms', max_queue_size=1000 )
        self.addLink( 's2', 's3', bw=10, delay='5ms', max_queue_size=1000 )
        self.addLink( 's2', 's6', bw=10, delay='5ms', max_queue_size=1000 )
        self.addLink( 's3', 's7', bw=10, delay='5ms', max_queue_size=1000 )
        self.addLink( 's3', 's4', bw=10, delay='5ms', max_queue_size=1000 )
        self.addLink( 's3', 's5', bw=10, delay='5ms', max_queue_size=1000 )
        self.addLink( 's4', 's7', bw=10, delay='5ms', max_queue_size=1000 )
        self.addLink( 's5', 's4', bw=10, delay='5ms', max_queue_size=1000 )
        self.addLink( 's5', 's8', bw=10, delay='5ms', max_queue_size=1000 )
        self.addLink( 's6', 's7', bw=10, delay='5ms', max_queue_size=1000 )
        self.addLink( 's6', 's9', bw=10, delay='5ms', max_queue_size=1000 )
        self.addLink( 's6', 's11', bw=10, delay='5ms', max_queue_size=1000 )
        self.addLink( 's7', 's8', bw=10, delay='5ms', max_queue_size=1000 )
        self.addLink( 's7', 's9', bw=10, delay='5ms', max_queue_size=1000 )
        self.addLink( 's9', 's12', bw=10, delay='5ms', max_queue_size=1000 )
        self.addLink( 's9', 's10', bw=10, delay='5ms', max_queue_size=1000 )
        self.addLink( 's8', 's10', bw=10, delay='5ms', max_queue_size=1000 )
        self.addLink( 's10', 's13', bw=10, delay='5ms', max_queue_size=1000 )
        self.addLink( 's10', 's14', bw=10, delay='5ms', max_queue_size=1000 )
        self.addLink( 's11', 's12', bw=10, delay='5ms', max_queue_size=1000 )
        self.addLink( 's11', 's15', bw=10, delay='5ms', max_queue_size=1000 )
        self.addLink( 's11', 's19', bw=10, delay='5ms', max_queue_size=1000 )
        self.addLink( 's12', 's13', bw=10, delay='5ms', max_queue_size=1000 )
        self.addLink( 's12', 's16', bw=10, delay='5ms', max_queue_size=1000 )
        self.addLink( 's13', 's14', bw=10, delay='5ms', max_queue_size=1000 )
        self.addLink( 's13', 's17', bw=10, delay='5ms', max_queue_size=1000 )
        self.addLink( 's14', 's18', bw=10, delay='5ms', max_queue_size=1000 )
        self.addLink( 's15', 's16', bw=10, delay='5ms', max_queue_size=1000 )
        self.addLink( 's15', 's20', bw=10, delay='5ms', max_queue_size=1000 )
        self.addLink( 's16', 's17', bw=10, delay='5ms', max_queue_size=1000 )
        self.addLink( 's16', 's21', bw=10, delay='5ms', max_queue_size=1000 )
        self.addLink( 's16', 's22', bw=10, delay='5ms', max_queue_size=1000 )
        self.addLink( 's17', 's18', bw=10, delay='5ms', max_queue_size=1000 )
        self.addLink( 's17', 's22', bw=10, delay='5ms', max_queue_size=1000 )
        self.addLink( 's17', 's23', bw=10, delay='5ms', max_queue_size=1000 )
        self.addLink( 's18', 's24', bw=10, delay='5ms', max_queue_size=1000 )
        self.addLink( 's19', 's20', bw=10, delay='5ms', max_queue_size=1000 )
        self.addLink( 's20', 's21', bw=10, delay='5ms', max_queue_size=1000 )
        self.addLink( 's21', 's22', bw=10, delay='5ms', max_queue_size=1000 )
        self.addLink( 's22', 's23', bw=10, delay='5ms', max_queue_size=1000 )
        self.addLink( 's23', 's24', bw=10, delay='5ms', max_queue_size=1000 )

def perfTest():
    topo = MyTopo()
    net = Mininet(topo, controller=partial(RemoteController, ip='192.168.1.1', port=6633), link=TCLink, host=CPULimitedHost)
    net.start()
    print "Dumping host connections"
    dumpNodeConnections(net.hosts)

    sleep(5)

    print "Testing network connectivity"
    h1,h2 = net.getNodeByName('h1', 'h2')
    h3,h20 = net.getNodeByName('h3', 'h20')
    h4,h12 = net.getNodeByName('h4', 'h12')
    h11,h19 = net.getNodeByName('h11', 'h19')
    h13,h22 = net.getNodeByName('h13', 'h22')
    h16,h20 = net.getNodeByName('h16', 'h20')
    h17,h23 = net.getNodeByName('h17', 'h23')
    h18,h21 = net.getNodeByName('h18', 'h21')
    h22,h24 = net.getNodeByName('h22', 'h24')
    
    net.ping((h1, h2))
    net.ping((h3, h20))
    
    sleep(20)

    #Call the Flow-Install.py function
    
    net.ping((h1, h2))
    net.ping((h3, h20))
    
#   print "Testing bandwidth between h1 and h2"
#   h1,h2 = net.getNodeByName('h1', 'h2')
#   net.iperf((h1, h2))

#   print "Testing bandwidth between h3 and h20"
#   h3,h20 = net.getNodeByName('h3', 'h20')
#   net.iperf((h3, h20))

    print "*** Running CLI"
    CLI( net )

if __name__ == '__main__':
    setLogLevel('info')
    perfTest()

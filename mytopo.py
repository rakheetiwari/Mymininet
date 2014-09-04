"""Custom topology example

Two directly connected switches plus a host for each switch:

   host --- switch --- switch --- host

Adding the 'topos' dict with a key/value pair to generate our newly defined
topology enables one to pass in '--topo=mytopo' from the command line.
"""

from mininet.topo import Topo
from mininet.net import Mininet
from mininet.node import CPULimitedHost
from mininet.link import TCLink

class MyTopo( Topo ):
    "Simple topology example."

    def __init__( self ):
        "Create custom topo."

        # Initialize topology
        Topo.__init__( self )

        # Add hosts and switches
        h1 = self.addHost( 'h1' )
        h2 = self.addHost( 'h2' )
        h3 = self.addHost( 'h3' )
        s1 = self.addSwitch( 's1' )
        s2 = self.addSwitch( 's2' )
        s3 = self.addSwitch( 's3' )
        s4 = self.addSwitch( 's4' )
        s5 = self.addSwitch( 's5' )
        s6 = self.addSwitch( 's6' )
        s7 = self.addSwitch( 's7' )
        

        # Add links
        self.addLink( s1, s2, bw=10 )
        self.addLink( s2, s3, bw=10 )
        self.addLink( s1, s3, bw=10 )
        self.addLink( s1, h1, bw=10 )
        self.addLink( s2, h2, bw=10 )
        self.addLink( s3, h3, bw=10 )
        self.addLink( s1, s4, bw=10 )
        self.addLink( s4, s5, bw=10 )
        self.addLink( s2, s5, bw=10 )
        self.addLink( s4, s7, bw=10 )
        self.addLink( s7, s6, bw=10 )
        self.addLink( s6, s5, bw=10 )


topos = { 'mytopo': ( lambda: MyTopo() ) }

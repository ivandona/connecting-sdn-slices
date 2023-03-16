#!/usr/bin/python3

from mininet.topo import Topo
from mininet.net import Mininet
from mininet.node import OVSKernelSwitch, RemoteController
from mininet.cli import CLI
from mininet.link import TCLink


class NetworkSlicingTopo(Topo):
    def __init__(self):
        # Initialize topology
        Topo.__init__(self)

        # Create template host, switch, and link
        host_config = dict(inNamespace=True)
        slice1_link_config = dict(bw=5)
        slice2_link_config = dict(bw=15)
        slice3_link_config = dict(bw=10)
        connecting_slices_link_config = dict(bw=20)
        host_link_config = dict()
        server_link_config = dict()

        # Create 12 switch nodes 
        for i in range(12):
            sconfig = {"dpid": "%016x" % (i + 1)}
            self.addSwitch("s%d" % (i + 1), protocols="OpenFlow10",**sconfig)

        # Create 10 host nodes
        for i in range(10):
            self.addHost("h%d" % (i + 1), **host_config)

        #Create 3 servers
        self.addHost("server1" , **host_config)
        self.addHost("server2" , **host_config)
        self.addHost("server3" , **host_config)

        # Add switch links for slice 1
        self.addLink("s1", "s2", **slice1_link_config)
        self.addLink("s1", "s3", **slice1_link_config)
        self.addLink("s2", "s4", **slice1_link_config)
        self.addLink("s3", "s5", **slice1_link_config)
        # Add switch links for slice 2
        self.addLink("s7", "s4", **slice2_link_config)
        self.addLink("s9", "s7", **slice2_link_config)
        self.addLink("s6", "s9", **slice2_link_config)
        self.addLink("s10", "s6", **slice2_link_config)
        self.addLink("s10", "s8", **slice2_link_config)
        self.addLink("s8", "s5", **slice2_link_config)
        # Add switch links for slice 3
        self.addLink("s11", "s9", **slice3_link_config)
        self.addLink("s10", "s11", **slice3_link_config)
        # Add switch links for s12 (switch that connects the three slices)
        self.addLink("s1", "s12", **connecting_slices_link_config)
        self.addLink("s6", "s12", **connecting_slices_link_config)
        self.addLink("s11", "s12", **connecting_slices_link_config)

        # Add 11 host links
        self.addLink("h1", "s2", **host_link_config)
        self.addLink("h2", "s4", **host_link_config)
        self.addLink("h3", "s4", **host_link_config)
        self.addLink("h4", "s7", **host_link_config)
        self.addLink("h5", "s3", **host_link_config)
        self.addLink("h6", "s5", **host_link_config)
        self.addLink("h7", "s5", **host_link_config)
        self.addLink("h8", "s8", **host_link_config)
        self.addLink("h9", "s9", **host_link_config)
        self.addLink("h10", "s10", **host_link_config)

        # Add 3 server links
        self.addLink("server1", "s12", **server_link_config)
        self.addLink("server2", "s12", **server_link_config)
        self.addLink("server3", "s12", **server_link_config)



topos = {"networkslicingtopo": (lambda: NetworkSlicingTopo())}

if __name__ == "__main__":
    topo = NetworkSlicingTopo()
    net = Mininet(
        topo=topo,
        switch=OVSKernelSwitch,
        build=False,
        autoSetMacs=True,
        autoStaticArp=True,
        link=TCLink,
    )
    net.build()
    net.start()

    
    net['s1'].cmd("ovs-vsctl set-controller s1 tcp:127.0.0.1:6633")
    net['s1'].cmd("ovs-vsctl set-controller s2 tcp:127.0.0.1:6633")
    net['s1'].cmd("ovs-vsctl set-controller s3 tcp:127.0.0.1:6633")
    net['s1'].cmd("ovs-vsctl set-controller s4 tcp:127.0.0.1:6633 tcp:127.0.0.1:6634")
    net['s1'].cmd("ovs-vsctl set-controller s5 tcp:127.0.0.1:6633 tcp:127.0.0.1:6634")
    net['s1'].cmd("ovs-vsctl set-controller s6 tcp:127.0.0.1:6634")
    net['s1'].cmd("ovs-vsctl set-controller s7 tcp:127.0.0.1:6634")
    net['s1'].cmd("ovs-vsctl set-controller s8 tcp:127.0.0.1:6634")
    net['s1'].cmd("ovs-vsctl set-controller s9 tcp:127.0.0.1:6634 tcp:127.0.0.1:6635")
    net['s1'].cmd("ovs-vsctl set-controller s10 tcp:127.0.0.1:6634 tcp:127.0.0.1:6635")
    net['s1'].cmd("ovs-vsctl set-controller s11 tcp:127.0.0.1:6635")
    net['s1'].cmd("ovs-vsctl set-controller s12 tcp:127.0.0.1:6636")
    CLI(net)
    net.stop()
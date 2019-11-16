#!/usr/bin/python

from mininet.net import Mininet
from mininet.node import Controller, RemoteController, OVSController
from mininet.node import CPULimitedHost, Host, Node
from mininet.node import OVSKernelSwitch, UserSwitch
from mininet.node import IVSSwitch
from mininet.cli import CLI
from mininet.log import setLogLevel, info
from mininet.link import TCLink, Intf
from subprocess import call
import sys

def myDumbellTopo():
    print('The command line arguments are:')
    print(sys.argv[1])
    print(sys.argv[2])
    n = int(sys.argv[1])
    m = int(sys.argv[2])
    net = Mininet( topo=None,
                   link=TCLink, #must be added in order to change link  parameters eg. bw,delay etc. 
                   build=False,
                   ipBase='10.0.0.0/8'
                   )

    c0=net.addController(name='c0',
                      controller=RemoteController,
                      ip='127.0.0.1',
                      protocol='tcp',
                      port=6633)

    s2 = net.addSwitch('s2', cls=OVSKernelSwitch)
    s1 = net.addSwitch('s1', cls=OVSKernelSwitch)

    l = 1
    hosts = []
    for node in range(1,(m+n+1)):
        tmp_hname = "h"+str(node)
        tmp_host = net.addHost(tmp_hname, cls=Host, defaultRoute=None)
        hosts.append(tmp_host)

    for node in range(0,n):
        net.addLink(hosts[node], s1)
    net.addLink(s1, s2)
    for node in range(n,(m+n)):
        net.addLink(hosts[node], s2)

    info( '*** Starting network\n')
    net.build()

    info( '*** Starting controllers\n')
    for controller in net.controllers:
        controller.start()

    info( '*** Starting switches\n')
    net.get('s2').start([c0])
    net.get('s1').start([c0])
    info( '*** Post configure switches and hosts\n')
    CLI(net)
    net.stop()

if __name__ == '__main__':
    setLogLevel( 'info' )
    myDumbellTopo()


from pox.core import core
import pox.openflow.libopenflow_01 as of
from pox.lib.util import dpid_to_str
from pox.lib.util import str_to_bool
from collections import defaultdict
import pox.lib.packet as pkt
from pox.lib.addresses import IPAddr,EthAddr
from pox.lib.packet.ipv4 import ipv4
from time import sleep
import struct
from collections import namedtuple
from pox.lib.revent import *
from pox.lib.recoco import Timer
from time import time

log = core.getLogger()

switches=0
Payload = namedtuple('Payload','timeSent')
SwitchMap={}

def _handle_ConnectionUp(event):
    global switches
    switches+=1
    switchNo=int(dpid_to_str(event.dpid)[-1])
    print ('Conection Up:',switchNo)
    SwitchMap[switchNo]=event

    if switchNo==1:
        msg=of.ofp_flow_mod()
        msg.match.in_port = 1
        msg.actions.append(of.ofp_action_output(port = 2))
        SwitchMap[1].connection.send(msg)

        msg=of.ofp_flow_mod()
        msg.priority = 60000
        msg.match.nw_proto=6
        msg.match.dl_type=0x800
        msg.match.tp_dst = 80
        msg.match.nw_dst = IPAddr("10.0.0.4")
        msg.match.in_port = 2
        SwitchMap[1].connection.send(msg)

        msg=of.ofp_flow_mod()
        msg.match.in_port = 2
        msg.priority = 200
        msg.actions.append(of.ofp_action_output(port = 3))
        msg.actions.append(of.ofp_action_output(port = 1))
        SwitchMap[1].connection.send(msg)

        msg=of.ofp_flow_mod()
        msg.match.in_port = 3
        msg.actions.append(of.ofp_action_output(port = 2))
        SwitchMap[1].connection.send(msg)

    else:
        msg=of.ofp_flow_mod()
        msg.match.in_port = 1
        msg.actions.append(of.ofp_action_output(port = 3))
        SwitchMap[2].connection.send(msg)

        msg=of.ofp_flow_mod()
        msg.match.in_port = 3
        msg.actions.append(of.ofp_action_output(port = 1))
        SwitchMap[2].connection.send(msg)

def launch(): 
    core.openflow.addListenerByName("ConnectionUp",_handle_ConnectionUp)


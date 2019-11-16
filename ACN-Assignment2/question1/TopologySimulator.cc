//For command line argument ./waf --run "scratch/myfirst --nodes=15"

#include "ns3/core-module.h"
#include "ns3/network-module.h"
#include "ns3/point-to-point-module.h"
#include "ns3/applications-module.h"
#include "ns3/animation-interface.h"
#include "ns3/netanim-module.h"
#include<string.h>
#include<string>
#include<iostream>
#include<sstream>
#include <vector>
using namespace ns3;

NS_LOG_COMPONENT_DEFINE ("FirstScriptExample");

int main (int argc, char *argv[])
{
  int num_nodes = 7;
  int i =0;
  CommandLine cmd;
  cmd.AddValue ("nodes", "Number of nodes in binary tree", num_nodes);
  cmd.Parse (argc, argv);
  
  Time::SetResolution (Time::NS);
  NodeContainer nodes;
  nodes.Create (num_nodes);
  
  std::vector<PointToPointHelper> p2ph;
  p2ph.reserve(num_nodes);

  for(i=0;i<num_nodes;i++){
     PointToPointHelper p2p;
     p2p.SetDeviceAttribute ("DataRate", StringValue ("5Mbps"));
     p2p.SetChannelAttribute ("Delay", StringValue ("2ms"));
     p2ph.push_back(p2p);;
  }

  std::vector<NetDeviceContainer> devicesF;
  devicesF.reserve(num_nodes-1);

  int c = 0;
  for(i=0;i<num_nodes/2;i++){
     NetDeviceContainer ndc;
     ndc = p2ph[c++].Install (nodes.Get(i),nodes.Get((2*i)+1));
     devicesF.push_back(ndc);
     NetDeviceContainer ndc2;
     ndc2 = p2ph[c++].Install (nodes.Get(i),nodes.Get((2*i)+2));
     devicesF.push_back(ndc2);
  }

  ns3::PacketMetadata::Enable();
  std::string animFile = "first.xml"; AnimationInterface anim(animFile);
  Ptr<Node> n = nodes.Get(0);
  anim.SetConstantPosition(n, 50, 0);
  n = nodes.Get(1);
  anim.SetConstantPosition(n, 25, 20);
  n = nodes.Get(2);
  anim.SetConstantPosition(n, 75, 20);
  n = nodes.Get(3);
  anim.SetConstantPosition(n, 13, 40);
  n = nodes.Get(4);
  anim.SetConstantPosition(n, 38, 40);
  n = nodes.Get(5);
  anim.SetConstantPosition(n, 63, 40);
  n = nodes.Get(6);
  anim.SetConstantPosition(n, 88, 40);

  Simulator::Run ();
  Simulator::Destroy ();
  return 0;
}

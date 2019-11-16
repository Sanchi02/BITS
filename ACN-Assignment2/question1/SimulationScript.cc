/* -*- Mode:C++; c-file-style:"gnu"; indent-tabs-mode:nil; -*- */
/*
 * This program is free software; you can redistribute it and/or modify
 * it under the terms of the GNU General Public License version 2 as
 * published by the Free Software Foundation;
 *
 * This program is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 * GNU General Public License for more details.
 *
 * You should have received a copy of the GNU General Public License
 * along with this program; if not, write to the Free Software
 * Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307  USA
 */

#include "ns3/core-module.h"
#include "ns3/network-module.h"
#include "ns3/internet-module.h"
#include "ns3/point-to-point-module.h" 
#include "ns3/netanim-module.h"
#include "ns3/applications-module.h" 
#include "ns3/animation-interface.h" 
#include "ns3/point-to-point-layout-module.h" 
#include "ns3/ipv4-static-routing-helper.h"
#include "ns3/ipv4-list-routing-helper.h" 
#include "ns3/ipv4-global-routing-helper.h" 
#include "ns3/flow-monitor.h"
#include "ns3/flow-monitor-helper.h"
#include "ns3/flow-monitor-module.h" 
#include <iostream>
#include <fstream> 
#include <vector> 
#include <string>
#include <cstdlib>
#include "ns3/animation-interface.h"
#include "ns3/netanim-module.h"

using namespace ns3;

NS_LOG_COMPONENT_DEFINE ("FifthScriptExample");

class MyApp : public Application 
{
public:

  MyApp ();
  virtual ~MyApp();

  void Setup (Ptr<Socket> socket, Address address, uint32_t packetSize, uint32_t nPackets, DataRate dataRate);

private:
  virtual void StartApplication (void);
  virtual void StopApplication (void);

  void ScheduleTx (void);
  void SendPacket (void);

  Ptr<Socket>     m_socket;
  Address         m_peer;
  uint32_t        m_packetSize;
  uint32_t        m_nPackets;
  DataRate        m_dataRate;
  EventId         m_sendEvent;
  bool            m_running;
  uint32_t        m_packetsSent;
};

MyApp::MyApp ()
  : m_socket (0), 
    m_peer (), 
    m_packetSize (0), 
    m_nPackets (0), 
    m_dataRate (0), 
    m_sendEvent (), 
    m_running (false), 
    m_packetsSent (0)
{
}

MyApp::~MyApp()
{
  m_socket = 0;
}

void
MyApp::Setup (Ptr<Socket> socket, Address address, uint32_t packetSize, uint32_t nPackets, DataRate dataRate)
{
  m_socket = socket;
  m_peer = address;
  m_packetSize = packetSize;
  m_nPackets = nPackets;
  m_dataRate = dataRate;
}

void
MyApp::StartApplication (void)
{
  m_running = true;
  m_packetsSent = 0;
  m_socket->Bind ();
  m_socket->Connect (m_peer);
  SendPacket ();
}

void 
MyApp::StopApplication (void)
{
  m_running = false;

  if (m_sendEvent.IsRunning ())
    {
      Simulator::Cancel (m_sendEvent);
    }

  if (m_socket)
    {
      m_socket->Close ();
    }
}

void 
MyApp::SendPacket (void)
{
  Ptr<Packet> packet = Create<Packet> (m_packetSize);
  m_socket->Send (packet);

  if (++m_packetsSent < m_nPackets)
    {
      ScheduleTx ();
    }
}

void 
MyApp::ScheduleTx (void)
{
  if (m_running)
    {
      Time tNext (Seconds (m_packetSize * 8 / static_cast<double> (m_dataRate.GetBitRate ())));
      m_sendEvent = Simulator::Schedule (tNext, &MyApp::SendPacket, this);
    }
}

static void
CwndChange (Ptr<OutputStreamWrapper> stream, uint32_t oldCwnd, uint32_t newCwnd)
{
 *stream->GetStream () << Simulator::Now ().GetSeconds () << "\t" << newCwnd << std::endl;
}

void tghptCalc(Ptr<FlowMonitor> monitor, Ptr<Ipv4FlowClassifier> classifier,Ptr<OutputStreamWrapper> stream1, int count)
{
  std::map<FlowId, FlowMonitor::FlowStats> stats = monitor->GetFlowStats ();
  for (std::map<FlowId, FlowMonitor::FlowStats>::const_iterator i = stats.begin (); i != stats.end (); ++i)
    {
    Ipv4FlowClassifier::FiveTuple t = classifier->FindFlow (i->first);
    *stream1->GetStream () << count << "\t" << i->first - 1 << " (" << t.sourceAddress << ":"<<t.sourcePort<< " -> " << t.destinationAddress << ":"<<t.destinationPort << ")\t"<<i->second.rxBytes * 8.0 /(i->second.timeLastRxPacket.GetSeconds()- i->second.timeFirstTxPacket.GetSeconds()) / 1024 / 1024 << " Mbps"<<std::endl;
    }

}

int 
main (int argc, char *argv[])
{
  int num_nodes = 7;
  int i =0;
  CommandLine cmd;
  cmd.AddValue ("nodes", "Number of nodes in binary tree", num_nodes);
  cmd.Parse (argc, argv);

  ns3::PacketMetadata::Enable();
  std::string animFile = "first.xml";

  Config::SetDefault ("ns3::TcpL4Protocol::SocketType", StringValue ("ns3::TcpCustom"));

  NodeContainer nodes;
  Ipv4InterfaceContainer iic[num_nodes-1];
  Ipv4Address address[num_nodes];
  nodes.Create (num_nodes);
  address[0] = "10.1.1.0";
  address[1] = "10.1.2.0";
  address[2] = "10.1.3.0";
  address[3] = "10.1.4.0";
  address[4] = "10.1.5.0";
  address[5] = "10.1.6.0";
  address[6] = "10.1.7.0";

  PointToPointHelper p2p;
  p2p.SetDeviceAttribute ("DataRate", StringValue ("5Mbps"));
  p2p.SetChannelAttribute ("Delay", StringValue ("2ms"));

  std::vector<NetDeviceContainer> devicesF;
  devicesF.reserve(num_nodes-1);

  for(i=0;i<num_nodes/2;i++){
     NetDeviceContainer ndc;
     ndc = p2p.Install (NodeContainer(nodes.Get(i),nodes.Get((2*i)+1)));
     devicesF.push_back(ndc);
     NetDeviceContainer ndc2;
     ndc2 = p2p.Install (NodeContainer(nodes.Get(i),nodes.Get((2*i)+2)));
     devicesF.push_back(ndc2);
  }

  Ipv4AddressHelper ipv4;
  NS_LOG_INFO("Flow Monitor");
  Ipv4StaticRoutingHelper staticRouting;
  Ipv4GlobalRoutingHelper globalRouting;
  Ipv4ListRoutingHelper list;
  list.Add(staticRouting, 0);
  list.Add(globalRouting, 10);
  InternetStackHelper internet;
  internet.SetRoutingHelper(list);
  internet.Install(nodes);

  for(i=0; i < num_nodes-1 ; i++)
  {
    ipv4.SetBase(address[i], "255.255.255.0");
    iic[i] = ipv4.Assign(devicesF[i]);
  }
  Ipv4GlobalRoutingHelper::PopulateRoutingTables();

  uint16_t sinkPort = 8080;
  Address sinkAddress1 (InetSocketAddress (iic[4].GetAddress (0), sinkPort));
  Address sinkAddress2 (InetSocketAddress (iic[2].GetAddress (0), sinkPort));
 
  PacketSinkHelper packetSinkHelper ("ns3::TcpSocketFactory", InetSocketAddress (Ipv4Address::GetAny (), sinkPort));
  ApplicationContainer sinkApps1 = packetSinkHelper.Install(nodes.Get(2));
  PacketSinkHelper packetSinkHelper1("ns3::UdpSocketFactory", InetSocketAddress (Ipv4Address::GetAny (), sinkPort));
  ApplicationContainer sinkApps2 = packetSinkHelper.Install(nodes.Get(1));

  sinkApps1.Start (Seconds (0.));
  sinkApps1.Stop (Seconds (20.));
  sinkApps2.Start (Seconds (0.));
  sinkApps2.Stop (Seconds (20.));

  Ptr<Socket> ns3TcpSocket1 = Socket::CreateSocket (nodes.Get(0), TcpSocketFactory::GetTypeId ());
  Ptr<Socket> ns3UdpSocket2 = Socket::CreateSocket (nodes.Get(1), UdpSocketFactory::GetTypeId ());
  
  AsciiTraceHelper asciiTraceHelper;
  Ptr<OutputStreamWrapper> stream = asciiTraceHelper.CreateFileStream ("cwnd.txt");
  ns3TcpSocket1->TraceConnectWithoutContext ("CongestionWindow", MakeBoundCallback (&CwndChange, stream));

  Ptr<MyApp> app1 = CreateObject<MyApp> ();
  Ptr<MyApp> app2 = CreateObject<MyApp> ();

  app1->Setup (ns3TcpSocket1, sinkAddress1, 10400, 10000, DataRate("1Mbps"));
  app2->Setup (ns3UdpSocket2, sinkAddress2,  10400, 10000,DataRate("1Mbps"));
  nodes.Get (0)->AddApplication (app1);
  nodes.Get (1)->AddApplication (app2);
  app1->SetStartTime (Seconds (1.));
  app1->SetStopTime (Seconds (20.));
  app2->SetStartTime (Seconds (1.));
  app2->SetStopTime (Seconds (20.));

  FlowMonitorHelper flowmon;
  Ptr<FlowMonitor> monitor = flowmon.InstallAll();
  monitor->CheckForLostPackets ();
  
  Ptr<Ipv4FlowClassifier> classifier = DynamicCast<Ipv4FlowClassifier> (flowmon.GetClassifier ());
  int count=0;
  Ptr<OutputStreamWrapper> stream1 = asciiTraceHelper.CreateFileStream ("throughput.txt");
  for(count=0; count<20; count++){
    Simulator::Schedule(Seconds(count),&tghptCalc, monitor,classifier, stream1,count);
  }

  AnimationInterface anim(animFile);
  anim.SetMaxPktsPerTraceFile(500000);
  Ptr<Node> n = nodes.Get(0);
  anim.SetConstantPosition(n, 50, 1);
  n = nodes.Get(1);
  anim.SetConstantPosition(n, 25, 20);
  n = nodes.Get(2);
  anim.SetConstantPosition(n, 75, 20);
  n = nodes.Get(3);
  anim.SetConstantPosition(n, 12, 40);
  n = nodes.Get(4);
  anim.SetConstantPosition(n, 37, 40);
  n = nodes.Get(5);
  anim.SetConstantPosition(n, 62, 40);
  n = nodes.Get(6);
  anim.SetConstantPosition(n, 87, 40);

  Simulator::Stop (Seconds (20));
  Simulator::Run ();
  Simulator::Destroy ();

  return 0;
}


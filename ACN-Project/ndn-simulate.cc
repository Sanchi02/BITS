#include "ns3/core-module.h"
#include "ns3/network-module.h"
#include "ns3/ndnSIM-module.h"

namespace ns3 {

int
main(int argc, char* argv[])
{

  int si=8;
  int no=pow(2,si);
  CommandLine cmd;
  cmd.Parse(argc, argv);

  AnnotatedTopologyReader topologyReader("", 1);
  topologyReader.SetFileName("/home/yashita/ndnSIM/ns-3/scratch/topo.txt");
  topologyReader.Read();

  // Install NDN stack on all nodes
   ndn::StackHelper ndnHelper;

for(int i=1;i<=no;i++)
{
   
      char s[10]="l";
     char h[10];
    // std::string s="l";
     std::string le=std::to_string(si);
     //std::cout<<"le="<<le<<"\n";
  	char l[le.length()];
      for(int c=0;le[c]!='\0';c++)
         l[c]=le[c];
       strncat(s,l,le.length());
       strncat(s,"-",1);
        std::string he= std::to_string(i);
       for(int c=0;he[c]!='\0';c++)
         h[c]=he[c];
      strncat(s,h,he.length());
    // std::cout<<"s = "<<s<<"\n";
     
   ndnHelper.SetOldContentStore("ns3::ndn::cs::Lru","MaxSize",
                               "150");
  ndnHelper.Install(Names::Find<Node>(s));
   
}
// std::cout<<"\n";


ndnHelper.SetOldContentStore("ns3::ndn::cs::Lru", "MaxSize",
                               "800");
  ndnHelper.Install(Names::Find<Node>("root"));
/*for(int i=1;i<=256;i++)
{
   
     char h[10];
      char s[10]="l8-";
    
        std::string he= std::to_string(i);
        for(int c=0;he[c]!='\0';c++)
         h[c]=he[c];
      strncat(s,h,he.length());
     //  std::cout<<s<<" ";
   ndnHelper.SetOldContentStore("ns3::ndn::cs::Lru","MaxSize",
                               "190");
  ndnHelper.Install(Names::Find<Node>(s));
   
}*/
for(int i=1;i<=128;i++)
{
   
     char h[10];
      char s[10]="l7-";
    
        std::string he= std::to_string(i);
        for(int c=0;he[c]!='\0';c++)
         h[c]=he[c];
      strncat(s,h,he.length());
      // std::cout<<s<<" ";
   ndnHelper.SetOldContentStore("ns3::ndn::cs::Lru","MaxSize",
                               "200");
  ndnHelper.Install(Names::Find<Node>(s));
   
}
for(int i=1;i<=64;i++)
{
   
     char h[10];
      char s[10]="l6-";
    
        std::string he= std::to_string(i);
        for(int c=0;he[c]!='\0';c++)
         h[c]=he[c];
      strncat(s,h,he.length());
    //   std::cout<<s<<" ";
   ndnHelper.SetOldContentStore("ns3::ndn::cs::Lru","MaxSize",
                               "300");
  ndnHelper.Install(Names::Find<Node>(s));
   
}
std::cout<<"\n";
for(int i=1;i<=32;i++)
{
   
     char h[10];
      char s[10]="l5-";
    
        std::string he= std::to_string(i);
        for(int c=0;he[c]!='\0';c++)
         h[c]=he[c];
      strncat(s,h,he.length());
    //   std::cout<<s<<" ";
   ndnHelper.SetOldContentStore("ns3::ndn::cs::Lru","MaxSize",
                               "400");
  ndnHelper.Install(Names::Find<Node>(s));
   
}
//std::cout<<"\n";


for(int i=1;i<=16;i++)
{
   
     char h[10];
      char s[10]="l4-";
    
        std::string he= std::to_string(i);
        for(int c=0;he[c]!='\0';c++)
         h[c]=he[c];
      strncat(s,h,he.length());
    //   std::cout<<s<<" ";
   ndnHelper.SetOldContentStore("ns3::ndn::cs::Lru","MaxSize",
                               "500");
  ndnHelper.Install(Names::Find<Node>(s));
   
}
//std::cout<<"\n";


for(int i=1;i<=8;i++)
{
   
     char h[10];
      char s[10]="l3-";
    
        std::string he= std::to_string(i);
        for(int c=0;he[c]!='\0';c++)
         h[c]=he[c];
      strncat(s,h,he.length());
    //   std::cout<<s<<" ";
   ndnHelper.SetOldContentStore("ns3::ndn::cs::Lru","MaxSize",
                               "550");
  ndnHelper.Install(Names::Find<Node>(s));
   
}
//std::cout<<"\n";

for(int i=1;i<=4;i++)
{
   
     char h[10];
      char s[10]="l2-";
    
        std::string he= std::to_string(i);
        for(int c=0;he[c]!='\0';c++)
         h[c]=he[c];
      strncat(s,h,he.length());
     //  std::cout<<s<<" ";
   ndnHelper.SetOldContentStore("ns3::ndn::cs::Lru","MaxSize",
                               "600");
  ndnHelper.Install(Names::Find<Node>(s));
   
}
//std::cout<<"\n";
for(int i=1;i<=2;i++)
{
      char h[10];
       char s[10]="l1-";
        std::string he= std::to_string(i);
      for(int c=0;he[c]!='\0';c++)
         h[c]=he[c];
      strncat(s,h,he.length());
    //   std::cout<<s<<" ";
   ndnHelper.SetOldContentStore("ns3::ndn::cs::Lru","MaxSize",
                              "700");
  ndnHelper.Install(Names::Find<Node>(s));
   
}
std::cout<<"\n";

  // Choosing forwarding strategy
  ndn::StrategyChoiceHelper::InstallAll("/prefix", "/localhost/nfd/strategy/best-route");

  // Installing global routing interface on all nodes
  ndn::GlobalRoutingHelper ndnGlobalRoutingHelper;
  ndnGlobalRoutingHelper.InstallAll();

  // Getting containers for the consumer/producer
 
 Ptr<Node>consumers[no];
  /*Ptr<Node> consumers[8] = {Names::Find<Node>("l3-1"), Names::Find<Node>("l3-2"),
                            Names::Find<Node>("l3-3"), Names::Find<Node>("l3-4"), Names::Find<Node>("l3-5"), Names::Find<Node>("l3-6"), Names::Find<Node>("l3-7"), Names::Find<Node>("l3-8")};*/
for(int i=1;i<=no;i++)
{    char h[10];
      char s[10]="l";
      std::string le= std::to_string(si);
    char l[le.length()];
      for(int c=0;le[c]!='\0';c++)
         l[c]=le[c];
       strncat(s,l,le.length());
       strncat(s,"-",1);
        std::string he= std::to_string(i);
      for(int c=0;he[c]!='\0';c++)
         h[c]=he[c];
      strncat(s,h,he.length());
 //      std::cout<<s<<" ";
     consumers[i-1]=Names::Find<Node>(s);
   
}
std::cout<<"\n";
  Ptr<Node> producer = Names::Find<Node>("root");
//ndn::Interest::setDefaultCanBePrefix("/newreq");
 
  for (int i = 0; i < no; i++) {
  
    ndn::AppHelper consumerHelper("ns3::ndn::ConsumerZipfMandelbrot");
    consumerHelper.SetAttribute("Frequency", StringValue("300")); // 300 interests a second
    consumerHelper.SetAttribute("Randomize", StringValue("exponential"));
    //consumerHelper.SetAttribute("s", StringValue("0.8"));

    consumerHelper.SetPrefix("/root");
    ApplicationContainer app = consumerHelper.Install(consumers[i]);
    app.Start(Seconds(0.01*i));
   //  consumerHelper.Install(consumers[i]);
    
  }

  ndn::AppHelper producerHelper("ns3::ndn::Producer");
  producerHelper.SetAttribute("PayloadSize", StringValue("1024"));

  // Register /root prefix with global routing controller and
  // install producer that will satisfy Interests in /root namespace
  ndnGlobalRoutingHelper.AddOrigins("/root", producer);
  producerHelper.SetPrefix("/root");
  producerHelper.Install(producer);

  // Calculate and install FIBs
  ndn::GlobalRoutingHelper::CalculateRoutes();

  Simulator::Stop(Seconds(10.0));

  ndn::L3RateTracer::InstallAll("rate-trace7.txt", Seconds(1));
  ndn::CsTracer::InstallAll("cs-trace7.txt", Seconds(1));
  ndn::AppDelayTracer::InstallAll("app-delays-trace.txt");

  Simulator::Run();
  Simulator::Destroy();

  return 0;
}

} // namespace ns3

int
main(int argc, char* argv[])
{
  return ns3::main(argc, argv);
}
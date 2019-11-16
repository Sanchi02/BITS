#include "tcp-mod520.h"
#include "ns3/log.h"

namespace ns3 {

NS_LOG_COMPONENT_DEFINE ("TcpMod520");
NS_OBJECT_ENSURE_REGISTERED (TcpMod520);

uint32_t prevLossBytes = 0;

uint32_t GetPreviousBytesInFlight (void)
{
  return prevLossBytes;
}

TypeId TcpMod520::GetTypeId (void)
{
  static TypeId tid = TypeId ("ns3::TcpMod520")
    .SetParent<TcpNewReno> ()
    .AddConstructor<TcpMod520> ()
    .SetGroupName ("Internet")
  ;
  return tid;
}

TcpMod520::TcpMod520 (void)
  : TcpNewReno (),
    m_ackCnt (0)
{
  NS_LOG_FUNCTION (this);
}

TcpMod520::TcpMod520 (const TcpMod520& sock)
  : TcpNewReno (sock),
    m_ackCnt (sock.m_ackCnt)
{
  NS_LOG_FUNCTION (this);
}

TcpMod520::~TcpMod520 (void)
{
  NS_LOG_FUNCTION (this);
}

Ptr<TcpCongestionOps> TcpMod520::Fork (void)
{
  return CopyObject<TcpMod520> (this);
}

uint32_t TcpMod520::SlowStart (Ptr<TcpSocketState> tcb, uint32_t segmentsAcked)
{
  if (segmentsAcked >= 1)
    {
      tcb->m_cWnd += tcb->m_segmentSize;
      return segmentsAcked - 1;
    }
  return 0;
}

void TcpMod520::IncreaseWindow (Ptr<TcpSocketState> tcb, uint32_t segmentsAcked)
{
  if (tcb->m_cWnd < tcb->m_ssThresh)
    {
      segmentsAcked = SlowStart(tcb, segmentsAcked);
    }

  if (tcb->m_cWnd >= tcb->m_ssThresh)
    {
      CongestionAvoidance (tcb, segmentsAcked);
    }
}

void TcpMod520::CongestionAvoidance (Ptr<TcpSocketState> tcb, uint32_t segmentsAcked)
{
  uint32_t bytesInFlight = GetPreviousBytesInFlight();
  uint32_t segCwnd = bytesInFlight / tcb->m_segmentSize;
  tcb->m_cWnd = tcb->m_cWnd + segCwnd;
}

std::string TcpMod520::GetName () const
{
  return "TcpMod520";
}

uint32_t TcpMod520::GetSsThresh (Ptr<const TcpSocketState> tcb,
                           uint32_t m_bytesInFlight)
{
  prevLossBytes = tcb->m_bytesInFlight;
  uint32_t segCwnd = (tcb->m_segmentSize)*(tcb -> m_cWnd/tcb->m_initialSsThresh);
  return segCwnd;
}
} // namespace ns3

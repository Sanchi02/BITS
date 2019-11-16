/* -*- Mode:C++; c-file-style:"gnu"; indent-tabs-mode:nil; -*- */
/*
 * Copyright (c) 2014 Natale Patriciello, <natale.patriciello@gmail.com>
 *
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
 *
 */

#ifndef TcpMod520_H
#define TcpMod520_H

#include "ns3/tcp-congestion-ops.h"

namespace ns3 {

class TcpMod520 : public TcpNewReno
{
public:
  static TypeId GetTypeId (void);
  TcpMod520 (void);
  TcpMod520 (const TcpMod520& sock);
  virtual ~TcpMod520 (void);
  virtual std::string GetName () const;
  virtual uint32_t GetSsThresh (Ptr<const TcpSocketState> tcb, uint32_t m_bytesInFlight);
  virtual void IncreaseWindow(Ptr<TcpSocketState> tcb, uint32_t segmentsAcked);
  virtual uint32_t SlowStart (Ptr<TcpSocketState> tcb, uint32_t segmentsAcked);
  virtual Ptr<TcpCongestionOps> Fork ();

protected:
  virtual void CongestionAvoidance (Ptr<TcpSocketState> tcb, uint32_t segmentsAcked);
  
private:
  uint32_t m_ackCnt;
};

} // namespace ns3

#endif // TcpMod520_H

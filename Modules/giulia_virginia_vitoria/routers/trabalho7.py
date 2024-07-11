from fastapi import FastAPI, Query, APIRouter
from typing import List
from scapy.all import rdpcap, IP, DNS
from pydantic import BaseModel
import uvicorn

router = APIRouter()
app = FastAPI()

class DNSData(BaseModel):
    timestamp: float
    src_ip: str
    dst_ip: str
    protocol: str
    length: int
    info: str

def extract_dns_info(pcap_file):
    packets = rdpcap(pcap_file)
    dns_packets = []
    
    for i, pkt in enumerate(packets):
        if DNS in pkt:
            ip_packet = pkt[IP]
            dns_packet = pkt[DNS]

            if dns_packet.qr == 0:  # QR == 0 significa que é uma consulta (query)
                query_name = dns_packet.qd.qname.decode() if dns_packet.qd and dns_packet.qd.qname else ""
                info = f"Standard query {dns_packet.id:#x} A {query_name}"
            else:  # QR == 1 significa que é uma resposta (response)
                query_name = dns_packet.qd.qname.decode() if dns_packet.qd and dns_packet.qd.qname else ""
                answer = dns_packet.an.rdata if dns_packet.an else ""
                info = f"Standard query response {dns_packet.id:#x} A {query_name} A {answer}"

            dns_data = DNSData(
                timestamp=pkt.time,
                src_ip=ip_packet.src,
                dst_ip=ip_packet.dst,
                protocol="DNS",
                length=len(pkt),
                info=info
            )
            dns_packets.append(dns_data)
                
    return dns_packets

pcap_file_path = './pcaps/dns.pcap'
dns_packets = extract_dns_info(pcap_file_path)

@router.get("/trabalho7", response_model=List[DNSData])
def read_trabalho7(skip: int = Query(0), limit: int = Query(10)):
    global dns_packets
    return dns_packets[skip: skip + limit]

app.include_router(router)

if __name__ == "__main__":
    uvicorn.run(app, host="localhost", port=3001)

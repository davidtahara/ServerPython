from fastapi import FastAPI, File, UploadFile
from typing import List
from scapy.all import ARP, rdpcap
from fastapi import APIRouter
import uvicorn

router = APIRouter()

app = FastAPI()

class ARPData:
    def __init__(self, timestamp, src_ip, dst_ip, src_mac, dst_mac, op):
        self.timestamp = timestamp
        self.src_ip = src_ip
        self.dst_ip = dst_ip
        self.src_mac = src_mac
        self.dst_mac = dst_mac
        self.op = op

def extract_arp_info(pcap_file):
    packets = rdpcap(pcap_file)
    arp_requests = []
    arp_replies = []
    
    for pkt in packets:
        if ARP in pkt:
            arp_packet = pkt[ARP]
            info = ARPData(
                timestamp=pkt.time,
                src_ip=arp_packet.psrc,
                dst_ip=arp_packet.pdst,
                src_mac=arp_packet.hwsrc,
                dst_mac=arp_packet.hwdst,
                op=arp_packet.op
            )
            if arp_packet.op == 1:  # ARP Request
                arp_requests.append(info)
            elif arp_packet.op == 2:  # ARP Reply
                arp_replies.append(info)
    
    return arp_requests, arp_replies

arp_requests, arp_replies = extract_arp_info('./pcaps/trabalho2.pcap')

@router.get("/trabalho2")
def read_trabalho2():
    return {
        "requests": [arp.__dict__ for arp in arp_requests],
        "replies": [arp.__dict__ for arp in arp_replies]
    }

app.include_router(router)

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=3001)  # Porta para o backend

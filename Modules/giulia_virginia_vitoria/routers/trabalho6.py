from fastapi import FastAPI, File, UploadFile
from typing import List
from scapy.all import rdpcap, IP, TCP
from fastapi import APIRouter
import uvicorn

router = APIRouter()

app = FastAPI()

class HTTPData:
    def __init__(self, timestamp, src_ip, dst_ip, src_port, dst_port, payload):
        self.timestamp = timestamp
        self.src_ip = src_ip
        self.dst_ip = dst_ip
        self.src_port = src_port
        self.dst_port = dst_port
        self.payload = payload

def extract_http_info(pcap_file):
    packets = rdpcap(pcap_file)
    http_packets = []
    
    for pkt in packets:
        if IP in pkt and TCP in pkt:
            ip_packet = pkt[IP]
            tcp_packet = pkt[TCP]
            if tcp_packet.dport == 80 or tcp_packet.sport == 80:
                payload = bytes(tcp_packet.payload).decode('utf-8', errors='ignore')
                info = HTTPData(
                    timestamp=pkt.time,
                    src_ip=ip_packet.src,
                    dst_ip=ip_packet.dst,
                    src_port=tcp_packet.sport,
                    dst_port=tcp_packet.dport,
                    payload=payload
                )
                http_packets.append(info)
    
    return http_packets

http_packets = extract_http_info('./pcaps/trabalho6.pcap')

@router.get("/trabalho6")
def read_trabalho6():
    return {
        "http_packets": [pkt.__dict__ for pkt in http_packets]
    }

app.include_router(router)

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=3002)  # Porta para o backend


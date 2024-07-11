import uvicorn
from fastapi import FastAPI, APIRouter
from pydantic import BaseModel
from scapy.all import rdpcap, IP, RIP
from typing import List

router = APIRouter()
app = FastAPI()

class RIPPacket(BaseModel):
    number: int
    time: float
    source: str
    destination: str
    protocol: str
    length: int
    info: str

def extract_rip_packets(pcap_file):
    packets = rdpcap(pcap_file)
    rip_packets = []

    for i, pkt in enumerate(packets):
        if RIP in pkt:
            rip_packet = pkt[RIP]
            rip_data = RIPPacket(
                number=i + 1,
                time=pkt.time,
                source=pkt[IP].src,
                destination=pkt[IP].dst,
                protocol="RIP",
                length=len(pkt),
                info="RIP Packet"
            )
            rip_packets.append(rip_data)

    print(f"Extracted {len(rip_packets)} RIP packets")
    return rip_packets

# Caminho para o arquivo pcap trabalho3 (assumindo conversão para .pcap)
pcap_file_path = './pcaps/trabalho3.pcap'

# Chama a função extract_rip_packets com o arquivo pcap desejado
rip_packets = extract_rip_packets(pcap_file_path)

@router.get("/trabalho3", response_model=List[RIPPacket])
def read_trabalho3():
    global rip_packets
    return rip_packets

app.include_router(router)

if __name__ == "__main__":
    uvicorn.run(app, host="localhost", port=3001)
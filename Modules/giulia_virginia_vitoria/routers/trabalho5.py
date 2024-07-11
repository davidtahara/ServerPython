#trabalho5.py
from fastapi import APIRouter
from typing import List
from scapy.all import rdpcap, IP, TCP, Raw
from pydantic import BaseModel  # Importe o BaseModel aqui

router = APIRouter()

# Classe para representar dados dos pacotes TCP
class TCPData(BaseModel):
    timestamp: float
    source: str
    destination: str
    length: int
    data: str

@router.get("/trabalho5", response_model=List[TCPData])
def read_trabalho5():
    pcap_file_path = './pcaps/trabalho5.pcap'  # Verifique o caminho do seu arquivo pcap
    tcp_packets = extract_tcp_info(pcap_file_path)
    return tcp_packets

# Função para extrair informações dos pacotes TCP do arquivo pcap usando Scapy
def extract_tcp_info(pcap_file):
    packets = rdpcap(pcap_file)
    tcp_packets = []

    for pkt in packets:
        if IP in pkt and TCP in pkt:
            # Verifica se o pacote possui carga útil (load)
            if pkt.haslayer(Raw):
                data_payload = pkt[Raw].load.hex()
            else:
                data_payload = ""

            tcp_data = TCPData(
                timestamp=pkt.time,
                source=pkt[IP].src,
                destination=pkt[IP].dst,
                length=len(pkt),
                data=data_payload
            )
            tcp_packets.append(tcp_data)

    return tcp_packets

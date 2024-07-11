# trabalho4.py
from fastapi import APIRouter
from typing import List
from scapy.all import rdpcap, IP, UDP

router = APIRouter()

# Classe para representar dados dos pacotes UDP
class UDPData:
    def __init__(self, timestamp, source, destination, length, data):
        self.timestamp = timestamp
        self.source = source
        self.destination = destination
        self.length = length
        self.data = data

# Função para extrair informações dos pacotes UDP do arquivo pcap usando Scapy
def extract_udp_info(pcap_file):
    packets = rdpcap(pcap_file)
    udp_packets = []
    
    for pkt in packets:
        if IP in pkt and UDP in pkt:
            # Verifica se o pacote possui carga útil (load)
            if pkt.haslayer(Raw):
                data_payload = pkt[Raw].load.hex()
            else:
                data_payload = ""
                
            udp_data = UDPData(
                timestamp=pkt.time,
                source=pkt[IP].src,
                destination=pkt[IP].dst,
                length=len(pkt),
                data=data_payload
            )
            udp_packets.append(udp_data)
    
    return udp_packets

# Path to your pcap file for trabalho4
pcap_file_path = './pcaps/trabalho4.pcap'

# Rota para obter dados dos pacotes UDP
@router.get("/trabalho4")
def read_trabalho4():
    pcap_file_path = './pcaps/trabalho4.pcap'
    udp_packets = extract_udp_info(pcap_file_path)
    return {
        "udp_packets": [udp.__dict__ for udp in udp_packets]
    }

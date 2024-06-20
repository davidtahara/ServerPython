import uvicorn
from fastapi import FastAPI, APIRouter
from scapy.all import rdpcap, IP, RIP

router = APIRouter()
app = FastAPI()

# Classe para representar dados dos pacotes RIP
class RIPData:
    def __init__(self, timestamp, source, destination, command, version, entries):
        self.timestamp = timestamp
        self.source = source
        self.destination = destination
        self.command = command
        self.version = version
        self.entries = entries

# Função para extrair informações dos pacotes RIP do arquivo pcap usando Scapy
def extract_rip_info(pcap_file):
    packets = rdpcap(pcap_file)
    rip_packets = []
    
    for pkt in packets:
        if IP in pkt and RIP in pkt:
            rip_packet = pkt[RIP]
            entries = []
            for entry in rip_packet.entries:
                entry_info = {
                    'addr': entry.address,
                    'mask': entry.subnet_mask,
                    'metric': entry.metric,
                    'next_hop': entry.next_hop
                }
                entries.append(entry_info)
            
            rip_data = RIPData(
                timestamp=pkt.time,
                source=pkt[IP].src,
                destination=pkt[IP].dst,
                command=rip_packet.cmd,
                version=rip_packet.version,
                entries=entries
            )
            rip_packets.append(rip_data)
    
    return rip_packets

# Path to your pcap file for trabalho3 (assumindo conversão para .pcap)
pcap_file_path = '././pcaps/trabalho2.pcap'

# Chama a função extract_rip_info com o arquivo pcap desejado
rip_packets = extract_rip_info(pcap_file_path)

@router.get("/trabalho3")
def read_trabalho3():
    global rip_packets  # Adiciona esta linha para acessar a variável rip_packets globalmente
    return {
        "rip_packets": [rip.__dict__ for rip in rip_packets]
    }

app.include_router(router)

if __name__ == "__main__":
    uvicorn.run(app, host="localhost", port=3001)

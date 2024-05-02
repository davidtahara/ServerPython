from fastapi import FastAPI
from fastapi.responses import JSONResponse
import scapy.all as scapy

app = FastAPI()

@app.get("/udp-analysis", response_class=JSONResponse)
async def udp_analysis():
    try:
        arquivo = './pcaps/trabalho4.pcap'
        pacotes = scapy.rdpcap(arquivo)

        ips = []
        protocolos = {}
        portas = {}

        for pacote in pacotes:
            if pacote.haslayer(scapy.UDP):
                if scapy.IP in pacote:
                    ips.append(pacote[scapy.IP].src)
                    portas[pacote[scapy.UDP].dport] = portas.get(pacote[scapy.UDP].dport, 0) + 1

        ips_count = {ip: ips.count(ip) for ip in set(ips)}

        tempo_total = pacotes[-1].time - pacotes[0].time
        tempo_total = round(tempo_total, 2)

        return {
            "Protocolos": protocolos,
            "IPs": ips_count,
            "Portas": portas,
            "Tempo total": tempo_total
        }
    except Exception as e:
        return {"error": f"An error occurred: {str(e)}"}

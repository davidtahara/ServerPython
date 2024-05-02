from fastapi import FastAPI
from fastapi.responses import JSONResponse
import scapy.all as scapy

app = FastAPI()

@app.get("/rip-analysis", response_class=JSONResponse)
async def rip_analysis():
    try:
        arquivo = './pcaps/trabalho3.pcap'
        pacotes = scapy.rdpcap(arquivo)

        # Inicialização de estruturas de dados
        ips = []
        protocolos = {}
        portas = {}

        # Percorre cada pacote no arquivo pcap
        for pacote in pacotes:
            if scapy.RIP in pacote:  # Verifica se o pacote contém protocolo RIP
                # Atualiza contadores de protocolos e portas
                protocolos['RIP'] = protocolos.get('RIP', 0) + 1
                if pacote.haslayer(scapy.UDP):
                    portas[pacote[scapy.UDP].dport] = portas.get(pacote[scapy.UDP].dport, 0) + 1
                
                # Coleta IPs de origem
                if pacote.haslayer(scapy.IP):
                    ips.append(pacote[scapy.IP].src)

        # Contagem de IPs
        ips_count = {ip: ips.count(ip) for ip in set(ips)}

        # Tempo total da captura
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

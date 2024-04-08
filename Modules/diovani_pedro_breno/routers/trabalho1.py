from fastapi import APIRouter
import scapy.all as scapy

router = APIRouter(prefix="/trabalho1", tags=[""])

@router.get("/analise2")
def analise():
    arquivo = './pcaps/pacotes.pcap'
    pacotes = scapy.rdpcap(arquivo)

    #ips
    ips = []

    # pega a quantidade de pacotes por protocolo
    protocolos = {}
    portas = {}
    for pacote in pacotes:
        # printa a porta do pacote
        if pacote.haslayer(scapy.TCP):
            portas[pacote[scapy.TCP].dport] = portas.get(pacote[scapy.TCP].dport, 0) + 1
        if pacote.haslayer(scapy.UDP):
            portas[pacote[scapy.UDP].dport] = portas.get(pacote[scapy.UDP].dport, 0) + 1
        if pacote.haslayer(scapy.IP):
            ips.append(pacote[scapy.IP].src)
            if pacote[scapy.IP].proto in protocolos:
                protocolos[pacote[scapy.IP].proto] += 1
            else:
                protocolos[pacote[scapy.IP].proto] = 1

        # pega a quantidade de pacotes por ip
        ips_count = {}
        for ip in ips:
            if ip in ips_count:
                ips_count[ip] += 1
            else:
                ips_count[ip] = 1

        # pega o tempo total da captura
        tempo_total = pacotes[-1].time - pacotes[0].time
        # passa para segundos
        tempo_total = round(tempo_total, 2)

    return {
        "Protocolos": protocolos,
        "IPs": ips_count,
        "Portas": portas,
        "Tempo total": tempo_total
    }
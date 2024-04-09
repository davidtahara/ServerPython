from fastapi import APIRouter
from ...rodrigo_thierry_joaovitor.Parser import PacketSource, IPPacket, ARPPacket
#from Parser import PacketSource, IPPacket, ARPPacket
# import scapy.all as scapy

router = APIRouter(prefix="/grupo_rodrigo_thierry_joao/t1", tags=[""])

src = PacketSource()

@router.get("/enviados/list")
def get_enviados_list():
    output = {packet.sourceIp for packet in src.allPackets}
    return output

@router.get("/enviados/{ip}")
def get_enviados(ip: str):
    output = [packet for packet in src.allPackets if packet.sourceIp == ip]
    return output


@router.get('/recebidos/list')
def get_recebidos_list():
    output = {packet.destinationIp for packet in src.allPackets}
    return output

@router.get("/recebidos/{ip}")
def get_recebidos(ip: str):
    output = [packet for packet in src.allPackets if packet.destinationIp == ip]
    return output

@router.get("/relatorio/simples/{ip}")
def get_soma(ip: str):
    output = {}
    output['origem'] = ip
    output['trafego'] = {}
    output['protocolo'] = {}
    for packet in src.allPackets:
        if isinstance(packet, ARPPacket) or (packet.sourceIp != ip and packet.destinationIp != ip):
            continue

        size = 0
        if packet.version == 4:
            size = packet.length
        elif packet.version == 6:
            size = packet.payloadLength
        if packet.sourceIp == ip:
            if packet.destinationIp not in output['trafego']:
                output['trafego'][packet.destinationIp] = 0
            output['trafego'][packet.destinationIp] += size
        else:
            if packet.sourceIp not in output['trafego']:
                output['trafego'][packet.sourceIp] = 0
            output['trafego'][packet.sourceIp] += size

        if packet.version == 4:
            output['protocolo'][packet.protocol] = output['protocolo'].get(packet.protocol, 0) + 1
    return output

@router.get("/todos/")
def get_todos():
    return src.allPackets

@router.get("/pacote/{id}")
def get_pacote(id: str):
    uniqueId = uuid.UUID(id)
    for packet in src.allPackets:
        if packet.uniqueId == uniqueId:
            return packet, src.packetData[uniqueId]

# @router.get("/analise2")
# def analise():
#     arquivo = './pcaps/pacotes.pcap'
#     pacotes = scapy.rdpcap(arquivo)

#     #ips
#     ips = []

#     # pega a quantidade de pacotes por protocolo
#     protocolos = {}
#     portas = {}
#     for pacote in pacotes:
#         # printa a porta do pacote
#         if pacote.haslayer(scapy.TCP):
#             portas[pacote[scapy.TCP].dport] = portas.get(pacote[scapy.TCP].dport, 0) + 1
#         if pacote.haslayer(scapy.UDP):
#             portas[pacote[scapy.UDP].dport] = portas.get(pacote[scapy.UDP].dport, 0) + 1
#         if pacote.haslayer(scapy.IP):
#             ips.append(pacote[scapy.IP].src)
#             if pacote[scapy.IP].proto in protocolos:
#                 protocolos[pacote[scapy.IP].proto] += 1
#             else:
#                 protocolos[pacote[scapy.IP].proto] = 1

#         # pega a quantidade de pacotes por ip
#         ips_count = {}
#         for ip in ips:
#             if ip in ips_count:
#                 ips_count[ip] += 1
#             else:
#                 ips_count[ip] = 1

#         # pega o tempo total da captura
#         tempo_total = pacotes[-1].time - pacotes[0].time
#         # passa para segundos
#         tempo_total = round(tempo_total, 2)

#     return {
#         "Protocolos": protocolos,
#         "IPs": ips_count,
#         "Portas": portas,
#         "Tempo total": tempo_total
#     }
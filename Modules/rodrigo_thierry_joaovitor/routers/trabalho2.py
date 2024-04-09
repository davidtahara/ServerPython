from fastapi import APIRouter
from ...rodrigo_thierry_joaovitor.Parser import PacketSource, IPPacket, ARPPacket
#from Parser import PacketSource, IPPacket, ARPPacket
# import scapy.all as scapy

router = APIRouter(prefix="/grupo_rodrigo_thierry_joao/arp", tags=[""])

src = PacketSource()

@router.get("/enviados/list")
def get_enviados_list():
    output = {packet.sourceIp for packet in src.allPackets if isinstance(packet, ARPPacket)}
    return output

@router.get("/enviados/{ip}")
def get_enviados(ip: str):
    output = [packet for packet in src.allPackets if isinstance(packet, ARPPacket) and packet.sourceIp == ip]
    return output

@router.get("/")

@router.get('/recebidos/list')
def get_recebidos_list():
    output = {packet.destinationIp for packet in src.allPackets if isinstance(packet, ARPPacket)}
    return output

@router.get("/recebidos/{ip}")
def get_recebidos(ip: str):
    output = [packet for packet in src.allPackets if isinstance(packet, ARPPacket) and packet.destinationIp == ip]
    return output
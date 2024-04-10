from fastapi import APIRouter
from ...rodrigo_thierry_joaovitor.Parser import PacketSource, IPPacket, ARPPacket, packetSource as src
from ...rodrigo_thierry_joaovitor.MacVendor import findVendor
#from Parser import PacketSource, IPPacket, ARPPacket
# import scapy.all as scapy

router = APIRouter(prefix="/grupo_rodrigo_thierry_joao/arp", tags=[""])

@router.get("/enviados/list")
def get_enviados_list():
    ''' Retorna uma lista de tuplas dos endereços(logicos e fisicos) que fizeram ARP requests'''
    for packet in src.allPackets:
        if not isinstance(packet, ARPPacket):
            continue
        arpPacket:ARPPacket = packet
        if arpPacket.operation == 1:
            yield (arpPacket.sourceIp, arpPacket.source_hardware_address)

@router.get("/getVendor/{ip}")
def get_vendor(ip: str):
    ''' Retorna o nome do fabricante do endereço MAC. Utiliza caching para prevenir rate limit'''
    output = findVendor(ip)
    return output

@router.get("/todos")
async def get_todos():
    '''Retorna uma lista com todos os requests ARP'''
    output = []

    for packet in src.allPackets:
        if not isinstance(packet, ARPPacket):
            continue
        arpPacket:ARPPacket = packet

        output.append({
            "sourceIp": arpPacket.source_protocol_address,
            "sourceMac": arpPacket.source_hardware_address,
            "targetIp": arpPacket.destination_protocol_address,
            "targetMac": arpPacket.destination_protocol_address,
            "operation": arpPacket.operation,
            "sourceVendor": findVendor(arpPacket.source_hardware_address),
            "targetVendor": findVendor(arpPacket.destination_hardware_address)
        })
    return output
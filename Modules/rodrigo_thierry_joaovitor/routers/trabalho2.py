from fastapi import APIRouter
from ...rodrigo_thierry_joaovitor.Parser import PacketSource, IPPacket, ARPPacket, packetSource as src
from ...rodrigo_thierry_joaovitor.MacVendor import findVendor
#from Parser import PacketSource, IPPacket, ARPPacket
# import scapy.all as scapy

router = APIRouter(prefix="/grupo_rodrigo_thierry_joao/arp", tags=[""])

@router.get("/enviados/list")
def get_enviados_list():
    ''' Retorna uma lista de tuplas dos endereços(logicos e fisicos) que fizeram ARP requests'''
    output = []
    for packet in src.allPackets:
        if not isinstance(packet, ARPPacket):
            continue
        arpPacket:ARPPacket = packet
        if arpPacket.operation == 1:
            output.append((arpPacket.sourceIp, arpPacket.source_hardware_address))

    # remover duplicatas
    output = list(set(output))
    return output

@router.get("/getVendor/{ip}")
def get_vendor(ip: str):
    ''' Retorna o nome do fabricante do endereço MAC. Usa um arquivo json com os prefixos'''
    output = findVendor(ip)
    return output

@router.get("/enviados/{ip}")
def get_enviados(ip: str):
    ''' Retorna todos os pacotes ARP que um ip enviou'''

    output = []
    for packet in src.allPackets:
        if not isinstance(packet, ARPPacket):
            continue
        arpPacket:ARPPacket = packet
        if not arpPacket.operation == 1:
            continue
        if arpPacket.source_protocol_address == ip:
            output.append({
                "hardwareType": arpPacket.hardware_type,
                "protocolType": arpPacket.protocol_type,
                "hardwareLength": arpPacket.hardware_length,
                "protocolLength": arpPacket.protocol_length,
                "sourceIp": arpPacket.source_protocol_address,
                "sourceMac": arpPacket.source_hardware_address,
                "targetIp": arpPacket.destination_protocol_address,
                "targetMac": arpPacket.destination_hardware_address,
                "operation": arpPacket.operation,
                "sourceVendor": findVendor(arpPacket.source_hardware_address),
                "targetVendor": findVendor(arpPacket.destination_hardware_address)
            })
    return output

@router.get("/recebidos/{ip}")
def get_recebidos(ip: str):
    ''' Retorna todos os pacotes ARP que um ip recebeu'''

    output = []
    for packet in src.allPackets:
        if not isinstance(packet, ARPPacket):
            continue
        arpPacket:ARPPacket = packet

        if not arpPacket.operation == 2:
            continue
        if arpPacket.destination_protocol_address == ip:
            output.append({
                "hardwareType": arpPacket.hardware_type,
                "protocolType": arpPacket.protocol_type,
                "hardwareLength": arpPacket.hardware_length,
                "protocolLength": arpPacket.protocol_length,
                "sourceIp": arpPacket.source_protocol_address,
                "sourceMac": arpPacket.source_hardware_address,
                "targetIp": arpPacket.destination_protocol_address,
                "targetMac": arpPacket.destination_hardware_address,
                "operation": arpPacket.operation,
                "sourceVendor": findVendor(arpPacket.source_hardware_address),
                "targetVendor": findVendor(arpPacket.destination_hardware_address)
            })
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
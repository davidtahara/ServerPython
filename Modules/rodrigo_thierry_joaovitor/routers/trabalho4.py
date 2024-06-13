from fastapi import APIRouter
from typing import Dict, List, Any
import json
from ...rodrigo_thierry_joaovitor.Parser import PacketSource, UDPPacket, IPPacket, packetSource as src
from ...rodrigo_thierry_joaovitor.PortFinder import findService

router = APIRouter(prefix="/grupo_rodrigo_thierry_joao/udp", tags=[""])


@router.get("/todos")
def get_todos():
    ''' Retorna todos os pacotes disponiveis'''
    for packet in src.allPackets:
        if isinstance(packet, UDPPacket):
            yield packet


@router.get("/services/{port}")
def get_services(port: int):
    ''' Retorna todos os serviços que usam uma porta UDP'''
    return findService(port)


@router.get("/port/{port}")
def get_in_port(port: int):
    ''' Retorna todos os pacotes que usam uma porta UDP como destino'''
    for packet in src.allPackets:
        if not isinstance(packet, UDPPacket):
            continue
        udpPacket: UDPPacket = packet
        if udpPacket.dstPort == port:
            yield udpPacket


@router.get("/graph")
def miserables():
    pre_nodes: Dict[str, Dict] = dict()
    edges: List[Dict[str, str]] = []

    allUDP: List[UDPPacket] = src.allPacketsDict[UDPPacket]
    category: List[str] = []

    for item in allUDP:

        ip: IPPacket = item.external_pdu

        # Categorias Baseadas em IP

        if ip.sourceIp not in category:
            category.append(ip.sourceIp)

        if ip.destinationIp not in category:
            category.append(ip.destinationIp)

        # Nodes, IP:PORT
        src_socket: str = ip.sourceIp + ":" + str(item.srcPort)
        if src_socket not in pre_nodes:
            tmp = {"id": src_socket,
                   "name": src_socket,
                   "size": 10,
                   "value": 10,
                   "symbolSize": 10,
                   "category": category.index(ip.sourceIp)}
            pre_nodes[src_socket] = tmp

        dst_socket: str = ip.destinationIp + ":" + str(item.dstPort)
        if dst_socket not in pre_nodes:
            pre_nodes[dst_socket] = {"id": dst_socket,
                                     "name": dst_socket,
                                     "size": 10,
                                     "value": 10,
                                     "symbolSize": 10,
                                     "category": category.index(ip.destinationIp)}

        # Edges, IP:PORT --> IP:PORT

        edges.append({
            "source": src_socket,
            "target": dst_socket
        })

        # incrementa o campo value/size do nó destino
        pre_nodes.get(dst_socket)["size"] += 1
        pre_nodes.get(dst_socket)["value"] += 1
        pre_nodes.get(dst_socket)["symbolSize"] += 1


    retorno: Dict[str, List[Dict[str, Any]]] = {"nodes": list(pre_nodes.values()), "links": edges,
                                                "categories": [{"name": i} for i in category]}

    return retorno

#
# Nao tem jeito facil de pegar o ip de cada pacote udp
# pela camada ip(nao tem pdu externo setado ainda eu acho)
# se conseguir arrumar, descomente os 2 endpoints abaixo
# 
# TODO: analisar de vale a pena fazer uma busca O(n) em
# todos os pacotes ip p/ achar o srcIp e dstIp em cada pacote
# udp. Vai acarretar em um O(n^2). (isso se ja nao ta uma 
# complexidade muito pior)
#

# @router.get("/enviados/{ip}")
# def get_enviados(ip: str):
#     ''' Retorna todos os pacotes UDP que um ip enviou'''
#     for packet in src.allPackets:
#         if not isinstance(packet, UDPPacket):
#             continue
#         udpPacket:UDPPacket = packet
#         if udpPacket.srcIp == ip:
#             yield udpPacket

# @router.get("/recebidos/{ip}")
# def get_recebidos(ip: str):
#     ''' Retorna todos os pacotes UDP que um ip recebeu'''
#     for packet in src.allPackets:
#         if not isinstance(packet, UDPPacket):
#             continue
#         udpPacket:UDPPacket = packet
#         if udpPacket.dstIp == ip:
#             yield udpPacket

# @router.get("/senders")
# def get_senders():
#     ''' Retorna todos os ips que enviaram pacotes UDP'''
#     output = []
#     for packet in src.allPackets:
#         if not isinstance(packet, UDPPacket):
#             continue
#         udpPacket: UDPPacket = packet
#         output.append(udpPacket.srcIp)
#     output = list(set(output))
#     return output

# @router.get("/receivers")
# def get_receivers():
#     ''' Retorna todos os ips que receberam pacotes UDP'''
#     output = []
#     for packet in src.allPackets:
#         if not isinstance(packet, UDPPacket):
#             continue
#         udpPacket:UDPPacket = packet
#         output.append(udpPacket.dstIp)
#     output = list(set(output))
#     return output

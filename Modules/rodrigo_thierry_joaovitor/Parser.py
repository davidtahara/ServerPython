from typing import List, Dict, Tuple, Any
import dpkt
import uuid
import os
import socket

# Constants EtherType
# https://en.wikipedia.org/wiki/EtherType#Values
# - Se isso crescer demais quem sabe seja bom por em um arquivo separado
ETH_TYPE_IPv4 = 0x0800
ETH_TYPE_IPv6 = 0x86DD
ETH_TYPE_ARP = 0x0806
ETH_TYPE_RARP = 0x8035


def int_to_ip4(addr: int) -> str:
    octets = []
    for _ in range(4):
        octet = addr & 255
        octets.insert(0, str(octet))
        addr >>= 8
    return '.'.join(octets)


class Packet:
    uniqueId: uuid.UUID = None

    '''
    Quem sabe seja útil quando for lidar com TCP e UDP
    '''
    payload: uuid.UUID

    external_pdu: 'Packet' = None
    internal_pdu: 'Packet' = None

    def setExternalPDU(self, pkt: 'Packet') -> None:
        self.external_pdu = pkt

    def setInternalPDU(self, pkt: 'Packet') -> None:
        self.internal_pdu = pkt

    def __init__(self):
        self.uniqueId = uuid.uuid4()

    def convert(pkg) -> 'Packet' | List['Packet'] | None:
        '''
        Converte o esquema de pacote do dpkt para IPPacket
        '''
        if isinstance(pkg, dpkt.ip.IP):
            return IPPacket.convert(pkg)
        elif isinstance(pkg, dpkt.ip6.IP6):
            return IP6Packet.convert(pkg)
        elif isinstance(pkg, dpkt.arp.ARP):
            return ARPPacket.convert(pkg)
        elif isinstance(pkg, dpkt.udp.UDP):
            return UDPPacket.convert(pkg)
        else:
            print("Tipo de pacote não tratado! Tipo:" + str(type(pkg)))
            return None


def appendPackets(destination: Dict[type, List[Packet]], source: List[Packet]):
    for pkt in source:
        if destination.get(pkt.__class__) is None:
            destination[pkt.__class__] = []
        destination[pkt.__class__].append(pkt)


class ARPPacket(Packet):
    """ARPPacket.

    Args:
        hardware_type (int): 16 bits. The type of the network on which ARP is running. Ethernet is given type 1.
        protocol_type (int): 16 bits. Defining the protocol. The value of this field for the IPv4 protocol is 0800H.
        hardware_length (int): 8 bits. Length of the hardware address in bytes.
        protocol_length (int): 8 bits. Length of the logical address in bytes.
        operation: (str): 16 bits. REQUEST OR REPLY

    """
    hardware_type: int
    protocol_type: int
    hardware_length: int
    protocol_length: int
    operation: str

    source_hardware_address: str
    source_protocol_address: str
    destination_hardware_address: str
    destination_protocol_address: str

    # Não quebrar a API
    sourceIp: str
    destinationIp: str

    def convert(pkg: dpkt.arp.ARP) -> 'ARPPacket':

        def format_protocol_address(value: bytes, proto_type) -> str:
            if proto_type == ETH_TYPE_IPv4:
                return f'{value[0]}.{value[1]}.{value[2]}.{value[3]}'
            elif proto_type == ETH_TYPE_IPv6:
                return socket.inet_ntop(socket.AF_INET6, value)
            else:
                return 'Unknown Protocol Type'

        def format_hardware_address(value: bytes, proto_type) -> str:
            if proto_type == 1:
                return ':'.join('{:02x}'.format(byte) for byte in value)
            else:
                return 'Unknown Protocol Type'

        arpPkg = ARPPacket()
        arpPkg.hardware_type = pkg.hrd
        arpPkg.protocol_type = pkg.pro
        arpPkg.hardware_length = pkg.hln
        arpPkg.protocol_length = pkg.pln
        arpPkg.operation = pkg.op
        arpPkg.source_protocol_address = format_protocol_address(pkg.spa, pkg.pro)
        arpPkg.source_hardware_address = format_hardware_address(pkg.sha, pkg.hrd)
        arpPkg.destination_protocol_address = format_protocol_address(pkg.tpa, pkg.pro)
        arpPkg.destination_hardware_address = format_hardware_address(pkg.tha, pkg.hrd)

        arpPkg.sourceIp = arpPkg.source_protocol_address
        arpPkg.destinationIp = arpPkg.destination_protocol_address

        return arpPkg


class IPPacket(Packet):
    '''
    Classe para encapsular dpkt.ip.IP e printar
    certinho na fastAPI
    '''
    version: int
    headerLength: int
    length: int
    sourceIp: str
    destinationIp: str
    ttl: int
    protocol: str

    fragmentationId: int
    flagDontFragment: bool
    flagMoreFragments: bool
    offset: int

    headerChecksum: int
    service: int

    def convert(ip: dpkt.ip.IP) -> list['IPPacket', Any]:
        packet = IPPacket()
        packet.version = 4
        packet.version = ip.v
        packet.headerLength = ip.hl
        packet.length = ip.len
        packet.sourceIp = f'{ip.src[0]}.{ip.src[1]}.{ip.src[2]}.{ip.src[3]}'
        packet.destinationIp = f'{ip.dst[0]}.{ip.dst[1]}.{ip.dst[2]}.{ip.dst[3]}'
        packet.ttl = ip.ttl
        packet.fragmentationId = ip.id
        packet.flagMoreFragments = bool(ip.mf)
        packet.flagDontFragment = bool(ip.df)
        packet.offset = ip.offset * 8

        packet.headerChecksum = ip.sum
        packet.service = ip.tos

        if ip.p == 6:
            packet.protocol = 'TCP'
        elif ip.p == 17:
            packet.protocol = 'UDP'
        elif ip.p == 1:
            packet.protocol = 'ICMP'
        else:
            packet.protocol = 'UNKN (' + str(ip.p) + ')'

        data = Packet.convert(ip.data)

        if data is not None:
            if type(data) == list:
                packet.payload = data[0].uniqueId
                packet.setInternalPDU(data[0])
                data[0].setExternalPDU(packet)
                return [packet, *data]
            else:
                packet.payload = data.uniqueId
                packet.setInternalPDU(data)
                data.setExternalPDU(packet)
                return [packet, data]


        else:
            return [packet]


class IP6Packet(Packet):
    version: int
    sourceIp: int
    sourceIp: int
    payloadLength: int
    nextHeader: int
    hopLimit: int
    flow: int
    fc: int  # flow control? nao sei oq é

    def convert(ip: dpkt.ip6.IP6) -> 'IP6Packet' | List[Packet]:
        packet = IP6Packet()
        packet.version = 6

        packet.sourceIp = socket.inet_ntop(socket.AF_INET6, ip.src)
        packet.destinationIp = socket.inet_ntop(socket.AF_INET6, ip.dst)
        packet.payloadLength = ip.plen
        packet.nextHeader = ip.nxt
        packet.hopLimit = ip.hlim
        packet.flow = ip.flow
        packet.fc = ip.fc

        data = None
        data = Packet.convert(ip.data)

        if data is not None:
            if type(data) == list:
                packet.payload = data[0].uniqueId
                packet.setInternalPDU(data[0])
                data[0].setExternalPDU(packet)
                return [packet, *data]
            else:
                packet.payload = data.uniqueId
                packet.setInternalPDU(data)
                data.setExternalPDU(packet)
                return [packet, data]

        return packet


class RIPPacket(Packet):
    command: int
    metrics: List[Dict[str, Any]] = list()

    def convert(rip: dpkt.rip.RIP) -> 'RIPPacket':
        pkt = RIPPacket()

        rip = dpkt.rip.RIP(rip)

        pkt.command = rip.cmd

        for item in rip.rtes:
            pkt.metrics.append(
                {"address": int_to_ip4(item.addr),
                 "mask": int_to_ip4(item.subnet),
                 "metric": item.metric,
                 "nextHop": item.next_hop}
            )

        return pkt


class UDPPacket(Packet):
    '''
    Classe para encapsular dpkt.udp.UDP e printar
    certinho na fastAPI
    '''

    srcIp: str
    srcPort: int
    dstPort: int
    length: int
    checksum: int

    def convert(pkt: dpkt.udp.UDP) -> 'UDPPacket' | List[Packet]:
        packet = UDPPacket()

        packet.dstPort = pkt.dport
        packet.srcPort = pkt.sport
        packet.length = pkt.ulen
        packet.checksum = pkt.sum

        # Não funcionando, UDP pode identificar o protocolo superior por Porta
        # data = Packet.convert(pkt.data)
        # Seria legal se existisse switch em python

        data: Packet | List[Packet] | None = None
        if packet.dstPort == 520:
            data = RIPPacket.convert(pkt.data)

        if data is not None:
            if type(data) == list:
                packet.payload = data[0].uniqueId
                packet.setInternalPDU(data[0])
                data[0].setExternalPDU(packet)
                return [packet, *data]
            else:
                packet.payload = data.uniqueId
                packet.setInternalPDU(data)
                data.setExternalPDU(packet)
                return [packet, data]

        return packet


class PacketSource:
    '''
    Classe que junta logica de captura e leitura de pacotes.
    Usado para prevenir que cada pacote tenha uuids diferentes
    a cada request.
    '''

    packetData: Dict[uuid.UUID, dpkt.Packet]
    '''Dicionario com o conteudo de cada pacote'''
    allPackets: List[Packet]
    '''Lista com todos os pacotes disponiveis(IP e ARP)'''

    '''Alternativa para evitar iterar sobre todos os pacotes em consultas e 
    para lidar melhtos com pacotes aninhados. ex.: IP(UDP(RIP))'''
    allPacketsDict: Dict[type, List[Packet]]

    def readPackets(self, filePath: str) -> list:
        '''
        Le um arquivo pcap e retorna uma lista de pacotes IP
        '''
        f = open(filePath, 'rb')
        pcap = None
        if filePath.endswith('.pcap'):
            pcap = dpkt.pcap.Reader(f)
        elif filePath.endswith('.pcapng'):
            pcap = dpkt.pcapng.Reader(f)
        else:
            print("Arquivo nao suportado: " + filePath)
            return []

        # pcap = dpkt.pcap.Reader(f)
        packets = []
        if pcap is None:
            print("Nao consegui ler o arquivo " + filePath + "!")
            return []
        for ts, buf in pcap:
            eth = dpkt.ethernet.Ethernet(buf)
            if eth.type == ETH_TYPE_IPv4 or eth.type == ETH_TYPE_IPv6:
                ip = eth.data
                packets.append(ip)
            elif eth.type == ETH_TYPE_ARP:
                arp = eth.data
                packets.append(arp)
            else:
                print("Ethernet type não tratado.")

        f.close()
        return packets

    def readAll(self) -> Tuple[List[Packet], Dict[type, List[Packet]]]:
        '''
        Le todos os pcap da pasta captures e retorna uma lista de pacotes IP
        '''

        arquivos = os.listdir('./pcaps')
        output = []
        outputDict: Dict[type, List[Packet]] = {}
        for arquivo in arquivos:
            print("Lendo arquivo: ", arquivo)
            packets = self.readPackets(f'./pcaps/{arquivo}')
            for packet in packets:
                pkt: Packet | List[Packet] = Packet.convert(packet)
                if pkt is None:
                    # print("um pacote nao foi convertido")
                    continue

                if type(pkt) != list:
                    # Esta condição não deve ocorrer,
                    # uniqueUuid está sendo definido na inicialização do objeto
                    if pkt.uniqueId is None:
                        pkt.uniqueId = uuid.uuid4()
                    self.packetData[pkt.uniqueId] = packet.data
                    output.append(pkt)

                    if outputDict.get(pkt.__class__) is None:
                        outputDict[pkt.__class__] = []
                    outputDict[pkt.__class__].append(pkt)
                elif type(pkt) == list:
                    appendPackets(outputDict, pkt)
                    for pkt_unit in pkt:
                        self.packetData[pkt_unit.uniqueId] = packet.data
                        output.append(pkt_unit)

        print("li um total de", len(output), "pacotes")
        return output, outputDict

    def __init__(self):
        self.packetData = {}
        self.allPackets, self.allPacketsDict = self.readAll()


packetSource = PacketSource()

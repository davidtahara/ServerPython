from scapy.all import *
from Modules.pedro_alan_rodrigo_henrique.routers.RipSniffer.PcapReader import PcapReader
import os

current_dir = os.path.dirname(os.path.abspath(__file__))


class RipSniffer:
    def __init__(self):
        pcapReader = PcapReader(current_dir + "/rip_backup.pcap")
        self.packets = pcapReader.get_content()

    def get_data(self):
        data = []
        for packet in self.packets:
            packet_data = {
                "srcIp": packet[IP].src,
                "dstIp": packet[IP].dst,
                "srcPort": packet[UDP].sport,
                "dstPort": packet[UDP].dport,
                "ripAddress": packet[RIP].addr,
                "ripMask": packet[RIP].mask,
                "ripNextHop": packet[RIP].nextHop,
            }
            data.append(packet_data)

        return data

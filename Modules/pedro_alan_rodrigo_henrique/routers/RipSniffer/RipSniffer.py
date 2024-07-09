from scapy.all import *
from Modules.pedro_alan_rodrigo_henrique.routers.RipSniffer.PcapReader import PcapReader
import os

current_dir = os.path.dirname(os.path.abspath(__file__))


def mask_to_cidr(mask):
    octets = mask.split(".")
    binary_str = "".join(format(int(octet), "08b") for octet in octets)
    cidr = binary_str.count("1")
    return f"/{cidr}"


class RipSniffer:
    def __init__(self):
        pcapReader = PcapReader(current_dir + "/rip_backup.pcap")
        self.packets = pcapReader.get_content()

    def get_data(self):
        ripNetCount = {}
        ripNetCount2 = {}
        routeTag = ""
        cmd = ""
        version = ""
        for packet in self.packets:
            packet_data = {
                "srcIp": packet[IP].src,
                "routeTag": packet[RIP].RouteTag,
                "cmd": packet[RIP].cmd,
                "version": packet[RIP].version,
                "ripNetwork": f"{packet[RIP].addr}{mask_to_cidr(packet[RIP].mask)}",
            }
            print(packet_data)
            # Os seguintes dados são constantes para todos pacotes
            routeTag = packet_data["routeTag"]
            cmd = packet_data["cmd"]
            version = packet_data["version"]

            ripNet = packet_data["ripNetwork"]
            if packet_data["srcIp"] == "10.0.0.1":
                ripNetCount[ripNet] = ripNetCount.get(ripNet, 0) + 1

            else:
                ripNetCount2[ripNet] = ripNetCount2.get(ripNet, 0) + 1
        return {
            "router1Data": ripNetCount,
            "router2Data": ripNetCount2,
            "routeTag": routeTag,
            "cmd": cmd,
            "version": version,
        }

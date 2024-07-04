from scapy.all import *
from Modules.pedro_alan_rodrigo_henrique.routers.PcapReader.PcapReader import PcapReader
import os

current_dir = os.path.dirname(os.path.abspath(__file__))
common_ports = {
    "20": "ftp-data",
    "21": "ftp",
    "22": "ssh",
    "23": "telnet",
    "25": "smtp",
    "53": "dns",
    "67": "dhcp",
    "68": "dhcp",
    "69": "tftp",
    "80": "http",
    "110": "pop3",
    "119": "nntp",
    "123": "ntp",
    "143": "imap",
    "161": "snmp",
    "194": "irc",
    "443": "https",
    "445": "microsoft-ds",
    "465": "smtps",
    "514": "syslog",
    "587": "submission",
    "993": "imaps",
    "995": "pop3s",
    "1080": "socks",
    "1433": "ms-sql-s",
    "1434": "ms-sql-m",
    "3306": "mysql",
    "3389": "rdp",
    "5432": "postgresql",
    "5900": "vnc",
    "6379": "redis",
    "8080": "http-alt",
    "8443": "https-alt",
    "27017": "mongodb",
}


class T4Udp:
    def __init__(self):
        pcapReader = PcapReader(current_dir + "/udp.pcap")
        print("Carregando pcap UDP...")
        self.packets = pcapReader.get_content()
        print("Pcap UDP carregado!")

    def get_data(self, slice_start, slice_end):
        if (
            slice_start < 0
            or slice_end < 0
            or slice_start > slice_end
            or slice_end > len(self.packets) - 1
        ):
            print("Value out of range")
            return
        data = []
        dst_port_freq = {}
        application_freq = {}
        for packet in self.packets[slice(slice_start, slice_end)]:
            try:
                if UDP in packet:
                    udp_layer = packet[UDP]
                    print(packet)
                    packet_data = {
                        "srcPort": udp_layer.sport,
                        "dstPort": udp_layer.dport,
                    }
                    dst_port_freq[packet_data["dstPort"]] = (
                        dst_port_freq.get(packet_data["dstPort"], 0) + 1
                    )
                    port = str(packet_data["dstPort"])
                    application_freq[common_ports[port]] = (
                        application_freq.get(common_ports[port], 0) + 1
                    )
                    data.append(packet_data)
            except Exception as e:
                print(f"Error processing packet: {e}")

        outputDict = {
            "dstPortFrequency": dst_port_freq,
            "applicationFrequency": application_freq,
        }
        return outputDict

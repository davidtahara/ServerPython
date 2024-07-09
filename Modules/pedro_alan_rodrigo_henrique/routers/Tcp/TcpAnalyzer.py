from scapy.all import *
from Modules.pedro_alan_rodrigo_henrique.routers.PcapReader.PcapReader import PcapReader
import os

current_dir = os.path.dirname(os.path.abspath(__file__))


class TcpAnalyzer:
    def __init__(self):
        pcapReader = PcapReader(current_dir + "/tcp.pcap")
        print("Carregando pcap TCP...")
        self.packets = pcapReader.get_content()
        print("Pcap TCP carregado!")

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
        flagFrequency = {}
        window_size = {}
        packet_error = 0
        for packet in self.packets[slice(slice_start, slice_end)]:
            try:
                if TCP in packet:
                    tcp_layer = packet[TCP]
                    calculated_checksum, packet_checksum = self.__verify_tcp_checksum(
                        packet
                    )
                    packet_data = {
                        "srcPort": tcp_layer.sport,
                        "dstPort": tcp_layer.dport,
                        "seq": tcp_layer.seq,
                        "ack": tcp_layer.ack,
                        "dataOffset": str(tcp_layer.dataofs),
                        "reserved": str(tcp_layer.reserved),
                        "flags": {
                            "urg": str(tcp_layer.flags & 32),
                            "ack": str(tcp_layer.flags & 16),
                            "psh": str(tcp_layer.flags & 8),
                            "rst": str(tcp_layer.flags & 4),
                            "syn": str(tcp_layer.flags & 2),
                            "fin": str(tcp_layer.flags & 1),
                        },
                        "window": str(tcp_layer.window),
                        "checksum": str(tcp_layer.chksum),
                        "calculated_checksum": calculated_checksum,
                        "checksum_match": calculated_checksum == packet_checksum,
                    }
                    window_size[packet_data["window"]] = (
                        window_size.get(packet_data["window"], 0) + 1
                    )
                    if not packet_data["checksum_match"]:
                        packet_error += 1
                    if packet_data["flags"]["urg"]:
                        flagFrequency["urg"] = flagFrequency.get("urg", 0) + 1
                    if packet_data["flags"]["ack"]:
                        flagFrequency["ack"] = flagFrequency.get("ack", 0) + 1
                    if packet_data["flags"]["psh"]:
                        flagFrequency["psh"] = flagFrequency.get("psh", 0) + 1
                    if packet_data["flags"]["rst"]:
                        flagFrequency["rst"] = flagFrequency.get("rst", 0) + 1
                    if packet_data["flags"]["syn"]:
                        flagFrequency["syn"] = flagFrequency.get("syn", 0) + 1
                    if packet_data["flags"]["fin"]:
                        flagFrequency["fin"] = flagFrequency.get("fin", 0) + 1
                    data.append(packet_data)
            except Exception as e:
                print(f"Error processing packet: {e}")

        outputDict = {
            "flagFrequency": flagFrequency,
            "windowSize": dict(
                sorted(window_size.items(), key=lambda x: x[1], reverse=True)[:5]
            ),
            "packetError": {"count": packet_error},
        }
        return outputDict

    def __calculate_checksum(self, data):
        if len(data) % 2 == 1:
            data += b"\x00"
        checksum = 0
        for i in range(0, len(data), 2):
            word = (data[i] << 8) + data[i + 1]
            checksum += word
            while checksum >> 16:
                checksum = (checksum & 0xFFFF) + (checksum >> 16)
        checksum = ~checksum & 0xFFFF
        return checksum

    def __verify_tcp_checksum(self, packet):
        ip_layer = packet[IP]
        tcp_layer = packet[TCP]
        src_ip = inet_aton(ip_layer.src)
        dst_ip = inet_aton(ip_layer.dst)
        tcp_header = raw(tcp_layer)[: tcp_layer.dataofs * 4]
        tcp_payload = raw(tcp_layer.payload)
        tcp_header = tcp_header[:16] + b"\x00\x00" + tcp_header[18:]
        pseudo_header = struct.pack(
            "!4s4sBBH", src_ip, dst_ip, 0, 6, len(tcp_header) + len(tcp_payload)
        )
        data = pseudo_header + tcp_header + tcp_payload
        calculated_checksum = self.__calculate_checksum(data)
        packet_checksum = tcp_layer.chksum
        return calculated_checksum, packet_checksum

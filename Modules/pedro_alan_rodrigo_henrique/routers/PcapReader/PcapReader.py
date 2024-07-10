from scapy.all import rdpcap
from scapy.layers.inet import IP, UDP


class PcapReader:
    def __init__(self, file_path):
        self.file_path = file_path
        self.packets = None

    def __read_pcap(self):
        try:
            self.packets = rdpcap(self.file_path)
            return True
        except Exception as e:
            print("Error reading pcap file:", e)
            return False

    def get_content(self):
        if self.packets is None:
            if not self.__read_pcap():
                return None
        return self.packets

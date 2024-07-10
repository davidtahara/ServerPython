from scapy.all import *
from Modules.pedro_alan_rodrigo_henrique.routers.PcapReader.PcapReader import PcapReader
import os

current_dir = os.path.dirname(os.path.abspath(__file__))


class T8Snmp:
    def __init__(self):
        pcapReader = PcapReader(current_dir + "/snmp.pcap")
        print("Carregando pcap HTTP...")
        self.packets = pcapReader.get_content()
        print("Pcap HTTP carregado!")

    def insert_into_tree(self, tree, oid):
        parts = oid.split(".")
        current = tree
        for part in parts:
            if part not in current:
                current[part] = {}
            current = current[part]

    def simplify_tree(self, tree, prefix=""):
        if not isinstance(tree, dict) or len(tree) == 0:
            return {}

        keys = list(tree.keys())
        if len(keys) == 1:
            only_key = keys[0]
            new_prefix = f"{prefix}.{only_key}" if prefix else only_key
            return self.simplify_tree(tree[only_key], new_prefix)

        result = {}
        for key in keys:
            full_key = f"{prefix}.{key}" if prefix else key
            result[full_key] = self.simplify_tree(tree[key], full_key)
        return result

    def get_data(self):
        varbindTree = {}

        for packet in self.packets:
            if packet.haslayer(SNMP):
                snmp_layer = packet[SNMP]

                for varbind in snmp_layer.PDU.varbindlist:
                    oid = varbind.oid.val
                    self.insert_into_tree(varbindTree, oid)

        varbindTree = self.simplify_tree(varbindTree)

        outputDict = {
            "varbindTree": varbindTree,
        }
        return outputDict


# Example of how to use the class
if __name__ == "__main__":
    snmp_parser = T8Snmp()
    data = snmp_parser.get_data()
    print(data)

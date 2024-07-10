import json
from scapy.all import rdpcap
from collections import defaultdict

def extract_topology(pcap_file):
    packets = rdpcap(pcap_file)

    topology = defaultdict(list)

    for pkt in packets:
        if pkt.haslayer('IP'):
            src_ip = pkt['IP'].src
            dst_ip = pkt['IP'].dst

            if src_ip not in topology[dst_ip]:
                topology[src_ip].append(dst_ip)
            if dst_ip not in topology[src_ip]:
                topology[dst_ip].append(src_ip)

    return topology

def save_topology_as_json(topology, json_file):
    with open(json_file, 'w') as f:
        json.dump(topology, f, indent=4)

if __name__ == "__main__":
    pcap_file = "trab3.pcap"
    topology = extract_topology(pcap_file)
    json_file = "topology.json"
    save_topology_as_json(topology, json_file)
    print(f"Topologia salva em {json_file}")
import json
import ipaddress
from scapy.all import *

def is_public_ip(ip):
    return not ipaddress.ip_address(ip).is_private

def obter_bytes_por_ip(file_path):
    packets = rdpcap(file_path)

    bytes_por_ip = {}
    for pkt in packets:
        if IP in pkt:
            ip_src = pkt[IP].src
            ip_dst = pkt[IP].dst
            
            if ip_src in bytes_por_ip:
                bytes_por_ip[ip_src]["bytes"] += len(pkt)
            else:
                bytes_por_ip[ip_src] = {"bytes": len(pkt), "public": is_public_ip(ip_src)}

            if ip_dst in bytes_por_ip:
                bytes_por_ip[ip_dst]["bytes"] += len(pkt)
            else:
                bytes_por_ip[ip_dst] = {"bytes": len(pkt), "public": is_public_ip(ip_dst)}

    bytes_por_ip = dict(sorted(bytes_por_ip.items(), key=lambda item: item[1]["bytes"], reverse=True))

    with open("../views/trab1.json", "w") as json_file:
        json.dump(bytes_por_ip, json_file, indent=4)

obter_bytes_por_ip("../../pcaps/trabalho1.pcapng")

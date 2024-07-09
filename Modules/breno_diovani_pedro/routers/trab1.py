import json
import ipaddress
from scapy.all import *
from fastapi import APIRouter

router = APIRouter(prefix="/trabalho1", tags=[""])

def is_public_ip(ip):
    return not ipaddress.ip_address(ip).is_private

@router.get("/trabalho1")
def obter_bytes_por_ip():
    file_path = "./pcaps/trabalho1.pcapng"
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

    with open("./Modules/diovani_breno_pedro/views/trab1.json", "w") as json_file:
        json.dump(bytes_por_ip, json_file, indent=4)

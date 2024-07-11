from typing import List
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import json
from datetime import datetime
import threading
import statistics
from scapy.all import sniff, IP, TCP  
packets_info = []

def capture_ipv4_packets():
    with open('ip.json') as file:
        data = json.load(file)
    public_ips = [ip for ip, details in data.items() if details['public']]

    def packet_callback(packet):
        if IP in packet and packet[IP].src in public_ips:
            packet_info = {
                "timestamp": datetime.now(),
                "packet_size": len(packet),
                "src_ip": packet[IP].src,
                "dst_ip": packet[IP].dst,
                "protocol": packet[IP].proto,
                "src_port": packet[TCP].sport if TCP in packet else None,
                "dst_port": packet[TCP].dport if TCP in packet else None,
                "payload_size": len(packet[IP].payload),
                "tcp_flags": packet[TCP].flags if TCP in packet else None,
                "ttl": packet[IP].ttl
            }
            packets_info.append(packet_info)
            print(f"Captured IPv4 packet of size {packet_info['packet_size']} bytes from {packet_info['src_ip']} to {packet_info['dst_ip']} at {packet_info['timestamp']}")

    sniff(filter="ip", prn=packet_callback, store=False)

threading.Thread(target=capture_ipv4_packets, daemon=True).start()

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/packets-sizes")
def get_packet_sizes():
    return packets_info

app.get("/packets-sizes-variation")   # Rota para obeter os tamanhos do pacote e suas variações
def get_packet_size_variation():
    if len(packets_info) == 0:
        return {"error": "No packets captured yet"}
    sizes = [info["packet_size"] for info in packets_info]
    average = sum(sizes) / len(sizes)
    median = statistics.median(sizes)
    return {
        "max": max(sizes),
        "min": min(sizes),
        "average": average,
        "median": median,
        "std_deviation": statistics.stdev(sizes) if len(sizes) > 1 else 0
    }

@app.get("/packets-sizes-time-range")     # Rota para  obter os tamanhos do pacote em um intervalo de tempo 
def get_packet_sizes_time_range(start: str, end: str):
    start_datetime = datetime.fromisoformat(start)
    end_datetime = datetime.fromisoformat(end)
    filtered_packets = [p for p in packets_info if start_datetime <= p["timestamp"] <= end_datetime]
    if not filtered_packets:
        return {"error": "No packets found in the specified time range"}
    sizes = [info["packet_size"] for info in filtered_packets]
    return {
        "max": max(sizes),
        "min": min(sizes),
        "average": sum(sizes) / len(sizes)
    }

# este endpoint Calcula o tamanho máximo e mínimo dos pacotes capturados.
#Determina a média dos tamanhos dos pacotes.
#Calcula a diferença entre os tamanhos máximos e mínimos dos pacotes.
#Conta quantos pacotes têm tamanhos acima e abaixo da média.
#Calcula a porcentagem de pacotes que estão acima e abaixo da média dos tamanhos.

@app.get("/packets-sizes-comparasion")
def get_packet_sizes_comparasion():
    if len(packets_info) == 0:
        return {"error": "No packets captured yet"}
    sizes = [info["packet_size"] for info in packets_info]
    average = sum(sizes) / len(sizes)
    max_size = max(sizes)
    min_size = min(sizes)
    above_average = [size for size in sizes if size > average]
    below_average = [size for size in sizes if size < average]
    return {
        "max_size": max_size,
        "min_size": min_size,
        "average_size": average,
        "difference_max_min": max_size - min_size,
        "count_above_average": len(above_average),
        "count_below_average": len(below_average),
        "percentage_above_average": (len(above_average) / len(sizes)) * 100,
        "percentage_below_average": (len(below_average) / len(sizes)) * 100
    }
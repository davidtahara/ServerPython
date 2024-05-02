from fastapi import FastAPI, File, UploadFile
from typing import List
from scapy.all import ARP, rdpcap
import requests

app = FastAPI()

def get_mac_address_vendor(mac_address):
    url = f"https://api.macvendors.com/{mac_address}"
    response = requests.get(url)
    if response.status_code == 200:
        return response.text.strip()
    else:
        return "Unknown"

def analyze_arp_packets(pcap_file):
    try:
        packets = rdpcap(pcap_file)
        mac_addresses = set()
        for packet in packets:
            if ARP in packet:
                mac_addresses.add(packet[ARP].hwsrc)
        
        mac_vendor_details = {}
        for mac_address in mac_addresses:
            vendor = get_mac_address_vendor(mac_address)
            mac_vendor_details[mac_address] = vendor
        
        return mac_vendor_details
    except Exception as e:
        print(f"An error occurred while analyzing ARP packets: {e}")
        return None

@app.post("/analyze-pcap/")
async def analyze_pcap(files: List[bytes] = File(...)):
    try:
        pcap_data = files[0]
        with open("temp.pcap", "wb") as pcap_file:
            pcap_file.write(pcap_data)
        
        result = analyze_arp_packets("temp.pcap")
        return result
    except Exception as e:
        return {"error": str(e)}

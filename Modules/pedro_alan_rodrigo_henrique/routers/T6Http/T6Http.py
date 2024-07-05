from scapy.all import *
from Modules.pedro_alan_rodrigo_henrique.routers.PcapReader.PcapReader import PcapReader
import os

from scapy.layers.http import HTTPRequest, HTTPResponse, _HTTPContent, _HTTPHeaderField

current_dir = os.path.dirname(os.path.abspath(__file__))


class T6Http:
    def __init__(self):
        pcapReader = PcapReader(current_dir + "/http.pcap")
        print("Carregando pcap HTTP...")
        self.packets = pcapReader.get_content()
        print("Pcap HTTP carregado!")

    def get_data(self):
        method_freq = {}
        status_code_freq = {}
        host_freq = {}

        for packet in self.packets:
            try:
                if packet.haslayer(HTTPRequest):
                    http_layer = packet[HTTPRequest]
                    method = http_layer.Method.decode()
                    host = http_layer.Host.decode() if http_layer.Host else None
                    path = http_layer.Path.decode() if http_layer.Path else None
                    method_freq[method] = method_freq.get(method, 0) + 1
                    if host:
                        host_freq[host] = host_freq.get(host, 0) + 1
                elif packet.haslayer(HTTPResponse):
                    http_layer = packet[HTTPResponse]
                    status_code = http_layer.Status_Code.decode()
                    reason_phrase = (
                        http_layer.Reason_Phrase.decode()
                        if http_layer.Reason_Phrase
                        else None
                    )
                    status_code_freq[status_code] = (
                        status_code_freq.get(status_code, 0) + 1
                    )

            except Exception as e:
                print(f"Error processing packet: {e}")

        outputDict = {
            "methodFrequency": method_freq,
            "statusCodeFrequency": status_code_freq,
            "hostFrequency": host_freq,
        }
        return outputDict

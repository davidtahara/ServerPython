from typing import List, Dict
import json

class UDPService:
    description: str
    isUdp: bool
    istTcp: bool
    isOfficial: bool
    port: int

loaded: bool = False
services: Dict[int, List[UDPService]] = {}

def loadServices():
    with open("Modules/rodrigo_thierry_joaovitor/ports.lists.json", encoding="utf8") as f:
        obj = json.load(f)
        for port in obj:
            services[int(port)] = []
            for service in obj[port]:
                s = UDPService()
                s.description = service["description"]
                s.isUdp = service["udp"]
                s.istTcp = service["tcp"]
                s.isOfficial = True if service["status"] == "Official" else False
                s.port = port
                services[int(port)].append(s)

def findService(port: int) -> List[UDPService]:
    if not loaded:
        loadServices()

    if port in services:
        return services[port]
    else:
        return []

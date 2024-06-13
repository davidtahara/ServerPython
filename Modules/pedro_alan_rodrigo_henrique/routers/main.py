import os
import sys
from Modules.pedro_alan_rodrigo_henrique.routers.PacketSniffer.PacketSniffer import (
    PacketSniffer,
)
from Modules.pedro_alan_rodrigo_henrique.routers.ArpDiscovery.ArpDiscovery import (
    ArpDiscovery,
)
from Modules.pedro_alan_rodrigo_henrique.routers.RipSniffer.RipSniffer import (
    RipSniffer,
)
from Modules.pedro_alan_rodrigo_henrique.routers.UdpDns.UdpDns import (
    UdpDns,
)

from fastapi import APIRouter


router = APIRouter(prefix="/grupo_pedro_alan_rodrigo_henrique/ip", tags=[""])

packet_sniffer = PacketSniffer()
rip_sniffer = RipSniffer()
arp_discovery = ArpDiscovery("172.21.0.1/28")
udp_dns = UdpDns()


@router.get("/sniffer-reports")
def get_sniffer_reports():
    return packet_sniffer.get_reports(5)


@router.post("/sniffer-start")
def start_sniffer():
    packet_sniffer.start()
    return {"status": "started"}


@router.post("/sniffer-stop")
def start_sniffer():
    packet_sniffer.stop()
    return {"status": "started"}


@router.post("/arp-start")
def start_arp():
    arp_discovery.start()
    return {"status": "started"}


@router.post("/arp-set-network/{network}/{mask}")
def set_arp_network(network: str, mask: str):
    arp_discovery.set_network(network + "/" + mask)
    return


@router.get("/arp-devices")
def get_arp_devices():
    if arp_discovery.finished:
        return {"finished": True}
    return arp_discovery.get_devices()


@router.get("/rip-data")
def get_rip_data():
    return rip_sniffer.get_data()


@router.post("/dns-start")
def start_dns():
    udp_dns.start()
    return {"status": "started"}


@router.post("/dns-stop")
def stop_dns():
    udp_dns.stop()
    return {"status": "stopped"}


@router.get("/dns-data")
def get_dns_data():
    return udp_dns.get_dns_results()

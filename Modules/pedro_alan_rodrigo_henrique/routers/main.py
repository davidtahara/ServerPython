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
from Modules.pedro_alan_rodrigo_henrique.routers.Tcp.TcpAnalyzer import TcpAnalyzer
from Modules.pedro_alan_rodrigo_henrique.routers.T4Udp.T4Udp import T4Udp
from Modules.pedro_alan_rodrigo_henrique.routers.T6Http.T6Http import T6Http
from Modules.pedro_alan_rodrigo_henrique.routers.T8Snmp.T8Snmp import T8Snmp
from typing import Dict
from fastapi import APIRouter, Query


router = APIRouter(prefix="/grupo_pedro_alan_rodrigo_henrique/ip", tags=[""])

packet_sniffer = PacketSniffer()
rip_sniffer = RipSniffer()
arp_discovery = ArpDiscovery("172.21.0.1/28")
udp_dns = UdpDns()
tcp = TcpAnalyzer()
t4_udp = T4Udp()
t6_http = T6Http()
t8_snmp = T8Snmp()


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


@router.get("/tcp-data", response_model=Dict[str, Dict[str, int]])
def get_tcp_data(
    slice_start: int = Query(..., ge=0), slice_end: int = Query(..., ge=0)
):
    return tcp.get_data(slice_start, slice_end)


@router.get("/t4-udp-data")
def get_udp_data(
    slice_start: int = Query(..., ge=0), slice_end: int = Query(..., ge=0)
):
    return t4_udp.get_data(slice_start, slice_end)


@router.get("/t6-http")
def get_http_data():
    return t6_http.get_data()


@router.get("/t8-snmp")
def get_snmp_data():
    return t8_snmp.get_data()

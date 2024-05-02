import os
import sys
from Modules.pedro_alan_rodrigo_henrique.routers.src.PacketSniffer import PacketSniffer
from fastapi import APIRouter


router = APIRouter(prefix="/grupo_pedro_alan_rodrigo_henrique/ip", tags=[""])

packet_sniffer = PacketSniffer()
packet_sniffer.start()


@router.get("/reports")
def get_reports():
    return packet_sniffer.get_reports(5)

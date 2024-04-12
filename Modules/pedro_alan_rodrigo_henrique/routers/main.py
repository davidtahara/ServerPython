import os
import sys
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from src.PacketSniffer import PacketSniffer
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware


router = FastAPI(prefix="/grupo_pedro_alan_rodrigo_henrique/ip", tags=[""])
router.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

packet_sniffer = PacketSniffer()
packet_sniffer.start()


@router.get("/reports")
def get_reports():
    return packet_sniffer.get_reports(5)

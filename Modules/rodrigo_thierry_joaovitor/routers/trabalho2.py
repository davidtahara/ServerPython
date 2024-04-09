from fastapi import APIRouter
from ...rodrigo_thierry_joaovitor.Parser import PacketSource, IPPacket, ARPPacket
#from Parser import PacketSource, IPPacket, ARPPacket
# import scapy.all as scapy

router = APIRouter(prefix="/grupo_rodrigo_thierry_joao/arp", tags=[""])

src = PacketSource()

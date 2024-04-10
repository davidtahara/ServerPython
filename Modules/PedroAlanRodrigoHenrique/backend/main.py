from typing import Union
from PacketSniffer import PacketSniffer
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(CORSMiddleware, allow_origins=["*"])
packet_sniffer = PacketSniffer()
packet_sniffer.start()


@app.get("/reports")
def get_reports():
    return packet_sniffer.get_reports(5)

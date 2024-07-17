from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
import uvicorn
import os

from t1redes.main import router as ipv4_router
from t2redes.main import router as arp_router
from t3redes.main import router as rip_router
from t4redes.main import router as udp_router
from t5redes.main import router as tcp_router
from t6redes.main import router as http_router
from t7redes.main import router as dns_router
from t8redes.main import router as snmp_router

app = FastAPI()

templates = Jinja2Templates(directory=os.path.join(os.path.dirname(__file__), 'templates'))

app.include_router(ipv4_router, prefix="/ipv4")
app.include_router(arp_router, prefix="/arp")
app.include_router(rip_router, prefix="/rip")
app.include_router(udp_router, prefix="/udp")
app.include_router(tcp_router, prefix="/tcp")
app.include_router(http_router, prefix="/http")
app.include_router(dns_router, prefix="/dns")
app.include_router(snmp_router, prefix="/snmp")

@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=3001)

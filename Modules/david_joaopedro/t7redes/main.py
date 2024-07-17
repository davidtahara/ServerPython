from fastapi import FastAPI, APIRouter
from fastapi.responses import HTMLResponse
from scapy.all import rdpcap, DNS, DNSQR
import matplotlib.pyplot as plt
import os
from collections import Counter
import io
import base64
import tldextract

router = APIRouter(tags=["dns"])

app = FastAPI()

pcap_file = os.path.join(os.path.dirname(__file__), 'dns.pcap')

def get_second_level_domain(url):
    ext = tldextract.extract(url)
    return f"{ext.domain}.{ext.suffix}"

def process_pcap(file_path):
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"Arquivo pcap '{file_path}' não encontrado.")

    pacotes = rdpcap(file_path)

    domains = []
    for packet in pacotes:
        if packet.haslayer(DNS) and packet.getlayer(DNS).qd:
            query = packet.getlayer(DNS).qd.qname.decode('utf-8')
            domains.append(get_second_level_domain(query))

    domain_counts = Counter(domains)

    total_requests = sum(domain_counts.values())
    filtered_domain_counts = {domain: count for domain, count in domain_counts.items() if (count / total_requests) * 100 >= 0.26}

    return filtered_domain_counts

@router.get("/", response_class=HTMLResponse)
async def get_dns_traffic_stats():
        domain_counts = process_pcap(pcap_file)

        labels = list(domain_counts.keys())
        sizes = list(domain_counts.values())

        fig, ax = plt.subplots()
        ax.pie(sizes, labels=labels, autopct='%1.1f%%', startangle=90, wedgeprops=dict(width=0.3))
        ax.axis('equal')

        buf = io.BytesIO()
        plt.savefig(buf, format='png')
        buf.seek(0)
        image_base64 = base64.b64encode(buf.getvalue()).decode('utf-8')
        buf.close()

        content = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <title>Estatísticas de Tráfego DNS</title>
        </head>
        <body>
            <h1>Tráfego DNS : Sites Acessados</h1>
            <div>
                <img src="data:image/png;base64,{image_base64}" />
            </div>
        </body>
        </html>
        """
        return content

app.include_router(router)
from fastapi import FastAPI, HTTPException
from fastapi.responses import HTMLResponse
from scapy.all import rdpcap, DNS, DNSQR
import uvicorn
import matplotlib.pyplot as plt
import os
from collections import Counter
import io
import base64
import tldextract

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

@app.get("/dns-traffic-stats", response_class=HTMLResponse)
async def get_dns_traffic_stats():
    try:
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
            <title>DNS Traffic Statistics</title>
        </head>
        <body>
            <h1>DNS Traffic: Sites Acessados</h1>
            <div>
                <img src="data:image/png;base64,{image_base64}" />
            </div>
        </body>
        </html>
        """
        return HTMLResponse(content=content)

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
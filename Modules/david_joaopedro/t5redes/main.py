from fastapi import FastAPI, APIRouter
from fastapi.responses import HTMLResponse
from scapy.all import rdpcap, IP, TCP
from collections import Counter
import json
import os

router = APIRouter(tags=["tcp"])

pcap_file = os.path.join(os.path.dirname(__file__), 'tcp.pcap')

if not os.path.exists(pcap_file):
    raise FileNotFoundError(f"Arquivo pcap '{pcap_file}' não encontrado.")

pacotes = rdpcap(pcap_file)

app = FastAPI()

tcp_length_counter = Counter()

for packet in pacotes:
    if IP in packet and TCP in packet:
        length = len(packet)
        tcp_length_counter[length] += 1

@router.get("/", response_class=HTMLResponse)
async def get_tcp_length_stats():
    sorted_lengths = sorted(tcp_length_counter.items(), key=lambda x: x[1], reverse=True)
    lengths = [length for length, count in sorted_lengths]
    counts = [count for length, count in sorted_lengths]

    content = """
    <!DOCTYPE html>
    <html>
    <head>
        <title>Estatísticas de Comprimento TCP</title>
        <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
    </head>
    <body>
        <h1>Distribuição de pacotes TCP por comprimento</h1>
        <div>
            <canvas id="pie-chart"></canvas>
        </div>
        <script>
            var ctx = document.getElementById('pie-chart').getContext('2d');
            var chart = new Chart(ctx, {
                type: 'pie',
                data: {
                    labels: """ + json.dumps(lengths) + """,
                    datasets: [{
                        label: 'Packet Count',
                        backgroundColor: [
                            'rgba(255, 99, 132, 0.2)',
                            'rgba(54, 162, 235, 0.2)',
                            'rgba(255, 206, 86, 0.2)',
                            'rgba(75, 192, 192, 0.2)',
                            'rgba(153, 102, 255, 0.2)',
                            'rgba(255, 159, 64, 0.2)'
                        ],
                        borderColor: [
                            'rgba(255, 99, 132, 1)',
                            'rgba(54, 162, 235, 1)',
                            'rgba(255, 206, 86, 1)',
                            'rgba(75, 192, 192, 1)',
                            'rgba(153, 102, 255, 1)',
                            'rgba(255, 159, 64, 1)'
                        ],
                        data: """ + json.dumps(counts) + """
                    }]
                },
                options: {
                    responsive: true,
                    title: {
                        display: true,
                        text: 'TCP Packet Length Distribution'
                    }
                }
            });
        </script>
    </body>
    </html>
    """
    return content

app.include_router(router)
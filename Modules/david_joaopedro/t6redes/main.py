from fastapi import FastAPI, HTTPException
from fastapi.responses import HTMLResponse
from scapy.all import rdpcap, IP, TCP
import json
import uvicorn
import os
import matplotlib.pyplot as plt

pcap_file = os.path.join(os.path.dirname(__file__), 'http_witp_jpegs.pcap')

if not os.path.exists(pcap_file):
    raise FileNotFoundError(f"Arquivo pcap '{pcap_file}' não encontrado.")

pacotes = rdpcap(pcap_file)

app = FastAPI()

relative_times = []
lengths = []

initial_time = None
for packet in pacotes:
    if IP in packet and TCP in packet:
        length = len(packet)
        time = float(packet.time)
        if initial_time is None:
            initial_time = time
        relative_time = time - initial_time
        lengths.append(length)
        relative_times.append(relative_time)

@app.get("/http-traffic-stats", response_class=HTMLResponse)
async def get_http_traffic_stats():
    relative_times_str = [str(time) for time in relative_times]
    lengths_str = lengths

    content = """
    <!DOCTYPE html>
    <html>
    <head>
        <title>HTTP Traffic Statistics</title>
        <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
    </head>
    <body>
        <h1>HTTP Traffic Length Over Time</h1>
        <div>
            <canvas id="line-chart"></canvas>
        </div>
        <script>
            var ctx = document.getElementById('line-chart').getContext('2d');
            var chart = new Chart(ctx, {
                type: 'line',
                data: {
                    labels: """ + json.dumps(relative_times_str) + """,
                    datasets: [{
                        label: 'Packet Length',
                        borderColor: 'rgba(75, 192, 192, 1)',
                        data: """ + json.dumps(lengths_str) + """
                    }]
                },
                options: {
                    responsive: true,
                    title: {
                        display: true,
                        text: 'HTTP Packet Length Over Time'
                    },
                    scales: {
                        xAxes: [{
                            type: 'linear',
                            position: 'bottom',
                            scaleLabel: {
                                display: true,
                                labelString: 'Time (s)'
                            }
                        }],
                        yAxes: [{
                            ticks: {
                                beginAtZero: true
                            },
                            scaleLabel: {
                                display: true,
                                labelString: 'Packet Length (bytes)'
                            }
                        }]
                    }
                }
            });
        </script>
    </body>
    </html>
    """
    return content

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
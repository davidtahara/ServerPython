from fastapi import FastAPI, APIRouter
from fastapi.responses import HTMLResponse
from scapy.all import rdpcap, SNMP, SNMPget, SNMPnext, SNMPresponse, SNMPset, SNMPtrapv2
from collections import Counter
import os
import json

router = APIRouter(tags=["snmp"])

pcap_file = os.path.join(os.path.dirname(__file__), 'snmp.pcap')

if not os.path.exists(pcap_file):
    raise FileNotFoundError(f"Arquivo pcap '{pcap_file}' não encontrado.")

app = FastAPI()

@router.get("/", response_class=HTMLResponse)
async def get_snmp_command_stats():
        packets = rdpcap(pcap_file)
        
        snmp_command_counter = Counter()

        for packet in packets:
            if SNMP in packet:
                snmp_pdu = packet[SNMP].PDU
                if isinstance(snmp_pdu, (SNMPget, SNMPnext, SNMPresponse, SNMPset, SNMPtrapv2)):
                    command_name = type(snmp_pdu).__name__
                    snmp_command_counter[command_name] += 1

        sorted_commands = sorted(snmp_command_counter.items(), key=lambda x: x[1], reverse=True)
        commands = [cmd for cmd, count in sorted_commands]
        counts = [count for cmd, count in sorted_commands]

        content = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <title>Frequência de comandos SNMP</title>
            <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
        </head>
        <body>
            <h1>Frequência de comandos SNMP</h1>
            <div>
                <canvas id="bar-chart"></canvas>
            </div>
            <script>
                var ctx = document.getElementById('bar-chart').getContext('2d');
                var chart = new Chart(ctx, {{
                    type: 'bar',
                    data: {{
                        labels: {json.dumps(commands)},
                        datasets: [{{
                            label: 'Command Count',
                            backgroundColor: 'rgba(75, 192, 192, 0.2)',
                            borderColor: 'rgba(75, 192, 192, 1)',
                            borderWidth: 1,
                            data: {json.dumps(counts)}
                        }}]
                    }},
                    options: {{
                        scales: {{
                            y: {{
                                beginAtZero: true
                            }}
                        }}
                    }}
                }});
            </script>
        </body>
        </html>
        """
        return content

app.include_router(router)
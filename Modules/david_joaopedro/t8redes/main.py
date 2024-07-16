from fastapi import FastAPI, HTTPException
from fastapi.responses import HTMLResponse
from scapy.all import rdpcap, SNMP, SNMPget, SNMPnext, SNMPresponse, SNMPset, SNMPtrapv2
from collections import Counter
import uvicorn
import os
import json
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

pcap_file = os.path.join(os.path.dirname(__file__), 'snmp.pcap')

if not os.path.exists(pcap_file):
    raise FileNotFoundError(f"Arquivo pcap '{pcap_file}' não encontrado.")

app = FastAPI()

@app.get("/snmp-command-stats", response_class=HTMLResponse)
async def get_snmp_command_stats():
    try:
        logger.info("Carregando pacotes do arquivo pcap")
        packets = rdpcap(pcap_file)
        
        snmp_command_counter = Counter()

        logger.info("Analisando pacotes SNMP")
        for packet in packets:
            if SNMP in packet:
                snmp_pdu = packet[SNMP].PDU
                if isinstance(snmp_pdu, (SNMPget, SNMPnext, SNMPresponse, SNMPset, SNMPtrapv2)):
                    command_name = type(snmp_pdu).__name__
                    snmp_command_counter[command_name] += 1

        sorted_commands = sorted(snmp_command_counter.items(), key=lambda x: x[1], reverse=True)
        commands = [cmd for cmd, count in sorted_commands]
        counts = [count for cmd, count in sorted_commands]

        logger.info("Gerando conteúdo HTML para visualização")
        content = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <title>SNMP Command Frequency</title>
            <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
        </head>
        <body>
            <h1>SNMP Command Frequency</h1>
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
        return HTMLResponse(content=content)
    except FileNotFoundError:
        logger.error("Arquivo pcap não encontrado")
        raise HTTPException(status_code=404, detail="Arquivo pcap não encontrado.")
    except Exception as e:
        logger.error(f"Erro ao processar arquivo pcap: {e}")
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
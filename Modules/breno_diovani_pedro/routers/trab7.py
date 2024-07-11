import pyshark
import json
from collections import Counter

# Carrega o arquivo .pcap
cap = pyshark.FileCapture('dns.pcap', display_filter='dns')

# Contador para armazenar as contagens de domínios
domain_counter = Counter()

# Itera sobre os pacotes e extrai os domínios das consultas DNS
for packet in cap:
    if hasattr(packet.dns, 'qry_name'):
        domain = packet.dns.qry_name
        domain_counter[str(domain)] += 1

# Obtém os 30 domínios mais consultados
most_common_domains = domain_counter.most_common(50)

# Converte para um formato apropriado para JSON
domains_data = [{'domain': domain, 'count': count} for domain, count in most_common_domains]

# Salva em um arquivo JSON
with open('trab7.json', 'w') as json_file:
    json.dump(domains_data, json_file, indent=4)

print("Dados salvos em no .json")

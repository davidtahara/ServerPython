from scapy.all import *
import json

def contar_flags_tcp(pcap_file):
    # Dicionário para contar as flags
    flags_count = {
        'SYN': 0,
        'FIN': 0,
        'ACK': 0,
        'PSH': 0,
        'URG': 0,
        'RST': 0
    }

    # Abrir o arquivo PCAP e iterar pelos pacotes
    packets = rdpcap(pcap_file)
    for pkt in packets:
        # Verificar se é um pacote TCP
        if TCP in pkt:
            # Verificar e contar as flags TCP
            if pkt[TCP].flags & 0x02:  # SYN flag
                flags_count['SYN'] += 1
            if pkt[TCP].flags & 0x01:  # FIN flag
                flags_count['FIN'] += 1
            if pkt[TCP].flags & 0x10:  # ACK flag
                flags_count['ACK'] += 1
            if pkt[TCP].flags & 0x08:  # PSH flag
                flags_count['PSH'] += 1
            if pkt[TCP].flags & 0x20:  # URG flag
                flags_count['URG'] += 1
            if pkt[TCP].flags & 0x04:  # RST flag
                flags_count['RST'] += 1

    return flags_count

# Exemplo de uso
if __name__ == '__main__':
    pcap_file = 'tcp.pcap'  # Substitua com o caminho para o seu arquivo PCAP
    flags_count = contar_flags_tcp(pcap_file)
    print("Quantidade de cada flag TCP:", flags_count)

    # Salvar dados em um arquivo JSON
    with open('flags_count.json', 'w') as json_file:
        json.dump(flags_count, json_file, indent=4)

    print("Dados salvos em flags_count.json.")

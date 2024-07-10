import json
from collections import Counter

def identificar_marcas_placas(arquivo):
    #importando a biblioteca pyshark
    import pyshark

    # Dicionário para mapear códigos OUI para marcas de placa de rede
    oui_to_brand = {
        '00:1C:14': 'Cisco',
        '9C:14:63': 'Zhejiang Dahua Technology Co., Ltd.',
        'E0:50:8B': 'Zhejiang Dahua Technology Co., Ltd.',
        '38:AF:29': 'Zhejiang Dahua Technology Co., Ltd.',
        '44:DF:65': 'Beijing Xiaomi Mobile Software Co., Ltd',
        '24:18:C6': 'HUNAN FN-LINK TECHNOLOGY LIMITED',
        '14:A7:8B': 'Zhejiang Dahua Technology Co., Ltd.',
        '80:19:34': 'Intel Corporate',
        '5C:D9:98': 'D-Link Corporation',
        '60:AB:67': 'Xiaomi Communications Co Ltd',
        '54:EF:44': 'Lumi United Technology Co., Ltd',
        'DA:A9:53': 'Technicolor CH USA Inc.',
        
        # Adicione mais mapeamentos conforme necessário
    }

    # Função para obter a marca da placa de rede com base no endereço MAC
    def get_mac_vendor(mac_address):
        # Obter os 6 primeiros caracteres do endereço MAC
        oui = mac_address[:8].upper()
        # Verificar se o OUI está mapeado em oui_to_brand, se não, retornar o próprio OUI
        return oui_to_brand.get(oui, oui)

    # Dicionário para armazenar a contagem de endereços MAC por marca de placa de rede
    mac_counts = {}

    # Conjunto para armazenar marcas de placa de rede não mapeadas
    unmapped_brands = set()

    # Analisar o arquivo pcap
    cap = pyshark.FileCapture(arquivo)
    for pkt in cap:
        if 'ARP' in pkt:
            mac_address = pkt.arp.src_hw_mac
            mac_vendor = get_mac_vendor(mac_address)
            if mac_vendor in mac_counts:
                mac_counts[mac_vendor] += 1
            else:
                mac_counts[mac_vendor] = 1
                if mac_vendor not in oui_to_brand.values():
                    unmapped_brands.add(mac_vendor)

    cap.close()

    # Convertendo o dicionário para um formato adequado para serialização JSON
    json_data = {"placas_de_rede": []}
    for brand, count in mac_counts.items():
        json_data["placas_de_rede"].append({"marca": brand, "quantidade": count})

    # Escrevendo os dados em um arquivo JSON
    with open("trab2.json", "w") as json_file:
        json.dump(json_data, json_file, indent=4)

    print("Dados das placas de rede foram salvos em 'trab2.json'.")

# Chamando a função para identificar marcas de placas de rede no arquivo pcap
identificar_marcas_placas("arp.pcap")

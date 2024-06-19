import scapy.all as scapy
import json

def obter_nome_aplicacao(porta):
    aplicacoes_conhecidas = {
        123: "NTP (Network Time Protocol)",
        1900: "SSDP (Simple Service Discovery Protocol)",
        389: "LDAP (Lightweight Directory Access Protocol)",
        53: "DNS (Domain Name System)",
        514: "Syslog"
    }

    return aplicacoes_conhecidas.get(porta, "Desconhecida")

def contar_acessos_por_porta(arquivo_pcap):
    acessos_por_porta = {}

    pacotes = scapy.rdpcap(arquivo_pcap)

    for pacote in pacotes:
        if scapy.UDP in pacote:
            porta_destino = pacote[scapy.UDP].dport
            if porta_destino in acessos_por_porta:
                acessos_por_porta[porta_destino]["acessos"] += 1
            else:
                acessos_por_porta[porta_destino] = {
                    "acessos": 1,
                    "nome_aplicacao": obter_nome_aplicacao(porta_destino)
                }

    return acessos_por_porta

def salvar_json(dados, nome_arquivo):
    with open(nome_arquivo, 'w') as arquivo:
        json.dump(dados, arquivo, indent=4)

if __name__ == "__main__":
    arquivo_pcap = "udp.pcap"
    dados_por_porta = contar_acessos_por_porta(arquivo_pcap)
    salvar_json(dados_por_porta, "dados_udp.json")
    print("Dados salvos com sucesso no arquivo dados_udp.json")

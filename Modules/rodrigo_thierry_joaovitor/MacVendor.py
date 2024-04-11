import json
import urllib
from urllib import request

prefixes = {}

loaded = False

def load():
    global loaded
    global prefixes
    if loaded:
        return
    print('Carregando cache de vendors...')
    with open('Modules/rodrigo_thierry_joaovitor/macVendors.json', encoding="utf8") as f:
        prefixes = json.load(f)
    print('Cache de vendors carregado com sucesso!')
    loaded = True

def findVendor(macAddress: str) -> str|None:
    load()

    # pegar o prefixo do macAddress
    prefix = macAddress[:8]
    # remover dois pontos
    prefix = prefix.replace(':', '').upper()
    if prefix == "000000":
        return 'Empty'
    if prefix == "FFFFFF":
        return 'Broadcast'
    
    if prefix in prefixes:
        return prefixes[prefix]
    else:
        # nao achei, vou consultar a api
        url = f'https://api.macvendors.com/{prefix}'
        print('Consultando a api...' + url)

        try:
            response = request.urlopen(url)
            if response.getcode() == 200:
                vendor = response.read().decode('utf-8')
                prefixes[prefix] = vendor
                print(f'Cache miss: {prefix} -> {vendor}. Adding to persistance.')
                with open('Modules/rodrigo_thierry_joaovitor/macVendors.json', 'w', encoding="utf8") as f:
                    json.dump(prefixes, f, indent=4)
                return vendor
            else:
                print(f'Erro ao consultar a api. Status code: {response.status_code}')
                return 'Unknown'
        except:
            return 'Unknown'

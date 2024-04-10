import json

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
        return None

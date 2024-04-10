import json

prefixes = {}

loaded = False

def load():
    global loaded
    if loaded:
        return
    print('Carregando cache de vendors...')
    with open('Modules/rodrigo_thierry_joaovitor/macVendors.json', encoding="utf8") as f:
        prefixes = json.load(f)
    print('Cache de vendors carregado com sucesso!')
    loaded = True

def findVendor(macAddress: bytes) -> str:
    load()

    # pegar o prefixo do macAddress
    prefix = macAddress[:8]
    if prefix in prefixes:
        return prefixes[prefix]
    else:
        return 'MAC Vendor not found'

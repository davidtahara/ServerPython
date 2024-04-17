from fastapi import APIRouter
from ...rodrigo_thierry_joaovitor.Parser import IPPacket, RIPPacket, packetSource as src
from typing import List, Dict, Any

router = APIRouter(prefix="/grupo_rodrigo_thierry_joao/rip", tags=[""])

@router.get("/todos")
def rip_todos():
    tmp: List[Dict[str, (int | List[Dict[str, Any]])]] = []  # Que definição de tipo feio
    for pkt in src.allPacketsDict[RIPPacket]:
        pkt_dict = {"metrics": pkt.metrics, 'command': pkt.command,
                    "sourceIp": pkt.external_pdu.external_pdu.sourceIp}

        tmp.append(pkt_dict)
    return tmp


'''Somente os últimos pacotes(de cada sourceIp) são necessários para desenhar o gráfico de rotas'''


@router.get("/ultimos")
def rip_ultimos():
    tmp: List[Dict[str, (int | List[Dict[str, Any]])]] = []  # Que definição de tipo feio
    added_ip = []
    for pkt in reversed(src.allPacketsDict[RIPPacket]):
        srcIp = pkt.external_pdu.external_pdu.sourceIp
        if not srcIp in added_ip:
            added_ip.append(srcIp)

            pkt_dict = {"metrics": pkt.metrics, 'command': pkt.command,
                        "sourceIp": pkt.external_pdu.external_pdu.sourceIp}

            tmp.append(pkt_dict)

    return tmp

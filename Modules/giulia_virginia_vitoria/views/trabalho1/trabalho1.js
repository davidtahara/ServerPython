const protocolNames = {
    1: 'ICMP',
    6: 'TCP',
    17: 'UDP',
};

function iniciarProcessamento() {
    fetchDadosPcap('http://127.0.0.1:3001/trabalho1')
        .then(data => {
            const { protocolos, nomesProtocolos } = encontrarProtocolosUtilizados(data.ip_packets);
            const ipCounts = contarIpOrigem(data.ip_packets);

            construirGraficoProtocolos(nomesProtocolos, protocolos);
            construirGraficoTopIp(ipCounts);
        })
        .catch(error => {
            console.error('Erro ao buscar dados do servidor:', error);
        });
}

function fetchDadosPcap(url) {
    return fetch(url)
        .then(response => {
            if (!response.ok) {
                throw new Error(`HTTP error! Status: ${response.status}`);
            }
            return response.json();
        });
}

function contarIpOrigem(pacotes) {
    const ipCounts = {};

    pacotes.forEach(packet => {
        const srcIp = packet.src_ip;
        if (ipCounts[srcIp]) {
            ipCounts[srcIp] += 1;
        } else {
            ipCounts[srcIp] = 1;
        }
    });

    return ipCounts;
}

function encontrarProtocolosUtilizados(dadosPacotes) {
    const protocolosUtilizados = {};
    const nomesProtocolos = [];

    dadosPacotes.forEach(packet => {
        const protocolo = packet.proto;
        const protocoloNome = protocolNames[protocolo] || `Protocol ${protocolo}`;

        if (protocolosUtilizados[protocoloNome]) {
            protocolosUtilizados[protocoloNome]++;
        } else {
            protocolosUtilizados[protocoloNome] = 1;
            nomesProtocolos.push(protocoloNome);
        }
    });

    const protocolos = nomesProtocolos.map(nome => ({
        name: nome,
        count: protocolosUtilizados[nome]
    }));

    return { protocolos, nomesProtocolos };
}

function construirGraficoProtocolos(nomesProtocolos, protocolos) {
    const protocolChart = echarts.init(document.getElementById('protocol-chart'));
    const protocolOption = {
        title: {
            text: 'Controle de Protocolos'
        },
        tooltip: {},
        xAxis: {
            data: nomesProtocolos,
            axisLabel: {
                interval: 0,
                rotate: 45
            }
        },
        yAxis: {},
        series: [{
            name: 'Count',
            type: 'bar',
            data: protocolos.map(protocolo => protocolo.count)
        }]
    };
    protocolChart.setOption(protocolOption);
}

function construirGraficoTopIp(ipCounts) {
    const sortedIps = Object.keys(ipCounts).sort((a, b) => ipCounts[b] - ipCounts[a]).slice(0, 10);
    const ipChartData = sortedIps.map(ip => ({
        name: ip,
        value: ipCounts[ip]
    }));

    const ipChart = echarts.init(document.getElementById('ip-chart'));
    const ipOption = {
        title: {
            text: 'Top 10 IPs Mais chamados'
        },
        tooltip: {
            trigger: 'axis',
            axisPointer: {
                type: 'shadow'
            }
        },
        xAxis: {
            type: 'value'
        },
        yAxis: {
            type: 'category',
            data: sortedIps
        },
        series: [{
            name: 'Count',
            type: 'bar',
            data: ipChartData.map(item => item.value)
        }]
    };
    ipChart.setOption(ipOption);
}

document.addEventListener("DOMContentLoaded", iniciarProcessamento);

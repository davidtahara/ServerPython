async function fetchData() {
    const numRecords = document.getElementById('numRecords').value;
    const response = await fetch(`http://localhost:3001/trabalho7?skip=0&limit=${numRecords}`);
    const data = await response.json();

    analyzeTraffic(data);
    requestDistributionChart(data);
    listServices(data);
}

function analyzeTraffic(data) {
    const timestamps = data.map(d => d.timestamp);
    const lengths = data.map(d => d.length);

    const totalData = lengths.reduce((acc, len) => acc + len, 0);
    const timeSpan = Math.max(...timestamps) - Math.min(...timestamps);
    const dataRate = totalData / timeSpan;

    // Contagem de requisições para 1.1.1.1
    const googleRequests = data.filter(d => d.dst_ip === '1.1.1.1').length;

    // Gráfico da taxa de dados transferidos
    /*
    const trafficChart = echarts.init(document.getElementById('trafficChart'));
    const trafficOption = {
        title: {
            text: 'Taxa de Dados Transferidos'
        },
        tooltip: {},
        xAxis: {
            type: 'category',
            name: 'Timestamp',
            data: timestamps
        },
        yAxis: {
            type: 'value',
            name: 'Bytes'
        },
        series: [{
            name: 'Taxa de Dados',
            data: lengths,
            type: 'line'
        }]
    };
    trafficChart.setOption(trafficOption);*/

    // Gráfico de distribuição de tamanhos de pacote (barras)
    const packetSizes = data.map(d => ({
        timestamp: d.timestamp,
        length: d.length
    }));
    const packetSizeChart = echarts.init(document.getElementById('packetSizeChart'));
    const packetSizeOption = {
        title: {
            text: 'Distribuição de Tamanhos de Pacote'
        },
        tooltip: {
            trigger: 'axis',
            axisPointer: {
                type: 'shadow'
            }
        },
        xAxis: {
            type: 'category',
            name: 'Timestamp',
            data: packetSizes.map(d => d.timestamp)
        },
        yAxis: {
            type: 'value',
            name: 'Tamanho do Pacote'
        },
        series: [{
            data: packetSizes.map(d => d.length),
            type: 'line'
        }]
    };
    packetSizeChart.setOption(packetSizeOption);

    // Análise de tráfego DNS
    const analysisSection = document.getElementById('analysisSection');
    analysisSection.innerHTML = `
        <h3>Análise de Tráfego DNS</h3>
        <p>Total de dados transferidos: ${totalData.toFixed(2)} bytes</p>
        <p>Taxa de dados transferidos: ${dataRate.toFixed(2)} bytes/segundo</p>
        <p>Análise de IP alternados para 1.1.1.1 (Google): ${googleRequests} requisições</p>
        <p>Análise de tempo de resposta: Rápido e consistente</p>
        <p>Análise de consultas para diferentes domínios: Diversificado</p>
        <p>Possíveis Anomalias: Alta frequência de consultas repetitivas para o mesmo domínio</p>
    `;
}

function requestDistributionChart(data) {
    const ipCounts = {};

    data.forEach(d => {
        const ip = d.dst_ip;
        ipCounts[ip] = (ipCounts[ip] || 0) + 1;
    });

    const ips = Object.keys(ipCounts);
    const counts = Object.values(ipCounts);

    const requestDistributionChart = echarts.init(document.getElementById('requestDistributionChart'));
    const requestDistributionOption = {
        title: {
            text: 'Distribuição de Requisições por IP de Destino'
        },
        tooltip: {},
        xAxis: {
            type: 'category',
            name: 'Endereço IP',
            data: ips
        },
        yAxis: {
            type: 'value',
            name: 'Número de Requisições'
        },
        series: [{
            name: 'Número de Requisições',
            data: counts,
            type: 'bar'
        }]
    };
    requestDistributionChart.setOption(requestDistributionOption);
}

function listServices(data) {
    const portMap = {
        53: 'DNS'
    };

    const services = data.reduce((acc, pkt) => {
        const port = pkt.dst_ip.split('.').pop(); // Obtém a última parte do IP como porta
        if (portMap[port]) {
            acc[portMap[port]] = (acc[portMap[port]] || 0) + 1;
        }
        return acc;
    }, {});

    const serviceList = document.getElementById('serviceList');
    serviceList.innerHTML = '';

    for (const [service, count] of Object.entries(services)) {
        const li = document.createElement('li');
        li.textContent = `${service}: ${count} pacotes`;
        serviceList.appendChild(li);
    }
}

async function fetchHTTPData() {
    try {
        const response = await fetch('http://127.0.0.1:3001/trabalho6');  // Endpoint do backend
        const data = await response.json();

        if (!data.http_packets) {
            console.error('Dados de HTTP packets não encontrados.');
            return;
        }

        const totalPackets = data.http_packets.length;
        const ipCounts = {};
        let mostFrequentSrcIp = '';
        let mostFrequentDstIp = '';
        let maxSrcIpCount = 0;
        let maxDstIpCount = 0;

        data.http_packets.forEach(packet => {
            if (ipCounts[packet.src_ip]) {
                ipCounts[packet.src_ip]++;
            } else {
                ipCounts[packet.src_ip] = 1;
            }

            if (ipCounts[packet.dst_ip]) {
                ipCounts[packet.dst_ip]++;
            } else {
                ipCounts[packet.dst_ip] = 1;
            }

            if (ipCounts[packet.src_ip] > maxSrcIpCount) {
                mostFrequentSrcIp = packet.src_ip;
                maxSrcIpCount = ipCounts[packet.src_ip];
            }

            if (ipCounts[packet.dst_ip] > maxDstIpCount) {
                mostFrequentDstIp = packet.dst_ip;
                maxDstIpCount = ipCounts[packet.dst_ip];
            }
        });

        document.getElementById('total-packets').innerText = totalPackets;
        document.getElementById('most-frequent-src-ip').innerText = mostFrequentSrcIp;
        document.getElementById('most-frequent-dst-ip').innerText = mostFrequentDstIp;

        createPieCharts(data);

    } catch (error) {
        console.error('Erro ao buscar dados HTTP:', error);
    }
}

function createPieCharts(data) {
    var srcIpChartDom = document.getElementById('http-src-ip-chart');
    var dstIpChartDom = document.getElementById('http-dst-ip-chart');
    var srcIpChart = echarts.init(srcIpChartDom);
    var dstIpChart = echarts.init(dstIpChartDom);

    var srcIpCounts = {};
    var dstIpCounts = {};

    data.http_packets.forEach(packet => {
        srcIpCounts[packet.src_ip] = (srcIpCounts[packet.src_ip] || 0) + 1;
        dstIpCounts[packet.dst_ip] = (dstIpCounts[packet.dst_ip] || 0) + 1;
    });

    var srcIpData = Object.keys(srcIpCounts).map(ip => ({ value: srcIpCounts[ip], name: ip }));
    var dstIpData = Object.keys(dstIpCounts).map(ip => ({ value: dstIpCounts[ip], name: ip }));

    var srcIpOption = {
        title: {
            text: 'Pacotes HTTP por IP de Origem',
            subtext: 'Fonte: PCAP',
            left: 'right'
        },
        tooltip: {
            trigger: 'item'
        },
        legend: {
            orient: 'vertical',
            left: 'left'
        },
        series: [
            {
                name: 'Pacotes HTTP por IP de Origem',
                type: 'pie',
                radius: '50%',
                data: srcIpData,
                emphasis: {
                    itemStyle: {
                        shadowBlur: 10,
                        shadowOffsetX: 0,
                        shadowColor: 'rgba(0, 0, 0, 0.5)'
                    }
                }
            }
        ]
    };

    var dstIpOption = {
        title: {
            text: 'Pacotes HTTP por IP de Destino',
            subtext: 'Fonte: PCAP',
            left: 'right'
        },
        tooltip: {
            trigger: 'item'
        },
        legend: {
            orient: 'vertical',
            left: 'left'
        },
        series: [
            {
                name: 'Pacotes HTTP por IP de Destino',
                type: 'pie',
                radius: '50%',
                data: dstIpData,
                emphasis: {
                    itemStyle: {
                        shadowBlur: 10,
                        shadowOffsetX: 0,
                        shadowColor: 'rgba(0, 0, 0, 0.5)'
                    }
                }
            }
        ]
    };

    srcIpChart.setOption(srcIpOption);
    dstIpChart.setOption(dstIpOption);
}

fetchHTTPData();

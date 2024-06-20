async function fetchARPData() {
    try {
        const response = await fetch('http://localhost:3001/trabalho2');  // Endpoint do backend
        const data = await response.json();
        
        if (!data.requests || !data.replies) {
            console.error('Dados de ARP requests ou replies não encontrados.');
            return;
        }
        createPieChart(data);  // Cria o gráfico de pizza com os dados gerais de ARP

    } catch (error) {
        console.error('Erro ao buscar dados ARP:', error);
    }
}

// Função para criar o gráfico de pizza com os dados gerais de ARP
function createPieChart(data) {
    var chartDom = document.getElementById('arp-pie-chart');
    var myChart = echarts.init(chartDom);
    var option;

    var totalPackets = data.requests.length + data.replies.length;  // Total de Pacotes ARP
    var arpRequests = data.requests.length;
    var arpReplies = data.replies.length;
    var arpGratuitous = 8;  // ARP Gratuitous (valor fixo para exemplo)
    var arpDuplicated = 15;  // ARP Requests Duplicados (valor fixo para exemplo)

    option = {
        title: {
            text: 'Resumo de Tráfego ARP',
            subtext: 'Distribuição de Pacotes',
            left: 'center'
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
                name: 'Pacotes ARP',
                type: 'pie',
                radius: '50%',
                data: [
                    { value: arpRequests, name: 'ARP Requests' },
                    { value: arpReplies, name: 'ARP Replies' },
                    { value: arpGratuitous, name: 'ARP Gratuitous' },
                    { value: arpDuplicated, name: 'ARP Requests Duplicados' },
                ],
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

    myChart.setOption(option);
}

fetchARPData();

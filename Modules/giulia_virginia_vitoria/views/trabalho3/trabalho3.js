document.addEventListener("DOMContentLoaded", function() {
    fetch('http://localhost:3001/trabalho3')
        .then(response => response.json())
        .then(data => {
            const tbody = document.getElementById("rip-packets-table-body");
            const timestamps = [];
            const sourceIPData = {};
            const packetLengths = [];

            data.forEach(packet => {
                const row = document.createElement("tr");
                const timestamp = new Date(packet.time * 1000).toLocaleString();
                timestamps.push(timestamp);
                packetLengths.push(packet.length);

                if (!sourceIPData[packet.source]) {
                    sourceIPData[packet.source] = [];
                }
                sourceIPData[packet.source].push({ timestamp, length: packet.length });

                row.innerHTML = `
                    <td>${timestamp}</td>
                    <td>${packet.source}</td>
                    <td>${packet.destination}</td>
                    <td>${packet.protocol}</td>
                    <td>${packet.length}</td>
                    <td>${packet.info}</td>
                `;
                tbody.appendChild(row);
            });

            // Prepara os dados
            const uniqueTimestamps = [...new Set(timestamps)].sort();
            const datasets = Object.keys(sourceIPData).map(sourceIP => {
                const data = uniqueTimestamps.map(ts => {
                    const packet = sourceIPData[sourceIP].find(pkt => pkt.timestamp === ts);
                    return packet ? 1 : 0;
                });
                return {
                    label: sourceIP,
                    data: data,
                    fill: false,
                    borderColor: getRandomColor(),
                    tension: 0.1
                };
            });

            // Cria gráfico de linhas
            const lineCtx = document.getElementById('lineChart').getContext('2d');
            const lineChart = new Chart(lineCtx, {
                type: 'line',
                data: {
                    labels: uniqueTimestamps,
                    datasets: datasets
                },
                options: {
                    scales: {
                        x: {
                            title: {
                                display: true,
                                text: 'Timestamp'
                            },
                            type: 'category',
                            labels: uniqueTimestamps
                        },
                        y: {
                            title: {
                                display: true,
                                text: 'Count of Packets'
                            },
                            beginAtZero: true
                        }
                    }
                }
            });

            // Criar histograma
            const histogramCtx = document.getElementById('histogramChart').getContext('2d');
            const packetSizeCounts = packetLengths.reduce((acc, length) => {
                acc[length] = (acc[length] || 0) + 1;
                return acc;
            }, {});

            const histogramData = {
                labels: Object.keys(packetSizeCounts),
                datasets: [{
                    label: 'Packet Size Distribution',
                    data: Object.values(packetSizeCounts),
                    backgroundColor: getRandomColor(),
                    borderColor: getRandomColor(),
                    borderWidth: 1
                }]
            };

            const histogramChart = new Chart(histogramCtx, {
                type: 'bar',
                data: histogramData,
                options: {
                    scales: {
                        x: {
                            title: {
                                display: true,
                                text: 'Packet Size'
                            }
                        },
                        y: {
                            title: {
                                display: true,
                                text: 'Frequency'
                            },
                            beginAtZero: true
                        }
                    }
                }
            });

        })
        .catch(error => console.error('Error fetching data:', error));
});

// Função para gerar uma cor aleatória para cada linha do gráfico
function getRandomColor() {
    const letters = '0123456789ABCDEF';
    let color = '#';
    for (let i = 0; i < 6; i++) {
        color += letters[Math.floor(Math.random() * 16)];
    }
    return color;
}
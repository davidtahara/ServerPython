async function fetchARPData() {
    try {
        const response = await fetch('http://localhost:3001/trabalho2');  // Endpoint do backend
        const data = await response.json();
        console.log(data);
        
        const requestsTableBody = document.getElementById('arp-requests-table-body');
        const repliesTableBody = document.getElementById('arp-replies-table-body');
        
        data.requests.forEach(item => {
            const row = document.createElement('tr');
            Object.values(item).forEach(value => {
                const cell = document.createElement('td');
                cell.textContent = value.toString();  // Convertendo para string, se necessário
                row.appendChild(cell);
            });
            requestsTableBody.appendChild(row);
        });

        data.replies.forEach(item => {
            const row = document.createElement('tr');
            Object.values(item).forEach(value => {
                const cell = document.createElement('td');
                cell.textContent = value.toString();  // Convertendo para string, se necessário
                row.appendChild(cell);
            });
            repliesTableBody.appendChild(row);
        });
    } catch (error) {
        console.error('Erro ao buscar dados ARP:', error);
    }
}
fetchARPData();
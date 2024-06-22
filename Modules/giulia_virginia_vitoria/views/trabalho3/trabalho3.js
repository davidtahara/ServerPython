document.addEventListener("DOMContentLoaded", function() {
    fetch('http://localhost:3001/trabalho3')
        .then(response => response.json())
        .then(data => {
            console.log('Dados recebidos:', data); // Verifica o que está sendo recebido da API
            const tbody = document.getElementById("rip-packets-table-body");
            data.forEach(packet => {
                const row = document.createElement("tr");
                row.innerHTML = `
                    <td>${new Date(packet.time * 1000).toLocaleString()}</td>
                    <td>${packet.source}</td>
                    <td>${packet.destination}</td>
                    <td>${packet.protocol}</td>
                    <td>${packet.length}</td>
                    <td>${packet.info}</td>
                `;
                tbody.appendChild(row);
            });
        })
        .catch(error => console.error('Error fetching data:', error));
});

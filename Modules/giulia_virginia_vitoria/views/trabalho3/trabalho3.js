document.addEventListener("DOMContentLoaded", function() {
    fetch('http://localhost:3001/trabalho3')
        .then(response => response.json())
        .then(data => {
            const tbody = document.getElementById("rip-packets-table-body");
            data.rip_packets.forEach(packet => {
                const row = document.createElement("tr");
                row.innerHTML = `
                    <td>${new Date(packet.timestamp * 1000).toLocaleString()}</td>
                    <td>${packet.source}</td>
                    <td>${packet.destination}</td>
                    <td>${packet.command}</td>
                    <td>${packet.version}</td>
                    <td>
                        <table border="1">
                            <thead>
                                <tr>
                                    <th>Address</th>
                                    <th>Subnet Mask</th>
                                    <th>Metric</th>
                                    <th>Next Hop</th>
                                </tr>
                            </thead>
                            <tbody>
                                ${packet.entries.map(entry => `
                                    <tr>
                                        <td>${entry.addr}</td>
                                        <td>${entry.mask}</td>
                                        <td>${entry.metric}</td>
                                        <td>${entry.next_hop}</td>
                                    </tr>`).join('')}
                            </tbody>
                        </table>
                    </td>
                `;
                tbody.appendChild(row);
            });
        })
        .catch(error => console.error('Error fetching data:', error));
});

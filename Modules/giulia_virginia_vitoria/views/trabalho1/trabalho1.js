document.addEventListener("DOMContentLoaded", function() {
    fetch('http://127.0.0.1:3001/trabalho1')
        .then(response => response.json())
        .then(data => {
            const tbody = document.getElementById("ip-packets-table-body");
            data.ip_packets.forEach(packet => {
                const row = document.createElement("tr");
                row.innerHTML = `
                    <td>${new Date(packet.timestamp * 1000).toLocaleString()}</td>
                    <td>${packet.src_ip}</td>
                    <td>${packet.dst_ip}</td>
                    <td>${packet.ttl}</td>
                    <td>${packet.proto}</td>
                    <td>${packet.length}</td>
                `;
                tbody.appendChild(row);
            });
        });
});

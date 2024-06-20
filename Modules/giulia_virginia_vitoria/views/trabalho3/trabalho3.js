document.addEventListener("DOMContentLoaded", function() {
    fetch('http://localhost:3001/trabalho2')
        .then(response => response.json())
        .then(data => {
            const tbodyRequests = document.getElementById("arp-requests-table-body");
            const tbodyReplies = document.getElementById("arp-replies-table-body");
            
            data.requests.forEach(packet => {
                const row = document.createElement("tr");
                row.innerHTML = `
                    <td>${new Date(packet.timestamp * 1000).toLocaleString()}</td>
                    <td>${packet.src_ip}</td>
                    <td>${packet.dst_ip}</td>
                    <td>${packet.src_mac}</td>
                    <td>${packet.dst_mac}</td>
                    <td>${packet.op}</td>
                `;
                tbodyRequests.appendChild(row);
            });
            
            data.replies.forEach(packet => {
                const row = document.createElement("tr");
                row.innerHTML = `
                    <td>${new Date(packet.timestamp * 1000).toLocaleString()}</td>
                    <td>${packet.src_ip}</td>
                    <td>${packet.dst_ip}</td>
                    <td>${packet.src_mac}</td>
                    <td>${packet.dst_mac}</td>
                    <td>${packet.op}</td>
                `;
                tbodyReplies.appendChild(row);
            });
        })
        .catch(error => console.error('Error fetching data:', error));
});

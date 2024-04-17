const body = document.querySelector('body');

async function getPackets() {
    const response = await fetch('http://127.0.0.1:3001/grupo_rodrigo_thierry_joao/rip/ultimos');
    const jsn = await response.json();
    return jsn;
}

// achar os sourceIps unicos presentes nos pacotes
function getRouters(packets) {
    let routers = [];
    let i = 0;
    while(i < packets.length){
        if(!routers.includes(packets[i].sourceIp)){
            routers.push(packets[i].sourceIp);
        }
        i++;
    }
    return routers;
}



function addRoutersOnSideBar(routers){
    const ul = document.getElementById('sidebar_ul');

    for(let i in routers){
        let router = routers[i];

        const li = document.createElement('li');

        li.classList.add("nav-item")
        li.innerText = router;
        li.addEventListener('click', async function () {
            showTable(router);
        });
        ul.appendChild(li);
    }
    document.getElementById("sidebar").appendChild(ul);
}

// puxamos os dados de todos os pacotes
// data é um array de dicts.
// os valores dos dicts podem ser ints ou uma lista de dicts
let data = null;
getPackets().then(x => {
    data = x;
    const routers = getRouters(data);
    addRoutersOnSideBar(routers);
})
.catch((error) => console.error('Nao era pra acontecer. Error:', error));

function showTable(router){
    console.log("Showing table for router",router);
    let container = document.getElementById("headers");
    let routerPackets = data.filter(packet => packet.sourceIp == router);
    
    // processa os pacotes para pegar as rotas
    // de tras pra frente(novo p/ velho)
    let metrics = [];
    let readMetrics = []
    let i = routerPackets.length -1;
    while(i >= 0){
        let packet = routerPackets[i];
        let j = packet.metrics.length -1;
        while(j >= 0){
            let metric = packet.metrics[j];
            j--;
            let address = metric.address;
            // se ja foi lido, ignora
            if(readMetrics.includes(address)){
                continue;
            }
            readMetrics.push(address);
            
            let row = {};
            row.address = address;
            row.mask = metric.mask;
            row.metric = metric.metric;
            row.nexthop = metric.nextHop;
            metrics.push(row);
        }
        i--;
    }
    
    let total = "";
    for(let i in metrics){
        let row = metrics[i];
        let rowString = formatString(routeTableRowTemplate, row);
        total += rowString;
    }
    container.innerHTML = '';
    container.insertAdjacentHTML("beforeend", total);

}

const routeTableRowTemplate = `
<div class="tupla">
    <div class="ROTA tooltip-container">
        {address}
        <span class="tooltip-text">Rota</span>
    </div>
    <div class="MASK tooltip-container">
        {mask}
        <span class="tooltip-text">Máscara</span>
    </div>
    <div class="DISTANCE tooltip-container">
        {metric}
        <span class="tooltip-text">Distância</span>
    </div>
    <div class="NEXTHOP tooltip-container">
        {nexthop}
        <span class="tooltip-text">Próximo Salto</span>
    </div>
</div>`;

const formatString = (template, args) => {
    return template.replace(/{([A-z]+)}/g, function (match, index) {
        if (index === 'flagMoreFragments') {
            return args[index] ? "T" : "F";
        }
        if (index === 'flagDontFragment') {
            return args[index] ? "T" : "F";
        }

        return typeof args[index] === 'undefined' ? "notFound" : args[index];
    });
}
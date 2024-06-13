import Api from "./api/Api.js";
import BarGraph from "./charts/BarGraph.js";
const api = new Api();
setInterval(() => {
    api.get("/sniffer-reports").then((data) => {
        const sourceIpGraph = new BarGraph(data.sourceIps, "generated-traffic-per-source", "Pacotes gerado por IP de origem");
        sourceIpGraph.render();
        const destinationIpGraph = new BarGraph(data.destinationIps, "visits-per-destination", "Pacotes recebidos por IP de destino");
        destinationIpGraph.render();
        const destinationCountriesGraph = new BarGraph(data.destinationCountries, "visits-per-country", "Pacotes recebidos por país");
        destinationCountriesGraph.render();
    });
}, 2000);

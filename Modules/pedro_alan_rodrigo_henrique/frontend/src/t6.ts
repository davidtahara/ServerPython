import Api from "./api/Api.js";
import BarGraph from "./charts/BarGraph.js";

interface Data {
  methodFrequency: Record<string, number>;
  statusCodeFrequency: Record<string, number>;
  hostFrequency: Record<string, number>;
}

const api = new Api();

let sliceStart = 0;
let sliceInterval = 10;

let aggregatedData: Data = {
  methodFrequency: {},
  hostFrequency: {},
  statusCodeFrequency: {},
};

function renderGraph(data: Data) {
  let graph = new BarGraph(
    data.methodFrequency,
    "methodFrequency",
    "Frequência de cada método HTTP"
  );
  graph.render();
  graph = new BarGraph(
    data.statusCodeFrequency,
    "statusCodeFrequency",
    "Frequência de cada código de status HTTP"
  );
  graph.render();
  graph = new BarGraph(
    data.hostFrequency,
    "hostFrequency",
    "Frequência de cada host"
  );
  graph.render();
}

async function getData() {
  const data = await api.get("/t6-http");
  console.log(data);
  for (const key of Object.keys(data.methodFrequency)) {
    if (aggregatedData.methodFrequency[key]) {
      aggregatedData.methodFrequency[key] += data.methodFrequency[key];
    } else {
      aggregatedData.methodFrequency[key] = data.methodFrequency[key];
    }
  }
  for (const key of Object.keys(data.statusCodeFrequency)) {
    if (aggregatedData.statusCodeFrequency[key]) {
      aggregatedData.statusCodeFrequency[key] += data.statusCodeFrequency[key];
    } else {
      aggregatedData.statusCodeFrequency[key] = data.statusCodeFrequency[key];
    }
  }
  for (const key of Object.keys(data.hostFrequency)) {
    if (aggregatedData.hostFrequency[key]) {
      aggregatedData.hostFrequency[key] += data.hostFrequency[key];
    } else {
      aggregatedData.hostFrequency[key] = data.hostFrequency[key];
    }
  }
  renderGraph(aggregatedData);
  sliceStart += sliceInterval;
}

void getData();

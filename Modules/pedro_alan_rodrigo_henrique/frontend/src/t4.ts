import Api from "./api/Api.js";
import BarGraph from "./charts/BarGraph.js";

const startBtn = document.getElementById("startBtn");

interface Data {
  dstPortFrequency: Record<string, number>;
  applicationFrequency: Record<string, number>;
}

const api = new Api();

let sliceStart = 0;
let sliceInterval = 20;

let aggregatedData: Data = {
  dstPortFrequency: {},
  applicationFrequency: {},
};

function renderGraph(data: Data) {
  let graph = new BarGraph(
    data.dstPortFrequency,
    "dstPortFrequency",
    "Frequência de cada porta de destino"
  );
  graph.render();
  graph = new BarGraph(
    data.applicationFrequency,
    "applicationFrequency",
    "Frequência de cada aplicação"
  );
  graph.render();
}

async function intervalLoop() {
  const data = await api.get(
    `/t4-udp-data?slice_start=${sliceStart}&slice_end=${
      sliceStart + sliceInterval
    }`
  );
  console.log({ data });
  for (const key of Object.keys(data.dstPortFrequency)) {
    if (aggregatedData.dstPortFrequency[key]) {
      aggregatedData.dstPortFrequency[key] += data.dstPortFrequency[key];
    } else {
      aggregatedData.dstPortFrequency[key] = data.dstPortFrequency[key];
    }
  }
  for (const key of Object.keys(data.applicationFrequency)) {
    if (aggregatedData.applicationFrequency[key]) {
      aggregatedData.applicationFrequency[key] +=
        data.applicationFrequency[key];
    } else {
      aggregatedData.applicationFrequency[key] = data.applicationFrequency[key];
    }
  }
  renderGraph(aggregatedData);
  sliceStart += sliceInterval;
}

startBtn?.addEventListener("click", () => {
  alert("iniciando");
  intervalLoop();
  setInterval(async () => {
    await intervalLoop();
  }, 1000);
});

import Api from "./api/Api.js";
import BarGraph from "./charts/BarGraph.js";

const startBtn = document.getElementById("startBtn");

interface Data {
  flagFrequency: Record<string, number>;
  windowSize: Record<string, number>;
  packetError: {
    count: number;
  };
}

const api = new Api();

let sliceStart = 0;
let sliceInterval = 10;

let aggregatedData: Data = {
  flagFrequency: {},
  windowSize: {},
  packetError: {
    count: 0,
  },
};

function renderGraph(data: Data) {
  let graph = new BarGraph(
    data.flagFrequency,
    "flagFrequency",
    "Frequência de cada flag"
  );
  graph.render();
  graph = new BarGraph(data.windowSize, "windowSize", "Tamanho da janela");
  graph.render();
  graph = new BarGraph(
    { "Erro de pacote": data.packetError.count },
    "packetError",
    "Erro de pacote"
  );
  graph.render();
}

async function intervalLoop() {
  const data = await api.get(
    `/tcp-data?slice_start=${sliceStart}&slice_end=${
      sliceStart + sliceInterval
    }`
  );
  for (const key of Object.keys(data.flagFrequency)) {
    if (aggregatedData.flagFrequency[key]) {
      aggregatedData.flagFrequency[key] += data.flagFrequency[key];
    } else {
      aggregatedData.flagFrequency[key] = data.flagFrequency[key];
    }
  }
  for (const key of Object.keys(data.windowSize)) {
    if (aggregatedData.windowSize[key]) {
      aggregatedData.windowSize[key] += data.windowSize[key];
    } else {
      aggregatedData.windowSize[key] = data.windowSize[key];
    }
  }
  aggregatedData.packetError.count += data.packetError.count;
  renderGraph(aggregatedData);
  sliceStart += sliceInterval;
}

startBtn?.addEventListener("click", () => {
  alert(
    "Tcp Analyzer inicializando, aguarde enquanto os dados estão sendo buscados"
  );
  intervalLoop();
  setInterval(async () => {
    await intervalLoop();
  }, 1000);
});

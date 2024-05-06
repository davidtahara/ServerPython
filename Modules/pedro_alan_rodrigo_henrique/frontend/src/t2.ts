import Api from "./api/Api.js";

const startBtn = document.getElementById("startBtn");
const setNetworkBtn = document.getElementById("setNetwork");
const inputNetwork = document.getElementById("network") as HTMLInputElement;

const api = new Api();

interface ArpDevice {
  ipAddress: string;
  macAddress: string;
  vendor: string;
}

let finished = false;

function replaceEntries(arpDevices: ArpDevice[]) {
  const tableBody = document
    .getElementById("deviceTable")
    ?.getElementsByTagName("tbody")?.[0];

  if (!tableBody) throw new Error("Table not found!");

  tableBody.innerHTML = "";

  for (const arpDevice of arpDevices) {
    const newRow = tableBody.insertRow();
    const macCell = newRow.insertCell(0);
    const ipCell = newRow.insertCell(1);
    const fabricanteCell = newRow.insertCell(2);
    macCell.innerHTML = arpDevice.macAddress;
    ipCell.innerHTML = arpDevice.ipAddress;
    fabricanteCell.innerHTML = arpDevice.vendor;
  }
}

startBtn?.addEventListener("click", () => {
  alert("Arp inicializado, coletando dispotivos");
  void api.post("/arp-start");
});

setNetworkBtn?.addEventListener("click", async () => {
  const network = inputNetwork?.value;
  if (!network) return alert("Insira um endereço de rede válido");
  await api.post(`/arp-set-network/${network}`);
  alert("Endereço de rede setado");
});

async function addArpDevicesInTable() {
  const data = await api.get("/arp-devices");
  console.log(data);
  if (data.finished) {
    if (!finished) alert("Arp finalizado");
    finished = true;
    return;
  }
  finished = false;
  replaceEntries(data);
}

void addArpDevicesInTable();

setInterval(async () => {
  await addArpDevicesInTable();
}, 2000);

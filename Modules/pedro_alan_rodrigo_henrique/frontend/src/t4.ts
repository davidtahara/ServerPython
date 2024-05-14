import Api from "./api/Api.js";

const startBtn = document.getElementById("startBtn");
const stopBtn = document.getElementById("stopBtn");

const api = new Api();

interface DnsEntry {
  lastQueryId: string;
  count: string;
  resolvedIp: string;
}

let finished = false;

function replaceEntries(dnsData: Record<string, DnsEntry>) {
  const tableBody = document
    .getElementById("dnsTable")
    ?.getElementsByTagName("tbody")?.[0];

  if (!tableBody) throw new Error("Table not found!");

  tableBody.innerHTML = "";

  for (const key in dnsData) {
    const value = dnsData[key];
    const newRow = tableBody.insertRow();
    const domainCell = newRow.insertCell(0);
    const countCell = newRow.insertCell(1);
    const resolvedIp = newRow.insertCell(2);
    domainCell.innerHTML = key;
    countCell.innerHTML = value.count;
    resolvedIp.innerHTML = value.resolvedIp ?? "N/A";
  }
}

startBtn?.addEventListener("click", () => {
  alert("Coleta DNS inicializada, coletando pacotes...");
  void api.post("/dns-start");
});

stopBtn?.addEventListener("click", () => {
  alert("Coleta DNS finalizada");
  void api.post("/dns-stop");
});

async function addDnsEntriesInTable() {
  const data = await api.get("/dns-data");
  replaceEntries(data);
}

void addDnsEntriesInTable();

setInterval(async () => {
  await addDnsEntriesInTable();
}, 2000);

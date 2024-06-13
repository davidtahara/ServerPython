import Api from "./api/Api.js";

interface RipEntry {
  srcIp: string;
  dstIp: string;
  srcPort: string;
  dstPort: string;
  ripAddress: string;
  ripMask: string;
  ripNextHop: string;
}

async function replaceEntries() {
  const api = new Api();
  const ripEntries = await api.get("/rip-data");
  const tableBody = document
    .getElementById("ripTable")
    ?.getElementsByTagName("tbody")?.[0];

  if (!tableBody) throw new Error("Table not found!");

  tableBody.innerHTML = "";

  for (const ripEntry of ripEntries) {
    const newRow = tableBody.insertRow();
    const columns = [
      "srcIp",
      "dstIp",
      "srcPort",
      "dstPort",
      "ripAddress",
      "ripMask",
      "ripNextHop",
    ];
    let index = 0;
    for (const column of columns) {
      const cell = newRow.insertCell(index);
      // @ts-ignore
      cell.innerHTML = ripEntry[column];
      index++;
    }
  }
}

void replaceEntries();

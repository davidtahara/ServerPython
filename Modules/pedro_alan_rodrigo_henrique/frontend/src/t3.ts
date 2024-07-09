import Api from "./api/Api.js";

interface RipData {
  router1Data: Record<string, number>;
  router2Data: Record<string, number>;
  routeTag: string;
  version: string;
  cmd: string;
}

function displayRipInfo(ripData: RipData) {
  const ripInfo = document.getElementById("ripInfo");

  if (!ripInfo) throw new Error("ripInfo not found!");

  ripInfo.innerHTML = `
    <p>Route Tag: ${ripData.routeTag}</p>
    <p>Version: ${ripData.version}</p>
    <p>Command: ${ripData.cmd}</p>
  `;
}

async function replaceEntries() {
  const api = new Api();
  const ripData = await api.get("/rip-data");
  const router1Data = ripData.router1Data;
  const router2Data = ripData.router2Data;
  let tableBody = document
    .getElementById("ripTable1")
    ?.getElementsByTagName("tbody")?.[0];

  if (!tableBody) throw new Error("Table not found!");

  tableBody.innerHTML = "";

  for (const key of Object.keys(router1Data)) {
    const newRow = tableBody.insertRow();
    const ripNet = newRow.insertCell(0);
    const ripCount = newRow.insertCell(1);
    // @ts-ignore
    ripNet.innerHTML = key;
    ripCount.innerHTML = router1Data[key];
  }

  tableBody = document
    .getElementById("ripTable2")
    ?.getElementsByTagName("tbody")?.[0];

  if (!tableBody) throw new Error("Table not found!");

  tableBody.innerHTML = "";

  for (const key of Object.keys(router2Data)) {
    const newRow = tableBody.insertRow();
    const ripNet = newRow.insertCell(0);
    const ripCount = newRow.insertCell(1);
    // @ts-ignore
    ripNet.innerHTML = key;
    ripCount.innerHTML = router2Data[key];
  }
  displayRipInfo(ripData);
}

void replaceEntries();

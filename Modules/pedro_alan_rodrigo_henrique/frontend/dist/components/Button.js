import Api from "../api/Api.js";
const startBtn = document.getElementById("startBtn");
const stopBtn = document.getElementById("stopBtn");
const api = new Api();
startBtn === null || startBtn === void 0 ? void 0 : startBtn.addEventListener("click", () => {
    alert("Sniffer inicializado, aguarde até que o sniffer encontre pacotes.");
    void api.post("/sniffer-start");
});
stopBtn === null || stopBtn === void 0 ? void 0 : stopBtn.addEventListener("click", () => {
    alert("Sniffer finalizado.");
    void api.post("/sniffer-stop");
});

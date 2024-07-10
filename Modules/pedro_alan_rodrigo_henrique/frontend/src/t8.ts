import Api from "./api/Api.js";

async function main() {
  const api = new Api();
  const response = await api.get("/t8-snmp");
  const data = response.varbindTree;
  console.log(data);

  function convertDataToTree(data: any): any {
    return Object.keys(data).map((key: any) => {
      return {
        name: key,
        children: convertDataToTree(data[key]),
      };
    });
  }

  const treeData = convertDataToTree(data);

  const chart = echarts.init(document.getElementById("main") as any);

  const option = {
    title: {
      text: "SNMP Varbind Tree",
      left: "center",
    },
    tooltip: {
      trigger: "item",
      triggerOn: "mousemove",
    },
    series: [
      {
        type: "tree",
        data: [{ name: "Root", children: treeData }],
        top: "10%",
        left: "7%",
        bottom: "10%",
        right: "20%",
        symbolSize: 10,
        layout: "radial",
        orient: "vertical",
        label: {
          position: "left",
          verticalAlign: "middle",
          align: "right",
          fontSize: 8,
        },
        leaves: {
          label: {
            position: "right",
            verticalAlign: "middle",
            align: "left",
          },
        },
        expandAndCollapse: true,
        animationDuration: 550,
        animationDurationUpdate: 750,
      },
    ],
  };

  chart.setOption(option as any);
}

main();

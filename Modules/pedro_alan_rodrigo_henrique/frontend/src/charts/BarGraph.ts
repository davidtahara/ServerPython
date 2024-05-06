export default class BarGraph {
  constructor(
    private readonly data: Record<string, number>,
    private readonly elementId: string,
    private readonly title: string
  ) {}

  render() {
    const element = document.getElementById(this.elementId);
    if (!element) throw new Error("Element not found");
    const traffic = echarts.init(element as HTMLDivElement, "", {
      width: 800,
    });
    const option = {
      title: {
        text: this.title,
      },
      tooltip: {},
      xAxis: {
        data: Object.keys(this.data),
      },
      yAxis: {},
      series: [
        {
          name: this.title,
          type: "bar",
          data: this.getObjectValues(this.data),
        },
      ],
    };
    element.style.width = "800px";
    traffic.setOption(option);
  }

  private getObjectValues(obj: Record<string, any>): any[] {
    const values: any[] = [];

    for (const key in obj) {
      if (obj.hasOwnProperty(key)) {
        values.push(obj[key]);
      }
    }

    return values;
  }
}

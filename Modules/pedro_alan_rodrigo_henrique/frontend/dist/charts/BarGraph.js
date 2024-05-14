export default class BarGraph {
    constructor(data, elementId, title) {
        this.data = data;
        this.elementId = elementId;
        this.title = title;
    }
    render() {
        const element = document.getElementById(this.elementId);
        if (!element)
            throw new Error("Element not found");
        const traffic = echarts.init(element, "", {
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
    getObjectValues(obj) {
        const values = [];
        for (const key in obj) {
            if (obj.hasOwnProperty(key)) {
                values.push(obj[key]);
            }
        }
        return values;
    }
}

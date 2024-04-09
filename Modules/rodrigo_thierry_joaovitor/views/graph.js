async function getSenders(){
    const response = await fetch('http://127.0.0.1:3001/grupo_rodrigo_thierry_joao/t1/enviados/list');
    const data = await response.json();
    return data;
}

async function getRelatorio(ip){
    const response = await fetch('http://127.0.0.1:3001/grupo_rodrigo_thierry_joao/t1/relatorio/simples/'+ip);
    const data = await response.json();
    return data;
}

async function convert(relatorios){
    const datas = []
    relatorios.forEach(relatorio => {
        const keys = Object.keys(relatorio.trafego);
        keys.forEach(key => {
            datas.push([relatorio.origem, key, relatorio.trafego[key]]);
        });
    });
    return datas;
}

async function maxTrafego(relatorios){
    const max = relatorios.reduce((acc, relatorio) => {
        const keys = Object.keys(relatorio.trafego);
        const max = keys.reduce((acc, key) => {
            if(relatorio.trafego[key] > acc){
                return relatorio.trafego[key];
            }
            return acc;
        }, 0);
        if(max > acc){
            return max;
        }
        return acc;
    }, 0);
    return max;
}

async function minTrafego(relatorios){
    const min = relatorios.reduce((acc, relatorio) => {
        const keys = Object.keys(relatorio.trafego);
        const min = keys.reduce((acc, key) => {
            if(relatorio.trafego[key] < acc){
                return relatorio.trafego[key];
            }
            return acc;
        }, 0);
        if(min < acc){
            return min;
        }
        return acc;
    }, 0);
    return min;
}


async function main(){
    var mychart = echarts.init(document.getElementById('graphContainer'));
    const ips = await getSenders();
    console.log(ips)

    const relatorios = await Promise.all(ips.map(ip => getRelatorio(ip)));
    console.log(relatorios);

    const data = await convert(relatorios);
    console.log(data);

    option = {
        tooltip: {
            position: 'top',
            trigger: 'item'
        },
        // grid: {
        //     height: '50%',
        //     top: '10%'
        // },
        xAxis: {
            type: 'category',
            data: ips,
            splitArea: {
            show: true
            }
        },
        yAxis: {
            type: 'category',
            data: ips,
            splitArea: { // fundo
            show: true
            }
        },
        visualMap: {
            min: await minTrafego(relatorios),
            max: await maxTrafego(relatorios),
            //calculable: true,
            orient: 'horizontal',
            left: 'center',
            bottom: '0%'
        },
        series: [
            {
            name: 'Trafego IPV4',
            type: 'heatmap',
            data: data,
            // oculta as escritas em cima
            // label: { 
            //     show: true
            // },
            emphasis: {
                itemStyle: {
                shadowBlur: 10,
                shadowColor: 'rgba(0, 0, 0, 0.5)'
                }
            }
            }
        ]
    };
      
    mychart.setOption(option);
}

main();

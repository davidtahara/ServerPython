import pyshark
from collections import Counter
from pyecharts.charts import Pie
from pyecharts import options as opts

# Função para ler o arquivo pcap e contar os métodos HTTP
def contar_metodos_http(file_path):
    cap = pyshark.FileCapture(file_path, keep_packets=False, display_filter='http.request.method')
    http_methods = []

    for pkt in cap:
        try:
            http_methods.append(pkt.http.request_method)
        except AttributeError:
            pass  # Pular pacotes que não são HTTP

    cap.close()
    return Counter(http_methods)

# Arquivo pcap de exemplo
pcap_file = 'http_witp_jpegs.pcap'

# Contar métodos HTTP no arquivo pcap
http_methods_count = contar_metodos_http(pcap_file)

# Preparar dados para o gráfico de pizza
labels = list(http_methods_count.keys())
data = list(http_methods_count.values())

# Construir gráfico de pizza com ECharts.js
pie_chart = (
    Pie()
    .add("", [list(z) for z in zip(labels, data)])
    .set_global_opts(title_opts=opts.TitleOpts(title="Distribuição de Métodos HTTP"))
    .set_series_opts(label_opts=opts.LabelOpts(formatter="{b}: {c}"))
)

# Salvar o gráfico como HTML
pie_chart.render("http_methods_pie_chart.html")

print("Gráfico gerado com sucesso. Verifique o arquivo http_methods_pie_chart.html.")

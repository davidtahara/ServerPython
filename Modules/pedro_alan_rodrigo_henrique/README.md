# Como executar o projeto

Esse projeto implementa um packet sniffer que descobre os ips da rede que mais estão gerando pacotes
e os ips públicos mais acessados na rede e também os países nos quais eles se localizam. O projeto faz
a análise da rede em tempo real, sem ler backups então para ao rodar o projeto é recomendado que esteja
conectado em alguma rede wifi e, se for o único que está acessando a rede, abrir um vídeo no youtube para
gerar alguns pacotes para testar. Inicialmente ao abrir o frontend talvez não tenham muitos dados mas ao longo
do tempo ele vai executando em background e acumulando os dados.

O projeto foi desenvolvido usando Ubuntu, é possível que no windows tenha algum passo que seja diferente para ser executado.

## Backend

O backend é feito usando fastapi, então é necessário baixar as dependências
listadas na documentação da biblioteca:

`pip install fastapi`

`pip install "uvicorn[standard]"`

Depois disso é possível rodar a aplicação executando os seguintes comandos a partir da raíz do projeto

`cd backend`

`sudo uvicorn main:app --reload`

OBS: sudo é necessário já que as funções do scapy precisar ser executados como admnistrador, talvez no windows isso signifique executar um terminal como admnistrador

OBS2: Para executar o projeto no windows precisei instalar o npcap e no instalador marcar opção que fala algo como "habilitar monitoramento para redes wifi 802.11"

## Frontend

O frontend é desenvolvido usando typescript e a bilbioteca do echarts.js, tentei usar o echarts como dependência do npm mas deu alguns problemas, então seguimos com o arquivo .js mesmo e só o @types dele pra não dar problema com o typescript.

OBS: USAR NPM, yarn da problema com o live server

Para instalar as dependências a partir da raíz do projeto:

`cd frontend`

`npm install`

Para compilar os arquivos ts:

`npm run build`

Para executar o live-server que entrega o arquivo .html

`npm run start`

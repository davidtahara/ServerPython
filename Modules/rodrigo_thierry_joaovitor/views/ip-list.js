const body = document.querySelector('body');


let data = null;

async function getSenders() {
    const response = await fetch('http://127.0.0.1:3001/grupo_rodrigo_thierry_joao/ip/enviados/list');
    const data = await response.json();
    const ul = document.getElementById('sidebar_ul');

    for (let i in data) {
        console.log(i)

        const li = document.createElement('li');

        // Set the text of the list item to the current address
        li.classList.add("nav-item")
        li.innerText = data[i];
        li.addEventListener('click', async function () {
            let conteiner = document.getElementById("headers");
            conteiner.innerHTML = '';
            await fetch('http://127.0.0.1:3001/grupo_rodrigo_thierry_joao/ip/enviados/' + data[i])
                .then(response => response.json())
                .then(data => {
                    for (let i in data) {
                        appendHeader(data[i])
                    }

                })
                .catch((error) => console.error('Error:', error));
        });

        // Append the list item to the unordered list
        ul.appendChild(li);
    }
    document.getElementById("sidebar").appendChild(ul);
}

getSenders();


function appendHeader(JSONobject) {

    let header_string = formatString(ip_header_template, JSONobject);


    let conteiner = document.getElementById("headers");
    conteiner.insertAdjacentHTML("beforeend", header_string);

    var test = {
        "version": 4,
        "headerLength": 5,
        "length": 60,
        "sourceIp": "192.168.69.1",
        "destinationIp": "192.168.69.2",
        "ttl": 64,
        "fragmentationId": 0,
        "flagMoreFragments": false,
        "flagDontFragment": true,
        "offset": 0,
        "headerChecksum": 12136,
        "service": 0,
        "protocol": "TCP",
        "uniqueId": "74c89bf6-d85a-42cd-9337-1ae63a87b52d"
    }
    console.log(JSONobject.version)
    console.log(JSONobject.headerLength)
    console.log(JSONobject.length)
    console.log(JSONobject.sourceIp)
    console.log(JSONobject.destinationIp)
    console.log(JSONobject.ttl)
    console.log(JSONobject.fragmentationId)
    console.log(JSONobject.flagMoreFragments)
    console.log(JSONobject.flagDontFragment)
    console.log(JSONobject.offset)
    console.log(JSONobject.headerChecksum)
    console.log(JSONobject.service)
    console.log(JSONobject.protocol)


}

//function to get an string with an IPv4 address and return it as a binary number

function IPv4ToBinary(address) {
    let binary = '';
    let octets = address.split('.');

    for (let i = 0; i < octets.length; i++) {
        let binaryOctet = parseInt(octets[i]).toString(2);

        while (binaryOctet.length < 8) {
            binaryOctet = '0' + binaryOctet;
        }

        binary += binaryOctet;
    }

    return binary;
}

console.log(IPv4ToBinary('192.168.100.100'));


/// -------------------------------------------------------------------

const ip_header_template = `<div class=\"row py-2\"> <div class=\"flexbox mg-3\" id=\"{0}\"> 
    <div class=\"tupla\">
        <div class=\"VER tooltip-container\">{version}
            <span class=\"tooltip-text\">Versão</span>
        </div>
        <div class=\"IHL tooltip-container\">{headerLength}<span class=\"tooltip-text\">Header Length</span></div>
        <div class=\"TOS tooltip-container\">{service}<span class=\"tooltip-text\">Type of Service</span></div>
        <div class=\"LEN tooltip-container\">{length}<span class=\"tooltip-text\">Length</span></div>
    </div>
    <div class=\"tupla\">
        <div class=\"ID tooltip-container\">{fragmentationId}<span class=\"tooltip-text\">Fragmentation ID</span></div>
        <div class=\"EVIL tooltip-container\">E<span class=\"tooltip-text\">EVIL BIT</span></div>
        <div class=\"DF tooltip-container\">{flagDontFragment}<span class=\"tooltip-text\">FLAG1</span></div>
        <div class=\"MF tooltip-container\">{flagMoreFragments}<span class=\"tooltip-text\">FLAG2</span></div>
        <div class=\"OFFSET tooltip-container\">{offset}<span class=\"tooltip-text\">Offset</span></div>
    </div>

    <div class=\"tupla\">
        <div class=\"TTL tooltip-container\">{ttl}<span class=\"tooltip-text\">Time to Live</span></div>
        <div class=\"PROTOCOL tooltip-container\">{protocol}<span class=\"tooltip-text\">Protocol</span></div>
        <div class=\"CHECKSUM tooltip-container\">{headerChecksum}<span class=\"tooltip-text\">Checksum</span> </div>
    </div>
    <div class=\"tupla\">
        <div class=\"SOURCE tooltip-container\">{sourceIp}<span class=\"tooltip-text\">Endereço de Origem</span> </div>
    </div>
    <div class=\"tupla\">
        <div class=\"DESTINATION tooltip-container\">{destinationIp}<span class=\"tooltip-text\">Endereço de Destino</span> </div>
    </div>
</div>
</div>
`;

const formatString = (template, args) => {
    return template.replace(/{([A-z]+)}/g, function (match, index) {
        console.log(match + " _ " + index)
        if (index === 'flagMoreFragments') {
            return args[index] ? "T" : "F";
        }
        if (index === 'flagDontFragment') {
            return args[index] ? "T" : "F";
        }

        return typeof args[index] === 'undefined' ? "notFound" : args[index];
    });
}

async function teste() {
    let a = await fetch('http://127.0.0.1:3001/grupo_rodrigo_thierry_joao/ip/enviados/2.1.1.2')
    let b = await a.json()
    document.getElementsByTagName("body")[0].innerHTML = formatString(ip_header_template, b[0])
    console.log(b[0])
}
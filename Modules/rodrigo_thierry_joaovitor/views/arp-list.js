const body = document.querySelector('body');


let data = null;

async function getSenders() {
    const response = await fetch('http://127.0.0.1:3001/grupo_rodrigo_thierry_joao/arp/enviados/list');
    const data = await response.json();
    const ul = document.getElementById('sidebar_ul');

    for (let i in data) {
        const ip = data[i][0];
        const mac = data[i][1];

        const li = document.createElement('li');

        // Set the text of the list item to the current address
        li.classList.add("nav-item")
        li.innerText = ip +" - "+ mac;
        li.addEventListener('click', async function () {
            let conteiner = document.getElementById("headers");
            conteiner.innerHTML = '';
            await fetch('http://127.0.0.1:3001/grupo_rodrigo_thierry_joao/arp/enviados/' + data[i][0])
                .then(response => response.json())
                .then(data => {
                    console.log(data)
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

    console.log(JSONobject)
    let header_string = formatString(arp_header_template, JSONobject);


    let conteiner = document.getElementById("headers");
    conteiner.insertAdjacentHTML("beforeend", header_string);
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


/// -------------------------------------------------------------------

const arp_header_template = `<div class=\"row py-2\" <div class=\"flexbox mg-3\" id=\"{0}\"> 
    <div class=\"tupla\">
        <div class=\"HARDWARE_TYPE tooltip-container\">{hardwareType}
            <span class=\"tooltip-text\">Hardware Type</span>
        </div>
        <div class=\"PROTOCOL_TYPE tooltip-container\">{protocolType}
            <span class=\"tooltip-text\">Protocol Type</span>
        </div>
    </div>
    <div class=\"tupla\">
        <div class=\"HARDWARE_LEN tooltip-container\">{hardwareLength}
            <span class=\"tooltip-text\">Hardware Length</span>
        </div>
        <div class=\"PROTOCOL_LEN tooltip-container\">{protocolLength}
            <span class=\"tooltip-text\">Protocol Length</span>
        </div>
        <div class=\"OPERATION tooltip-container\">{operation}
            <span class=\"tooltip-text\">Operation</span>
        </div>
    </div>

    <div class=\"tupla\">
        <div class=\"SENDER_HARDWARE_ADDRESS tooltip-container\">
            {sourceMac}
            <br>
            ({sourceVendor})
            <span class=\"tooltip-text\">Sender Hardware Address</span>
        </div>
    </div>
    <div class=\"tupla\">
        <div class=\"SENDER_PROTOCOL_ADDRESS tooltip-container\">{sourceIp}
            <span class=\"tooltip-text\">Sender Protocol Address</span>
        </div>
    </div>
    <div class=\"tupla\">
        <div class=\"TARGET_HARDWARE_ADDRESS tooltip-container\">
            {targetMac}
            <br>
            ({targetVendor})
            <span class=\"tooltip-text\">Target Hardware Address</span>
        </div>
    </div>
    <div class=\"tupla\">
        <div class=\"TARGET_PROTOCOL_ADDRESS tooltip-container\">
            {targetIp}
            <span class=\"tooltip-text\">Target Protocol Address</span>
        </div>
    </div>
</div>
</div>
`;

const formatString = (template, args) => {
    console.log(args)
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

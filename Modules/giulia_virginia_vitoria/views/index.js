function openTab(evt, tabName) {
    var i, tabcontent, tablinks;

    // Esconde todo o conteúdo das abas
    tabcontent = document.getElementsByClassName("tabcontent");
    for (i = 0; i < tabcontent.length; i++) {
        tabcontent[i].style.display = "none";
    }

    // Remove a classe "active" de todos os botões de abas
    tablinks = document.getElementsByClassName("tablinks");
    for (i = 0; i < tablinks.length; i++) {
        tablinks[i].className = tablinks[i].className.replace(" active", "");
    }

    // Mostra a aba atual e adiciona a classe "active" ao botão da aba
    document.getElementById(tabName).style.display = "block";
    evt.currentTarget.className += " active";
}

// Abre a primeira aba por padrão
document.addEventListener('DOMContentLoaded', (event) => {
    document.querySelector('.tab button').click();
});

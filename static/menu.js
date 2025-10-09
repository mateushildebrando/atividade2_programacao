function mostrarMenu() {
    const menu = document.querySelector(".menu-opcoes");
    menu.style.display = "block";
}

function ocultarMenu() {
    const menu = document.querySelector(".menu-opcoes");
    menu.style.display = "none";
}

document.addEventListener("DOMContentLoaded", function () {
    const botao = document.querySelector(".menu-titulo");
    const menu = document.querySelector(".menu-opcoes");

    if (botao && menu) {
        botao.addEventListener("click", function (e) {
            e.stopPropagation();
            if (menu.style.display === "block") {
                ocultarMenu();
            } else {
                mostrarMenu();
            }
        });

        document.addEventListener("click", function () {
            ocultarMenu();
        });

        menu.addEventListener("click", function (e) {
            e.stopPropagation();
        });
    }
});
// Control de deslizar (slider)
const slider = document.querySelector('.slider-container');
let isDown = false;
let startX;
let scrollLeft;

slider.addEventListener('mousedown', (e) => {
    isDown = true;
    slider.classList.add('active');
    startX = e.pageX - slider.offsetLeft;
    scrollLeft = slider.scrollLeft;
});

slider.addEventListener('mouseleave', () => {
    isDown = false;
    slider.classList.remove('active');
});

slider.addEventListener('mouseup', () => {
    isDown = false;
    slider.classList.remove('active');
});

slider.addEventListener('mousemove', (e) => {
    if (!isDown) return;
    e.preventDefault();
    const x = e.pageX - slider.offsetLeft;
    const walk = (x - startX) * 2; // Velocidad de desplazamiento
    slider.scrollLeft = scrollLeft - walk;
});

window.onload = function() {
    // Comprobar si el parámetro success=true está presente en la URL
    if (window.location.search.includes("success=true")) {
        mostrarPopup(); // Mostrar el pop-up
    }

    // Cerrar el pop-up al hacer clic en el botón de cerrar
    document.querySelector(".popup-close").addEventListener("click", function() {
        cerrarPopup(); // Cerrar el pop-up cuando se haga clic en el botón
    });
};

function mostrarPopup() {
    var popup = document.getElementById("popup");
    popup.style.display = "flex"; // Hacerlo visible para que la transición se pueda ejecutar

    // Agregar la clase 'show' para activar la animación de opacidad
    setTimeout(function() {
        popup.classList.add("show"); // Añadir clase show para hacer el pop-up opaco
    }, 100);

    // Después de 3 segundos, hacer que el pop-up se desvanezca
    setTimeout(function() {
        popup.style.transition = "opacity 2s ease-out"; // Cambio en la transición para que el fade-out ocurra
        popup.classList.remove("show"); // Remover clase show para reducir la opacidad
    }, 3000); // Espera 3 segundos antes de empezar a desvanecerse

    // Después de 5 segundos (cuando la animación haya terminado), ocultar el pop-up
    setTimeout(function() {
        popup.style.display = "none"; // Ocultar el pop-up
    }, 5000); // Después de 5 segundos, se oculta completamente
}
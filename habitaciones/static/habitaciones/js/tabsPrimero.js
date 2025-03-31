
function cargarDatos(tabContentId, url) {
    const contenedor = document.getElementById(tabContentId);
    // Si el contenedor está vacío, carga los datos
    // console.log("1111")
    if (contenedor && contenedor.childElementCount === 0) {
        // console.log("222")
        fetch(url)
            .then(response => {
                if (!response.ok) {
                    throw new Error('Error al cargar la lista de Tipos de Habitaciones' + response);
                }
                return response.text();
            })
            .then(html => {
                // console.log("3333")
                contenedor.innerHTML = html;  // Inserta el HTML en el contenedor
            })
            .catch(error => console.error('Error:', error));
    }
}

function galeriaFotos() {
    const inputFotos = document.getElementById("id_nuevas_fotos");
    const btnAgregarFoto = document.getElementById("btn-agregar-foto");
    const galeria = document.getElementById("galeria-fotos");
    const fotosSeleccionadasInput = document.getElementById("id_fotos_seleccionadas");
    let fotosSeleccionadas = new Set();

    // ABRIR EXPLORADOR DE ARCHIVOS
    btnAgregarFoto.addEventListener("click", () => inputFotos.click());

    // AGREGAR IMÁGENES A LA GALERÍA (evita duplicaciones)
    inputFotos.addEventListener("change", function () {
        [...inputFotos.files].forEach(file => {
            const reader = new FileReader();
            reader.onload = e => {
                if (![...galeria.children].some(img => img.dataset.src === e.target.result)) { 
                    const divFoto = document.createElement("div");
                    divFoto.classList.add("p-1", "border", "rounded");
                    divFoto.dataset.id = "nuevo-" + Date.now();
                    divFoto.dataset.src = e.target.result; // Evita duplicados

                    divFoto.innerHTML = `<img src="${e.target.result}" class="img-thumbnail img-miniatura">`;
                    galeria.appendChild(divFoto);

                    fotosSeleccionadas.add(divFoto.dataset.id);
                    actualizarSeleccionadas();
                }
            };
            reader.readAsDataURL(file);
        });

        inputFotos.value = ""; // LIMPIA el input para evitar que el mismo archivo se duplique
    });

    // SELECCIONAR Y DESELECCIONAR FOTOS (funciona desde el primer clic)
    galeria.addEventListener("click", function (event) {
        const foto = event.target.closest("div");
        if (!foto) return;

        const id = foto.dataset.id;
        if (fotosSeleccionadas.has(id)) {
            fotosSeleccionadas.delete(id);
            foto.classList.remove("border-primary");
        } else {
            fotosSeleccionadas.add(id);
            foto.classList.add("border-primary");
        }

        actualizarSeleccionadas();
    });

    function actualizarSeleccionadas() {
        fotosSeleccionadasInput.value = [...fotosSeleccionadas].join(",");
    }
}

document.addEventListener('DOMContentLoaded', function () {
    // Cargar los datos de las habitaciones al iniciar la página
    cargarDatos('tablaHabitaciones', '/habitaciones/lista/');
    document.querySelectorAll('.nav-link').forEach(tab => {
        tab.addEventListener('click', function (event) {
            const targetTab = event.target.getAttribute('aria-controls');
            // Determina qué tab se ha clickeado y carga los datos correspondientes
            if (targetTab === 'habitaciones') {
                cargarDatos('habitacion-lista', '/habitaciones/lista/');
            } else if (targetTab === 'tipos-habitacion') {
                cargarDatos('tipos-habitacion-content', '/tipos-habitacion/lista/');
            } else if (targetTab === 'servicios-habitacion') {
                cargarDatos('servicios-habitacion-content', '/servicios-habitacion/lista/');
            }
        });
    });

    // Evento delegado para el modal de servicios de habitación
    document.body.addEventListener('click', function (event) {
        if (event.target.matches('#tipos-habitacion-agregar')) {
            cargarDatos('form-tipo-hab', '/tipos-habitacion/crear/');
            galeriaFotos();
        }
        // if (event.target.matches('#btn-agregar-foto')) {
        //     console.log("entra")
        //     galeriaFotos();
        // }
    });
});


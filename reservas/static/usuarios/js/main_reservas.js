import { cargarContenidoModal, deshabilitarRegistro } from "/static/js/main.js";

document.addEventListener('DOMContentLoaded', function () {
    // Evento delegado para las ventanas modales
    document.body.addEventListener('click', function (event) {
        const btn = event.target.closest('[data-url]'); // Encuentra el elemento más cercano con data-url
        if (!btn) return;

        const content = btn.getAttribute('data-content');
        const url = btn.getAttribute('data-url');

        if (btn.id===("huesped-agregar") || btn.id===("huesped-editar")){
            cargarContenidoModal(content, url)
        }

        else if(btn.id===("huesped-eliminar")){
            deshabilitarRegistro(content,url);
        }
    });
});


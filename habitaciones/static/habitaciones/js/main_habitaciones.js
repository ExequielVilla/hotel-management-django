import { cargarContenidoModal, deshabilitarRegistro } from "/static/js/main.js";
import { initTipoHab } from './tipo_habitacion.js';
import { initServicioHab } from './servicio_habitacion.js';



document.addEventListener('DOMContentLoaded', function () {
    // Evento delegado para las ventanas modales
    document.body.addEventListener('click', function (event) {
        const btn = event.target.closest('[data-url]'); // Encuentra el elemento más cercano con data-url
        if (!btn) return;

        const content = btn.getAttribute('data-content');
        const url = btn.getAttribute('data-url');

        if (btn.id===("habitacion-agregar") || btn.id===("habitacion-editar")){
            cargarContenidoModal(content, url)
        }

        else if (btn.id==="tipo-habitacion-agregar" || btn.id==="tipo-habitacion-editar") {
            cargarContenidoModal(content, url)
                .then(() => {
                    initTipoHab();
                })
        }

        else if (btn.id===("servicio-habitacion-agregar") || btn.id===("servicio-habitacion-editar")){
            cargarContenidoModal(content, url)
            .then(() => {
                initServicioHab();
            })
        }

        else if(btn.id===("tipo-habitacion-eliminar") || btn.id===("servicio-habitacion-eliminar") || btn.id===("habitacion-eliminar")){
            deshabilitarRegistro(content,url);
        }
    });
});


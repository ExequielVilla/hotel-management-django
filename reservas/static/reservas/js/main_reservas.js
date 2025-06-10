import { cargarContenidoModal, deshabilitarRegistro } from "/static/js/main.js";

document.addEventListener('DOMContentLoaded', function () {
    // Evento delegado para las ventanas modales
    document.body.addEventListener('click', function (event) {
        const btn = event.target.closest('[data-url]'); // Encuentra el elemento más cercano con data-url
        if (!btn) return;

        const content = btn.getAttribute('data-content');
        const url = btn.getAttribute('data-url');

        if (btn.id===("reserva-agregar") || btn.id===("reserva-editar")){
            cargarContenidoModal(content, url)
        }

        else if(btn.id===("reserva-eliminar")){
            deshabilitarRegistro(content,url);
        }
    });

    // Cancelar reserva
    const modalCancelar = document.getElementById('reserva-modal-cancelar');
    const formCancelar = document.getElementById('form-cancelar-reserva');
    const spanHuesped = document.getElementById('cancelar-huesped-nombre');
    modalCancelar.addEventListener('show.bs.modal', function (event) {
        const button = event.relatedTarget;
        const url = button.getAttribute('data-url');
        const huesped = button.getAttribute('data-huesped');

        formCancelar.action = url;
        spanHuesped.textContent = huesped;
    });

    // Pago de reserva pendiente
    const pagoModal = document.getElementById('pago-modal');
    if (pagoModal) {
        pagoModal.addEventListener('show.bs.modal', function(event) {
            const button = event.relatedTarget;
            const modal = this;
            
            // Actualiza los datos del formulario
            document.getElementById('reserva-id-pago').value = button.getAttribute('data-reserva-id');
            document.getElementById('monto-pago').value = button.getAttribute('data-monto');
            
            // Configura el envío AJAX del formulario
            const form = modal.querySelector('#form-pago-reserva');
            form.addEventListener('submit', function(e) {
                e.preventDefault();
                
                fetch(form.action, {
                    method: 'POST',
                    body: new FormData(form),
                    headers: {
                        'X-Requested-With': 'XMLHttpRequest'
                    }
                })
                .then(response => response.json())
                .then(data => {
                    if (data.success) {
                        window.location.reload(); // Recarga la página tras éxito
                    } else {
                        alert('Error: ' + JSON.stringify(data.errors));
                    }
                });
            });
        });
    }

    const btnTabla = document.getElementById('btn-vista-tabla');
    const btnAgenda = document.getElementById('btn-vista-agenda');
    const vistaTabla = document.getElementById('reserva-lista');
    const vistaAgenda = document.getElementById('reserva-calendario');
    btnTabla.addEventListener('click', () => {
        btnTabla.classList.add('active');
        btnAgenda.classList.remove('active');
        vistaTabla.classList.remove('d-none');
        vistaAgenda.classList.add('d-none');
    });
    btnAgenda.addEventListener('click', () => {
        btnAgenda.classList.add('active');
        btnTabla.classList.remove('active');
        vistaAgenda.classList.remove('d-none');
        vistaTabla.classList.add('d-none');
        setTimeout(() => {
            calendar.render();
            calendar.updateSize();
        }, 1);
    });
    // Inicializar el calendario solo si no existe
    if (!window.calendar) {
        window.calendar = new FullCalendar.Calendar(vistaAgenda, {
            initialView: 'dayGridMonth',
            locale: 'es',
            headerToolbar: {
                left: 'prev next today',
                center: 'title',
                right: 'dayGridMonth,dayGridWeek'
            },
            events: '/reservas/calendario-api/',
            eventColor: '#FFFFFF',
            eventDidMount: function(info) {
                const estado = info.event.extendedProps.estado;
                if (estado === 'Pendiente') info.el.style.backgroundColor = ' #8d6606';
                else if (estado === 'Confirmada') info.el.style.backgroundColor = ' #114a15';
                else if (estado === 'En curso') info.el.style.backgroundColor = ' #2744ae';
                else if (estado === 'Cancelada') info.el.style.backgroundColor = ' #620f17';
                else if (estado === 'Finalizada') info.el.style.backgroundColor = ' #6c757d';
            }
        });
        calendar.render();
    }

    // Vista tabla vs agenda
    // Inicializar calendario
});


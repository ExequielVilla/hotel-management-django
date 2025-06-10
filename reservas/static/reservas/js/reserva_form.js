import { getCookie } from "/static/js/main.js";
import { reserva_form_validacion } from "/static/reservas/js/reserva_form_validacion.js";

document.addEventListener("DOMContentLoaded", function () {
    const checkInInput = document.getElementById("id_fecha_check_in_esperada");
    const checkOutInput = document.getElementById("id_fecha_check_out_esperada");
    const nochesDisplay = document.getElementById("noches");
    const cantidadHuespedesInput = document.getElementById('id_cantidad_huespedes');

    const huespedSeleccionado = document.getElementById("huesped-seleccionado");
    const habitacionesDisponiblesContainer = document.getElementById('tipos-habitaciones-disponibles');

    const resumenReserva = document.getElementById('resumen-reserva');

    // Calcula la cantidad de noches entre el checkin y checkout
    function calcularNoches() {
        const checkIn = new Date(checkInInput.value);
        const checkOut = new Date(checkOutInput.value);
        if (!isNaN(checkIn) && !isNaN(checkOut) && checkOut > checkIn) {
            const noches = Math.ceil((checkOut - checkIn) / (1000 * 60 * 60 * 24));
            nochesDisplay.textContent = noches;
        } else {
            nochesDisplay.textContent = "0";
        }
    }

    // carga las habitacines (tipos de habitaciones) disponibles
    async function cargarTiposDisponibles() {
        const checkIn = new Date(checkInInput.value).toISOString().split('T')[0];
        const checkOut = new Date(checkOutInput.value).toISOString().split('T')[0];
        const cantidadHuespedes = cantidadHuespedesInput.value;

        // Validación simple
        if (!checkIn || !checkOut || !cantidadHuespedes || cantidadHuespedes <= 0) {
            habitacionesDisponiblesContainer.innerHTML = '';
            return;
        }

        const url = `/reservas/tipo-habitacion-disponibilidad/?check_in=${checkIn}&check_out=${checkOut}&cantidad_huespedes=${cantidadHuespedes}`;
        try {
            const response = await fetch(url);
            const html = await response.text();
            habitacionesDisponiblesContainer.innerHTML = html;
        } catch (error) {
            console.error("Error al obtener habitaciones disponibles:", error);
            habitacionesDisponiblesContainer.innerHTML = "<p class='text-danger'>Ocurrió un error al cargar las habitaciones disponibles.</p>";
        }
    }

    // Formatea un precio a monedaARG
    const formatoPrecioArg = new Intl.NumberFormat('es-AR', {
        style: 'currency',
        currency: 'ARS',
        minimumFractionDigits: 2,
        maximumFractionDigits: 2,
    });

    // Acualiza el resumen de habitaciones
    async function actualizarResumenHabitaciones() {
        const inputsCantidad = document.querySelectorAll('.input-tipo-habitacion');
        const detalleHabitaciones = document.getElementById('detalle-habitaciones');
        const subtotalHabitaciones = document.getElementById('subtotal-habitaciones');

        let htmlDetalle = '';
        let subtotal = 0;
        let habitacionesSeleccionadas = [];
        inputsCantidad.forEach(input => {
            const cantidad = parseInt(input.value) || 0;
            if (cantidad > 0) {
                // Encuentra la tarjeta padre para obtener los detalles de la habitación
                const card = input.closest('.card');
                const nombre = card.dataset.nombre;
                const precio = parseFloat(card.dataset.precio);

                const totalHabitacion = precio * cantidad;
                subtotal += totalHabitacion;
                const totalHabitacionStr = formatoPrecioArg.format(totalHabitacion);

                htmlDetalle += `
                    <div class="d-flex justify-content-between mb-3">
                        <span>${cantidad} ${nombre}</span>
                        <span>${totalHabitacionStr}</span>
                    </div>
                `;
                habitacionesSeleccionadas.push({ // Agrega objeto a la lista
                    cantidad: cantidad,
                    nombre: nombre,
                    totalHabitacion: totalHabitacion,
                    totalHabitacion_str: formatoPrecioArg.format(totalHabitacion),
                });
            }
        });

        // Rellena el resumen de Reserva del final
        if (htmlDetalle){
            detalleHabitaciones.innerHTML = htmlDetalle
            const subtotalStr = formatoPrecioArg.format(subtotal);
            subtotalHabitaciones.textContent = subtotal > 0 ? `Subtotal: ${subtotalStr}` : '';
            const checkIn = new Date(checkInInput.value).toISOString().split('T')[0];
            const checkOut = new Date(checkOutInput.value).toISOString().split('T')[0];
            const noches = parseInt(nochesDisplay.textContent);
            const cantidadHuespedes = cantidadHuespedesInput.value
            const datosReserva = {
                check_in: checkIn,
                check_out: checkOut,
                noches: noches,
                cantidad_huespedes: cantidadHuespedes,
                habitaciones_seleccionadas: habitacionesSeleccionadas,
                total: subtotal,
                total_str: formatoPrecioArg.format(subtotal),
            };
            const url = `/reservas/resumen-reserva/`;
            try {
                const response = await fetch(url, {
                    method: "POST",
                    body: JSON.stringify(datosReserva),
                    headers: {
                        "Content-Type": "application/json",
                        "X-CSRFToken": getCookie("csrftoken"),
                    },
                });
                const html = await response.text();
                resumenReserva.innerHTML = html;
                document.getElementById("id_total_reserva").value = subtotal;
            } catch (error) {
                console.error("Error al obtener el resumen HTML:", error);
                resumenReserva.innerHTML = "<p class='text-danger'>No se pudo cargar el resumen.</p>";
            }
        }
        else
            detalleHabitaciones.innerHTML = '<p class="text-muted">No hay habitaciones seleccionadas</p>';
    }

    // Rellena los campos de husped al seleccionar un huesped
    async function cargarHuesped(huespedId) {
        const nombre = document.getElementById("id_nombre");
        const apellido = document.getElementById("id_apellido");
        const dni_pasaporte = document.getElementById("id_dni_pasaporte");
        const email = document.getElementById("id_email");
        const telefono = document.getElementById("id_telefono");
        const preferencias = document.getElementById("id_preferencias")

        if(!huespedId){
            nombre.value = "";
            apellido.value = "";
            dni_pasaporte.value = "";
            email.value = "";
            telefono.value = "";
            preferencias.value = "";
        }
        else{
            try {
                const response = await fetch(`/huesped/json/${huespedId}/`);
                const data = await response.json();
                if (data.error) {
                    console.error("Error:", data.error);
                }
                // Autocompletamos los campos
                nombre.value = data.nombre;
                apellido.value = data.apellido;
                dni_pasaporte.value = data.dni_pasaporte;
                email.value = data.email;
                telefono.value = data.telefono;
                preferencias.value = data.preferencias;
            } catch (error) {
                console.error("Error al obtener huésped:", error);
            }
        }
    }

    // Cambios en Datos de Alojamiento
    checkInInput.addEventListener("change", calcularNoches);
    checkOutInput.addEventListener("change", calcularNoches);
    calcularNoches();
    [checkInInput, checkOutInput, cantidadHuespedesInput].forEach(input => {
        input.addEventListener('change', cargarTiposDisponibles);
    });
    cargarTiposDisponibles();
    document.addEventListener('change', function(e) {
        if (e.target && e.target.matches('.input-tipo-habitacion')) {
            actualizarResumenHabitaciones();
        }
    });

    // Cambios en Datos del Huesped
    $('.select2').select2();
    $('.select2').on('select2:open', () => {
        document.querySelector('.select2-search__field').focus();
    });
    $('#huesped-seleccionado').on('select2:select', function (e) {
        const selectedId = e.params.data.id;
        cargarHuesped(selectedId);
    });

    // Codigo de Validación del formulario
    reserva_form_validacion();
});
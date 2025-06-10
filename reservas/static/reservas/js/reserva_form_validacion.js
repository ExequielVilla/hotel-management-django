export async function reserva_form_validacion() {
    document.getElementById('form-reserva').addEventListener('submit', async function(e) {
        e.preventDefault(); // Prevenir envío normal
        const form = document.getElementById('form-reserva');
        const formData = new FormData(form);

        const tipos_hab_seleccionadas = [];
        document.querySelectorAll('.input-tipo-habitacion').forEach(input => { // Seleccionar TODOS los inputs de clase input-tipo-habitacion
            const cantidad = parseInt(input.value);
            if (cantidad > 0) {
                const tipoHabId = input.id.split('-')[2]; // Extraer el ID del tipo de habitación (ej: "tipo-habitacion-3" → 3)
                tipos_hab_seleccionadas.push({
                    tipo_hab_id: tipoHabId,
                    cantidad: cantidad
                });
            }
        });
        //$('#huesped-seleccionado').trigger('change');
        formData.append('tipos_hab_seleccionadas', JSON.stringify(tipos_hab_seleccionadas));
        const metodoPago = document.getElementById('id_metodo_pago');
        if (metodoPago) {
            formData.set('metodo_pago', metodoPago.value);
        }
        for (let [key, value] of formData.entries()) {
            console.log(key, value);
        }
        const url = `/reservas/crear/`;
        try {
            fetch(url, {
                method: "POST",
                body: formData,
                headers: {
                    "X-CSRFToken": getCookie2("csrftoken"),
                },
            })
            .then(response => {
                if (response.ok) {
                    return response.json().then(data => {
                        if (data.success) {
                            // Opción 1: Redirigir directamente
                            window.location.href = data.redirect_url;
                            
                            // Opción 2: Mostrar mensaje y luego redirigir (mejor UX)
                            Swal.fire({
                                title: 'Éxito',
                                text: data.message,
                                icon: 'success'
                            }).then(() => {
                                window.location.href = data.redirect_url;
                            });
                        } else {
                            throw new Error(data.message || 'Error desconocido');
                        }
                    });
                } else {
                    return response.json().then(errData => {
                        throw new Error(errData.error || 'Error en el servidor');
                    });
                }
            })
            .catch(error => {
                Swal.fire({
                    title: 'Error',
                    text: error.message,
                    icon: 'error'
                });
                console.error('Error:', error);
            });
        } catch (error) {
            alert("Error" + error.message);
        }
    });
}

function getCookie2(name) {
    return document.cookie.split(';')
        .find(c => c.trim().startsWith(`${name}=`))
        ?.split('=')[1];
}

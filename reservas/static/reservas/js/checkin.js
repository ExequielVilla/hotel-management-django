import { getCookie } from "/static/js/main.js";

document.addEventListener('DOMContentLoaded', () => {
    const modal = document.getElementById('checkin-modal-registrar');
    const form = document.getElementById('form-checkin-registrar');
    const huespedNombre = document.getElementById('huesped-nombre');

    modal.addEventListener('show.bs.modal', function (event) {
        const button = event.relatedTarget;
        const url = button.getAttribute('data-url');
        const huesped = button.getAttribute('data-huesped');

        form.action = url;
        huespedNombre.textContent = huesped;
    });
    form.addEventListener('submit', async function (e) {
        e.preventDefault();
        const url = form.action;
        console.log(url);

        try {
            const response = await fetch(url, {
                method: 'POST',
                headers: {
                    'X-CSRFToken': getCookie('csrftoken'),
                    'X-Requested-With': 'XMLHttpRequest'
                }
            });

            const data = await response.json();

            const modalInstance = bootstrap.Modal.getInstance(modal);
            modalInstance.hide();

            Swal.fire({
                icon: data.success ? 'success' : 'error',
                title: data.success ? 'Check-in exitoso' : 'Error',
                text: data.message,
                timer: 2000,
                showConfirmButton: false
            });

            if (data.success) {
                setTimeout(() => location.reload(), 2000);
            }
        } catch (error) {
            console.error('Error en el check-in:', error);
            Swal.fire({
                icon: 'error',
                title: 'Error no se pudo realizar el checkin',
                text: 'No se pudo completar el check-in',
            });
        }
    });
});
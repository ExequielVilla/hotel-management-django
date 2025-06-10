document.addEventListener('DOMContentLoaded', () => {
    const modal = document.getElementById('checkout-modal-registrar');
    const form = document.getElementById('form-checkout-registrar');
    const huespedNombre = document.getElementById('huesped-nombre');

    modal.addEventListener('show.bs.modal', function (event) {
        const button = event.relatedTarget;
        const url = button.getAttribute('data-url');
        const huesped = button.getAttribute('data-huesped');

        form.action = url;
        huespedNombre.textContent = huesped;
    });
});

export async function cargarContenidoModal(contenedorId, url) {
    if (!contenedorId || !url) {
        throw new Error('Parámetros inválidos');
    }
    const contenedor = document.getElementById(contenedorId);
    if (!contenedor) {
        throw new Error(`Contenedor no encontrado: ${contenedorId}`);
    }

    contenedor.innerHTML = '';
    const response = await fetch(url);
    if (!response.ok) {
        throw new Error(`Error HTTP: ${response.status}`);
    }
    contenedor.innerHTML = await response.text();
}

export function deshabilitarRegistro(formId, url) {
    const formEliminar = document.getElementById(formId);
    if (!formEliminar) {
        console.warn(`Formulario no encontrado: ${formId}`);
        return;
    }
    formEliminar.action = url;
}

export function getCookie(name) {
    return document.cookie.split(';')
        .find(c => c.trim().startsWith(`${name}=`))
        ?.split('=')[1];
}

export function SweetAlert2PopUp(classname) {
    const botones = document.querySelectorAll(`.${classname}`);
    botones.forEach(btn => {
        btn.addEventListener("click", () => {
            fetch(btn.dataset.url, {
                method: "POST",
                headers: {
                    "X-CSRFToken": getCookie("csrftoken"),
                    "X-Requested-With": "XMLHttpRequest"
                }
            })
            .then(res => res.json())
            .then(data => {
                Swal.fire({
                    icon: data.success ? 'success' : 'error',
                    title: data.success ? 'Éxito' : 'Error',
                    text: data.message,
                    timer: 1500,
                    showConfirmButton: false
                });
                if (data.success) setTimeout(() => location.reload(), 1500);
            });
        });
    });
}
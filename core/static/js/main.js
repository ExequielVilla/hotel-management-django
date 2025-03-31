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

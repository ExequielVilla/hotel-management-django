import { fetchData } from './fetch_untils.js';

export function initTabs() {
    const tabLinks = document.querySelectorAll('.nav-link');

    tabLinks.forEach(tab => {
        tab.addEventListener('click', async function (event) {
            const targetTab = event.target.getAttribute('aria-controls');
            const urlMap = {
                'habitaciones': '/habitaciones/lista/',
                'tipos-habitacion': '/tipos-habitacion/lista/',
                'servicios-habitacion': '/servicios-habitacion/lista/'
            };

            const url = urlMap[targetTab];
            if (url) {
                const tabContentId = `${targetTab}-content`;
                await cargarDatos(tabContentId, url);
            }
        });
    });
}

async function cargarDatos(tabContentId, url) {
    const contenedor = document.getElementById(tabContentId);
    if (contenedor && contenedor.childElementCount === 0) {
        try {
            const html = await fetchData(url);
            contenedor.innerHTML = html;
        } catch (error) {
            console.error('Error al cargar datos:', error);
        }
    }
}
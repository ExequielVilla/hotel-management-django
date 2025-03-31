// Función para inicializar el modal de servicios
export function initServicioHab() {
    const iconContainer = document.querySelector(".icon-container");
    const searchInput = document.getElementById("busqueda");
    const selectedIconInput = document.getElementById("icono-seleccionado");
    
    // Filtrar iconos en tiempo real sin reescribir el HTML
    searchInput.addEventListener("input", () => {
        const filter = searchInput.value.toLowerCase();
        document.querySelectorAll(".icon-option").forEach(option => {
            const icon = option.getAttribute("data-icono");
            option.style.display = icon.includes(filter) ? "block" : "none";
        });
        console.log(selectedIconInput.value)
    });
    
    // Seleccionar icono
    document.querySelectorAll(".icon-option").forEach(option => {
        option.addEventListener("click", () => {
            selectedIconInput.value = option.getAttribute("data-icono");
            document.querySelectorAll(".icon-option").forEach(el => el.classList.remove("selected"));
            option.classList.add("selected");
            console.log(selectedIconInput.value)
        });
    
        // Marcar como seleccionado si es el icono guardado
        if (option.getAttribute("data-icono") === selectedIconInput.value) {
            option.classList.add("selected");
            console.log(selectedIconInput.value)
        }
        
    });



    const formContainer = document.getElementById("form-container"); // Contenedor donde está el formulario

    // PARA MANEJAR VALIDACIONES EN EL FORMULARIO
    // formContainer.addEventListener("submit", function (event) {
    //     event.preventDefault();

    //     const form = event.target;
    //     const formData = new FormData(form);

    //     fetch(form.action, {
    //         method: "POST",
    //         body: formData,
    //         headers: { "X-Requested-With": "XMLHttpRequest" }
    //     })
    //     .then(response => response.json())
    //     .then(data => {
    //         if (data.success) {
    //             alert("Servicio guardado correctamente.");
    //             window.location.reload();
    //         } else {
    //             formContainer.innerHTML = data.form_html; // Reemplaza el formulario con los errores
    //         }
    //     })
    //     .catch(error => console.error("Error en la solicitud:", error));
    // });
}
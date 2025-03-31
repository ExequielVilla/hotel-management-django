export function initTipoHab() {
    
    const inputFotos = document.getElementById("id_nuevas_fotos");
    const btnAgregarFoto = document.getElementById("btn-agregar-foto");
    const mensajeSinFotos = document.getElementById("mensaje-sin-fotos")
    const galeria = document.getElementById("galeria-fotos");
    const fotosSeleccionadasInput = document.getElementById("fotos-seleccionadas");
    let fotosSeleccionadas = new Set(
        (fotosSeleccionadasInput.dataset.seleccionadas || "")
            .split(",")
            .filter(id => id) // Filtra valores vacíos
            .map(id => Number(id)) // Convierte cada cadena a número
    );
    fotosSeleccionadasInput.value = Array.from(fotosSeleccionadas).join(","); // Refleja los valores en el input hidden

    // Abrir explorador de archivos
    btnAgregarFoto?.addEventListener("click", () => inputFotos?.click());

    // Subir y mostrar imágenes al seleccionar archivos - Func. boton Agregar Foto
    inputFotos?.addEventListener("change", async function () {
        const files = Array.from(inputFotos.files);
        if (files.length === 0) return;

        const formData = new FormData();
        files.forEach((file, index) => {
            formData.append("fotos", file); 
        })
        try {
            const csrftoken = document.querySelector('[name=csrfmiddlewaretoken]').value;
            const response = await fetch("/subir-foto/", {
                method: "POST",
                body: formData,
                headers: {
                    "X-CSRFToken": csrftoken
                }
            });

            if (!response.ok) {
                throw new Error("Error al subir las fotoss");
            }
            const data = await response.json();
            if (data.fotos) {
                data.fotos.forEach(foto => {
                    const divFoto = document.createElement("div");
                    divFoto.classList.add("p-1", "border", "rounded");
                    divFoto.dataset.id = foto.id;

                    divFoto.innerHTML = `<img src="${foto.url}" class="img-thumbnail img-miniatura border-0 p-0">`;
                    galeria.appendChild(divFoto);
                    if(mensajeSinFotos)
                        mensajeSinFotos.remove()
                    // Agregar a las fotos seleccionadas
                    fotosSeleccionadas.add(foto.id);
                    divFoto.classList.add("border-primary", "border-3");
                    fotosSeleccionadasInput.value = Array.from(fotosSeleccionadas).join(",");
                });
            }
        } catch (error) {
            alert("EError al subir las fotos: " + error.message);
        } finally {
            inputFotos.value = "";  // Limpiar el input de archivos
        }
    });


    // Seleccionar y deseleccionar fotos
    galeria?.addEventListener("click", (event) => {
        const foto = event.target.closest("div");
        if (!foto) return;

        const id = parseInt(foto.dataset.id);
        if (fotosSeleccionadas.has(id)) {
            fotosSeleccionadas.delete(id);
            foto.classList.remove("border-primary", "border-3");
        } else {
            if (id){ 
                fotosSeleccionadas.add(id);
                foto.classList.add("border-primary", "border-3");
            }
        }
        fotosSeleccionadasInput.value = Array.from(fotosSeleccionadas).join(","); // actualiza el fotosSeleccionadasInput, exactamente como está fotosSeleccionadas
        console.log(fotosSeleccionadas);
        console.log("fotos seleccionadas: ", fotosSeleccionadasInput.value);
    });
    console.log(fotosSeleccionadas);
    console.log(fotosSeleccionadasInput.value);

}
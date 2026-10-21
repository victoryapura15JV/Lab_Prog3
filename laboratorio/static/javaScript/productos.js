// Elementos del formulario (los ids los genera ProductoForm con auto_id='%s')

const formulario = document.getElementById("formulario-producto");
const nombre = document.getElementById("nombre");
const categoria = document.getElementById("categoria");
const descripcion = document.getElementById("descripcion");
const imagen = document.getElementById("imagen");
const mensajeError = document.getElementById("mensaje-error");


// Validación del producto en el navegador (el servidor valida de nuevo en ProductoForm)

if (formulario) {
    formulario.addEventListener("submit", function(event) {

        mensajeError.textContent = "";

        if (nombre.value.trim() === "") {
            event.preventDefault();
            mensajeError.textContent = "Debe ingresar el nombre del producto.";
            nombre.focus();
            return;
        }

        if (categoria.value === "") {
            event.preventDefault();
            mensajeError.textContent = "Debe seleccionar una categoría.";
            categoria.focus();
            return;
        }

        if (descripcion.value.trim() === "") {
            event.preventDefault();
            mensajeError.textContent = "Debe ingresar una descripción.";
            descripcion.focus();
            return;
        }

        if (descripcion.value.trim().length < 10) {
            event.preventDefault();
            mensajeError.textContent = "La descripción debe ser más detallada.";
            descripcion.focus();
            return;
        }
        // Si todo está bien, el formulario se envía al servidor (Django).
    });
}


// Vista previa de la imagen

if (imagen) {
    imagen.addEventListener("change", function() {

        if (imagen.files.length > 0) {

            const archivo = imagen.files[0];
            const lector = new FileReader();

            lector.addEventListener("load", function() {

                let preview = document.getElementById("preview-foto");

                if (preview === null) {
                    preview = document.createElement("div");
                    preview.id = "preview-foto";
                    imagen.parentNode.appendChild(preview);
                }

                preview.innerHTML = "";

                const foto = document.createElement("img");

                foto.src = lector.result;
                foto.alt = "Vista previa de la imagen";
                foto.className = "img-miniatura-tabla mt-2";

                preview.appendChild(foto);
            });

            lector.readAsDataURL(archivo);
        }
    });
}


// Eliminar productos: confirmación antes de enviar el formulario POST al servidor

document.querySelectorAll(".form-eliminar").forEach(function(form) {

    form.addEventListener("submit", function(event) {

        if (!confirm("¿Desea eliminar este producto?")) {
            event.preventDefault();
        }
    });
});
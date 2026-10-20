// Elementos del formulario

const formulario = document.getElementById("formulario-producto");
const nombre = document.getElementById("nombre");
const categoria = document.getElementById("categoria");
const descripcion = document.getElementById("descripcion");
const imagen = document.getElementById("imagen");
const mensajeError = document.getElementById("mensaje-error");


// Validación del producto

formulario.addEventListener("submit", function(event) {

    event.preventDefault();

    mensajeError.textContent = "";

    if (nombre.value.trim() === "") {
        mensajeError.textContent = "Debe ingresar el nombre del producto.";
        nombre.focus();
        return;
    }

    if (categoria.value === "") {
        mensajeError.textContent = "Debe seleccionar una categoría.";
        categoria.focus();
        return;
    }

    if (descripcion.value.trim() === "") {
        mensajeError.textContent = "Debe ingresar una descripción.";
        descripcion.focus();
        return;
    }

    if (descripcion.value.trim().length < 10) {
        mensajeError.textContent = "La descripción debe ser más detallada.";
        descripcion.focus();
        return;
    }

    formulario.submit();
});


// Vista previa de la imagen

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
            foto.className = "img-miniatura-tabla";

            preview.appendChild(foto);
        });

        lector.readAsDataURL(archivo);
    }
});


// Eliminar productos

const botonesEliminar = document.querySelectorAll(".btn-eliminar");

botonesEliminar.forEach(function(boton) {

    boton.addEventListener("click", function(event) {

        event.preventDefault();

        if (confirm("¿Desea eliminar este producto?")) {
            boton.closest("tr").remove();
        }
    });
});


// Modificar productos

const botonesModificar = document.querySelectorAll(".btn-modificar");

botonesModificar.forEach(function(boton) {

    boton.addEventListener("click", function(event) {

        event.preventDefault();

        const fila = boton.closest("tr");

        nombre.value = fila.cells[0].textContent.trim();

        const textoCategoria = fila.cells[1].textContent.trim();

        for (let i = 0; i < categoria.options.length; i++) {

            if (categoria.options[i].textContent === textoCategoria) {
                categoria.selectedIndex = i;
                break;
            }
        }

        descripcion.value = fila.cells[2].textContent.trim();
    });
});
const botonLike = document.getElementById("btn-like");

if (botonLike) {
    botonLike.addEventListener("click", function() {

        botonLike.disabled = true;

        fetch(botonLike.dataset.url, {
            method: "POST",
            headers: { "X-CSRFToken": botonLike.dataset.csrf },
            credentials: "same-origin"
        })
        .then(function(respuesta) {
            if (!respuesta.ok) {
                throw new Error("Error en la respuesta del servidor");
            }
            return respuesta.json();
        })
        .then(function(datos) {
            document.getElementById("total-likes").textContent = datos.total;
            botonLike.classList.toggle("activo", datos.liked);
            botonLike.setAttribute("aria-pressed", datos.liked);
            botonLike.querySelector(".icono-like").textContent = datos.liked ? "♥" : "♡";
        })
        .catch(function() {
            alert("No se pudo registrar tu Me gusta. Intentá de nuevo.");
        })
        .finally(function() {
            botonLike.disabled = false;
        });
    });
}
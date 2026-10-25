document.addEventListener("DOMContentLoaded", function() {
    const btnOjo = document.getElementById('btnTogglePassword');
    const inputPass = document.getElementById('loginPassword');

    if (btnOjo && inputPass) {
        btnOjo.addEventListener('click', function() {
            const tipoActual = inputPass.getAttribute('type');
            if (tipoActual === 'password') {
                inputPass.setAttribute('type', 'text');
                btnOjo.style.opacity = '0.5';
            } else {
                inputPass.setAttribute('type', 'password');
                btnOjo.style.opacity = '1';
            }
        });
    }
});

document.addEventListener("DOMContentLoaded", function() {
    // ---------------------------------------------------------
    // 1. LÓGICA DEL OJO DE CONTRASEÑA (Mantenemos tu código)
    // ---------------------------------------------------------
    const btnOjo = document.getElementById('btnTogglePassword');
    const inputPass = document.getElementById('loginPassword');

    if (btnOjo && inputPass) {
        btnOjo.addEventListener('click', function() {
            const tipoActual = inputPass.getAttribute('type');
            if (tipoActual === 'password') {
                inputPass.setAttribute('type', 'text');
                btnOjo.style.opacity = '0.5';
            } else {
                inputPass.setAttribute('type', 'password');
                btnOjo.style.opacity = '1';
            }
        });
    }

    // ---------------------------------------------------------
    // 2. LÓGICA DE COLORES DE LA PÍLDORA (Forzado con JS)
    // ---------------------------------------------------------
    const pildoraDerecha = document.querySelector('.nav-pildora-azul');

    if (pildoraDerecha) {
        // Forzar fondo azul oscuro al contenedor principal
        pildoraDerecha.style.setProperty('background-color', '#2A354E', 'important');

        // Seleccionamos todos los botones que deben tener efecto hover
        const botonesInteractivos = document.querySelectorAll('.btn-pildora-interactiva, .dropdown-item-azul');

        botonesInteractivos.forEach(btn => {
            // Estado por defecto (Azul con letras blancas y un micro-borde para separarlos)
            btn.style.setProperty('background-color', '#2A354E', 'important');
            btn.style.setProperty('color', '#FFFFFF', 'important');
            btn.style.setProperty('border', '1px solid rgba(255, 255, 255, 0.15)', 'important');
            btn.style.setProperty('transition', 'all 0.3s ease', 'important'); // Transición suave

            // Efecto al pasar el mouse (Se vuelve mostaza)
            btn.addEventListener('mouseenter', function() {
                this.style.setProperty('background-color', '#B0923D', 'important');
                this.style.setProperty('border-color', '#B0923D', 'important');
            });

            // Efecto al quitar el mouse (Vuelve a azul)
            btn.addEventListener('mouseleave', function() {
                this.style.setProperty('background-color', '#2A354E', 'important');
                this.style.setProperty('border-color', 'rgba(255, 255, 255, 0.15)', 'important');
            });
        });

        // Aseguramos que la etiqueta del nombre/correo sea blanca con letras mostaza (Excepción)
        const badgeUsuario = document.querySelector('.badge-pildora');
        if (badgeUsuario) {
            badgeUsuario.style.setProperty('background-color', '#FFFFFF', 'important');
            badgeUsuario.style.setProperty('color', '#B0923D', 'important');
            badgeUsuario.style.setProperty('border', 'none', 'important');
        }
    }
});
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
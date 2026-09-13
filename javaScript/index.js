document.addEventListener("DOMContentLoaded", function() {
    const topNav = document.getElementById('main-nav-wrapper');
    const bottomNav = document.getElementById('mobile-bottom-nav');
    const observer = new IntersectionObserver(function(entries) {
        if (entries[0].isIntersecting) {
            bottomNav.classList.remove('mostrar-menu');
        } else {
            bottomNav.classList.add('mostrar-menu');
        }
    }, { 
        threshold: 0.1
    });

    observer.observe(topNav);
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


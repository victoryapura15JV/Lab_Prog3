from django.shortcuts import render, redirect
from django.urls import reverse
from django.utils.http import url_has_allowed_host_and_scheme
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages


def _url_retorno(request):
    """Devuelve la página desde donde se envió el formulario (si es segura) o el inicio."""
    destino = request.POST.get('next') or request.META.get('HTTP_REFERER')
    if destino and url_has_allowed_host_and_scheme(
        destino,
        allowed_hosts={request.get_host()},
        require_https=request.is_secure(),
    ):
        return destino
    return reverse('home')


def iniciar_sesion(request):
    if request.method == 'POST':
        email = request.POST.get('username', '').strip()
        clave = request.POST.get('password', '')

        if not email or not clave:
            request.session['login_error'] = 'Completá el correo y la contraseña.'
            request.session['login_email'] = email
            return redirect(_url_retorno(request))

        #  authenticate valida el correo y la clave
        usuario = authenticate(request, username=email, password=clave)

        if usuario is not None:
            login(request, usuario)
            if usuario.rol and usuario.rol.nombre == 'CLIENTE':
                return redirect('artesanos:dashboard_cliente')
            return redirect(_url_retorno(request))

        # El error se guarda aparte de "messages" para mostrarlo dentro del
        # modal de inicio de sesión, en la MISMA página desde la que se intentó.
        request.session['login_error'] = 'Correo o contraseña incorrectos.'
        request.session['login_email'] = email
        return redirect(_url_retorno(request))

    return redirect('home')


def cerrar_sesion(request):
    logout(request)
    return redirect('home')

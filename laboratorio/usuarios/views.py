from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages

def iniciar_sesion(request):
    if request.method == 'POST':
        email = request.POST.get('username')  # El input del modal envía el correo bajo name="username"
        clave = request.POST.get('password')

        # Como USERNAME_FIELD = 'email', authenticate valida el correo y la clave
        usuario = authenticate(request, username=email, password=clave)

        if usuario is not None:
            login(request, usuario)
            # Redirección según rol (RNF-05)
            if usuario.rol and usuario.rol.nombre == 'CLIENTE':
                return redirect('artesanos:dashboard_cliente')
            return redirect('home')
        else:
            messages.error(request, 'Correo o contraseña incorrectos.')
            return redirect('home')

    return redirect('home')

def cerrar_sesion(request):
    logout(request)
    return redirect('home')
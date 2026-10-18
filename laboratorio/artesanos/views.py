from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .models import Solicitud
from .forms import SolicitudForm
def crear_solicitud(request):
    if request.method == 'POST':
        formulario = SolicitudForm(request.POST)
        if formulario.is_valid():
            formulario.save()
            messages.success(request, 'Solicitud enviada con exito!')
            return redirect('artesanos:crear_solicitud')
    else:
        formulario = SolicitudForm()
    return render(request,'artesanos/solicitud_artesano.html',{'formulario':formulario})

def listar_solicitudes(request):
    solicitudes = Solicitud.objects.all()
    return render(request, 'artesanos/listar_solicitudes.html', {'solicitudes': solicitudes})
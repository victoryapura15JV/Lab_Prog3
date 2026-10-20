from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .models import Solicitud, Artesano, Stand
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

def evaluar_solicitud(request, solicitud_id):
    solicitud = get_object_or_404(Solicitud, id=solicitud_id)
    if request.method == 'POST':
        nuevo_estado = request.POST.get('nuevo_estado')
        if nuevo_estado:
            solicitud.estado = nuevo_estado
            solicitud.save()
            if nuevo_estado == 'Aprobado':
                Artesano.objects.get_or_create(solicitud=solicitud)
            return redirect('artesanos:listar_solicitudes')
    return render(request, 'artesanos/evaluar_solicitud.html', {'solicitud': solicitud})

def asignar_stand(request, artesano_id):
    artesano = get_object_or_404(Artesano, id=artesano_id)
    stands_disponibles = Stand.objects.filter(estado='Disponible')

    if request.method == 'POST':
        stand_id = request.POST.get('stand_id')
        if stand_id:
            stand_elegido = get_object_or_404(Stand, id=stand_id)
            artesano.stand = stand_elegido
            artesano.save()
            stand_elegido.estado = 'Ocupado'
            stand_elegido.save()

            return redirect('artesanos:listar_solicitudes')

    return render(request, 'artesanos/asignar_stand.html', {
        'artesano': artesano,
        'stands': stands_disponibles
    })
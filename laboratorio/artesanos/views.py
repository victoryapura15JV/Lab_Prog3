from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .models import Solicitud, Artesano, Stand
from .forms import SolicitudForm
def crear_solicitud(request):
    if request.method == 'POST':
        dni_ingresado = request.POST.get('dni')
        solicitud_existente = Solicitud.objects.filter(dni=dni_ingresado).first()

        if solicitud_existente:
            messages.info(request,f'Ya estás inscripto. Tu número de solicitud es: {solicitud_existente.id} Podes consultar el estado de tu solicitud en la seccion "Consultar Estado"')
            return redirect('artesanos:crear_solicitud')
        formulario = SolicitudForm(request.POST)
        if formulario.is_valid():
            formulario.save()
            messages.success(request, 'Solicitud enviada con exito!Tu número de solicitud es: f{nueva_solicitud.id}. Anotalo para consultar tu estado.')
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
            justificacion = request.POST.get('justificacion')
            solicitud.justificacion = justificacion
            solicitud.save()
            if nuevo_estado == 'Aprobado':
                Artesano.objects.get_or_create(solicitud=solicitud)
            return redirect('artesanos:listar_solicitudes')
    return render(request, 'artesanos/evaluar_solicitud.html', {'solicitud': solicitud})


def asignar_stand(request, artesano_id):
    artesano = get_object_or_404(Artesano, id=artesano_id)
    stands_disponibles = Stand.objects.filter(estado='Disponible')

    if request.method == 'POST':
        if 'desasignar' in request.POST:
            if artesano.stand:
                stand_id_viejo = artesano.stand.id
                artesano.stand = None
                artesano.save()
                stand_viejo = Stand.objects.get(id=stand_id_viejo)
                stand_viejo.estado = 'Disponible'
                stand_viejo.save()

            return redirect('artesanos:listar_solicitudes')
        stand_id = request.POST.get('stand_id')
        if stand_id:
            if artesano.stand:
                stand_id_viejo = artesano.stand.id
                stand_viejo = Stand.objects.get(id=stand_id_viejo)
                stand_viejo.estado = 'Disponible'
                stand_viejo.save()

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


def estado_solicitud(request):
    if request.method == 'POST':
        id_ingresado = request.POST.get('numero_solicitud')
        dni_ingresado = request.POST.get('dni')
        solicitud = get_object_or_404(Solicitud, id=id_ingresado, dni=dni_ingresado)

        return render(request, 'artesanos/resultado_estado.html', {'solicitud': solicitud})

    return render(request, 'artesanos/consultar_estado.html')
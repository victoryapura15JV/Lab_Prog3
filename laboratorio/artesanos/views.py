from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .forms import SolicitudForm
from django.db.models import Count
from .models import Solicitud, Artesano, Stand, TendenciaBusqueda
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
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

@login_required
def dashboard_cliente(request):
    """
    Vista exclusiva para el rol Cliente.
    Cumple con HU-16 (Panel Estratégico) y HU-17 (Tendencias).
    """
    # Validación estricta de seguridad (RNF-05)
    if not request.user.rol or request.user.rol.nombre != 'CLIENTE':
        raise PermissionDenied("Acceso denegado. Esta vista es exclusiva para el Cliente institucional.")

    # 1. Cálculos de Stands (Ocupación)
    total_stands = Stand.objects.count()
    # 1. Cálculos de Stands (Ocupación)
    total_stands = Stand.objects.count()
    stands_ocupados = Stand.objects.filter(estado='Ocupado').count()
    stands_disponibles = Stand.objects.filter(estado='Disponible').count()

    porcentaje_ocupacion = 0
    if total_stands > 0:
        porcentaje_ocupacion = round((stands_ocupados / total_stands) * 100, 1)

    # 2. Agrupación de Artesanos Aprobados por Localidad y Rubro
    artesanos_por_localidad = Solicitud.objects.filter(estado='Aprobado').values('localidad').annotate(
        total=Count('id')).order_by('-total')
    artesanos_por_rubro = Solicitud.objects.filter(estado='Aprobado').values('rubro').annotate(
        total=Count('id')).order_by('-total')

    # 3. Top 10 Stands más visitados (Popularidad)
    top_artesanos = Artesano.objects.order_by('-visitas')[:10]

    # 4. Top 10 Términos más buscados por los visitantes
    top_busquedas = TendenciaBusqueda.objects.values('termino').annotate(total=Count('id')).order_by('-total')[:10]

    # Empaquetamos todo para enviarlo al HTML
    contexto = {
        'total_stands': total_stands,
        'stands_ocupados': stands_ocupados,
        'stands_disponibles': stands_disponibles,
        'porcentaje_ocupacion': porcentaje_ocupacion,
        'artesanos_por_localidad': artesanos_por_localidad,
        'artesanos_por_rubro': artesanos_por_rubro,
        'top_artesanos': top_artesanos,
        'top_busquedas': top_busquedas,
    }

    return render(request, 'artesanos/dashboard_cliente.html', contexto)

def estado_solicitud(request):
    if request.method == 'POST':
        id_ingresado = request.POST.get('numero_solicitud')
        dni_ingresado = request.POST.get('dni')
        solicitud = get_object_or_404(Solicitud, id=id_ingresado, dni=dni_ingresado)

        return render(request, 'artesanos/resultado_estado.html', {'solicitud': solicitud})

    return render(request, 'artesanos/consultar_estado.html')

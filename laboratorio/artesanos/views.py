from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.views.decorators.http import require_POST
from usuarios.decoradores import rol_requerido
from .forms import SolicitudForm, StandForm
from django.db.models import Count
from .models import Solicitud, Artesano, Stand, TendenciaBusqueda
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.db import transaction

def crear_solicitud(request):
    if request.method == 'POST':
        dni_ingresado = request.POST.get('dni')
        solicitud_existente = Solicitud.objects.filter(dni=dni_ingresado).first()

        if solicitud_existente:
            messages.warning(request,f'Este dni ya se encuentra registrado. Podes consultar tu estado en el apartado con tu dni')
            return redirect('artesanos:crear_solicitud')
        formulario = SolicitudForm(request.POST)
        if formulario.is_valid():
            formulario.save()
            messages.success(request, f'Solicitud enviada con exito! Podes consultar tu estado con tu DNI')
            return redirect('artesanos:crear_solicitud')
    else:
        formulario = SolicitudForm()
    return render(request,'artesanos/solicitud_artesano.html',{'formulario':formulario})

@rol_requerido('ADMINISTRADOR')
def listar_solicitudes(request):
    solicitudes = Solicitud.objects.all()
    return render(request, 'artesanos/listar_solicitudes.html', {'solicitudes': solicitudes})

@rol_requerido('ADMINISTRADOR')
def evaluar_solicitud(request, solicitud_id):
    solicitud = get_object_or_404(Solicitud, id=solicitud_id)
    if request.method == 'POST':
        nuevo_estado = request.POST.get('nuevo_estado')
        if nuevo_estado:
            justificacion = request.POST.get('justificacion','')
            if nuevo_estado in ['Modificacion','Rechazado']and justificacion == '':
                messages.error(request, 'Tenes que escribir una justificación del motivo de tu evaluacion')
                return render(request, 'artesanos/evaluar_solicitud.html', {'solicitud': solicitud})

            solicitud.estado = nuevo_estado
            solicitud.justificacion = justificacion
            solicitud.save()
            if nuevo_estado == 'Aprobado':
                Artesano.objects.get_or_create(solicitud=solicitud)

            messages.success(request, f'El resultado de tu evaluacion fue enviada, resultado: {nuevo_estado}')
            return redirect('artesanos:listar_solicitudes')
    return render(request, 'artesanos/evaluar_solicitud.html', {'solicitud': solicitud})


@rol_requerido('ADMINISTRADOR')
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

            return redirect('artesanos:listar_stands')

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

            return redirect('artesanos:listar_stands')

    return render(request, 'artesanos/asignar_stand.html', {
        'artesano': artesano,
        'stands': stands_disponibles
    })

@login_required
def dashboard_cliente(request):
    """
    Vista exclusiva para el rol Cliente
    """
    if not request.user.rol or request.user.rol.nombre != 'CLIENTE':
        raise PermissionDenied("Acceso denegado. Esta vista es exclusiva para el Cliente institucional.")

    # Cantidad de stands ocupados y disponibles
    total_stands = Stand.objects.count()
    stands_ocupados = Stand.objects.filter(estado='Ocupado').count()
    stands_disponibles = Stand.objects.filter(estado='Disponible').count()
    porcentaje_ocupacion = round((stands_ocupados / total_stands) * 100, 1) if total_stands > 0 else 0

    # Artesanos registrados por localidad y rubro
    artesanos_por_localidad = Solicitud.objects.filter(estado='Aprobado').values('localidad').annotate(total=Count('id')).order_by('-total')
    artesanos_por_rubro = Solicitud.objects.filter(estado='Aprobado').values('rubro').annotate(total=Count('id')).order_by('-total')

    # Total de Artesanos registrados
    total_artesanos = Artesano.objects.count()

    # Estadísticas completas por artesano
    artesanos_stats = Artesano.objects.annotate(
        total_productos=Count('productos', distinct=True),
        total_likes=Count('productos__likes', distinct=True)
    ).select_related('solicitud').order_by('-visitas')

    top_artesanos = Artesano.objects.order_by('-visitas')[:10]
    top_busquedas = TendenciaBusqueda.objects.values('termino').annotate(total=Count('id')).order_by('-total')[:15]

    contexto = {
        'total_stands': total_stands,
        'stands_ocupados': stands_ocupados,
        'stands_disponibles': stands_disponibles,
        'porcentaje_ocupacion': porcentaje_ocupacion,
        'artesanos_por_localidad': artesanos_por_localidad,
        'artesanos_por_rubro': artesanos_por_rubro,
        'total_artesanos': total_artesanos,
        'artesanos_stats': artesanos_stats,
        'top_artesanos': top_artesanos,
        'top_busquedas': top_busquedas,
    }

    return render(request, 'artesanos/dashboard_cliente.html', contexto)

def estado_solicitud(request):
    if request.method == 'POST':
        dni_ingresado = request.POST.get('dni')
        solicitud = Solicitud.objects.filter(dni=dni_ingresado).first()
        if solicitud:
            return render(request, 'artesanos/resultado_estado.html', {'solicitud':solicitud})
        else:
            messages.error(request, 'No se encontro ninguna solicitud con ese dni.')
            return render(request,'artesanos/consultar_estado.html')
    return render(request, 'artesanos/consultar_estado.html')

@rol_requerido('ADMINISTRADOR')
def listar_stands(request):
    stands = Stand.objects.select_related('artesanos__solicitud')
    artesanos = Artesano.objects.select_related('solicitud', 'stand')
    return render(request, 'artesanos/listar_stands.html', {
        'stands': stands,
        'artesanos': artesanos,
    })


@rol_requerido('ADMINISTRADOR')
def crear_stand(request):
    if request.method == 'POST':
        formulario = StandForm(request.POST)
        if formulario.is_valid():
            formulario.save()
            messages.success(request, 'Stand cargado con éxito.')
            return redirect('artesanos:listar_stands')
    else:
        formulario = StandForm()
    return render(request, 'artesanos/form_stand.html', {
        'formulario': formulario,
        'titulo': 'Cargar stand',
    })


@rol_requerido('ADMINISTRADOR')
def modificar_stand(request, stand_id):
    stand = get_object_or_404(Stand, id=stand_id)
    if request.method == 'POST':
        formulario = StandForm(request.POST, instance=stand)
        if formulario.is_valid():
            formulario.save()
            messages.success(request, 'Stand modificado con éxito.')
            return redirect('artesanos:listar_stands')
    else:
        formulario = StandForm(instance=stand)
    return render(request, 'artesanos/form_stand.html', {
        'formulario': formulario,
        'titulo': 'Modificar stand',
    })


@rol_requerido('ADMINISTRADOR')
@require_POST
def eliminar_stand(request, stand_id):
    stand = get_object_or_404(Stand, id=stand_id)
    if Artesano.objects.filter(stand=stand).exists():
        messages.error(request, 'No se puede eliminar un stand asignado. Dalo de baja primero para liberarlo.')
    else:
        stand.delete()
        messages.success(request, 'Stand dado de baja.')
    return redirect('artesanos:listar_stands')

@rol_requerido('ADMINISTRADOR')
@require_POST
def liberar_stand(request, stand_id):
    """Da de baja la asignación,el artesano pierde el stand y el stand queda Disponible."""
    stand = get_object_or_404(Stand, id=stand_id)
    with transaction.atomic():
        Artesano.objects.filter(stand=stand).update(stand=None)
        stand.estado = 'Disponible'
        stand.save()
    messages.success(request, 'Stand dado de baja: quedó disponible y el artesano ya no lo tiene asignado.')
    return redirect('artesanos:listar_stands')


def corregir_solicitud(request, token):
    solicitud = get_object_or_404(Solicitud, token_acceso=token)
    if solicitud.estado != 'Modificacion':
        messages.error(request, 'Esta solicitud no requiere modificaciones.')
        return redirect('home')

    if request.method == 'POST':
        formulario = SolicitudForm(request.POST, request.FILES, instance=solicitud)

        if formulario.is_valid():
            solicitud_actualizada = formulario.save(commit=False)
            solicitud_actualizada.estado = 'Pendiente'
            solicitud_actualizada.justificacion = ''
            solicitud_actualizada.save()

            messages.success(request, 'Tu solicitud fue enviada nuevamente para su revisión.')
            return redirect('artesanos:estado_solicitud')
    else:
        formulario = SolicitudForm(instance=solicitud)

    return render(request, 'artesanos/solicitud_artesano.html', {
        'formulario': formulario,
        'modo_edicion': True
    })


@rol_requerido('ADMINISTRADOR')
def reportes_operativos(request):
    """
    Vista exclusiva para el Administrador.
    """
    tendencias = TendenciaBusqueda.objects.values('termino').annotate(total=Count('id')).order_by('-total')[:15]

    artesanos_sin_stand = Artesano.objects.filter(stand__isnull=True).select_related('solicitud')
    stands_disponibles = Stand.objects.filter(estado='Disponible').order_by('pabellon', 'numero_puesto')
    solicitudes_atascadas = Solicitud.objects.filter(estado__in=['Pendiente', 'Modificacion']).order_by('-envio')

    contexto = {
        'tendencias': tendencias,
        'artesanos_sin_stand': artesanos_sin_stand,
        'stands_disponibles': stands_disponibles,
        'solicitudes_atascadas': solicitudes_atascadas,
    }

    return render(request, 'artesanos/reportes_operativos.html', contexto)

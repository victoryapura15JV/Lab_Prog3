from django.contrib import messages
from django.db import IntegrityError, transaction
from django.db.models import F, Q
from django.http import JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_POST

from artesanos.models import Artesano, TendenciaBusqueda
from .forms import ProductoForm, ComentarioForm
from .models import Producto, Like
from .visitante import obtener_visitor_id, guardar_cookie


def catalogo(request):
    """Vista pública: muestra los productos cargados, con filtro por categoría y búsqueda."""
    productos = Producto.objects.select_related('artesano__solicitud', 'artesano__stand')
    categoria = request.GET.get('categoria', '').strip()
    q = request.GET.get('q', '').strip()

    if categoria:
        productos = productos.filter(categoria=categoria)
    if q:
        TendenciaBusqueda.objects.create(termino=q.lower())
        productos = productos.filter(
            Q(nombre__icontains=q)
            | Q(descripcion__icontains=q)
            | Q(categoria__icontains=q)
            | Q(artesano__solicitud__nombre_emprendimiento__icontains=q)
        )

    return render(request, 'productos/catalogo.html', {
        'productos': productos,
        'categorias': Producto.categorias,
        'categoria_activa': categoria,
        'q': q,
    })


def gestionar_productos(request, artesano_id):
    """Vista del artesano: formulario de carga + listado de sus productos."""
    artesano = get_object_or_404(Artesano.objects.select_related('solicitud'), id=artesano_id)

    if request.method == 'POST':
        formulario = ProductoForm(request.POST, request.FILES)
        if formulario.is_valid():
            producto = formulario.save(commit=False)
            producto.artesano = artesano
            producto.save()
            messages.success(request, 'Producto guardado con éxito.')
            return redirect('productos:gestionar', artesano_id=artesano.id)
    else:
        formulario = ProductoForm()

    return render(request, 'productos/gestionar_productos.html', {
        'artesano': artesano,
        'formulario': formulario,
        'productos': artesano.productos.all(),
    })


def modificar_producto(request, producto_id):
    producto = get_object_or_404(Producto.objects.select_related('artesano__solicitud'), id=producto_id)

    if request.method == 'POST':
        formulario = ProductoForm(request.POST, request.FILES, instance=producto)
        if formulario.is_valid():
            formulario.save()
            messages.success(request, 'Producto modificado con éxito.')
            return redirect('productos:gestionar', artesano_id=producto.artesano_id)
    else:
        formulario = ProductoForm(instance=producto)

    return render(request, 'productos/modificar_producto.html', {
        'producto': producto,
        'artesano': producto.artesano,
        'formulario': formulario,
    })


def eliminar_producto(request, producto_id):
    producto = get_object_or_404(Producto, id=producto_id)
    artesano_id = producto.artesano_id

    
    if request.method == 'POST':
        producto.delete()
        messages.success(request, 'Producto eliminado.')

    return redirect('productos:gestionar', artesano_id=artesano_id)

def detalle_producto(request, producto_id):
    producto = get_object_or_404(
        Producto.objects.select_related('artesano__solicitud', 'artesano__stand'),
        id=producto_id
    )
    visitor_id, es_nuevo = obtener_visitor_id(request)

    otros_productos = (
        producto.artesano.productos
        .exclude(id=producto.id)
        .select_related('artesano__solicitud', 'artesano__stand')[:4]
    )

    respuesta = render(request, 'productos/producto_detalle.html', {
        'producto': producto,
        'artesano': producto.artesano,
        'total_likes': producto.likes.count(),
        'liked': producto.likes.filter(visitor_id=visitor_id).exists(),
        'comentarios': producto.comentarios.filter(visible=True),
        'ya_comento': producto.comentarios.filter(visitor_id=visitor_id).exists(),
        'formulario': ComentarioForm(),
        'otros_productos': otros_productos,
    })
    if es_nuevo:
        guardar_cookie(respuesta, visitor_id)
    return respuesta


@require_POST
def dar_like(request, producto_id):
    """Alterna el 'Me gusta' del visitante: el primer clic lo da y el segundo lo quita."""
    producto = get_object_or_404(Producto, id=producto_id)
    visitor_id, es_nuevo = obtener_visitor_id(request)

    like, creado = Like.objects.get_or_create(producto=producto, visitor_id=visitor_id)
    if not creado:
        like.delete()

    respuesta = JsonResponse({'liked': creado, 'total': producto.likes.count()})
    if es_nuevo:
        guardar_cookie(respuesta, visitor_id)
    return respuesta


@require_POST
def comentar(request, producto_id):
    producto = get_object_or_404(Producto, id=producto_id)
    visitor_id, es_nuevo = obtener_visitor_id(request)
    formulario = ComentarioForm(request.POST)

    if producto.comentarios.filter(visitor_id=visitor_id).exists():
        messages.error(request, 'Ya comentaste este producto.')
    elif formulario.is_valid():
        comentario = formulario.save(commit=False)
        comentario.producto = producto
        comentario.visitor_id = visitor_id
        try:
            with transaction.atomic():
                comentario.save()
            messages.success(request, 'Gracias por tu comentario.')
        except IntegrityError:
            messages.error(request, 'Ya comentaste este producto.')
    else:
        for errores in formulario.errors.values():
            for error in errores:
                messages.error(request, error)

    respuesta = redirect('productos:detalle', producto_id=producto.id)
    if es_nuevo:
        guardar_cookie(respuesta, visitor_id)
    return respuesta


def perfil_artesano(request, artesano_id):
    artesano = get_object_or_404(
        Artesano.objects.select_related('solicitud', 'stand'),
        id=artesano_id
    )

    Artesano.objects.filter(id=artesano.id).update(visitas=F('visitas') + 1)

    productos = artesano.productos.select_related('artesano__solicitud', 'artesano__stand')
    total_likes = Like.objects.filter(producto__artesano=artesano).count()

    return render(request, 'productos/perfil_artesano.html', {
        'artesano': artesano,
        'solicitud': artesano.solicitud,
        'productos': productos,
        'total_likes': total_likes,
    })
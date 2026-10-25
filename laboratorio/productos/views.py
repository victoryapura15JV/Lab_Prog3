from django.contrib import messages
from django.db.models import Q
from django.shortcuts import render, redirect, get_object_or_404

from artesanos.models import Artesano, TendenciaBusqueda
from .forms import ProductoForm
from .models import Producto


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

    # Solo se elimina por POST (el botón del listado envía un formulario con csrf_token).
    if request.method == 'POST':
        producto.delete()
        messages.success(request, 'Producto eliminado.')

    return redirect('productos:gestionar', artesano_id=artesano_id)
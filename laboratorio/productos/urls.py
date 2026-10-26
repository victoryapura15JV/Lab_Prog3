from django.urls import path
from . import views

app_name = 'productos'

urlpatterns = [
    path('', views.catalogo, name='catalogo'),
    path('buscar/', views.catalogo, name='buscar'),
    path('artesano/<int:artesano_id>/', views.gestionar_productos, name='gestionar'),
    path('perfil/<int:artesano_id>/', views.perfil_artesano, name='perfil'),
    path('modificar/<int:producto_id>/', views.modificar_producto, name='modificar'),
    path('eliminar/<int:producto_id>/', views.eliminar_producto, name='eliminar'),
    path('<int:producto_id>/', views.detalle_producto, name='detalle'),
    path('<int:producto_id>/like/', views.dar_like, name='like'),
    path('<int:producto_id>/comentar/', views.comentar, name='comentar'),
]
from django.urls import path
from . import views

app_name = 'artesanos'

urlpatterns = [
    path('solicitud/artesanos/', views.crear_solicitud, name='crear_solicitud'),
    path('panel/inscriptos/', views.listar_solicitudes, name='listar_solicitudes'),
    path('evaluar/solicitud/<int:solicitud_id>/', views.evaluar_solicitud, name='evaluar_solicitud'),
    path('panel/asignarstand/<int:artesano_id>/', views.asignar_stand, name='asignar_stand'),
    path('panel/cliente/', views.dashboard_cliente, name='dashboard_cliente'),
    path('estadosolicitud/', views.estado_solicitud, name='estado_solicitud'),
    path('panel/stands/', views.listar_stands, name='listar_stands'),
    path('panel/stands/nuevo/', views.crear_stand, name='crear_stand'),
    path('panel/stands/<int:stand_id>/modificar/', views.modificar_stand, name='modificar_stand'),
    path('panel/stands/<int:stand_id>/eliminar/', views.eliminar_stand, name='eliminar_stand'),
]
from django.urls import path
from . import views

app_name = 'artesanos'

urlpatterns = [
    path('solicitud/artesanos/', views.crear_solicitud, name='crear_solicitud'),
    path('panel/inscriptos/', views.listar_solicitudes, name='listar_solicitudes'),
    path('evaluar/solicitud/<int:solicitud_id>/', views.evaluar_solicitud, name='evaluar_solicitud'),
    path('panel/asignarstand/<int:artesano_id>/', views.asignar_stand, name='asignar_stand'),
    path('panel/cliente/', views.dashboard_cliente, name='dashboard_cliente'),
]
from django.urls import path
from . import views

app_name = 'artesanos'

urlpatterns = [
    path('solicitud/artesanos/', views.crear_solicitud, name='crear_solicitud'),
    path('panel/inscriptos/', views.listar_solicitudes, name='listar_solicitudes'),
]
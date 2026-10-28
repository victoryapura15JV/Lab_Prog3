from django.contrib import admin
from .models import Solicitud, Artesano, Stand


@admin.register(Solicitud)
class SolicitudAdmin(admin.ModelAdmin):
    list_display = ('nombre_emprendimiento', 'nombre_apellido', 'estado', 'envio')
    list_filter = ('estado', 'rubro')


@admin.register(Artesano)
class ArtesanoAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'stand', 'usuario', 'visitas')


admin.site.register(Stand)
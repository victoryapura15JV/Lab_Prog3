from django.contrib import admin
from .models import Producto


@admin.register(Producto)
class ProductoAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'categoria', 'artesano', 'fecha_publicacion')
    list_filter = ('categoria',)
    search_fields = ('nombre', 'descripcion')
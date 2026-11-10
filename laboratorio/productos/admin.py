from django.contrib import admin
from .models import Producto, Like, Comentario


@admin.register(Producto)
class ProductoAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'categoria', 'artesano', 'fecha_publicacion')
    list_filter = ('categoria',)
    search_fields = ('nombre', 'descripcion')


@admin.register(Comentario)
class ComentarioAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'producto', 'visible', 'creado')
    list_filter = ('visible',)
    list_editable = ('visible',)  


admin.site.register(Like)
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Usuario, Rol

# Registramos el modelo Rol
admin.site.register(Rol)


# Registramos nuestro Usuario personalizado usando la estructura segura de UserAdmin
@admin.register(Usuario)
class CustomUserAdmin(UserAdmin):
    list_display = ('email', 'first_name', 'last_name', 'rol', 'is_staff')
    list_filter = ('rol', 'is_staff', 'is_active')

    # Agregamos "or ()" para que PyCharm entienda estrictamente que es una tupla
    fieldsets = (UserAdmin.fieldsets or ()) + (
        ('Información de Rol', {'fields': ('rol',)}),
    )
    add_fieldsets = (UserAdmin.add_fieldsets or ()) + (
        ('Información de Rol', {'fields': ('rol',)}),
    )
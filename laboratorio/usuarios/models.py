from django.db import models
from django.contrib.auth.models import AbstractUser


class Rol(models.Model):
    ROLES_OPCIONES = [
        ('ADMINISTRADOR', 'Administrador'),
        ('ARTESANO', 'Artesano'),
        ('VISITANTE', 'Visitante'),
        ('CLIENTE', 'Cliente'),
    ]

    nombre = models.CharField(max_length=20, choices=ROLES_OPCIONES, unique=True)
    descripcion = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        verbose_name_plural = "Roles"

    def __str__(self):
        return self.get_nombre_display()


class Usuario(AbstractUser):
    email = models.EmailField('correo electrónico', unique=True)

    rol = models.ForeignKey(Rol, on_delete=models.SET_NULL, null=True, blank=True, related_name='usuarios')

    USERNAME_FIELD = 'email'

    REQUIRED_FIELDS = ['username', 'first_name', 'last_name']

    def __str__(self):
        return f"{self.email} - {self.rol.nombre if self.rol else 'Sin Rol'}"
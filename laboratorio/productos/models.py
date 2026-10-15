from django.db import models

# Create your models here.

class Producto(models.Model):
    categorias = [
        ('Productos Artesanales', 'Productos Artesanales'),
        ('Productos Textiles', 'Productos Textiles'),
        ('Productos Regionales', 'Productos Regionales'),
        ('Productos Culturales', 'Productos Culturales'),
    ]

    nombre = models.CharField(max_length=100)
    categoria = models.CharField(max_length=30, choices=categorias)
    descripcion = models.TextField()
    imagen = models.ImageField(upload_to='productos/')
    fecha_publicacion = models.DateTimeField(auto_now_add=True)
    fecha_actualizacion = models.DateTimeField(auto_now=True)

    artesano = models.ForeignKey(
        'artesanos.Artesano',
        on_delete=models.CASCADE,
        related_name='productos'
    )

    class Meta:
        ordering = ('-fecha_publicacion',)

    def __str__(self):
        return f'{self.nombre} ({self.artesano.solicitud.nombre_emprendimiento})'
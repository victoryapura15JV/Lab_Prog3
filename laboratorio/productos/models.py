from django.db import models


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
    imagen = models.FileField(upload_to='productos/')
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


class Like(models.Model):
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE, related_name='likes')
    visitor_id = models.CharField(max_length=36)
    creado = models.DateTimeField(auto_now_add=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['producto', 'visitor_id'], name='un_like_por_visitante')
        ]

    def __str__(self):
        return f'Like en {self.producto.nombre}'


class Comentario(models.Model):
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE, related_name='comentarios')
    visitor_id = models.CharField(max_length=36)
    nombre = models.CharField(max_length=60)
    texto = models.TextField(max_length=500)
    visible = models.BooleanField(default=True)  # permite ocultar comentarios desde el admin
    creado = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ('-creado',)
        constraints = [
            models.UniqueConstraint(fields=['producto', 'visitor_id'], name='un_comentario_por_visitante')
        ]

    def __str__(self):
        return f'{self.nombre} en {self.producto.nombre}'
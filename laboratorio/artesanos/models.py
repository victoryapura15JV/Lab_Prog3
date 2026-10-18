from django.db import models

class Stand(models.Model):
   pabellones = [
        ('Pabellon A', 'Pabellon A'),
        ('Pabellon B', 'Pabellon B'),
        ('Pabellon C', 'Pabellon C'),
        ('Sector Exterior', 'Sector Exterior'),
   ]

   estado_stand = [
        ('Disponible', 'Disponible'),
        ('Ocupado', 'Ocupado'),
   ]

   pabellon = models.CharField(max_length=20, choices=pabellones)
   numero_puesto = models.IntegerField()
   dimensiones = models.CharField(max_length=50)
   estado = models.CharField(max_length=15, choices=estado_stand, default='Disponible')

   class Meta:
        ordering = ('pabellon', 'numero_puesto')

   def __str__(self):
        return f'{self.pabellon} - Puesto {self.numero_puesto} ({self.estado})'

class Solicitud(models.Model):
    provincias = [
        ('Catamarca', 'Catamarca'),
        ('Salta', 'Salta'),
        ('Tucuman', 'Tucumán'),
        ('Otra', 'Otra provincia'),
    ]

    localidades = [
        ('Capital', 'Capital'),
        ('Valle Viejo', 'Valle Viejo'),
        ('Fray Mamerto Esquiu', 'Fray Mamerto Esquiú'),
        ('Belen', 'Belén'),
        ('Cafayate', 'Cafayate'),
        ('Tartagal', 'Tartagal'),
        ('Tafi del Valle', 'Tafí del Valle'),
        ('Yerba Buena', 'Yerba Buena'),
        ('Otra', 'Otra localidad'),
    ]

    rubros = [
        ('Productos Artesanales', 'Productos Artesanales'),
        ('Productos Textiles', 'Productos Textiles'),
        ('Productos Regionales', 'Productos Regionales'),
        ('Productos Culturales', 'Productos Culturales'),
    ]

    estados_solicitud = [
        ('Pendiente', 'Pendiente'),
        ('Aprobado', 'Aprobado'),
        ('Rechazado', 'Rechazado'),
        ('Modificacion', 'Modificación solicitada'),
    ]

    nombre_apellido = models.CharField(max_length=100)
    dni = models.CharField(max_length=8, unique=True)
    fecha_nacimiento = models.DateField()
    telefono = models.CharField(max_length=20)
    email = models.EmailField(unique=True)
    provincia = models.CharField(max_length=20, choices=provincias)
    localidad = models.CharField(max_length=30, choices=localidades)
    nombre_emprendimiento = models.CharField(max_length=100)
    anios_trayectoria = models.IntegerField()
    historia_emprendimiento = models.TextField()
    rubro = models.CharField(max_length=30, choices=rubros)
    productos_principales = models.CharField(max_length=200)

    estado = models.CharField(max_length=15, choices=estados_solicitud, default='Pendiente')
    envio = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ('envio',)

    def __str__(self):
        return f'{self.nombre_apellido} - {self.nombre_emprendimiento} ({self.estado})'

class Artesano(models.Model):
    solicitud = models.OneToOneField(
        Solicitud,
        on_delete=models.PROTECT,
        related_name='artesanos'
    )
    stand = models.OneToOneField(
        Stand,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='artesanos'
    )
    usuario = models.OneToOneField('usuarios.Usuario', on_delete=models.PROTECT, null=True, blank=True, related_name='artesanos')

    materiales = models.CharField(max_length=200, blank=True)
    horarios_asistencia = models.CharField(max_length=150, blank=True)
    contacto = models.URLField(blank=True)
    redes = models.URLField(blank=True)
    visitas = models.IntegerField(default=0)

    class Meta:
        ordering = ('solicitud',)

    def __str__(self):
        return f'Artesano: {self.solicitud.nombre_apellido} - {self.solicitud.nombre_emprendimiento}'
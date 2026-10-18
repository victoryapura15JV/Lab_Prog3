from django import forms
from .models import Solicitud
class SolicitudForm(forms.ModelForm):
    class Meta:
        model= Solicitud
        fields=['nombre_apellido','dni','fecha_nacimiento','telefono','email','provincia','localidad','nombre_emprendimiento','anios_trayectoria','historia_emprendimiento','rubro','productos_principales']

from django import forms
from .models import Solicitud, Stand
class SolicitudForm(forms.ModelForm):
    class Meta:
        model= Solicitud
        fields=['nombre_apellido','dni','fecha_nacimiento','telefono','email','provincia','localidad','nombre_emprendimiento','anios_trayectoria','historia_emprendimiento','rubro','productos_principales']

class StandForm(forms.ModelForm):
    class Meta:
        model = Stand
        fields = ['pabellon', 'numero_puesto', 'dimensiones']
        widgets = {
            'pabellon': forms.Select(attrs={'class': 'form-select'}),
            'numero_puesto': forms.NumberInput(attrs={'class': 'form-control', 'min': 1}),
            'dimensiones': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ej: 3x3 m'}),
        }

    def clean_numero_puesto(self):
        numero = self.cleaned_data['numero_puesto']
        if numero < 1:
            raise forms.ValidationError('El número de puesto debe ser mayor a 0.')
        return numero

    def clean(self):
        datos = super().clean()
        pabellon = datos.get('pabellon')
        numero = datos.get('numero_puesto')
        if pabellon and numero:
            repetidos = Stand.objects.filter(pabellon=pabellon, numero_puesto=numero)
            if self.instance.pk:
                repetidos = repetidos.exclude(pk=self.instance.pk)
            if repetidos.exists():
                raise forms.ValidationError('Ya existe un stand con ese pabellón y número de puesto.')
        return datos
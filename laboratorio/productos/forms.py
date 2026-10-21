import os

from django import forms

from .models import Producto

EXTENSIONES_VALIDAS = ('.jpg', '.jpeg', '.png', '.webp')
TAMANIO_MAXIMO_MB = 5


class ProductoForm(forms.ModelForm):
    class Meta:
        model = Producto
        fields = ['nombre', 'categoria', 'descripcion', 'imagen']
        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'form-control'}),
            'categoria': forms.Select(attrs={'class': 'form-select'}),
            'descripcion': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
            'imagen': forms.ClearableFileInput(attrs={'class': 'form-control', 'accept': 'image/*'}),
        }

    def __init__(self, *args, **kwargs):
        # ids simples (nombre, categoria, ...) para que productos.js los encuentre
        kwargs.setdefault('auto_id', '%s')
        super().__init__(*args, **kwargs)
        self.fields['categoria'].choices = [('', 'Seleccione una categoría')] + list(Producto.categorias)

    def clean_nombre(self):
        nombre = self.cleaned_data['nombre'].strip()
        if not nombre:
            raise forms.ValidationError('Debe ingresar el nombre del producto.')
        return nombre

    def clean_descripcion(self):
        descripcion = self.cleaned_data['descripcion'].strip()
        if len(descripcion) < 10:
            raise forms.ValidationError('La descripción debe ser más detallada (mínimo 10 caracteres).')
        return descripcion

    def clean_imagen(self):
        imagen = self.cleaned_data.get('imagen')
        # Al modificar sin subir una imagen nueva, Django devuelve el archivo ya guardado.
        if imagen and hasattr(imagen, 'size') and hasattr(imagen, 'content_type'):
            extension = os.path.splitext(imagen.name)[1].lower()
            if extension not in EXTENSIONES_VALIDAS:
                raise forms.ValidationError('Formato no permitido. Use JPG, PNG o WEBP.')
            if imagen.size > TAMANIO_MAXIMO_MB * 1024 * 1024:
                raise forms.ValidationError(f'La imagen no puede superar los {TAMANIO_MAXIMO_MB} MB.')
        return imagen
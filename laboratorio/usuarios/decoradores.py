from functools import wraps

from django.core.exceptions import PermissionDenied
from django.shortcuts import redirect


def rol_requerido(*roles):
    """Permite el acceso solo a usuarios logueados cuyo rol esté en la lista."""
    def decorador(vista):
        @wraps(vista)
        def envoltura(request, *args, **kwargs):
            if not request.user.is_authenticated:
                return redirect('home')
            if not request.user.rol or request.user.rol.nombre not in roles:
                raise PermissionDenied('Acceso denegado. No tenés permiso para ver esta página.')
            return vista(request, *args, **kwargs)
        return envoltura
    return decorador
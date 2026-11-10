def login_error(request):
    """
    Expone (una sola vez) el error del último intento fallido de inicio de sesión,
    para que base.html reabra el modal de login mostrando el motivo.
    """
    sesion = getattr(request, 'session', None)
    if sesion is None:
        return {}
    error = sesion.pop('login_error', None)
    email = sesion.pop('login_email', '')
    return {'login_error': error, 'login_email': email}

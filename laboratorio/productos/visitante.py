import uuid

COOKIE_NOMBRE = 'poncho_vid'
UN_ANIO = 60 * 60 * 24 * 365


def obtener_visitor_id(request):
    """Devuelve (visitor_id, es_nuevo). Si la cookie no existe o es inválida, genera un UUID nuevo."""
    valor = request.COOKIES.get(COOKIE_NOMBRE, '')
    try:
        return str(uuid.UUID(valor)), False
    except ValueError:
        return str(uuid.uuid4()), True


def guardar_cookie(respuesta, visitor_id):
    respuesta.set_cookie(
        COOKIE_NOMBRE, visitor_id,
        max_age=UN_ANIO, httponly=True, samesite='Lax'
    )
    return respuesta
from agentes.perfil_usuario import leer_preferencias

def generar_recomendaciones(libros):
    preferencias = leer_preferencias()
    if not preferencias:
        return [], "No hay suficientes preferencias para hacer recomendaciones."

    genero_preferido = max(preferencias, key=preferencias.get)
    libros_recomendados = [libro for libro in libros if libro["genero"] == genero_preferido]
    mensaje = f"Basado en tus gustos, te recomendamos libros de género: {genero_preferido}"
    return libros_recomendados, mensaje

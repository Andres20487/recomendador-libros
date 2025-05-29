from flask import Flask, render_template, request
from rdflib import Graph, Namespace, URIRef
from rdflib.namespace import RDF
import os

app = Flask(__name__)

# Cargar la ontología
g = Graph()
g.parse("ontologia.owl", format="xml")
print("Ontología cargada correctamente.")
print("Total de triples cargados:", len(g))

# Namespace base
EX = Namespace("http://example.org/")

# Archivo para guardar preferencias
PREFERENCIAS_FILE = "preferencias.txt"

def guardar_preferencia(genero, valor):
    """Guarda la preferencia de género (Me gusta o No me gusta) en un archivo."""
    with open(PREFERENCIAS_FILE, "a", encoding="utf-8") as f:
        f.write(f"{genero},{valor}\n")

def obtener_libros_con_detalles():
    libros = []

    for libro_uri in g.subjects(RDF.type, EX.Libro):
        titulo = g.value(libro_uri, EX.titulo)
        isbn = g.value(libro_uri, EX.isbn)

        autor_uri = g.value(libro_uri, EX.escritoPor)
        autor_nombre = g.value(autor_uri, EX.nombre) if autor_uri else "Desconocido"
        autor_pais = g.value(autor_uri, EX.pais) if autor_uri else "Desconocido"

        genero_uri = g.value(libro_uri, EX.perteneceAGenero)
        genero = genero_uri.split("/")[-1] if genero_uri else "Desconocido"

        libros.append({
            "nombre": str(titulo) if titulo else "Sin título",
            "isbn": str(isbn) if isbn else "N/A",
            "genero": genero,
            "anio": "N/A",
            "autor": str(autor_nombre),
            "pais_autor": str(autor_pais)
        })

    return libros

def leer_preferencias():
    """Lee el archivo de preferencias y devuelve un diccionario con conteo de 'me gusta' por género."""
    preferencias = {}
    if os.path.exists(PREFERENCIAS_FILE):
        with open(PREFERENCIAS_FILE, "r", encoding="utf-8") as f:
            for linea in f:
                partes = linea.strip().split(",")
                if len(partes) == 2:
                    genero, valor = partes
                    if valor == "me_gusta":
                        preferencias[genero] = preferencias.get(genero, 0) + 1
    return preferencias


@app.route('/')
def index():
    libros = obtener_libros_con_detalles()
    return render_template('index.html', libros=libros)

@app.route('/preferencia', methods=['POST'])
def registrar_preferencia():
    genero = request.form['genero']
    valor = request.form['valor']
    guardar_preferencia(genero, valor)
    return "Preferencia registrada", 200

@app.route('/recomendaciones')
def recomendaciones():
    libros = obtener_libros_con_detalles()
    preferencias = leer_preferencias()

    if not preferencias:
        mensaje = "No hay suficientes preferencias para hacer recomendaciones."
        libros_recomendados = []
    else:
        genero_preferido = max(preferencias, key=preferencias.get)
        libros_recomendados = [libro for libro in libros if libro["genero"] == genero_preferido]
        mensaje = f"Basado en tus gustos, te recomendamos libros de género: {genero_preferido}"

    return render_template("recomendaciones.html", libros=libros_recomendados, mensaje=mensaje)

if __name__ == '__main__':
    app.run(debug=True)

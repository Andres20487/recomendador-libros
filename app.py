from flask import Flask, render_template, request
from rdflib import Graph, Namespace, URIRef
from rdflib.namespace import RDF
import os

from agentes.perfil_usuario import guardar_preferencia
from agentes.recomendador import generar_recomendaciones

app = Flask(__name__)

# Cargar la ontología
g = Graph()
g.parse("ontologia.owl", format="xml")
print("Ontología cargada correctamente.")
print("Total de triples cargados:", len(g))

# Namespace base
EX = Namespace("http://example.org/")

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

@app.route('/')
def index():
    libros = obtener_libros_con_detalles()
    return render_template('index.html', libros=libros)

@app.route('/preferencia', methods=['POST'])
def registrar_preferencia():
    genero = request.form['genero']
    valor = request.form['valor']
    nombre_libro = request.form.get('libro', 'Libro desconocido')
    guardar_preferencia(genero, valor)
    return render_template("feedback.html", accion=valor, libro=nombre_libro)

@app.route('/recomendaciones')
def recomendaciones():
    libros = obtener_libros_con_detalles()
    libros_recomendados, mensaje = generar_recomendaciones(libros)
    return render_template("recomendaciones.html", libros=libros_recomendados, mensaje=mensaje)

@app.route('/feedbacks')
def ver_feedbacks():
    registros = []
    if os.path.exists("preferencias.txt"):
        with open("preferencias.txt", "r", encoding="utf-8") as f:
            for linea in f:
                if "," in linea:
                    genero, accion = linea.strip().split(",")
                    registros.append((genero, accion))
    return render_template("feedbacks.html", registros=registros)

if __name__ == '__main__':
    app.run(debug=True)

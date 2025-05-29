from rdflib import Graph, Namespace
from rdflib.namespace import RDF, RDFS

g = Graph()
g.parse("ontologia.owl", format="xml")

print("Ontología cargada correctamente.")
print(f"Total de triples cargados: {len(g)}")

EX = Namespace("http://example.org/")

consulta = """
PREFIX ex: <http://example.org/>

SELECT ?titulo WHERE {
  ?libro a ex:Libro .
  ?libro ex:titulo ?titulo .
}
"""

resultados = g.query(consulta)

print(" Libros en la ontología:")
for fila in resultados:
    print(f"- {fila['titulo']}")

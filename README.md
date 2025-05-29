
# Recomendador de Libros con Web Semántica y Agentes Inteligentes

Este sistema recomienda libros personalizados según los intereses del usuario, combinando tecnologías de la Web Semántica (RDF, OWL, SPARQL) y lógica de agentes inteligentes. La interfaz está desarrollada con Flask y permite registrar preferencias directamente desde la web.

---

## Tecnologías utilizadas

- Python 3.x  
- Flask  
- RDFLib  
- OWL / RDF  
- SPARQL

---

## Estructura del proyecto

```
proyecto_recomendador_libros/
│
├── app.py                  # Lógica principal del sistema
├── ontologia.owl           # Ontología RDF/OWL con libros, autores y géneros
├── preferencias.txt        # Archivo donde se guardan las preferencias
├── templates/
│   ├── index.html          # Página principal con listado de libros
│   └── recomendaciones.html # Recomendaciones basadas en gustos
```

---

## Requisitos previos

Antes de ejecutar el proyecto, asegúrate de tener instalado:

```bash
pip install flask rdflib
```

---

## Cómo ejecutar

1. Clona este repositorio.
2. Asegúrate de que `ontologia.owl` esté en la raíz del proyecto.
3. Ejecuta el servidor:

```bash
python app.py
```

4. Abre tu navegador y visita:  
`http://localhost:5000`

---

## ¿Qué hace el sistema?

- Carga libros desde una ontología OWL.
- Muestra detalles de cada libro (autor, género, ISBN...).
- Permite marcar libros como "Me gusta" o "No me gusta".
- Almacena preferencias en un archivo `.txt`.
- Genera recomendaciones basadas en los géneros preferidos del usuario.

---


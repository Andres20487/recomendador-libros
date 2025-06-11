import os

PREFERENCIAS_FILE = "preferencias.txt"

def guardar_preferencia(genero, valor):
    with open(PREFERENCIAS_FILE, "a", encoding="utf-8") as f:
        f.write(f"{genero},{valor}\n")

def leer_preferencias():
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

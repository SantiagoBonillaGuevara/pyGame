# configuracion.py
dificultad_actual = "Fácil"

selecciones = {
    "personaje": "Arcade",
    "enemigos": "Arcade",
    "balas": "Arcade",
    "fondo": "Arcade",
    "sonido": "Arcade"
}

def set_opcion(tipo, valor):
    selecciones[tipo] = valor

def get_opcion(tipo):
    return selecciones[tipo]

def set_dificultad(nueva):
    global dificultad_actual
    dificultad_actual = nueva
    print(f"Dificultad establecida en: {dificultad_actual}")

def get_dificultad():
    return dificultad_actual
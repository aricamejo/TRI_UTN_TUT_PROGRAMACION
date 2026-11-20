def es_consulta(comando):
    """Devuelve True si el comando SCPI termina en signo de pregunta."""
    if not isinstance(comando, str):
        return False
    return comando.endswith("?")


def validar(comando):
    """
    Valida la sintaxis básica de un comando SCPI.
    Devuelve None si es válido, o un texto descriptivo del error si no lo es.
    """
    if not isinstance(comando, str) or comando == "":
        return "El comando no puede estar vacío"

    if not comando.startswith((":", "*")):
        return "El comando debe empezar con ':' o '*'"

    if "  " in comando:
        return "El comando no puede contener dos espacios seguidos"

    if comando.count("?") > 1:
        return "El comando puede contener a lo sumo un '?'"

    if "?" in comando and not comando.endswith("?"):
        return "El '?' debe ir únicamente al final del comando"

    if es_consulta(comando):
        if " " in comando:
            return "Una consulta no lleva argumentos ni espacios"
    else:
        partes = comando.split(" ")
        if len(partes) != 2 or partes[1] == "":
            return "Una orden debe llevar exactamente un argumento"

    return None


# ---------------- PRUEBAS ----------------

# Pruebas de es_consulta()
assert es_consulta("*IDN?") is True
assert es_consulta(":MEASUrement:CH1:FREQuency?") is True
assert es_consulta(":CH1:DISPlay ON") is False

# Pruebas de validar() con comandos válidos
assert validar("*IDN?") is None
assert validar(":MEASUrement:CH1:FREQuency?") is None
assert validar(":CH1:DISPlay ON") is None
assert validar(":CH1:SCALe 1v") is None

# Pruebas de validar() rompiendo cada una de las 7 reglas
assert validar("") == "El comando no puede estar vacío"
assert validar("CH1:DISPlay ON") == "El comando debe empezar con ':' o '*'"
assert validar(":CH1:DISPlay  ON") == "El comando no puede contener dos espacios seguidos"
assert validar(":CH1:DISPlay??") == "El comando puede contener a lo sumo un '?'"
assert validar(":CH1:DIS?Play") == "El '?' debe ir únicamente al final del comando"
assert validar(":CH1:DISPlay ON?") == "Una consulta no lleva argumentos ni espacios"
assert validar(":CH1:SCALe 1 v") == "Una orden debe llevar exactamente un argumento"
assert validar(":CH1:DISPlay") == "Una orden debe llevar exactamente un argumento"

print("pruebas OK")
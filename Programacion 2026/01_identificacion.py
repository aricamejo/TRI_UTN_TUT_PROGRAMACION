def parsear_idn(respuesta):
    # Descartamos respuestas vacías o mensajes de error explícitos
    if not respuesta or respuesta.strip().startswith("ERROR"):
        return None

    # Separamos la respuesta en campos usando las comas
    datos = respuesta.split(",")

    # Si hay menos de cuatro campos, la respuesta no sirve
    if len(datos) < 4:
        return None

    # Nos quedamos con los primeros cuatro campos y quitamos espacios sobrantes
    fabricante = datos[0].strip()
    modelo = datos[1].strip()
    serie = datos[2].strip()
    version = datos[3].strip()

    # Si alguno de los cuatro campos obligatorios quedó vacío, no sirve
    if not fabricante or not modelo or not serie or not version:
        return None

    # Armamos el diccionario con los datos del instrumento
    return {
        "fabricante": fabricante,
        "modelo": modelo,
        "serie": serie,
        "version": version
    }

    return equipo


# ---------------- PRUEBAS ----------------

# Caso 1: respuesta del osciloscopio (cuatro campos)
resultado = parsear_idn("OWON,ADS3202,25470803,V1.2.0")
assert resultado["modelo"] == "ADS3202"

# Caso 2: respuesta del multímetro (cinco campos)
resultado = parsear_idn("OWON,XDM1041,25470803,V4.4.0,3")
assert resultado["version"] == "V4.4.0"

# Caso 3: respuesta con menos de cuatro campos
assert parsear_idn("OWON,ADS3202,25470803") is None

# Caso 4: respuesta vacía
assert parsear_idn("") is None

# Caso 5: campos con espacios alrededor
resultado = parsear_idn(" OWON , ADS3202 , 25470803 , V1.2.0 ")
assert resultado["fabricante"] == "OWON"

# Caso 6: respuesta de error del instrumentop
assert parsear_idn("ERROR: comando desconocido") is None

print("pruebas OK")

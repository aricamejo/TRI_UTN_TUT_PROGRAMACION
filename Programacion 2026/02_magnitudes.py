import math


def a_numero(texto):
    try:
        numero = float(texto)
        if math.isnan(numero) or math.isinf(numero):
            return None
        return numero
    except (ValueError, TypeError):
        return None


def con_unidad(valor, unidad):
    if valor == 0:
        return f"0 {unidad}"

    prefijos = [
        ("p", 1e-12),
        ("n", 1e-9),
        ("u", 1e-6),
        ("m", 1e-3),
        ("", 1.0),
        ("k", 1e3),
        ("M", 1e6),
        ("G", 1e9),
    ]

    magnitud = abs(valor)

    # Buscamos el índice del prefijo adecuado (de mayor a menor)
    indice = 0
    for i in range(len(prefijos) - 1, -1, -1):
        if magnitud >= prefijos[i][1]:
            indice = i
            break

    prefijo, factor = prefijos[indice]
    convertido = round(valor / factor, 3)

    # Si al redondear llega a 1000 (o -1000) y no es el prefijo más grande, subimos un nivel
    if abs(convertido) >= 1000 and indice < len(prefijos) - 1:
        indice += 1
        prefijo, factor = prefijos[indice]
        convertido = round(valor / factor, 3)

    return f"{convertido:g} {prefijo}{unidad}"


# ---------------- PRUEBAS ----------------

# Pruebas de a_numero()
assert a_numero("1.000000E+03") == 1000.0
assert a_numero("2.5E+02") == 250.0
assert a_numero("hola") is None
assert a_numero("NaN") is None
assert a_numero("2,003812") is None

# Pruebas de con_unidad()
assert con_unidad(1000.0, "Hz") == "1 kHz"
assert con_unidad(2500.0, "Hz") == "2.5 kHz"
assert con_unidad(2.0, "V") == "2 V"
assert con_unidad(0.707, "V") == "707 mV"
assert con_unidad(0.0005, "s") == "500 us"
assert con_unidad(0.0, "V") == "0 V"
assert con_unidad(-0.707, "V") == "-707 mV"

# Caso especial de redondeo
assert con_unidad(999.9999, "Hz") == "1 kHz"

print("pruebas OK")
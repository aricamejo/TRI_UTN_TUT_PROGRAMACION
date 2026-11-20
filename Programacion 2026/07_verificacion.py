import math


def vrms_teorico(vpp):
    """
    Calcula el Vrms teórico de una onda senoidal a partir de su Vpp.
    Devuelve None si vpp es None, no es numérico o no es positivo.
    """
    if vpp is None or isinstance(vpp, bool) or not isinstance(vpp, (int, float)):
        return None
    if math.isnan(vpp) or math.isinf(vpp) or vpp <= 0:
        return None

    vp = vpp / 2.0
    return vp / math.sqrt(2)


def coincide(medido, teorico, tolerancia=0.02):
    """
    Devuelve True si el valor medido está dentro de la tolerancia relativa
    respecto al teórico (2% por defecto).
    """
    if medido is None or teorico is None or teorico == 0:
        return False

    error = abs(medido - teorico) / abs(teorico)
    return error <= tolerancia


def verificar_canal(filas, canal):
    """
    Busca PKPK y CYCRMS de un canal en el resultado de barrer() y
    verifica si la medición de Vrms coincide con la predicción senoidal.
    """
    vpp_medido = None
    vrms_medido = None

    for fila in filas:
        if fila.get("canal") == canal:
            if fila.get("magnitud") == "PKPK":
                vpp_medido = fila.get("valor")
            elif fila.get("magnitud") == "CYCRMS":
                vrms_medido = fila.get("valor")

    teorico = vrms_teorico(vpp_medido)
    ok = coincide(vrms_medido, teorico)

    return {
        "canal": canal,
        "vpp": vpp_medido,
        "vrms_medido": vrms_medido,
        "vrms_teorico": teorico,
        "coincide": ok,
    }


# ---------------- PRUEBAS ----------------

# 1. Prueba de vrms_teorico con valores válidos e inválidos
assert round(vrms_teorico(2.0), 4) == 0.7071
assert vrms_teorico(0) is None
assert vrms_teorico(-2.0) is None
assert vrms_teorico(None) is None

# 2. Prueba de coincide con tolerancia (simula el "temblor" real del instrumento)
assert coincide(0.709, 0.7071) is True       # ~0.27% de error -> dentro del 2%
assert coincide(0.750, 0.7071) is False      # ~6.07% de error -> fuera del 2%
assert coincide(None, 0.7071) is False

# 3. Prueba de verificar_canal con señal senoidal válida (2 Vpp -> ~0.7071 Vrms)
barrido_senoidal = [
    {"canal": "CH1", "magnitud": "FREQ", "unidad": "Hz", "crudo": "1.00E+03", "valor": 1000.0},
    {"canal": "CH1", "magnitud": "PKPK", "unidad": "V", "crudo": "2.00E+00", "valor": 2.0},
    {"canal": "CH1", "magnitud": "CYCRMS", "unidad": "V", "crudo": "7.09E-01", "valor": 0.709},
]
res_seno = verificar_canal(barrido_senoidal, "CH1")
assert res_seno["coincide"] is True

# 4. Prueba que demuestra que la verificación sirve (recuadro amarillo de la consigna):
# Señal cuadrada de 2 Vpp -> tiene Vrms = 1.0 V (no 0.7071 V), debe dar False
barrido_cuadrada = [
    {"canal": "CH1", "magnitud": "PKPK", "unidad": "V", "crudo": "2.00E+00", "valor": 2.0},
    {"canal": "CH1", "magnitud": "CYCRMS", "unidad": "V", "crudo": "1.00E+00", "valor": 1.0},
]
res_cuadrada = verificar_canal(barrido_cuadrada, "CH1")
assert res_cuadrada["coincide"] is False

# 5. Caso borde: canal inexistente en el barrido
res_inexistente = verificar_canal(barrido_senoidal, "CH3")
assert res_inexistente["coincide"] is False

print("pruebas OK")
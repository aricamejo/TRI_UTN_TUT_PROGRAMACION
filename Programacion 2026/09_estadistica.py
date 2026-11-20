import importlib
import math


def resumen(valores):
    """
    Calcula n, minimo, maximo, promedio y desvío estándar muestral de una lista.
    Devuelve None si la lista está vacía.
    """
    if not valores:
        return None

    n = len(valores)
    minimo = min(valores)
    maximo = max(valores)
    promedio = sum(valores) / n

    if n == 1:
        desvio = 0.0
    else:
        suma_cuadrados = sum((v - promedio) ** 2 for v in valores)
        desvio = math.sqrt(suma_cuadrados / (n - 1))

    return {
        "n": n,
        "minimo": minimo,
        "maximo": maximo,
        "promedio": promedio,
        "desvio": desvio,
    }


def fuera_de_rango(valores, minimo, maximo):
    """
    Devuelve una lista con los índices de los valores que están
    estrictamente fuera de [minimo, maximo]. Los extremos cuentan como adentro.
    """
    posiciones = []
    for i, valor in enumerate(valores):
        if valor < minimo or valor > maximo:
            posiciones.append(i)
    return posiciones


# ---------------- PRUEBAS ----------------

# 1. Caso borde: lista vacía en resumen() y un solo elemento (desvio = 0.0)
assert resumen([]) is None
assert resumen([42.0]) == {
    "n": 1,
    "minimo": 42.0,
    "maximo": 42.0,
    "promedio": 42.0,
    "desvio": 0.0,
}

# 2. Prueba numérica conocida: [2, 4, 4, 4, 5, 5, 7, 9] -> promedio = 5.0
datos = [2.0, 4.0, 4.0, 4.0, 5.0, 5.0, 7.0, 9.0]
est = resumen(datos)
assert est["n"] == 8
assert est["minimo"] == 2.0
assert est["maximo"] == 9.0
assert est["promedio"] == 5.0
assert round(est["desvio"], 4) == 2.1381

# 3. Prueba de fuera_de_rango() incluyendo extremos exactos
muestras = [990.0, 995.0, 1000.0, 1005.0, 1012.0]
# Extremos 995.0 (índice 1) y 1005.0 (índice 3) cuentan como adentro
assert fuera_de_rango(muestras, 995.0, 1005.0) == [0, 4]
assert fuera_de_rango([], 0.0, 10.0) == []

# 4. Prueba de control de la consigna sobre mediciones.log (CH1 FREQ)
mod_log = importlib.import_module("08_log")
series_log, _ = mod_log.leer_log("mediciones.log")
freq_ch1 = series_log[("ADS3202", "CH1", "FREQ")]

res_ch1 = resumen(freq_ch1)
assert abs(res_ch1["promedio"] - 1000.0) < 5.0   # Menos del 0.5% de 1000 Hz
assert res_ch1["desvio"] < 5.0                    # Desvío menor que 5 Hz

print("pruebas OK")
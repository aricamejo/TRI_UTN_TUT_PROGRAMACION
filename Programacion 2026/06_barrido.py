import importlib

mod_magnitudes = importlib.import_module("02_magnitudes")


def barrer(instrumento, canales):
    """
    Consulta FREQ, PKPK y CYCRMS para cada canal indicado.
    Devuelve una lista de diccionarios con canal, magnitud, unidad, crudo y valor.
    """
    mediciones = [
        ("FREQ", "FREQuency", "Hz"),
        ("PKPK", "PKPK", "V"),
        ("CYCRMS", "CYCRms", "V"),
    ]

    resultados = []

    for canal in canales:
        for nombre_mag, comando_scpi, unidad in mediciones:
            consulta = f":MEASUrement:{canal}:{comando_scpi}?"
            crudo = instrumento.preguntar(consulta)
            valor = mod_magnitudes.a_numero(crudo)

            resultados.append({
                "canal": canal,
                "magnitud": nombre_mag,
                "unidad": unidad,
                "crudo": crudo,
                "valor": valor,
            })

    return resultados


# ---------------- PRUEBAS ----------------

class InstrumentoFalso:
    """Simula un instrumento SCPI para probar barrer() sin red ni ruido."""

    def __init__(self, respuestas):
        self.respuestas = respuestas

    def preguntar(self, comando):
        return self.respuestas.get(comando, "ERROR: comando desconocido")


# 1. Prueba de barrido completo en 2 canales (6 mediciones) sin red
falso_ok = InstrumentoFalso({
    ":MEASUrement:CH1:FREQuency?": "1.000000E+03",
    ":MEASUrement:CH1:PKPK?": "2.000000E+00",
    ":MEASUrement:CH1:CYCRms?": "7.071068E-01",
    ":MEASUrement:CH2:FREQuency?": "2.500000E+03",
    ":MEASUrement:CH2:PKPK?": "8.000000E-01",
    ":MEASUrement:CH2:CYCRms?": "2.828427E-01",
})

filas = barrer(falso_ok, ["CH1", "CH2"])
assert len(filas) == 6
assert filas[0] == {
    "canal": "CH1",
    "magnitud": "FREQ",
    "unidad": "Hz",
    "crudo": "1.000000E+03",
    "valor": 1000.0,
}
assert filas[4]["canal"] == "CH2"
assert filas[4]["magnitud"] == "PKPK"
assert filas[4]["valor"] == 0.8

# 2. Caso borde: instrumento devuelve error en una medición (valor=None, crudo guardado)
falso_error = InstrumentoFalso({
    ":MEASUrement:CH1:FREQuency?": "ERROR: sin señal",
    ":MEASUrement:CH1:PKPK?": "0.000000E+00",
    ":MEASUrement:CH1:CYCRms?": "0.000000E+00",
})
filas_err = barrer(falso_error, ["CH1"])
assert len(filas_err) == 3
assert filas_err[0]["crudo"] == "ERROR: sin señal"
assert filas_err[0]["valor"] is None

# 3. Caso borde: lista de canales vacía
assert barrer(falso_ok, []) == []

print("pruebas OK")
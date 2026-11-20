import importlib

mod_magnitudes = importlib.import_module("02_magnitudes")


def _hora_valida(hora_txt):
    """Verifica que la hora tenga formato HH:MM:SS y valores reales (00-23, 00-59, 00-59)."""
    partes = hora_txt.split(":")
    if len(partes) != 3:
        return False
    try:
        hh, mm, ss = int(partes[0]), int(partes[1]), int(partes[2])
    except ValueError:
        return False
    return 0 <= hh <= 23 and 0 <= mm <= 59 and 0 <= ss <= 59


def _fecha_valida(fecha_txt):
    """Verifica formato básico AAAA-MM-DD."""
    partes = fecha_txt.split("-")
    if len(partes) != 3:
        return False
    try:
        anio, mes, dia = int(partes[0]), int(partes[1]), int(partes[2])
    except ValueError:
        return False
    return anio > 0 and 1 <= mes <= 12 and 1 <= dia <= 31


def analizar_linea(linea):
    """
    Analiza una línea de mediciones.log.
    Devuelve (medicion, motivo) donde uno de los dos siempre es None.
    Si la línea debe ignorarse (vacía o comentario #), devuelve (None, None).
    """
    texto = linea.strip()

    # Líneas ignoradas (no son error)
    if not texto or texto.startswith("#"):
        return (None, None)

    # Usamos split() sin argumentos para soportar tanto espacios como tabulaciones
    campos = texto.split()

    if len(campos) != 6:
        return (None, f"cantidad de campos incorrecta ({len(campos)} en lugar de 6)")

    fecha, hora, equipo, canal, magnitud, valor_txt = campos

    if not _fecha_valida(fecha):
        return (None, f"fecha inválida: {fecha}")

    if not _hora_valida(hora):
        return (None, f"hora imposible: {hora}")

    if canal not in ("CH1", "CH2"):
        return (None, f"canal inválido: {canal}")

    if magnitud not in ("FREQ", "PKPK", "CYCRMS"):
        return (None, f"magnitud inválida: {magnitud}")

    valor = mod_magnitudes.a_numero(valor_txt)
    if valor is None:
        return (None, f"valor no numérico: {valor_txt}")

    medicion = {
        "fecha": fecha,
        "hora": hora,
        "equipo": equipo,
        "canal": canal,
        "magnitud": magnitud,
        "valor": valor,
    }
    return (medicion, None)


def leer_log(ruta):
    """
    Lee un archivo .log y devuelve (series, rechazadas).
    - series: diccionario {(equipo, canal, magnitud): [valores...]}
    - rechazadas: lista de diccionarios con linea, texto y motivo
    """
    series = {}
    rechazadas = []

    with open(ruta, "r", encoding="utf-8") as archivo:
        for num_linea, linea in enumerate(archivo, start=1):
            medicion, motivo = analizar_linea(linea)

            if motivo is not None:
                rechazadas.append({
                    "linea": num_linea,
                    "texto": linea.strip(),
                    "motivo": motivo,
                })
            elif medicion is not None:
                clave = (medicion["equipo"], medicion["canal"], medicion["magnitud"])
                if clave not in series:
                    series[clave] = []
                series[clave].append(medicion["valor"])

    return series, rechazadas


# ---------------- PRUEBAS ----------------

# 1. Líneas ignoradas (vacía y comentario) -> (None, None)
assert analizar_linea("   \n") == (None, None)
assert analizar_linea("# reconexion del puerto LAN\n") == (None, None)

# 2. Línea válida estándar y línea válida separada por tabulaciones (trampa de la consigna)
med_ok, mot_ok = analizar_linea("2026-09-08 09:14:00 ADS3202 CH1 FREQ 9.993761E+02\n")
assert mot_ok is None and med_ok["valor"] == 999.3761

med_tab, mot_tab = analizar_linea("2026-09-08\t09:17:31\tADS3202\tCH1\tFREQ\t1.001000E+03\n")
assert mot_tab is None and med_tab["valor"] == 1001.0

# 3. Casos rechazados reales extraídos de mediciones.log
assert analizar_linea("2026-09-08 09:14:31 ADS3202 CH1 FREQ ERROR: comando desconocido")[0] is None
assert analizar_linea("2026-09-08 09:15:01 ADS3202 CH2 PKPK")[0] is None
assert analizar_linea("2026-09-08 09:15:31 ADS3202 CH1 PKPK 2,003812")[0] is None
assert analizar_linea("2026-09-08 09:16:01 ADS3202 CH2 CYCRMS NaN")[0] is None
assert analizar_linea("2026-09-08 09:16:31 ADS3202 CH3 FREQ 1.000000E+03")[0] is None
assert analizar_linea("2026-09-08 09:17:01 ADS3202 CH1 TEMP 3.150000E+02")[0] is None
assert analizar_linea("2026-09-08 25:61:00 ADS3202 CH2 FREQ 2.500000E+03")[0] is None
assert analizar_linea("2026-09-08 09:18:31 ADS3202 CH1 CYCRMS 7.071000E-01 VERIFICADO")[0] is None

# 4. Prueba integral sobre el archivo real mediciones.log
series_log, rechazadas_log = leer_log("mediciones.log")
assert len(rechazadas_log) == 8
assert len(series_log[("ADS3202", "CH1", "FREQ")]) == 21  # 16 regulares + 1 con tabulaciones

print("pruebas OK")
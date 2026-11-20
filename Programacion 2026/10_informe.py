import importlib

mod_idn = importlib.import_module("01_identificacion")
mod_mag = importlib.import_module("02_magnitudes")
mod_cli = importlib.import_module("05_cliente")
mod_bar = importlib.import_module("06_barrido")
mod_ver = importlib.import_module("07_verificacion")
mod_log = importlib.import_module("08_log")
mod_est = importlib.import_module("09_estadistica")

UNIDADES = {
    "FREQ": "Hz",
    "PKPK": "V",
    "CYCRMS": "V",
}


def armar_informe(idn, series, verificaciones):
    """
    Función pura: recibe los datos ya procesados y devuelve el informe
    completo en una sola cadena de texto (sin imprimir ni abrir archivos).
    """
    lineas = ["=== INFORME DEL BANCO DE MEDICIONES ==="]

    # 1. Identificación del instrumento
    if idn:
        lineas.append(
            f"Instrumento: {idn['fabricante']} {idn['modelo']} "
            f"(Serie: {idn['serie']}, Version: {idn['version']})"
        )
    else:
        lineas.append("Instrumento: No identificado")

    # 2. Resumen estadístico por serie (una línea por serie)
    lineas.append("\n--- Series registradas ---")
    if not series:
        lineas.append("Sin series registradas.")
    else:
        for clave in sorted(series.keys()):
            equipo, canal, magnitud = clave
            valores = series[clave]
            est = mod_est.resumen(valores)
            if est is None:
                continue

            unidad = UNIDADES.get(magnitud, "")
            prom_txt = mod_mag.con_unidad(est["promedio"], unidad)
            min_txt = mod_mag.con_unidad(est["minimo"], unidad)
            max_txt = mod_mag.con_unidad(est["maximo"], unidad)

            lineas.append(
                f"{equipo} {canal} {magnitud}: n={est['n']}, "
                f"promedio={prom_txt}, minimo={min_txt}, maximo={max_txt}"
            )

    # 3. Resultados de verificación en vivo
    lineas.append("\n--- Verificacion de canales ---")
    if not verificaciones:
        lineas.append("Sin verificaciones realizadas.")
    else:
        for ver in verificaciones:
            canal = ver.get("canal", "?")
            estado = "OK (coincide)" if ver.get("coincide") else "FALLA (no coincide)"
            vpp_txt = (
                mod_mag.con_unidad(ver["vpp"], "V")
                if ver.get("vpp") is not None
                else "N/A"
            )
            vrms_med_txt = (
                mod_mag.con_unidad(ver["vrms_medido"], "V")
                if ver.get("vrms_medido") is not None
                else "N/A"
            )
            vrms_teo_txt = (
                mod_mag.con_unidad(ver["vrms_teorico"], "V")
                if ver.get("vrms_teorico") is not None
                else "N/A"
            )

            lineas.append(
                f"{canal}: {estado} | Vpp={vpp_txt}, "
                f"Vrms medido={vrms_med_txt}, Vrms teorico={vrms_teo_txt}"
            )

    return "\n".join(lineas)


# ---------------- PRUEBAS (sin red ni archivos) ----------------

idn_prueba = {
    "fabricante": "OWON",
    "modelo": "ADS3202",
    "serie": "25470803",
    "version": "V1.2.0",
}
series_prueba = {
    ("ADS3202", "CH1", "FREQ"): [1000.0, 1002.0, 998.0],
}
verif_prueba = [
    {
        "canal": "CH1",
        "vpp": 2.0,
        "vrms_medido": 0.707,
        "vrms_teorico": 0.70710678,
        "coincide": True,
    },
    {
        "canal": "CH2",
        "vpp": 2.0,
        "vrms_medido": 1.0,
        "vrms_teorico": 0.70710678,
        "coincide": False,
    },
]

texto_informe = armar_informe(idn_prueba, series_prueba, verif_prueba)

# 1. Verificamos que devuelva un str con los datos del equipo y la serie con unidades
assert isinstance(texto_informe, str)
assert "OWON ADS3202" in texto_informe
assert "ADS3202 CH1 FREQ: n=3, promedio=1 kHz, minimo=998 Hz, maximo=1.002 kHz" in texto_informe

# 2. Verificamos que refleje tanto una verificación exitosa como una fallida
assert "CH1: OK (coincide)" in texto_informe
assert "CH2: FALLA (no coincide)" in texto_informe

# 3. Caso borde: instrumento no identificado, series vacías y sin verificaciones
informe_vacio = armar_informe(None, {}, [])
assert "No identificado" in informe_vacio
assert "Sin series registradas." in informe_vacio
assert "Sin verificaciones realizadas." in informe_vacio

print("pruebas OK\n")


# ---------------- EJECUCIÓN COMPLETA DEL BANCO ----------------
# (Requiere que instrumento_virtual.py esté corriendo en otra terminal)

if __name__ == "__main__":
    osc = mod_cli.Instrumento("127.0.0.1", 5555)
    try:
        respuesta_idn = osc.preguntar("*IDN?")
        equipo = mod_idn.parsear_idn(respuesta_idn)

        filas_barrido = mod_bar.barrer(osc, ["CH1", "CH2"])
        verificaciones = [
            mod_ver.verificar_canal(filas_barrido, "CH1"),
            mod_ver.verificar_canal(filas_barrido, "CH2"),
        ]
    finally:
        osc.cerrar()

    series_log, _ = mod_log.leer_log("mediciones.log")
    informe_final = armar_informe(equipo, series_log, verificaciones)
    print(informe_final)
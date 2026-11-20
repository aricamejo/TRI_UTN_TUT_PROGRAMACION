import importlib


def comandos_de_canal(canal, display, acoplamiento, sonda, escala):
    """
    Genera la lista de 4 órdenes SCPI para configurar un canal del osciloscopio.
    Devuelve None si el canal no es CH1 ni CH2.
    """
    if canal not in ("CH1", "CH2"):
        return None

    return [
        f":{canal}:DISPlay {display}",
        f":{canal}:COUPling {acoplamiento}",
        f":{canal}:PROBe {sonda}",
        f":{canal}:SCALe {escala}",
    ]


# ---------------- PRUEBAS ----------------

# 1. Prueba exacta de los 4 comandos en orden para CH1
esperado_ch1 = [
    ":CH1:DISPlay ON",
    ":CH1:COUPling DC",
    ":CH1:PROBe 10X",
    ":CH1:SCALe 1v",
]
cmds_ch1 = comandos_de_canal("CH1", "ON", "DC", "10X", "1v")
assert cmds_ch1 == esperado_ch1

# 2. Prueba para CH2
cmds_ch2 = comandos_de_canal("CH2", "OFF", "AC", "1X", "500mv")
assert cmds_ch2 == [
    ":CH2:DISPlay OFF",
    ":CH2:COUPling AC",
    ":CH2:PROBe 1X",
    ":CH2:SCALe 500mv",
]

# 3. Caso borde: canal inexistente devuelve None
assert comandos_de_canal("CH3", "ON", "DC", "10X", "1v") is None
assert comandos_de_canal("ch1", "ON", "DC", "10X", "1v") is None

# 4. Prueba cruzada con validar() del ejercicio 3 ("una prueba que vale por diez")
mod_comandos = importlib.import_module("03_comandos")
for cmd in cmds_ch1:
    assert mod_comandos.validar(cmd) is None

print("pruebas OK")
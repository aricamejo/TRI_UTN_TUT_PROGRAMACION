import importlib
import socket


class Instrumento:
    """Cliente TCP para comunicarse con instrumentos SCPI por red."""

    def __init__(self, direccion="127.0.0.1", puerto=5555):
        self.direccion = direccion
        self.puerto = puerto
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.settimeout(2.0)
        self.sock.connect((self.direccion, self.puerto))
        self.lector = self.sock.makefile("r", encoding="utf-8")

    def enviar(self, comando):
        """Manda una orden SCPI terminada en salto de línea y no espera respuesta."""
        mensaje = comando.strip() + "\n"
        self.sock.sendall(mensaje.encode("utf-8"))

    def preguntar(self, comando):
        """Manda una consulta SCPI y devuelve la respuesta limpia (sin \\n)."""
        self.enviar(comando)
        respuesta = self.lector.readline()
        return respuesta.strip()

    def cerrar(self):
        """Cierra la conexión de red con el instrumento."""
        self.lector.close()
        self.sock.close()


# ---------------- PRUEBAS ----------------
# IMPORTANTE: Para correr estas pruebas tiene que estar corriendo
# `python3 instrumento_virtual.py` en otra terminal.

mod_idn = importlib.import_module("01_identificacion")

osc = Instrumento()  # Usa 127.0.0.1 y 5555 por defecto

# 1. Consulta *IDN? devuelve el texto exacto esperado
respuesta_idn = osc.preguntar("*IDN?")
assert respuesta_idn == "OWON,ADS3202,25470803,V1.2.0"

# 2. Pasada por parsear_idn del ejercicio 1, el modelo es ADS3202
datos_equipo = mod_idn.parsear_idn(respuesta_idn)
assert datos_equipo is not None
assert datos_equipo["modelo"] == "ADS3202"

# 3. Prueba de enviar orden y consultar estado (verificamos que no se cuelga)
osc.enviar(":CH1:DISPlay ON")
estado_ch1 = osc.preguntar(":CH1:DISPlay?")
assert estado_ch1 != ""

# 4. Caso borde: comando inválido devuelve mensaje de error del instrumento
resp_error = osc.preguntar(":COMANDO:INEXISTENTE?")
assert resp_error.startswith("ERROR")

osc.cerrar()

print("pruebas OK")
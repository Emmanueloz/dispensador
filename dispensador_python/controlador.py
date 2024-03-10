from dispensador_python.crud import Crud
from dispensador_python.conexion_serial import ConnectionArduino
from time import sleep
from re import match
from .vista import *
from threading import Thread


def validar_string(prefijo, valor):
    """Función para validar un string con un prefijo y un número entero."""
    patron = rf"^{prefijo}:\d+$"

    if match(patron, valor):
        return True
    else:
        return False


class ControllerVista:
    def __init__(self, vista) -> None:
        self.vista: Ventana = vista
        self.inicio: Inicio = self.vista.inicio
        self.tiempo: Tiempo = self.vista.tiempo
        self.db = Crud()
        self.arduino = ConnectionArduino(puerto="COM2")
        self.estado_agua = 0
        self.estado_comida = 0
        self.hilo_lectura = Thread(target=self.leer_serial)
        self.vista.protocol("WM_DELETE_WINDOW", self.finalizar)
        self.corriendo = True

    def conectar_todo(self):
        try:
            # Conectar a la base de datos
            self.db.conectar_BD(host="localhost", user="emmanuel",
                                passwd="", database="dispensadorBD")

            # Conectar a Arduino
            if self.arduino.conectar() is not None:
                raise Exception("Error en la conexión con Arduino.")

            print("Conexión exitosa a la base de datos y Arduino.")
        except Exception as e:
            print(f"Error en la conexión: {e}")

    def finalizar(self):
        self.corriendo = False
        self.hilo_lectura.join(0.1)
        self.vista.quit()
        self.vista.destroy()
        self.db.cerrar_conexion()
        self.arduino.cerrar_arduino()

    def dispensar_agua(self):
        if self.inicio.var_dispensar_agua.get() == 1:
            self.arduino.enviar_dato("wd:1")
        else:
            self.arduino.enviar_dato("wd:0")

    def dispensar_comida(self):
        if self.inicio.var_dispensar_comida.get() == 1:
            self.arduino.enviar_dato("fd:1")
        else:
            self.arduino.enviar_dato("fd:0")

    def activar_check_button(self):
        self.inicio.check_agua.config(command=self.dispensar_agua)
        self.inicio.check_comida.config(command=self.dispensar_comida)

    def procesar_resultado(self, result):
        if result == 1:
            return "Abierto"
        elif result == 0:
            return "Cerrado"
        elif result == -1:
            return "Ya esta en ese estado"
        elif result == -2:
            return "El contenedor esta vacío"
        elif result == -3:
            return "El recipiente esta lleno"
        else:
            return "Error"

    def iniciar_estados(self):
        try:
            self.arduino.enviar_dato("all:1")
            sleep(1)
            result = self.arduino.recibir_dato()
            result = result.replace("\r", "")
            # orden de los estados:
            # wdP:0,fdP:0,wdSIs:0,fdSIs:0,wdTget:90m,fdTget:90m
            result = result.split(",")
            es_agua = int(result[0])
            msg_agua = self.procesar_resultado(es_agua)
            self.inicio.set_estado_agua(es_agua, msg_agua)
            es_alimento = int(result[1])
            msg_alimento = self.procesar_resultado(es_alimento)
            self.inicio.set_estado_comida(es_alimento, msg_alimento)

            msg_contenedor_agua = "El contenedor de agua esta lleno" if int(
                result[2]) == 0 else "El contenedor de agua esta vacío."

            msg_contenedor_alimento = "El contenedor de alimento esta lleno" if int(
                result[3]) == 0 else "El contenedor de alimento esta vacío."
            self.inicio.set_contenedor_agua(msg_contenedor_agua)
            self.inicio.set_contenedor_comida(msg_contenedor_alimento)

            msgT_agua = "Intervalo:"+result[4]
            self.tiempo.set_estado_aguaT(
                int(result[4].strip("mhs")), result[4][-1], msgT_agua)

            self.tiempo.set_estado_comidaT(
                int(result[5].strip("mhs")), result[5][-1], "Intervalo:"+result[5])

            print(result)

        except Exception as e:
            print(f"Error al iniciar los estados: {e}")

    def leer_serial(self):
        while self.corriendo:
            try:
                mensaje = self.arduino.recibir_dato()
                if mensaje.startswith("wdP:") or mensaje.startswith("wdR:"):
                    result = int(mensaje.split(":")[1])
                    msg = self.procesar_resultado(result)
                    self.inicio.set_estado_agua(result, msg)
                    if result == -2:
                        self.inicio.set_contenedor_agua(
                            "El contenedor de agua esta vacío.")
                    elif result == 1 or result == 0:
                        self.inicio.set_contenedor_agua(
                            "El contenedor de agua esta lleno")

                elif mensaje.startswith("fdP:") or mensaje.startswith("fdR:"):
                    result = int(mensaje.split(":")[1])
                    msg = self.procesar_resultado(result)
                    self.inicio.set_estado_comida(result, msg)
                    if result == -2:
                        self.inicio.set_contenedor_comida(
                            "El contenedor de alimento esta vació.")
                    elif result == 1 or result == 0:
                        self.inicio.set_contenedor_comida(
                            "El contenedor de alimento esta lleno")
                elif mensaje.startswith("wdACon:0"):

                    self.inicio.set_contenedor_agua(
                        "El contenedor de agua esta vacío.")
                    self.inicio.set_estado_agua(0, "Cerrado")
                elif mensaje.startswith("fdACon:0"):
                    self.inicio.set_contenedor_comida(
                        "El contenedor de alimento esta vació.")
                    self.inicio.set_estado_comida(0, "Cerrado")

                elif mensaje.startswith("wdARes:0"):
                    self.inicio.set_estado_agua(
                        0, "El recipiente esta lleno.")
                elif mensaje.startswith("fdARes:0"):
                    self.inicio.set_estado_comida(
                        0, "El recipiente esta lleno.")

            except Exception as error:
                print(f"Error al leer el puerto serial: {error}")

    def iniciar(self):
        self.conectar_todo()
        self.iniciar_estados()
        self.activar_check_button()
        self.hilo_lectura.start()
        self.vista.mainloop()

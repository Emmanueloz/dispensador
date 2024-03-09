from dispensador_python.crud import Crud
from dispensador_python.conexion_serial import ConnectionArduino
from time import sleep
from re import match
from .vista import *


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
        self.db = Crud()
        self.arduino = ConnectionArduino(puerto="COM2")
        self.estado_agua = 0
        self.estado_comida = 0

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

    def iniciar(self):
        self.conectar_todo()
        self.vista.mainloop()


class Controller:
    def __init__(self):
        # Crear instancias de las clases Crud y ConnectionArduino
        self.db = Crud()
        # Especifica el puerto correcto
        self.arduino = ConnectionArduino(puerto="COM2")

    def conectar_todo(self):
        try:
            # Conectar a la base de datos
            self.db.conectar_BD(host="localhost", user="emmanuel",
                                passwd="", database="dispensadorBD")

            # Conectar a Arduino
            self.arduino.conectar()
            return "Conexión exitosa a la base de datos y Arduino."
        except Exception as e:
            return f"Error en la conexión: {e}"

    def cerrar_todo(self):
        try:
            # Cerrar conexión con la base de datos
            self.db.cerrar_conexion()

            # Cerrar conexión con Arduino
            self.arduino.cerrar_arduino()
            return "Conexiones cerradas correctamente."
        except Exception as e:
            return f"Error al cerrar las conexiones: {e}"

    def abrir_dispensador_agua(self):
        try:
            comando = "wd:1"
            self.arduino.enviar_dato(comando)
            sleep(2)
            respuesta_arduino = self.arduino.recibir_dato()
            if "90" in respuesta_arduino:
                respuesta_db = self.db.insertar_registro(
                    idComponente="1", estado="ABIERTO")
                return respuesta_db
            elif "wdCount:0" == respuesta_arduino:
                return "El contenedor de agua está vacío."
            elif "-1" == respuesta_arduino:
                return "El dispensador de agua ya está abierto."
            else:
                return f"Error al abrir el dispensador de agua en el Arduino: {respuesta_arduino}"
        except Exception as error:
            return f"Error al abrir el dispensador de agua: {error}"

    def cerrar_dispensador_agua(self):
        try:
            comando = "wd:0"
            self.arduino.enviar_dato(comando)
            sleep(2)
            respuesta_arduino = self.arduino.recibir_dato()
            if "0" in respuesta_arduino:
                respuesta_db = self.db.insertar_registro(
                    idComponente="1", estado="CERRADO")
                return respuesta_db
            elif "wdCount:0" == respuesta_arduino:
                return "El contenedor de agua está vacío."
            elif "-1" == respuesta_arduino:
                return "El dispensador de agua ya está cerrado."
            else:
                return f"Error al cerrar el dispensador de agua en el Arduino: {respuesta_arduino}"
        except Exception as error:
            return f"Error al cerrar el dispensador de agua: {error}"

    def abrir_dispensador_alimento(self):
        try:
            comando = "fd:1"
            self.arduino.enviar_dato(comando)
            sleep(2)
            respuesta_arduino = self.arduino.recibir_dato()
            if "90" in respuesta_arduino:
                respuesta_db = self.db.insertar_registro(
                    idComponente="2", estado="ABIERTO")
                return respuesta_db
            elif "fdCount:0" == respuesta_arduino:
                return "El contenedor de alimento está vacío."
            elif "-1" == respuesta_arduino:
                return "El dispensador de alimento ya está abierto."
            else:
                return f"Error al abrir el dispensador de alimento en el Arduino: {respuesta_arduino}"
        except Exception as error:
            return f"Error al abrir el dispensador de alimento: {error}"

    def cerrar_dispensador_alimento(self):
        try:
            comando = "fd:0"
            self.arduino.enviar_dato(comando)
            sleep(2)
            respuesta_arduino = self.arduino.recibir_dato()
            if "0" in respuesta_arduino:
                respuesta_db = self.db.insertar_registro(
                    idComponente="2", estado="CERRADO")
                return respuesta_db
            elif "fdCount:0" == respuesta_arduino:
                return "El contenedor de alimento está vacío."
            elif "-1" == respuesta_arduino:
                return "El dispensador de cerrado ya está abierto."
            else:
                return f"Esperando"
        except Exception as error:
            return f"Esperando"

    def obtener_posicion_servo_agua(self):
        try:
            comando = "wd:2"
            self.arduino.enviar_dato(comando)
            sleep(2)
            respuesta_arduino = self.arduino.recibir_dato()

            if respuesta_arduino.startswith("wdP:"):
                posicion_servo = respuesta_arduino.split(":")[1]
                return posicion_servo
            return "Error al obtener la posición del servo de gua."

        except Exception as error:
            return f"Error al obtener la posición del servo de agua: {error}"

    def obtener_posicion_servo_alimento(self):
        """
        Obtiene la posición actual del servo de alimentación.

        Returns:
            str: Posición actual del servo (0 o 90) o mensaje de error.
        """
        try:
            comando = "fd:2"
            self.arduino.enviar_dato(comando)
            sleep(2)
            respuesta_arduino = self.arduino.recibir_dato()

            if respuesta_arduino.startswith("fdP:"):
                # Extrae el valor numérico después de "fdP:"
                posicion_servo = respuesta_arduino.split(":")[1]
                return posicion_servo

            return "Error al obtener la posición del servo de alimento."
        except Exception as error:
            return f"Error al obtener la posición del servo de alimento: {error}"

    def obtener_distancia_ultrasonico_agua(self):
        try:
            comando = "wdS:1"
            self.arduino.enviar_dato(comando)
            sleep(2)
            respuesta_arduino = self.arduino.recibir_dato()

            if respuesta_arduino.startswith("wdSget:"):
                distancia = int(respuesta_arduino.split(":")[1])
                if distancia > 38:
                    return "porfavor el agua se esta basio."
                elif distancia < 30:
                    return "El contenedor de agua está lleno."
                elif distancia < 15:
                    return "El contenedor de agua esta medio."
                else:
                    return "El contenedor de agua esta lleno"
            else:
                print(f"Respuesta no válida: {respuesta_arduino}")
                return "Error al obtener el estado del contenedor de agua: Respuesta no válida."

        except SerialException as serial_error:
            print(f"Error de comunicación serial: {str(serial_error)}")
            return f"Error de comunicación serial: {str(serial_error)}"
        except Exception as error:
            print(f"Error inesperado: {str(error)}")
            return f"Error inesperado: {str(error)}"

    def obtener_estado_contenedor_alimento(self):
        try:
            comando = "fdS:1"
            self.arduino.enviar_dato(comando)
            sleep(2)
            respuesta_arduino = self.arduino.recibir_dato()

            if respuesta_arduino.startswith("fdSget:"):
                distancia = int(respuesta_arduino.split(":")[1])
                if distancia > 40:
                    return "El contenedor de alimento está vacío."
                elif distancia < 15:
                    return "El contenedor de alimento está lleno."
                else:
                    return "El contenedor de alimento esta medio."
            else:
                print(f"Respuesta no válida: {respuesta_arduino}")
                return "Error al obtener el estado del contenedor de alimento: Respuesta no válida."

        except SerialException as serial_error:
            print(f"Error de comunicación serial: {str(serial_error)}")
            return f"Error de comunicación serial: {str(serial_error)}"
        except Exception as error:
            print(f"Error inesperado: {str(error)}")
            return f"Error inesperado: {str(error)}"

    def consultar_tarea(self, idTarea):
        try:
            return self.db.consultar_tarea(idTarea)
        except Exception as error:
            return f"Error al consultar la tarea: {error}"

    def consultar_registro(self, idComponente):
        try:
            return self.db.consultar_registro(idComponente)
        except Exception as error:
            return f"Error al consultar el registro: {error}"

    def consultar_intervalo_tiempo_agua(self):
        try:
            commad = "wdT:2"
            self.arduino.enviar_dato(commad)
            sleep(2)
            respuesta_arduino = self.arduino.recibir_dato()
            if not validar_string("wdTget", respuesta_arduino):
                return "Error al obtener el intervalo de tiempo para el dispensador de agua."
            return respuesta_arduino
        except Exception as error:
            return f"Error al obtener el intervalo de tiempo para el dispensador de agua en el arduino: {error}"

    def consultar_intervalo_tiempo_comida(self):
        try:
            commad = "fdT:2"
            self.arduino.enviar_dato(commad)
            sleep(2)
            respuesta_arduino = self.arduino.recibir_dato()
            if not validar_string("fdTget", respuesta_arduino):
                return "Error al obtener el intervalo de tiempo para el dispensador de comida."
            return respuesta_arduino
        except Exception as error:
            return f"Error al obtener el intervalo de tiempo para el dispensador de comida en el arduino: {error}"

    def definir_intervalo_tiempo_agua(self, tiempo, unidad):
        try:
            if unidad not in ['s', 'm']:
                raise ValueError(
                    "Unidad de tiempo no válida. Debe ser 's' para segundos, 'm' para minutos.")

            comando = f"wdT:{tiempo}{unidad}"
            self.arduino.enviar_dato(comando)
            sleep(2)
            respuesta_arduino = self.arduino.recibir_dato()

            # Guardar la respuesta en la tabla de registros de tareas si es correcta
            if f"wdTset:{tiempo}{unidad}" in respuesta_arduino:
                respuesta_db = self.db.insertar_tarea(
                    idComponente="1", tipo="Agua", tiempo=tiempo, unidadtiempo=unidad)
                return respuesta_db
            else:
                return f"Error al definir el intervalo de tiempo para el dispensador de agua: {respuesta_arduino}"
        except Exception as error:
            return f"Error al definir el intervalo de tiempo para el dispensador de agua: {error}"

    def definir_intervalo_tiempo_comida(self, tiempo, unidad):
        try:
            if unidad not in ['s', 'm']:
                raise ValueError(
                    "Unidad de tiempo no válida. Debe ser 's' para segundos, 'm' para minutos.")

            comando = f"fdT:{tiempo}{unidad}"
            self.arduino.enviar_dato(comando)
            sleep(2)
            respuesta_arduino = self.arduino.recibir_dato()

            # Guardar la respuesta en la tabla de registros de tareas si es correcta
            if f"fdTset:{tiempo}{unidad}" in respuesta_arduino:
                respuesta_db = self.db.insertar_tarea(
                    idComponente="2", tipo="Alimento", tiempo=tiempo, unidadtiempo=unidad)
                return respuesta_db
            else:
                return f"Error al definir el intervalo de tiempo para el dispensador de comida: {respuesta_arduino}"
        except Exception as error:
            return f"Error al definir el intervalo de tiempo para el dispensador de comida: {error}"

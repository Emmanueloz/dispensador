from dispensador_python.crud import Crud
from dispensador_python.conexion_serial import ConnectionArduino
from time import sleep


class Controller:
    def __init__(self):
        # Crear instancias de las clases Crud y ConnectionArduino
        self.db = Crud()
        # Especifica el puerto correcto
        self.arduino = ConnectionArduino(puerto="COM1")

    def conectar_todo(self, host="localhost", user="root", passwd="", database="dispensadorBD"):
        try:
            # Conectar a la base de datos
            self.db.conectar_BD(host=host, user=user,
                                passwd=passwd, database=database)

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
            sleep(1)
            respuesta_arduino = self.arduino.recibir_dato()
            if "90" in respuesta_arduino:
                respuesta_db = self.db.insertar_registro(
                    idSensor="1", estado="ABIERTO")
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
            sleep(1)
            respuesta_arduino = self.arduino.recibir_dato()
            if "0" in respuesta_arduino:
                respuesta_db = self.db.insertar_registro(
                    idSensor="1", estado="CERRADO")
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
            sleep(1)
            respuesta_arduino = self.arduino.recibir_dato()
            if "90" in respuesta_arduino:
                respuesta_db = self.db.insertar_registro(
                    idSensor="2", estado="ABIERTO")
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
            sleep(1)
            respuesta_arduino = self.arduino.recibir_dato()
            if "0" in respuesta_arduino:
                respuesta_db = self.db.insertar_registro(
                    idSensor="2", estado="CERRADO")
                return respuesta_db
            elif "fdCount:0" == respuesta_arduino:
                return "El contenedor de alimento está vacío."
            elif "-1" == respuesta_arduino:
                return "El dispensador de cerrado ya está abierto."
            else:
                return f"Error al cerrar el dispensador de alimento en el Arduino: {respuesta_arduino}"
        except Exception as error:
            return f"Error al cerrar el dispensador de alimento: {error}"

    def obtener_posicion_servo_agua(self):
        try:
            comando = "wd:2"
            self.arduino.enviar_dato(comando)
            sleep(1)
            respuesta_arduino = self.arduino.recibir_dato()
            return respuesta_arduino
        except Exception as error:
            return f"Error al obtener la posición del servo de agua: {error}"

    def obtener_posicion_servo_alimento(self):
        try:
            comando = "fd:2"
            self.arduino.enviar_dato(comando)
            sleep(1)
            respuesta_arduino = self.arduino.recibir_dato()
            return respuesta_arduino
        except Exception as error:
            return f"Error al obtener la posición del servo de alimento: {error}"

    def obtener_distancia_ultrasonico_agua(self):
        try:
            comando = "wdR:1"
            self.arduino.enviar_dato(comando)
            sleep(1)
            respuesta_arduino = self.arduino.recibir_dato()
            return respuesta_arduino
        except Exception as error:
            return f"Error al obtener la distancia con el sensor ultrasónico de agua: {error}"

    def obtener_distancia_ultrasonico_alimento(self):
        try:
            comando = "fdR:1"
            self.arduino.enviar_dato(comando)
            sleep(1)
            respuesta_arduino = self.arduino.recibir_dato()
            return respuesta_arduino
        except Exception as error:
            return f"Error al obtener la distancia con el sensor ultrasónico de alimento: {error}"

    def consultar_tarea(self, idTarea):
        try:
            return self.db.consultar_tarea(idTarea)
        except Exception as error:
            return f"Error al consultar la tarea: {error}"

    def consultar_registro(self, idSensor):
        try:
            return self.db.consultar_registro(idSensor)
        except Exception as error:
            return f"Error al consultar el registro: {error}"

    def definir_intervalo_tiempo_agua(self, tiempo, unidad):
        try:
            if unidad not in ['s', 'm']:
                raise ValueError(
                    "Unidad de tiempo no válida. Debe ser 's' para segundos, 'm' para minutos.")

            comando = f"wdT:{tiempo}{unidad}"
            self.arduino.enviar_dato(comando)
            sleep(1)
            respuesta_arduino = self.arduino.recibir_dato()

            # Guardar la respuesta en la tabla de registros de tareas si es correcta
            if f"wdTset:{tiempo}{unidad}" in respuesta_arduino:
                respuesta_db = self.db.insertar_tarea(
                    idSensor="1", tipo="Agua", tiempo=tiempo, unidadtiempo=unidad)
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
            sleep(1)
            respuesta_arduino = self.arduino.recibir_dato()

            # Guardar la respuesta en la tabla de registros de tareas si es correcta
            if f"fdTset:{tiempo}{unidad}" in respuesta_arduino:
                respuesta_db = self.db.insertar_tarea(
                    idSensor="2", tipo="Alimento", tiempo=tiempo, unidadtiempo=unidad)
                return respuesta_db
            else:
                return f"Error al definir el intervalo de tiempo para el dispensador de comida: {respuesta_arduino}"
        except Exception as error:
            return f"Error al definir el intervalo de tiempo para el dispensador de comida: {error}"

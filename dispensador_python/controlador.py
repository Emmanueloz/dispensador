from crud import Crud
from conexion_serial import ConnectionArduino

class Controller:
    def __init__(self):
        # Crear instancias de las clases Crud y ConnectionArduino
        self.db = Crud()
        self.arduino = ConnectionArduino()  # La conexión se establecerá cuando sea necesario

    def conectar_todo(self, host="localhost", user="root", passwd="", database="dispensadorBD"):
        try:
            # Conectar a la base de datos
            self.db.conectar_BD(host=host, user=user, passwd=passwd, database=database)

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
            self.arduino.cerrar() 
            return "Conexiones cerradas correctamente."
        except Exception as e:
            return f"Error al cerrar las conexiones: {e}"
    def abrir_dispensador_agua(self):
        try:
            comando = "wd:1"
            self.arduino.enviar_comando(comando)
            respuesta_arduino = self.arduino.leer_respuesta_serial()
            if "correcto" in respuesta_arduino:
                respuesta_db = self.db.insertar_registro(idRegistro="ID_AGUA", estado="ABIERTO")
                return respuesta_db
            else:
                return f"Error al abrir el dispensador de agua en el Arduino: {respuesta_arduino}"
        except Exception as error:
            return f"Error al abrir el dispensador de agua: {error}"

    def abrir_dispensador_alimento(self):
        try:
            comando = "fd:1"
            self.arduino.enviar_comando(comando)
            respuesta_arduino = self.arduino.leer_respuesta_serial()
            if "correcto" in respuesta_arduino:
                respuesta_db = self.db.insertar_registro(idRegistro="ID_ALIMENTO", estado="ABIERTO")
                return respuesta_db
            else:
                return f"Error al abrir el dispensador de alimento en el Arduino: {respuesta_arduino}"
        except Exception as error:
            return f"Error al abrir el dispensador de alimento: {error}"

    def obtener_posicion_servo_agua(self):
        try:
            comando = "wdR"
            self.arduino.enviar_comando(comando)
            respuesta_arduino = self.arduino.leer_respuesta_serial()
            return respuesta_arduino
        except Exception as error:
            return f"Error al obtener la posición del servo de agua: {error}"

    def obtener_posicion_servo_alimento(self):
        try:
            comando = "fdR"
            self.arduino.enviar_comando(comando)
            respuesta_arduino = self.arduino.leer_respuesta_serial()
            return respuesta_arduino
        except Exception as error:
            return f"Error al obtener la posición del servo de alimento: {error}"

    def obtener_distancia_ultrasonico_agua(self):
        try:
            comando = "wdT"
            self.arduino.enviar_comando(comando)
            respuesta_arduino = self.arduino.leer_respuesta_serial()
            return respuesta_arduino
        except Exception as error:
            return f"Error al obtener la distancia con el sensor ultrasónico de agua: {error}"

    def obtener_distancia_ultrasonico_alimento(self):
        try:
            comando = "fdT"
            self.arduino.enviar_comando(comando)
            respuesta_arduino = self.arduino.leer_respuesta_serial()
            return respuesta_arduino
        except Exception as error:
            return f"Error al obtener la distancia con el sensor ultrasónico de alimento: {error}"
   
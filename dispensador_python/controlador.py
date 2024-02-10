class Controller:
    def __init__(self, crud_instance, arduino_instance):
        self.db = crud_instance
        self.arduino = arduino_instance

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
            respuesta = self.db.insertar_registro(idRegistro="ID_AGUA", estado="ABIERTO")
            if "correctamente" in respuesta:
                comando = "wd:1"
                respuesta_arduino = self.arduino.enviar_comando(comando)
                return respuesta_arduino
            else:
                return respuesta
        except Exception as error:
            return f"Error al abrir el dispensador de agua: {error}"

    def abrir_dispensador_alimento(self):
        try:
            respuesta = self.db.insertar_registro(idRegistro="ID_ALIMENTO", estado="ABIERTO")
            if "correctamente" in respuesta:
                comando = "fd:1"
                respuesta_arduino = self.arduino.enviar_comando(comando)
                return respuesta_arduino
            else:
                return respuesta
        except Exception as error:
            return f"Error al abrir el dispensador de alimento: {error}"

    def obtener_posicion_servo_agua(self):
        try:
            respuesta_arduino = self.arduino.enviar_comando("posA")
            return respuesta_arduino
        except Exception as error:
            return f"Error al obtener la posición del servo de agua: {error}"

    def obtener_posicion_servo_alimento(self):
        try:
            respuesta_arduino = self.arduino.enviar_comando("posF")
            return respuesta_arduino
        except Exception as error:
            return f"Error al obtener la posición del servo de alimento: {error}"

    def obtener_distancia_ultrasonico_agua(self):
        try:
            respuesta_arduino = self.arduino.enviar_comando("distA")
            return respuesta_arduino
        except Exception as error:
            return f"Error al obtener la distancia con el sensor ultrasónico de agua: {error}"

    def obtener_distancia_ultrasonico_alimento(self):
        try:
            respuesta_arduino = self.arduino.enviar_comando("distF")
            return respuesta_arduino
        except Exception as error:
            return f"Error al obtener la distancia con el sensor ultrasónico de alimento: {error}"

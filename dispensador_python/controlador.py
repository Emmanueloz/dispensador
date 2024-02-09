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
            if not self.arduino.esta_conectado():
                self.arduino.conectar()  
            return "Conexión exitosa a la base de datos y Arduino."
        except Exception as e:
            return f"Error en la conexión: {e}"

    def cerrar_todo(self):
        try:
            # Cerrar conexión con la base de datos
            self.db.cerrar_conexion()

            # Cerrar conexión con Arduino
            if self.arduino.esta_conectado():
                self.arduino.cerrar() 
            return "Conexiones cerradas correctamente."
        except Exception as e:
            return f"Error al cerrar las conexiones: {e}"


    def abrir_dispensador_agua(self):
        try:
            # Verificar si la conexión con Arduino está establecida
            if not self.arduino.esta_conectado():##compurba la conxion al arduino
                return "Error: No se puede abrir el dispensador de agua. La conexión con Arduino no está establecida."

            # Enviar comando al Arduino para abrir el dispensador de agua
            #despues envia los datos al aduino
            #despues returna el resultado en este caso la variable de respuesta 
            comando = "wd"
            respuesta = self.arduino.enviar_comando(comando)
            return respuesta
        ##si esto es falso o ocurre un error manda este mensaje 
        except Exception as error:
            return f"Error al abrir el dispensador de agua: {error}"

    def abrir_dispensador_alimento(self):
        try:
            # Verificar si la conexión con Arduino está establecida
            if not self.arduino.esta_conectado():
                return "Error: No se puede abrir el dispensador de alimento. La conexión con Arduino no está establecida."

            comando = "fd"
            respuesta = self.arduino.enviar_comando(comando)
            return respuesta 
        except Exception as error:
            return f"Error al abrir el dispensador de alimento: {error}"

    def obtener_posicion_servo_agua(self):
        try:
            # Verificar si la conexión con Arduino está establecida
            if not self.arduino.esta_conectado():
                return "Error: No se puede obtener la posición del servo de agua. La conexión con Arduino no está establecida."

            # Enviar comando al Arduino para obtener la posición del servo de agua
            comando = "posA"
            respuesta = self.arduino.enviar_comando(comando)
            return respuesta  # Puedes ajustar la respuesta según la lógica de tu aplicación
        except Exception as error:
            return f"Error al obtener la posición del servo de agua: {error}"

    def obtener_posicion_servo_alimento(self):
        try:
            # Verificar si la conexión con Arduino está establecida
            if not self.arduino.esta_conectado():
                return "Error: No se puede obtener la posición del servo de alimento. La conexión con Arduino no está establecida."

            # Enviar comando al Arduino para obtener la posición del servo de alimento
            comando = "posF"
            respuesta = self.arduino.enviar_comando(comando)
            return respuesta  # Puedes ajustar la respuesta según la lógica de tu aplicación
        except Exception as error:
            return f"Error al obtener la posición del servo de alimento: {error}"

    def obtener_distancia_ultrasonico_agua(self):
        try:
            # Verificar si la conexión con Arduino está establecida
            if not self.arduino.esta_conectado():
                return "Error: No se puede obtener la distancia con el sensor ultrasónico de agua. La conexión con Arduino no está establecida."

            # Enviar comando al Arduino para obtener la distancia con el sensor ultrasónico de agua
            comando = "distA"
            respuesta = self.arduino.enviar_comando(comando)
            return respuesta  # Puedes ajustar la respuesta según la lógica de tu aplicación
        except Exception as error:
            return f"Error al obtener la distancia con el sensor ultrasónico de agua: {error}"

    def obtener_distancia_ultrasonico_alimento(self):
        try:
            # Verificar si la conexión con Arduino está establecida
            if not self.arduino.esta_conectado():
                return "Error: No se puede obtener la distancia con el sensor ultrasónico de alimento. La conexión con Arduino no está establecida."

            # Enviar comando al Arduino para obtener la distancia con el sensor ultrasónico de alimento
            comando = "distF"
            respuesta = self.arduino.enviar_comando(comando)
            return respuesta  # Puedes ajustar la respuesta según la lógica de tu aplicación
        except Exception as error:
            return f"Error al obtener la distancia con el sensor ultrasónico de alimento: {error}"

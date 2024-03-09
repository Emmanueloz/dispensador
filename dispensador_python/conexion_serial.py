import serial
import time


class ConnectionArduino:
    arduino = None
    # Constructor

    def __init__(self, puerto, velocidad=9600):
        self.puerto = puerto
        self.velocidad = velocidad

    def conectar(self):
        try:
            self.arduino = serial.Serial(self.puerto, self.velocidad)
            time.sleep(1)
            return None
        except serial.SerialException as e:
            return f"Error en la conexión: {e}"

    def enviar_dato(self, dato):
        try:
            self.arduino.write(dato.encode())
        except Exception as e:
            return f"Error el arduino no esta conectado: {e}"

    def recibir_dato(self):
        try:
            # recibir_dato = self.arduino.readline().decode().strip()
            message = self.arduino.readline()

            return message[:1].decode()
        except Exception as e:
            return f"Error al recibir los datos: {e}"

    def cerrar_arduino(self):
        if self.arduino is not None:
            if self.arduino.is_open:
                self.arduino.close()
                return "Conexión cerrada"
            else:
                return "El puerto ya esta cerrado"
        else:
            return "Arduino no conectado"

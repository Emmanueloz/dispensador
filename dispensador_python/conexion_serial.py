import serial
import time

class ConexionArduino:
    arduino = None
    #Constructor
    def __init__(self, puerto, velocidad = 9600, time = 2):
        self.puerto = puerto
        self.velocidad = velocidad
        self.time = time

    def conectar(self):
        self.arduino = serial.Serial(self.puerto, self.velocidad)
        time(2)

    def enviar_dato(self, dato):
        self.arduino.write(dato.encode())

    def recibir_dato(self):
        recibir_dato = self.arduino.readline().decode().strip()
        return recibir_dato
    
    def cerrar_arduino(self):
        self.arduino.close()


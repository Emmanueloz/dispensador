import serial
from crud import Crud
from conexion_serial import ConnectionArduino

class Controller:
    def __init__(self):
        # Crear instancias de las clases Crud y ConnectionArduino
        self.db = Crud()
        self.arduino = None  # La conexión se establecerá cuando sea necesario

    def conectar_todo(self, puerto, velocidad=9600, time=2, host="localhost", user="root", passwd="", database="dispensadorBD"):
        try:
            # Conectar a la base de datos
            self.db.conectar_BD(host=host, user=user, passwd=passwd, database=database)

            # Conectar a Arduino
            if self.arduino is None:
                self.arduino = ConnectionArduino(puerto, velocidad, time)
                self.arduino.conectar()

            return "Conexión exitosa a la base de datos y Arduino."
        except Exception as e:
            return f"Error en la conexión: {e}"

    def cerrar_todo(self):
        try:
            # Cerrar conexión con la base de datos
            self.db.cerrar_conexion()

            # Cerrar conexión con Arduino
            if self.arduino:
                self.arduino.cerrar_arduino()
                self.arduino = None  # Limpiar la instancia de ConnectionArduino

            return "Conexiones cerradas correctamente."
        except Exception as e:
            return f"Error al cerrar las conexiones: {e}"

    def validar_sensor(self, idSensor, nombre, uso):
        # Agregar aquí tu lógica de validación
        if not all([idSensor, nombre, uso]):
            return False, "Todos los campos son obligatorios."
        # Puedes agregar más validaciones según tus necesidades, por ejemplo:
        if not isinstance(idSensor, int):
            return False, "El ID del sensor debe ser un número entero."
        if len(nombre) > 50:
            return False, "El nombre del sensor no puede exceder los 50 caracteres."
        if len(uso) > 100:
            return False, "El campo 'uso' del sensor no puede exceder los 100 caracteres."
        # Si todas las validaciones pasan, retornar True y un mensaje de éxito
        return True, "Datos válidos."

    def insertar_sensor(self, tabla, idSensor, nombre, uso):
        # Validar los datos del sensor antes de insertarlos en la base de datos
        valido, mensaje = self.validar_sensor(idSensor, nombre, uso)
        if valido:
            try:
                # Intentar insertar el sensor en la base de datos
                self.db.insertar_sensor(tabla=tabla, idSensor=idSensor, nombre=nombre, uso=uso)
                return "Sensor insertado correctamente."
            except Exception as error:
                return f"Error al insertar en la tabla: {error}"
        else:
            return mensaje

    def consultar_datos(self, tabla, identificador, tipo):
        """
        Consulta datos en la base de datos.

        Parameters:
        - tabla: Nombre de la tabla en la base de datos.
        - identificador: ID del sensor o registro.
        - tipo: "sensor" o "registro" para indicar el tipo de consulta.

        Returns:
        - Resultado de la consulta o un mensaje indicando que no se encontraron resultados.
        """
        # Validar el tipo de consulta
        if tipo not in ["sensor", "registro"]:
            return "Tipo de consulta no válido. Use 'sensor' o 'registro'."

        # Realizar la consulta según el tipo especificado
        if tipo == "sensor":
            # Validar que el identificador del sensor sea un número entero positivo
            if not isinstance(identificador, int) or identificador <= 0:
                return "El identificador del sensor debe ser un número entero positivo."
            return self.db.consultar_sensor(tabla, identificador)
        elif tipo == "registro":
            # Validar que el identificador del registro sea un número entero positivo
            if not isinstance(identificador, int) or identificador <= 0:
                return "El identificador del registro debe ser un número entero positivo."
            return self.db.consultar_registros(tabla, identificador)

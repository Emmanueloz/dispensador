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
            self.arduino.conectar()  # método en ConnectionArduino
            return "Conexión exitosa a la base de datos y Arduino."
        except Exception as e:
            return f"Error en la conexión: {e}"

    def cerrar_todo(self):
        try:
            # Cerrar conexión con la base de datos
            self.db.cerrar_conexion()

            # Cerrar conexión con Arduino
            self.arduino.cerrar_arduino()  #método en ConnectionArduino
            return "Conexiones cerradas correctamente."
        except Exception as e:
            return f"Error al cerrar las conexiones: {e}"

    def validar_tarea(self, idSensor, tipo, tiempo, unidadtiempo):
        # Agregar aquí tu lógica de validación
        if not all([idSensor, tipo, tiempo, unidadtiempo]):
            return False, "Todos los campos son obligatorios."
        # Puedes agregar más validaciones según tus necesidades, por ejemplo:
        if not isinstance(idSensor, int):
            return False, "El ID del sensor debe ser un número entero."
        # Validar otros campos como tipo, tiempo, etc.

        # Si todas las validaciones pasan, retornar True y un mensaje de éxito
        return True, "Datos válidos."

    def insertar_tarea(self, idSensor, tipo, tiempo, unidadtiempo):
        # Validar los datos de la tarea antes de insertarlos en la base de datos
        valido, mensaje = self.validar_tarea(idSensor, tipo, tiempo, unidadtiempo)
        if valido:
            try:
                # Enviar el comando a Arduino para realizar la tarea
                if tipo == "agua":
                    comando = "wd"  # Comando para dispensar agua
                elif tipo == "comida":
                    comando = "fd"  # Comando para dispensar comida
                else:
                    return "Tipo de tarea no válido."

                # Enviar el comando a Arduino
                self.arduino.enviar_comando(comando)

                # Si el comando se envió correctamente, insertar la tarea en la base de datos
                self.db.insertar_tarea(idSensor, tipo, tiempo, unidadtiempo)
                return "Tarea insertada correctamente."
            except Exception as error:
                return f"Error al insertar la tarea: {error}"
        else:
            return mensaje

    def insertar_registro(self, idRegistro, estado):
        try:
            # Insertar el registro en la base de datos
            self.db.insertar_registro(idRegistro, estado)
            return "Registro insertado correctamente."
        except Exception as error:
            return f"Error al insertar el registro: {error}"

    def consultar_datos(self, idRegistro, tipo):
        """
        Consulta datos en la base de datos.

        Parameters:
        - idRegistro: ID del sensor o registro.
        - tipo: "sensor" o "registro" para indicar el tipo de consulta.

        Returns:
        - Resultado de la consulta o un mensaje indicando que no se encontraron resultados.
        """
        # Realizar la consulta según el tipo especificado
        if tipo == "sensor":
            # Consultar datos de tarea
            return self.db.consultar_tarea(idRegistro)
        elif tipo == "registro":
            # Consultar datos de registro
            return self.db.consultar_registro(idRegistro)
        else:
            return "Tipo de consulta no válido. Use 'sensor' o 'registro'."

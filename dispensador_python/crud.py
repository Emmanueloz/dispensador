import mysql.connector
from datetime import datetime


class Crud:
    def __init__(self, host, user, passwd, database):
        self.conexion = self.conectar_BD(
            user=user, passwd=passwd, host=host, database=database)

    def conectar_BD(self, host, user, passwd, database):
        try:
            return mysql.connector.connect(host=host, user=user, passwd=passwd, database=database)
        except mysql.connector.Error as error:
            raise RuntimeError(
                f"Error al conectar a la base de datos: {error}")

    def cerrar_conexion(self):
        try:
            if self.conexion.is_connected():
                self.conexion.close()
                return "Conexión cerrada correctamente."
        except mysql.connector.Error as error:
            raise RuntimeError(f"Error al cerrar la conexión: {error}")

    def consultar_tarea(self, idTarea):
        try:
            instruccion = "SELECT * FROM tareas WHERE idTarea = %s"
            consulta = self.conexion.cursor()
            consulta.execute(instruccion, (idTarea,))
            resultado = ""
            for (idTarea, idSensor, tipo, fechaRegistro, horaRegistro, tiempo, unidadtiempo) in consulta:
                resultado += f"""{idTarea}\t{idSensor}\t{tipo}\t{fechaRegistro}
                    \t{horaRegistro}\t{tiempo}\t{unidadtiempo}\n"""
            consulta.close()
            return resultado if resultado else "No se encontraron resultados."
        except mysql.connector.Error as error:
            raise RuntimeError(f"Error al consultar la base de datos: {error}")

    def consultar_registro(self, idRegistro):
        try:
            instruccion = "SELECT * FROM registros WHERE idRegistro = %s"
            consulta = self.conexion.cursor()
            consulta.execute(instruccion, (idRegistro,))
            resultado = ""
            for (idRegistro, estado, fecha, hora) in consulta:
                resultado += f"{idRegistro}\t{estado}\t{fecha}\t{hora}\n"
            consulta.close()
            return resultado if resultado else "No se encontraron resultados."
        except mysql.connector.Error as error:
            raise RuntimeError(f"Error al consultar la base de datos: {error}")

    def insertar_registro(self, idRegistro, estado):
        try:
            fecha_hora = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            instruccion = "INSERT INTO registros (idRegistro, estado, fecha, hora) VALUES (%s, %s, %s, %s)"
            valores = (idRegistro, estado, fecha_hora.split()
                       [0], fecha_hora.split()[1])
            consulta = self.conexion.cursor()
            consulta.execute(instruccion, valores)
            self.conexion.commit()
            consulta.close()
            return "Registro insertado correctamente."
        except mysql.connector.Error as error:
            raise RuntimeError(f"Error al insertar en la tabla: {error}")

    def insertar_tarea(self, idTarea, idSensor, tipo, tiempo, unidadtiempo):
        try:
            fecha_hora = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            instruccion = "INSERT INTO tareas (idTarea, idSensor, tipo, fechaRegistro, horaRegistro, tiempo, unidadtiempo) VALUES (%s, %s, %s, %s, %s, %s, %s)"
            valores = (idTarea, idSensor, tipo, fecha_hora.split()[
                       0], fecha_hora.split()[1], tiempo, unidadtiempo)
            consulta = self.conexion.cursor()
            consulta.execute(instruccion, valores)
            self.conexion.commit()
            consulta.close()
            return "Tarea insertada correctamente."
        except mysql.connector.Error as error:
            raise RuntimeError(f"Error al insertar en la tabla: {error}")

import mysql.connector
from datetime import datetime


class Crud:
    conexion = None

    def conectar_BD(self, host, user, passwd, database):
        try:
            self.conexion = mysql.connector.connect(
                host=host, user=user, password=passwd, database=database)
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

    def consultar_tarea(self, tipo):
        try:
            instruccion = "SELECT * FROM tareas WHERE tipo = %s"
            consulta = self.conexion.cursor()
            consulta.execute(instruccion, (tipo,))
            resultado = ""
            for (idTarea, idComponente, tipo, fechaRegistro, horaRegistro, tiempo, unidadtiempo) in consulta:
                resultado += f"""{idTarea}\t{idComponente}\t{tipo}\t{fechaRegistro}
                    \t{horaRegistro}\t{tiempo}\t{unidadtiempo}\n"""
            consulta.close()
            return resultado if resultado else "No se encontraron resultados."
        except mysql.connector.Error as error:
            raise RuntimeError(f"Error al consultar la base de datos: {error}")

    def consultar_registro(self, idComponente):
        try:
            instruccion = "SELECT * FROM registros WHERE idComponente = %s"
            consulta = self.conexion.cursor()
            consulta.execute(instruccion, (idComponente,))
            resultados = consulta.fetchall()
            consulta.close()
            return resultados, None if resultados else None, "No se encontraron resultados."
        except mysql.connector.Error as error:
            raise RuntimeError(f"Error al consultar la base de datos: {error}")

    def consultar_ultimo_registro(self, idComponente):
        try:
            instruccion = "SELECT * FROM registros WHERE idComponente = %s ORDER BY idRegistro DESC LIMIT 1"
            consulta = self.conexion.cursor()
            consulta.execute(instruccion, (idComponente,))
            resultados = consulta.fetchall()
            consulta.close()
            return resultados if resultados else ["No se encontraron resultados."]
        except mysql.connector.Error as error:
            raise RuntimeError(f"Error al consultar la base de datos: {error}")

    def insertar_registro(self, idComponente, estado):
        try:
            fecha_hora = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            instruccion = "INSERT INTO registros (idComponente, estado, fecha, hora) VALUES (%s, %s, %s, %s)"
            valores = (idComponente, estado, fecha_hora.split()
                       [0], fecha_hora.split()[1])
            consulta = self.conexion.cursor()
            consulta.execute(instruccion, valores)
            self.conexion.commit()
            consulta.close()
            return "Registro insertado correctamente."
        except mysql.connector.Error as error:
            raise RuntimeError(f"Error al insertar en la tabla: {error}")

    def insertar_tarea(self, idComponente, tipo, tiempo, unidadtiempo):
        try:
            fecha_hora = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            instruccion = "INSERT INTO tareas (idTarea,idComponente, tipo, fechaRegistro, horaRegistro, tiempo, unidadtiempo) VALUES (NULL,%s, %s, %s, %s, %s, %s)"
            valores = (idComponente, tipo, fecha_hora.split()[
                0], fecha_hora.split()[1], tiempo, unidadtiempo)
            consulta = self.conexion.cursor()
            consulta.execute(instruccion, valores)
            self.conexion.commit()
            consulta.close()
            return "Tarea insertada correctamente."
        except mysql.connector.Error as error:
            raise RuntimeError(f"Error al insertar en la tabla: {error}")

import mysql.connector

class Crud:
    def __init__(self):
        self.conexion = self.conectar_BD()

    def conectar_BD(self):
        try:
            return mysql.connector.connect(host="localhost", user="root", passwd="", database="dispensadorBD")
        except mysql.connector.Error as error:
            return f"Error al conectar a la base de datos: {error}"

    def cerrar_conexion(self):
        try:
            if self.conexion.is_connected():
                self.conexion.close()
                return "Conexión cerrada correctamente."
        except mysql.connector.Error as error:
            return f"Error al cerrar la conexión: {error}"

    def consultar_sensor(self, tabla, idSensor):
        try:
            instruccion = f"SELECT * FROM {tabla} WHERE IdSensor = %s"
            consulta = self.conexion.cursor()
            consulta.execute(instruccion, (idSensor,))
            resultado = ""
            for (idSensor,nombre, uso) in consulta:
                resultado += "{}\t{}\t{}\n".format(idSensor,nombre, uso)
            consulta.close()
            return resultado if resultado else "No se encontraron resultados."
        except mysql.connector.Error as error:
            return f"Error al consultar la base de datos: {error}"


    
    def consultar_registros(self, tabla):
        try:
            instruccion = f"SELECT * FROM {tabla}"
            consulta = self.conexion.cursor()
            consulta.execute(instruccion)
            resultado = ""
            for (idRegistro, estado, fecha, hora) in consulta:
                resultado += "{}\t{}\t{}\t{}\n".format(idRegistro, estado, fecha, hora)
            consulta.close()
            return resultado if resultado else "No se encontraron resultados."
        except mysql.connector.Error as error:
            return f"Error al consultar la base de datos: {error}"

    def insertar_registro(self, tabla, idRegistro, estado, fecha, hora):
        try:
            instruccion = f'''INSERT INTO {tabla} (idRegistro, estado, fecha, hora) 
                              VALUES (%s, %s, %s, %s)'''
            valores = (idRegistro, estado, fecha, hora)
            consulta = self.conexion.cursor()
            consulta.execute(instruccion, valores)
            self.conexion.commit()
            consulta.close()
            return "Registro insertado correctamente."
        except mysql.connector.Error as error:
            return f"Error al insertar en la tabla: {error}"

    def insertar_sensor(self, tabla, idSensor, nombre, uso):
        try:
            instruccion = f'''INSERT INTO {tabla} (idSensor, nombre, uso) 
                              VALUES (%s, %s, %s)'''
            valores = (idSensor, nombre, uso)
            consulta = self.conexion.cursor()
            consulta.execute(instruccion, valores)
            self.conexion.commit()
            consulta.close()
            return "Sensor insertado correctamente."
        except mysql.connector.Error as error:
            return f"Error al insertar en la tabla: {error}"



crud = Crud()

# Consultar sensores
#resultado = crud.consultar_sensor("sensores", "nombre_del_sensor")
print(crud.consultar_sensor("Sensores", 1))
#print(resultado)

# Consultar registros
#print(crud.consultar_registros("Registros"))

# Insertar un nuevo sensor
#print(crud.insertar_sensor("Sensores", 2, "nombre_del_sensor", "uso_del_sensor"))

# Insertar un nuevo registro
#print(crud.insertar_registro("Registros", 2, "estado_del_registro", "2024-02-07", "12:00:00"))

# Cerrar la conexión
print(crud.cerrar_conexion())

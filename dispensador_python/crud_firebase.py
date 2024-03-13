from pyrebase import initialize_app
from datetime import datetime


class CrudFirebase:
    connection = None
    config = None

    def __init__(self, config):
        self.config = config

    def conectar_BD(self):
        try:
            self.connection = initialize_app(self.config)
        except Exception as error:
            raise RuntimeError(
                f"Error al conectar a la base de datos: {error}")

    def insertar_registro(self, idComponente, estado):
        try:
            db = self.connection.database()
            fecha = datetime.now().strftime('%Y-%m-%d')

            hora = datetime.now().strftime('%H:%M:%S')
            db.child("dispensador/registros").push({
                "idComponente": idComponente,
                "estado": estado,
                "fecha": fecha,
                "hora": hora,
            })
            return "Registro insertado correctamente."
        except Exception as error:
            raise RuntimeError(f"Error al insertar el registro: {error}")

    def consultar_registro(self):
        try:
            db = self.connection.database()
            registros = db.child("dispensador/registros").get()
            if registros.val() is None:
                raise Exception("No se encontraron resultados.")
            return registros, None
        except Exception as error:
            return None, f"{error}"


crudPrueba = CrudFirebase({
    'apiKey': "AIzaSyD3l2W0fhM7QfF3PhvSK3dU5Sghsn7ORBs",
    'authDomain': "aplicacionesiot-1622a.firebaseapp.com",
    'databaseURL': "https://aplicacionesiot-1622a-default-rtdb.firebaseio.com",
    'projectId': "aplicacionesiot-1622a",
    'storageBucket': "aplicacionesiot-1622a.appspot.com",
    'messagingSenderId': "801264676158",
    'appId': "1:801264676158:web:b39b19991c7167cc89106f"
})


"""
    Usar dos combos
    primero: para consultar para los registros de todos,agua y alimento   
    segundo: para consultar todos los registros del estado todo, abierto, estado 
"""

crudPrueba.conectar_BD()
# crudPrueba.insertar_registro("1", "ABIERTO")

consulta, error = crudPrueba.consultar_registro()


if error is None:
    for fila in consulta.each():
        print(fila.val())
else:
    print(error)

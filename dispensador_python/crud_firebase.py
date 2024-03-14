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

    def consultar_registro(self, idComponente=None, estado=None):
        try:
            db = self.connection.database()
            registros = None
            if idComponente is not None:
                idComponente = str(idComponente)
                registros = db.child("dispensador/registros").order_by_child(
                    "idComponente").equal_to(idComponente).get()
            elif estado is not None:
                registros = db.child("dispensador/registros").order_by_child(
                    "estado").equal_to(estado).get()
            else:
                registros = db.child("dispensador/registros").get()

            if registros.val() is None or len(registros.val()) == 0:
                raise Exception("No se encontraron resultados.")

            lista_registros = []
            for registro in registros.each():
                lista_registros.append(
                    (
                        int(registro.val()["idComponente"]),
                        registro.val()["estado"],
                        registro.val()["fecha"],
                        registro.val()["hora"]
                    )
                )

            return lista_registros, None
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

"""
crudPrueba.conectar_BD()

crudPrueba.insertar_registro("2", "ABIERTO")
crudPrueba.insertar_registro("1", "CERRADO")
crudPrueba.insertar_registro("2", "CERRADO")


consulta, error = crudPrueba.consultar_registro()

print("consulta total")
print(consulta)
print(error)
error = None
print("consulta del dispensador de agua")
consulta, error = crudPrueba.consultar_registro(idComponente=1)
print(consulta)
print(error)
error = None
print("consulta del dispensador de alimento")
consulta, error = crudPrueba.consultar_registro(idComponente=2)
print(consulta)
print(error)
error = None
print("consulta de los registros de estado abierto")
consulta, error = crudPrueba.consultar_registro(estado="ABIERTO")
print(consulta)
print(error)
error = None
print("consulta de los registros de estado cerrado")
consulta, error = crudPrueba.consultar_registro(estado="CERRADO")
print(consulta)
print(error)
"""

from pyrebase import initialize_app
from datetime import datetime


class CrudFirebase:
    connection = None
    config = None

    def __init__(self, name_id) -> None:
        self.name_id = name_id

    def conectar_BD(self, config):
        self.config = config
        try:
            self.connection = initialize_app(self.config)
        except Exception as error:
            raise RuntimeError(
                f"Error al conectar a la base de datos: {error}")

    def cerrar(self):
        self.stream.close()

    def consultar_estados_all(self):
        try:
            db = self.connection.database()
            estados = db.child("dispensador/estados/").get()

            estados_dic = {e.key(): e.val() for e in estados.each()}

            return estados_dic, None
        except Exception as e:
            return {}, str(e)

    def set_stream_handler(self, stream_handler):
        try:
            db = self.connection.database()
            self.stream = db.child(
                "dispensador/estados/").stream(stream_handler)
            return None
        except Exception as e:
            return str(e)

    def update_estado(self, idComponente, estado):
        try:
            db = self.connection.database()
            fecha = datetime.now().strftime('%Y-%m-%d')
            hora = datetime.now().strftime('%H:%M:%S')
            result = db.child(
                f"dispensador/estados/{self.name_id}").child(f"dispensador{idComponente}").update(
                    {
                        "estado": estado,
                        "fecha": fecha,
                        "hora": hora
                    }
            )

            return result, None
        except Exception as error:
            return None, str(error)

    def update_estado_contenedores(self, idComponente, estado):
        try:
            db = self.connection.database()
            fecha = datetime.now().strftime('%Y-%m-%d')
            hora = datetime.now().strftime('%H:%M:%S')
            result = db.child(
                f"dispensador/estados/{self.name_id}").child(f"contenedor{idComponente}").update(
                    {
                        "estado": estado,
                        "fecha": fecha,
                        "hora": hora,
                    }
            )

            return result, None
        except Exception as error:
            return None, str(error)

    def update_estado_recipiente(self, idComponente, estado):
        try:
            db = self.connection.database()
            fecha = datetime.now().strftime('%Y-%m-%d')
            hora = datetime.now().strftime('%H:%M:%S')
            result = db.child(
                f"dispensador/estados/{self.name_id}").child(f"contenedor{idComponente}").update(
                    {
                        "estado": estado,
                        "fecha": fecha,
                        "hora": hora,
                    }
            )

            return result, None
        except Exception as error:
            return None, str(error)

    def update_estado_tiempo(self, idComponente, intervalo, tipo):
        try:
            db = self.connection.database()
            fecha = datetime.now().strftime('%Y-%m-%d')
            hora = datetime.now().strftime('%H:%M:%S')
            result = db.child(
                f"dispensador/estados/{self.name_id}").child(f"tiempo{idComponente}").update(
                    {
                        "intervalo": intervalo,
                        "tipo": tipo,
                        "fecha": fecha,
                        "hora": hora,
                    }
            )

            return result, None
        except Exception as error:
            return None, str(error)

    def update_estado_tiempo_resultado(self, idComponente, estado):
        try:
            db = self.connection.database()
            fecha = datetime.now().strftime('%Y-%m-%d')
            hora = datetime.now().strftime('%H:%M:%S')
            result = db.child(
                f"dispensador/estados/{self.name_id}").child(f"tResultado{idComponente}").update(
                    {
                        "estado": estado,
                        "fecha": fecha,
                        "hora": hora,
                    }
            )

            return result, None
        except Exception as error:
            return None, str(error)

    def insertar_registro(self, idComponente, estado, id_update=True):
        try:
            db = self.connection.database()
            idComponente = int(idComponente)
            fecha = datetime.now().strftime('%Y-%m-%d')
            hora = datetime.now().strftime('%H:%M:%S')

            if id_update:
                upd_estado = 1 if estado == "ABIERTO" else 0

                upd, error = self.update_estado(
                    idComponente=idComponente, estado=upd_estado)

                if error is not None:
                    raise Exception(error)

            db.child(f"dispensador/registros/{self.name_id}").push({
                "idComponente": idComponente,
                "estado": estado,
                "fecha": fecha,
                "hora": hora,
            })

            return "Registro insertado correctamente."
        except Exception as error:
            raise RuntimeError(f"Error al insertar el registro: {error}")

    def consulta_filtrado(self, idComponente, estado):
        try:
            db = self.connection.database()

            registros = db.child(
                f"dispensador/registros/{self.name_id}").order_by_key().limit_to_last(5).order_by_child("estado").equal_to(estado).get()

            lista_registros = []
            for registro in registros.each():
                if registro.val()["idComponente"] == idComponente:
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
            return None, str(error)

    def consultar_registro(self, idComponente=None, estado=None):
        try:
            idComponente = int(
                idComponente) if idComponente is not None else None

            db = self.connection.database()
            registros = None
            if idComponente is not None and estado is not None:

                lista_registros, error = self.consulta_filtrado(
                    idComponente, estado)

                if error is not None:
                    raise Exception(error)

                return lista_registros, None

            elif idComponente is not None:
                registros = db.child(f"dispensador/registros/{self.name_id}").order_by_key().limit_to_last(5).order_by_child(
                    "idComponente").equal_to(idComponente).get()
            elif estado is not None:
                registros = db.child(f"dispensador/registros/{self.name_id}").order_by_key().limit_to_last(5).order_by_child(
                    "estado").equal_to(estado).get()
            else:
                registros = db.child(
                    f"dispensador/registros/{self.name_id}").limit_to_last(5).order_by_key().get()

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
            return None, str(error)

    def consultar_ultimo_registro(self, idComponente):
        try:
            idComponente = int(idComponente)
            db = self.connection.database()
            registros = db.child(f"dispensador/registros/{self.name_id}").order_by_child(
                "idComponente").equal_to(idComponente).limit_to_last(1).get()

            # print(registros.val())
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
            return None, str(error)


"""
crudPrueba = CrudFirebase("dis1")

crudPrueba.conectar_BD({
    'apiKey': "AIzaSyD3l2W0fhM7QfF3PhvSK3dU5Sghsn7ORBs",
    'authDomain': "aplicacionesiot-1622a.firebaseapp.com",
    'databaseURL': "https://aplicacionesiot-1622a-default-rtdb.firebaseio.com",
    'projectId': "aplicacionesiot-1622a",
    'storageBucket': "aplicacionesiot-1622a.appspot.com",
    'messagingSenderId': "801264676158",
    'appId': "1:801264676158:web:b39b19991c7167cc89106f"
})

# crudPrueba.insertar_registro(1, "CERRADO")
# crudPrueba.insertar_registro(2, "CERRADO")


estados_dic, error = crudPrueba.consultar_estados_all()

print(error)
print(estados_dic)


def example(message):
    print(message)


crudPrueba.set_stream_handler(example)
"""

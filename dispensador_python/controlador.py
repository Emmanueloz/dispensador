from dispensador_python.crud_firebase import CrudFirebase
from dispensador_python.conexion_serial import ConnectionArduino
from time import sleep
from re import match
from .vista import *
from threading import Thread


def validar_string(prefijo, valor):
    """Función para validar un string con un prefijo y un número entero."""
    patron = rf"^{prefijo}:\d+$"

    if match(patron, valor):
        return True
    else:
        return False


class ControllerVista:
    def __init__(self, vista, name_id) -> None:

        self.vista: Ventana = vista
        self.name_id = name_id

        inicio = None
        tiempo = None
        registros = None

        match name_id:
            case "dis1":
                inicio = self.vista.inicio.dash_board1
                tiempo = self.vista.tiempo.dash_board_tiempo1
                registros = self.vista.registro.registro1
            case "dis2":
                inicio = self.vista.inicio.dash_board2
                tiempo = self.vista.tiempo.dash_board_tiempo2
                registros = self.vista.registro.registro2
            case "dis3":
                inicio = self.vista.inicio.dash_board3
                tiempo = self.vista.tiempo.dash_board_tiempo3
                registros = self.vista.registro.registro3
            case "dis4":
                inicio = self.vista.inicio.dash_board4
                tiempo = self.vista.tiempo.dash_board_tiempo4
                registros = self.vista.registro.registro4
            case "dis5":
                inicio = self.vista.inicio.dash_board5
                tiempo = self.vista.tiempo.dash_board_tiempo5
                registros = self.vista.registro.registro5

        self.inicio: DashBoard = inicio
        self.tiempo: DashBoardTiempo = tiempo
        self.registros: Tablas = registros

        self.db = CrudFirebase(name_id=name_id)
        self.arduino = ConnectionArduino(puerto="COM2")
        self.estado_agua = 0
        self.estado_comida = 0
        self.hilo_lectura = Thread(target=self.leer_serial)
        self.vista.protocol("WM_DELETE_WINDOW", self.finalizar)
        self.corriendo = True
        self.error_bd = False
        self.filtro_tipo = "Todo"
        self.filtro_estado = "Todo"

    def vistas(self):
        self.inicio1: DashBoard = self.vista.inicio.dash_board1
        self.tiempo1: DashBoardTiempo = self.vista.tiempo.dash_board_tiempo1
        self.registros1: Tablas = self.vista.registro.registro1

        self.inicio2: DashBoard = self.vista.inicio.dash_board2
        self.tiempo2: DashBoardTiempo = self.vista.tiempo.dash_board_tiempo2
        self.registros2: Tablas = self.vista.registro.registro2

        self.inicio3: DashBoard = self.vista.inicio.dash_board3
        self.tiempo3: DashBoardTiempo = self.vista.tiempo.dash_board_tiempo3
        self.registros3: Tablas = self.vista.registro.registro3

        self.inicio4: DashBoard = self.vista.inicio.dash_board4
        self.tiempo4: DashBoardTiempo = self.vista.tiempo.dash_board_tiempo4
        self.registros4: Tablas = self.vista.registro.registro4

        self.inicio5: DashBoard = self.vista.inicio.dash_board5
        self.tiempo5: DashBoardTiempo = self.vista.tiempo.dash_board_tiempo5
        self.registros5: Tablas = self.vista.registro.registro5

    def conectar_todo(self):
        try:
            # Conectar a la base de datos
            self.db.conectar_BD({
                'apiKey': "AIzaSyD3l2W0fhM7QfF3PhvSK3dU5Sghsn7ORBs",
                'authDomain': "aplicacionesiot-1622a.firebaseapp.com",
                'databaseURL': "https://aplicacionesiot-1622a-default-rtdb.firebaseio.com",
                'projectId': "aplicacionesiot-1622a",
                'storageBucket': "aplicacionesiot-1622a.appspot.com",
                'messagingSenderId': "801264676158",
                'appId': "1:801264676158:web:b39b19991c7167cc89106f"
            })

            self.db.set_stream_handler(self.actualizar_vista)

            print("Conexión exitosa a la base de datos y Arduino.")
            messagebox.showinfo(
                "Conexión exitosa", "Conexión exitosa a la base de datos y Arduino.")
        except Exception as e:
            self.error_bd = True
            messagebox.showerror("Error", f"Error al conectar: {e}")

        try:
            if self.arduino.conectar() is not None:
                raise Exception("Error en la conexión con Arduino.")

        except Exception as e:
            messagebox.showerror("Error", f"Error al conectar: {e}")

    def actualizar_vista(self, data):
        estados, error = self.db.consultar_estados_all()
        if error is not None:
            messagebox.showerror("Error", error)
            return

        print(estados)

    def finalizar(self):
        self.corriendo = False
        self.hilo_lectura.join(0.1)
        self.vista.quit()
        self.vista.destroy()
        self.db.cerrar()
        # self.db.cerrar_conexion()
        self.arduino.cerrar_arduino()

    def dispensar_agua(self):
        if self.inicio.var_dispensar_agua.get() == 1:
            self.arduino.enviar_dato("wd:1")
        else:
            self.arduino.enviar_dato("wd:0")

    def dispensar_comida(self):
        if self.inicio.var_dispensar_comida.get() == 1:
            self.arduino.enviar_dato("fd:1")
        else:
            self.arduino.enviar_dato("fd:0")

    def activar_check_button(self):
        self.inicio.check_agua.config(command=self.dispensar_agua)
        self.inicio.check_comida.config(command=self.dispensar_comida)

    def procesar_resultado(self, result):
        if result == 1:
            return "Abierto"
        elif result == 0:
            return "Cerrado"
        elif result == -1:
            return "Ya esta en ese estado"
        elif result == -2:
            return "El contenedor esta vacío"
        elif result == -3:
            return "El recipiente esta lleno"
        else:
            return "Error"

    def enviar_tiempo_agua(self):
        try:
            tiempo = self.tiempo.tiempo_agua_var.get()
            unidad = self.tiempo.select_agua.get()
            unidad = "m" if unidad == "Minutos" else "s"
            self.arduino.enviar_dato(f"wdT:{tiempo}{unidad}")
        except Exception as e:
            print(f"Error al enviar el tiempo de agua: {e}")

    def enviar_tiempo_comida(self):
        try:
            tiempo = self.tiempo.tiempo_comida_var.get()
            unidad = self.tiempo.select_comida.get()
            unidad = "m" if unidad == "Minutos" else "s"
            self.arduino.enviar_dato(f"fdT:{tiempo}{unidad}")
        except Exception as e:
            print(f"Error al enviar el tiempo de comida: {e}")

    def filtrar(self):
        self.filtro_estado = self.registros.filtro_estado.get()
        self.filtro_tipo = self.registros.filtro_tipo.get()
        self.actualizar_registros()

    def activar_botones(self):
        self.tiempo.btn_enviar_agua.config(command=self.enviar_tiempo_agua)
        self.tiempo.btn_enviar_comida.config(command=self.enviar_tiempo_comida)
        self.registros.btn_actualizar.config(command=self.actualizar_registros)
        self.registros.btn_enviar_filtro.config(command=self.filtrar)

    def iniciar_estados(self):
        try:
            self.arduino.enviar_dato("all:1")
            sleep(1)
            result = self.arduino.recibir_dato()
            result = result.replace("\r", "")
            # orden de los estados:
            # wdP:0,fdP:0,wdSIs:0,fdSIs:0,wdTget:90m,fdTget:90m

            result = result.split(",")

            es_agua = int(result[0])

            self.db.update_estado(1, es_agua)

            es_alimento = int(result[1])

            self.db.update_estado(2, es_alimento)

            self.db.update_estado_contenedores(1, result[2])

            self.db.update_estado_contenedores(1, result[3])

            self.db.update_estado_tiempo(
                1, int(result[4].strip("mhs")), result[4][-1])

            self.tiempo.set_estado_comidaT(
                2, int(result[5].strip("mhs")), result[5][-1])

            print(result)

        except Exception as e:
            print(f"Error al iniciar los estados: {e}")

    def leer_serial(self):
        while self.corriendo:
            try:
                mensaje = self.arduino.recibir_dato()
                registro_anterior_agua, error_ag = self.db.consultar_ultimo_registro(
                    1)
                registro_anterior_alimento, error_al = self.db.consultar_ultimo_registro(
                    2)

                if error_ag is not None:
                    registro_anterior_agua = [("", "", "", "", "")]

                estado_anterior_bd_agua = registro_anterior_agua[0][1]

                if error_al is not None:
                    registro_anterior_alimento = [("", "", "", "", "")]

                estado_anterior_bd_alimento = registro_anterior_alimento[0][1]

                if mensaje.startswith("wdP:") or mensaje.startswith("wdR:"):
                    result = int(mensaje.split(":")[1])
                    msg = self.procesar_resultado(result)

                    self.inicio.set_estado_agua(result, msg)

                    if result in [-2, -3]:
                        self.db.update_estado(1, result)

                    if result == -2:
                        self.inicio.set_contenedor_agua(
                            "El contenedor de agua esta vacío.")

                    elif result == 1 or result == 0:
                        estado_actual = "ABIERTO" if result == 1 else "CERRADO"

                        if estado_anterior_bd_agua != estado_actual:
                            self.db.insertar_registro(1, estado_actual)
                        self.inicio.set_contenedor_agua(
                            "El contenedor de agua esta lleno")

                elif mensaje.startswith("fdP:") or mensaje.startswith("fdR:"):
                    result = int(mensaje.split(":")[1])
                    msg = self.procesar_resultado(result)

                    self.inicio.set_estado_comida(result, msg)

                    if result in [-2, -3]:
                        self.db.update_estado(1, result)

                    if result == -2:
                        self.inicio.set_contenedor_comida(
                            "El contenedor de alimento esta vació.")
                    elif result == 1 or result == 0:
                        estado_actual = "ABIERTO" if result == 1 else "CERRADO"

                        if estado_anterior_bd_alimento != estado_actual:
                            self.db.insertar_registro(2, estado_actual)

                        self.inicio.set_contenedor_comida(
                            "El contenedor de alimento esta lleno")

                elif mensaje.startswith("wdACon:0"):

                    self.inicio.set_contenedor_agua(
                        "El contenedor de agua esta vacío.")
                    self.inicio.set_estado_agua(0, "Cerrado")
                    if estado_anterior_bd_agua != "CERRADO":
                        self.db.insertar_registro(1, "CERRADO")

                elif mensaje.startswith("fdACon:0"):
                    self.inicio.set_contenedor_comida(
                        "El contenedor de alimento esta vació.")
                    self.inicio.set_estado_comida(0, "Cerrado")
                    if estado_anterior_bd_alimento != "CERRADO":
                        self.db.insertar_registro(2, "CERRADO")

                elif mensaje.startswith("wdARes:0"):
                    self.inicio.set_estado_agua(
                        0, "El recipiente esta lleno.")

                    if estado_anterior_bd_agua != "CERRADO":
                        self.db.insertar_registro(1, "CERRADO")

                elif mensaje.startswith("fdARes:0"):
                    self.inicio.set_estado_comida(
                        0, "El recipiente esta lleno.")

                    if estado_anterior_bd_alimento != "CERRADO":
                        self.db.insertar_registro(2, "CERRADO")

                elif mensaje.startswith("wdTset:"):
                    mensaje = mensaje.replace("\r", "")
                    result = mensaje.split(":")[1]
                    msg = "Intervalo:"+result
                    intervalo = int(result.strip("mhs"))
                    tipo = result[-1]
                    self.tiempo.set_estado_aguaT(intervalo, tipo, msg)

                    self.db.update_estado_tiempo(1, intervalo, tipo)

                elif mensaje.startswith("fdTset:"):
                    mensaje = mensaje.replace("\r", "")
                    result = mensaje.split(":")[1]
                    msg = "Intervalo:"+result
                    intervalo = int(result.strip("mhs"))
                    tipo = result[-1]
                    self.tiempo.set_estado_comidaT(intervalo, tipo, msg)
                    self.db.update_estado_tiempo(2, intervalo, tipo)

                elif mensaje.startswith("wdTR:"):
                    mensaje = mensaje.replace("\r", "")
                    result = mensaje.split(":")[1]
                    result = int(result)

                    if result == 1:
                        self.inicio.set_estado_agua(result, "Abierto")
                        self.tiempo.set_resultado_aguaT(
                            "El dispensador se abrió")
                        self.db.update_estado_tiempo_resultado(
                            1, "El dispensador se abrió")

                        if estado_anterior_bd_agua != "ABIERTO":
                            self.db.insertar_registro(1, "ABIERTO", False)

                    elif result == -1:
                        estado = self.inicio.var_dispensar_agua.get()
                        msg = "Abierto" if estado == 1 else "Cerrado"
                        self.inicio.set_estado_agua(estado, msg)
                        self.tiempo.set_resultado_aguaT(
                            "El dispensador ya esta abierto.")

                        self.db.update_estado_tiempo_resultado(
                            1, "El dispensador ya esta abierto.")

                    elif result == -2:
                        self.inicio.set_contenedor_agua(
                            "El contenedor de agua esta vacío.")
                        self.tiempo.set_resultado_aguaT(
                            "No se abrió. El contenedor de agua esta vacío.")

                        self.db.update_estado_tiempo_resultado(
                            1, "No se abrió. El contenedor de agua esta vacío.")
                        if estado_anterior_bd_agua != "CERRADO":
                            self.db.insertar_registro(1, "CERRADO", False)

                    elif result == -3:
                        self.inicio.set_estado_agua(0, msg)
                        self.tiempo.set_resultado_aguaT(
                            "No se abrió. El recipiente esta lleno."
                        )

                        self.db.update_estado_tiempo_resultado(
                            1, "No se abrió. El recipiente esta lleno.")

                        if estado_anterior_bd_agua != "CERRADO":
                            self.db.insertar_registro(1, "CERRADO", False)

                    if result != -1:
                        self.db.update_estado(1, result)

                elif mensaje.startswith("fdTR:"):
                    mensaje = mensaje.replace("\r", "")
                    result = mensaje.split(":")[1]
                    result = int(result)

                    if result == 1:
                        self.inicio.set_estado_comida(result, "Abierto")
                        self.tiempo.set_resultado_comidaT(
                            "El dispensador se abrió")
                        self.db.update_estado_tiempo_resultado(
                            2, "El dispensador se abrió")

                        if estado_anterior_bd_alimento != "ABIERTO":
                            self.db.insertar_registro(2, "ABIERTO", False)

                    elif result == -1:
                        estado = self.inicio.var_dispensar_comida.get()
                        msg = "Abierto" if estado == 1 else "Cerrado"
                        self.inicio.set_estado_comida(estado, msg)
                        self.tiempo.set_resultado_comidaT(
                            "El dispensador ya esta abierto.")

                        self.db.update_estado_tiempo_resultado(
                            2, "El dispensador ya esta abierto.")

                    elif result == -2:
                        self.inicio.set_contenedor_comida(
                            "El contenedor de alimento esta vacío.")
                        self.tiempo.set_resultado_comidaT(
                            "No se abrió. El contenedor de alimento esta vacío.")

                        self.db.update_estado_tiempo_resultado(
                            2, "No se abrió. El contenedor de alimento esta vacío.")

                        if estado_anterior_bd_alimento != "CERRADO":
                            self.db.insertar_registro(2, "CERRADO", False)

                    elif result == -3:
                        self.inicio.set_estado_comida(0, msg)
                        self.tiempo.set_resultado_comidaT(
                            "No se abrió. El recipiente esta lleno.")
                        self.db.update_estado_tiempo_resultado(
                            2, "No se abrió. El recipiente esta lleno.")

                        if estado_anterior_bd_alimento != "CERRADO":
                            self.db.insertar_registro(2, "CERRADO", False)

                    if result != -1:
                        self.db.update_estado(2, result)

            except Exception as error:
                print(f"Error al leer el puerto serial: {error}")

    def actualizar_registros(self):
        registro = None
        error = None
        if self.filtro_tipo == "Todo" and self.filtro_estado == "Todo":
            registro, error = self.db.consultar_registro()
        elif self.filtro_tipo == "Agua" and self.filtro_estado == "Abierto":
            registro, error = self.db.consultar_registro(
                idComponente=1, estado="ABIERTO")
        elif self.filtro_tipo == "Agua" and self.filtro_estado == "Cerrado":
            registro, error = self.db.consultar_registro(
                idComponente=1, estado="CERRADO")
        elif self.filtro_tipo == "Alimento" and self.filtro_estado == "Abierto":
            registro, error = self.db.consultar_registro(
                idComponente=2, estado="ABIERTO")
        elif self.filtro_tipo == "Alimento" and self.filtro_estado == "Cerrado":
            registro, error = self.db.consultar_registro(
                idComponente=2, estado="CERRADO")

        elif self.filtro_tipo == "Agua":
            registro, error = self.db.consultar_registro(idComponente=1)
        elif self.filtro_tipo == "Alimento":
            registro, error = self.db.consultar_registro(idComponente=2)
        elif self.filtro_estado == "Abierto":
            registro, error = self.db.consultar_registro(estado="ABIERTO")
        elif self.filtro_estado == "Cerrado":
            registro, error = self.db.consultar_registro(estado="CERRADO")

        if error is None:
            self.registros.actualizar_tabla(registro)

    def iniciar(self):
        self.conectar_todo()
        self.iniciar_estados()
        self.activar_check_button()
        self.activar_botones()
        self.actualizar_registros()
        self.hilo_lectura.start()
        self.vista.mainloop()

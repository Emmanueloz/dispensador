from tkinter import Tk, Frame, Button, Label, IntVar, Scale, PhotoImage, messagebox, Toplevel, ttk, Scrollbar, Tk, Frame, Label, Checkbutton, IntVar, Listbox, LabelFrame
from tkinter.ttk import Treeview, Combobox, Notebook


class DashBoard(LabelFrame):
    def __init__(self, master=None, imagen_agua=None, imagen_comida=None, name="Dashboard"):
        super().__init__(master)
        self.master = master
        self.pack()
        self.var_dispensar_agua = IntVar()
        self.var_dispensar_comida = IntVar()
        self.imagen_agua = imagen_agua
        self.imagen_comida = imagen_comida
        self.name = name
        self.interfaz()

    def interfaz(self):
        self.label = Label(
            self, text=f"..:: {self.name} ::..")
        self.label.pack(pady=10)
        self.msg_estados()
        self.imagenes()
        self.mis_checkbox()

    def msg_estados(self):
        # barra de estado(servo)
        self.lb_estado_dis_agua = Label(
            self, fg="blue", font=("Courier New", 10, "bold"))
        self.lb_estado_dis_agua.place(x=60, y=40)

        self.lb_estado_dis_alimento = Label(self, fg="green", font=(
            "Courier New", 10, "bold"))
        self.lb_estado_dis_alimento.place(x=360, y=40)

        self.lb_estado_con_agua = Label(
            self, fg="blue", font=("Courier New", 14, "bold"))

        self.lb_estado_con_agua.place(x=30, y=240)

        self.lb_estado_con_alimento = Label(self, fg="green", font=(
            "Courier New", 14, "bold"))

        self.lb_estado_con_alimento.place(x=30, y=260)

    def imagenes(self):
        # imagen de agua
        Label(self, image=self.imagen_agua).place(x=70, y=80)

        # imagen de comida
        Label(self, image=self.imagen_comida).place(x=370, y=80)

    def mis_checkbox(self):
        self.check_agua = Checkbutton(
            self, text="Dispensar Agua", variable=self.var_dispensar_agua, onvalue=1, offvalue=0)
        self.check_agua.place(x=100, y=200)

        self.check_comida = Checkbutton(
            self, text="Dispensar Comida", variable=self.var_dispensar_comida, onvalue=1, offvalue=0)
        self.check_comida.place(x=400, y=200)

    def set_estado_agua(self, estado, msg):
        self.var_dispensar_agua.set(estado)
        self.lb_estado_dis_agua.config(text=msg)

    def set_estado_comida(self, estado, msg):
        self.var_dispensar_comida.set(estado)
        self.lb_estado_dis_alimento.config(text=msg)

    def set_contenedor_agua(self, estado):
        self.lb_estado_con_agua.config(text=estado)

    def set_contenedor_comida(self, estado):
        self.lb_estado_con_alimento.config(text=estado)


class Inicio(Frame):
    def __init__(self, master=None, imagen_agua=None, imagen_comida=None):
        super().__init__(master)
        self.dash_board = DashBoard(
            self, imagen_agua, imagen_comida, name="Dispensador 1")
        self.dash_board.place(x=10, y=10, width=600, height=300)

        self.dash_board2 = DashBoard(self, imagen_agua, imagen_comida)
        self.dash_board2.place(x=10, y=310, width=600, height=300)


class Tiempo(Frame):
    def __init__(self, master=None, imagen_agua=None, imagen_comida=None, name="Tiempo para dispensar"):
        super().__init__(master)
        self.master = master
        self.pack()
        self.tiempo_agua_var = IntVar()
        self.tiempo_comida_var = IntVar()
        self.imagen_agua = imagen_agua
        self.imagen_comida = imagen_comida
        self.name = name
        self.interfaz()

    def interfaz(self):
        Label(self, text=f"..:: {self.name} ::..").place(x=300, y=10)
        self.labels()
        self.scales()
        self.imagenes()
        self.selects()
        self.buttons()

    def labels(self):
        self.lbl_estado_aguaT = Label(
            self, fg="blue", font=("Courier New", 14, "bold"))
        self.lbl_estado_aguaT.place(x=90, y=70)

        self.lbl_estado_comidaT = Label(
            self, fg="green", font=("Courier New", 14, "bold"))
        self.lbl_estado_comidaT.place(x=400, y=70)

        self.lbl_resultado_aguaT = Label(
            self, fg="blue", font=("Courier New", 14, "bold"))
        self.lbl_resultado_aguaT.place(x=20, y=450)

        self.lbl_resultado_comidaT = Label(
            self, fg="green", font=("Courier New", 14, "bold"))
        self.lbl_resultado_comidaT.place(x=400, y=450)

    def scales(self):
        Scale(self,  from_=0, to=60, orient="vertical", tickinterval=30,
              length=400, variable=self.tiempo_agua_var).place(x=10, y=10)
        Scale(self, from_=0, to=60, orient="vertical", tickinterval=30, length=400,
              variable=self.tiempo_comida_var).place(x=720, y=10)

    def imagenes(self):
        # imagen de agua
        Label(self, image=self.imagen_agua).place(x=90, y=100)

        # imagen de comida
        Label(self, image=self.imagen_comida).place(x=400, y=100)

    def selects(self):
        self.select_agua = Combobox(self, values=["Minutos", "Segundos"])
        self.select_agua.set("Minutos")
        self.select_agua.place(x=150, y=350)

        self.select_comida = Combobox(self, values=["Minutos", "Segundos"])
        self.select_comida.set("Minutos")
        self.select_comida.place(x=450, y=350)

    def buttons(self):
        self.btn_enviar_agua = Button(self, width=8, text="Enviar")
        self.btn_enviar_agua.place(x=150, y=400)
        self.btn_enviar_comida = Button(self, width=8, text="Enviar")
        self.btn_enviar_comida.place(x=450, y=400)

    def set_estado_aguaT(self, tiempo, unidad, msg):
        self.tiempo_agua_var.set(tiempo)
        unidad = "Minutos" if unidad == "m" else "Segundos"
        self.select_agua.set(unidad)
        self.lbl_estado_aguaT.config(text=msg)
        self.lbl_resultado_aguaT.config(text="")

    def set_estado_comidaT(self, tiempo, unidad, msg):
        self.tiempo_comida_var.set(tiempo)
        unidad = "Minutos" if unidad == "m" else "Segundos"
        self.select_comida.set(unidad)
        self.lbl_estado_comidaT.config(text=msg)
        self.lbl_resultado_comidaT.config(text="")

    def set_resultado_aguaT(self, msg):
        self.lbl_resultado_aguaT.config(text=msg)

    def set_resultado_comidaT(self, msg):
        self.lbl_resultado_comidaT.config(text=msg)


class Tablas(LabelFrame):
    def __init__(self, master=None, name="Consultar Registros"):
        super().__init__(master)
        self.master = master
        self.pack()
        self.name = name
        self.interfaz()

    def interfaz(self):
        Label(self, text=f"..:: {self.name} ::..").place(x=160, y=10)
        self.btn_actualizar = Button(self, text="Actualizar")
        self.btn_actualizar.place(x=10, y=10)
        self.filtro_tipo = Combobox(self, values=["Todo", "Agua", "Alimento"])
        self.filtro_tipo.set("Todo")
        Label(self, text="Filtrar por tipo:").place(x=10, y=50)
        self.filtro_tipo.place(x=100, y=50, width=100)

        Label(self, text="Filtrar por estado:").place(x=300, y=50)
        self.filtro_estado = Combobox(
            self, values=["Todo", "Abierto", "Cerrado"])
        self.filtro_estado.set("Todo")
        self.filtro_estado.place(x=400, y=50, width=100)
        self.btn_enviar_filtro = Button(self, text="Filtrar")
        self.btn_enviar_filtro.place(x=510, y=50)

        self.tabla_registros()

    def tabla_registros(self):
        self.tabla = Treeview(self, selectmode="browse")

        scroll_tabla = Scrollbar(
            self, orient="vertical", command=self.tabla.yview)
        scroll_tabla.pack(side="right", fill="y")
        self.tabla.configure(yscrollcommand=scroll_tabla.set)

        self.tabla.place(x=10, y=80, width=560, height=200)
        self.tabla["columns"] = ("Dispensador", "Estado", "Fecha", "Hora")
        self.tabla.column("#0", width=0, stretch="no")
        self.tabla.column("Dispensador", anchor="nw", width=80)
        self.tabla.column("Estado", anchor="center", width=60)
        self.tabla.column("Fecha", anchor="center", width=200)
        self.tabla.column("Hora", anchor="center", width=200)
        self.tabla.heading("#0", text="", anchor="w")
        self.tabla.heading("Dispensador", text="Dispensador")
        self.tabla.heading("Estado", text="Estado")
        self.tabla.heading("Fecha", text="Fecha")
        self.tabla.heading("Hora", text="Hora")

    def actualizar_tabla(self, registros):

        # Limpiar tablas
        self.tabla.delete(*self.tabla.get_children())
        # Actualizar tabla de agua
        for registro in registros:
            # Modificar la columna "id" con "Servo1"
            registro = list(registro)
            registro[0] = "agua" if registro[0] == 1 else "alimento"
            self.tabla.insert("", "end", values=registro)


class Registro(Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.registro1 = Tablas(self, "Dispensador 1")
        self.registro1.place(x=10, y=10, width=600, height=300)

        self.registro2 = Tablas(self, "Dispensador 1")
        self.registro2.place(x=10, y=310, width=600, height=300)


class Ventana(Tk):
    def __init__(self):
        super().__init__()
        self.title("Monitor de dispensador")
        self.geometry("1200x900")
        # self.resizable(0, 0)
        self.imagen_agua = PhotoImage(file="imagen/agua.png")
        self.imagen_comida = PhotoImage(file="imagen/comida.png")
        self.imagen_agua = self.imagen_agua.subsample(2)
        self.imagen_comida = self.imagen_comida.subsample(2)
        self.taps()

    def taps(self):
        self.tap = Notebook(self)
        self.tap.pack(fill='both', expand=True)
        self.inicio = Inicio(self.tap, self.imagen_agua, self.imagen_comida)
        self.tiempo = Tiempo(self.tap, self.imagen_agua, self.imagen_comida)
        self.registro = Registro(self.tap)
        self.tap.add(self.inicio, text="Inicio")
        self.tap.add(self.tiempo, text="Tiempo")
        self.tap.add(self.registro, text="Registro")

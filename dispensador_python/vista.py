from tkinter import Tk, Frame, Button, Label, IntVar, Scale, PhotoImage, messagebox, Toplevel, ttk, Scrollbar, Tk, Frame, Label, Checkbutton, IntVar, Listbox
from tkinter.ttk import Treeview, Combobox, Notebook


class Inicio(Frame):
    def __init__(self, master=None, imagen_agua=None, imagen_comida=None):
        super().__init__(master)
        self.master = master
        self.pack()
        self.var_dispensar_agua = IntVar()
        self.var_dispensar_comida = IntVar()
        self.imagen_agua = imagen_agua
        self.imagen_comida = imagen_comida
        self.interfaz()

    def interfaz(self):
        self.label = Label(
            self, text="..:: Encender Dispensador ::..")
        self.label.pack(pady=10)
        self.msg_estados()
        self.imagenes()
        self.mis_checkbox()

    def msg_estados(self):
        # barra de estado(servo)
        self.lb_estado_dis_agua = Label(
            self, fg="blue", font=("Courier New", 10, "bold"))
        self.lb_estado_dis_agua.place(x=100, y=40)

        self.lb_estado_dis_alimento = Label(self, fg="green", font=(
            "Courier New", 10, "bold"))
        self.lb_estado_dis_alimento.place(x=400, y=40)

        self.lb_estado_con_agua = Label(
            self, fg="blue", font=("Courier New", 14, "bold"))

        self.lb_estado_con_agua.place(x=30, y=500)

        self.lb_estado_con_alimento = Label(self, fg="green", font=(
            "Courier New", 14, "bold"))

        self.lb_estado_con_alimento.place(x=30, y=480)

    def imagenes(self):
        # imagen de agua
        Label(self, image=self.imagen_agua).place(x=70, y=100)

        # imagen de comida
        Label(self, image=self.imagen_comida).place(x=370, y=100)

    def mis_checkbox(self):
        self.check_agua = Checkbutton(
            self, text="Dispensar Agua", variable=self.var_dispensar_agua, onvalue=1, offvalue=0)
        self.check_agua.place(x=100, y=300)

        self.check_comida = Checkbutton(
            self, text="Dispensar Comida", variable=self.var_dispensar_comida, onvalue=1, offvalue=0)
        self.check_comida.place(x=400, y=300)

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


class Tiempo(Frame):
    def __init__(self, master=None, imagen_agua=None, imagen_comida=None):
        super().__init__(master)
        self.master = master
        self.pack()
        self.tiempo_agua_var = IntVar()
        self.tiempo_comida_var = IntVar()
        self.imagen_agua = imagen_agua
        self.imagen_comida = imagen_comida

        self.interfaz()

    def interfaz(self):
        Label(self, text="..:: Tiempo para dispensar ::..").place(x=300, y=10)
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


class Registro(Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.pack()
        self.interfaz()

    def interfaz(self):
        self.label = Label(
            self, text="..:: Consultar Registros ::..")
        self.label.pack(pady=10)
        self.btn_actualizar = Button(self, text="Actualizar")
        self.btn_actualizar.place(x=10, y=10)
        self.tabla_registros_agua()
        self.tabla_registros_comida()

    def tabla_registros_agua(self):
        scroll_dato_agua = Scrollbar(self, orient="vertical")

        Label(self, text="Registro de Agua").place(x=10, y=40)
        self.agua = Treeview(
            self, height=10, yscrollcommand=scroll_dato_agua.set)

        scroll_dato_agua.place(x=750, y=100)
        scroll_dato_agua.configure(command=self.agua.yview)

        self.agua.place(x=10, y=60)
        self.agua["columns"] = ("Servo", "id", "Estado", "Fecha", "Hora")
        self.agua.column("#0", width=0, stretch="no")
        self.agua.column("Servo", anchor="center", width=60)
        self.agua.column("id", anchor="center", width=60)
        self.agua.column("Estado", anchor="center", width=50)
        self.agua.column("Fecha", anchor="center", width=200)
        self.agua.column("Hora", anchor="center", width=200)

        self.agua.heading("#0", text="", anchor="w")
        self.agua.heading("Servo", text="Servo")
        self.agua.heading("id", text="id")
        self.agua.heading("Estado", text="Estado")
        self.agua.heading("Fecha", text="Fecha")
        self.agua.heading("Hora", text="Hora")

    def tabla_registros_comida(self):

        Label(self, text="Registro de Comida").place(x=10, y=320)
        scroll_dato_comida = Scrollbar(self, orient="vertical")

        self.comida = Treeview(self, height=10,
                               yscrollcommand=scroll_dato_comida.set)

        scroll_dato_comida.place(x=750, y=400)
        scroll_dato_comida.configure(command=self.comida.yview)

        self.comida.place(x=10, y=340)

        # trecera pestaña

        self.comida["columns"] = ("Servo", "id", "Estado", "Fecha", "Hora")
        self.comida.column("#0", width=0, stretch="no")
        self.comida.column("Servo", anchor="center", width=60)
        self.comida.column("id", anchor="center", width=60)
        self.comida.column("Estado", anchor="center", width=50)
        self.comida.column("Fecha", anchor="center", width=200)
        self.comida.column("Hora", anchor="center", width=200)

        self.comida.heading("#0", text="", anchor="w")
        self.comida.heading("Servo", text="Servo")
        self.comida.heading("id", text="id")
        self.comida.heading("Estado", text="Estado")
        self.comida.heading("Fecha", text="Fecha")
        self.comida.heading("Hora", text="Hora")

    def actualizar_tabla_agua(self, registros_agua):

        # Limpiar tablas
        self.agua.delete(*self.agua.get_children())
        # Actualizar tabla de agua
        for registro in registros_agua:
            # Modificar la columna "id" con "Servo1"
            registro = list(registro)
            registro[0] = "agua" if registro[0] == 1 else "agua"
            self.agua.insert("", "end", values=registro)

    def actualizar_tabla_alimento(self, registros_comida):

        self.comida.delete(*self.comida.get_children())

        # Actualizar tabla de agu
        # Actualizar tabla de comida
        for registro in registros_comida:
            # Modificar la columna "id" con "Servo1"
            registro = list(registro)
            registro[0] = "comida" if registro[0] == 1 else "comida"
            self.comida.insert("", "end", values=registro)


class Ventana(Tk):
    def __init__(self):
        super().__init__()
        self.title("Dispensador de Medicamentos")
        self.geometry("800x600")
        self.resizable(0, 0)
        self.imagen_agua = PhotoImage(file="imagen/agua.png")
        self.imagen_comida = PhotoImage(file="imagen/comida.png")
        self.taps()

    def taps(self):
        self.taps = Notebook(self)
        self.taps.pack(fill='both', expand=True)
        self.inicio = Inicio(self.taps, self.imagen_agua, self.imagen_comida)
        self.tiempo = Tiempo(self.taps, self.imagen_agua, self.imagen_comida)
        self.registro = Registro(self.taps)
        self.taps.add(self.inicio, text="Inicio")
        self.taps.add(self.tiempo, text="Tiempo")
        self.taps.add(self.registro, text="Registro")

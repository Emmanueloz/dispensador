from tkinter import Tk, Frame, Button, Label, Entry, StringVar, IntVar, Scale, PhotoImage, messagebox, Toplevel, ttk, Scrollbar, Tk, Frame, Label, Checkbutton, StringVar, IntVar
from tkinter import Tk, Frame, Label, StringVar, Listbox, Scrollbar
import threading


class Inicio(Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.pack()
        self.var_dispensar_agua = IntVar()
        self.var_dispensar_comida = IntVar()

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
        self.imagen_agua = PhotoImage(file="imagen/agua.png")
        self.imagen_comida = PhotoImage(file="imagen/comida.png")
        # imagen de agua
        self.im_agua = Label(self, image=self.imagen_agua)
        self.im_agua.place(x=70, y=100)

        # imagen de comida
        self.im_comida = Label(self, image=self.imagen_comida)
        self.im_comida.place(x=370, y=100)

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
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.pack()
        self.interfaz()

    def interfaz(self):
        self.label = Label(
            self, text="..:: Configurar Tiempo ::..")
        self.label.pack(pady=10)


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


class Ventana(Tk):
    def __init__(self):
        super().__init__()
        self.title("Dispensador de Medicamentos")
        self.geometry("800x600")
        self.resizable(0, 0)
        self.taps()

    def taps(self):
        self.taps = ttk.Notebook(self)
        self.taps.pack(fill='both', expand=True)
        self.inicio = Inicio(self.taps)
        self.tiempo = Tiempo(self.taps)
        self.registro = Registro(self.taps)
        self.taps.add(self.inicio, text="Inicio")
        self.taps.add(self.tiempo, text="Tiempo")
        self.taps.add(self.registro, text="Registro")

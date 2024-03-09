from tkinter import Tk, Frame, Button, Label, Entry, StringVar, IntVar, Scale, PhotoImage, messagebox, Toplevel, ttk, Scrollbar, Tk, Frame, Label, Checkbutton, StringVar, IntVar
from tkinter import Tk, Frame, Label, StringVar, Listbox, Scrollbar
import threading


class Inicio(Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.pack()
        self.interfaz()

    def interfaz(self):
        self.label = Label(
            self, text="..:: Encender Dispensador ::..")
        self.label.pack(pady=10)


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

        self.imagen_agua = PhotoImage(file="imagen/agua.png")
        self.imagen_comida = PhotoImage(file="imagen/comida.png")
        # imagen de agua
        self.im_agua = Label(self, image=self.imagen_agua)
        self.im_agua.place(x=70, y=100)

        # imagen de comida
        self.im_comida = Label(self, image=self.im_comida)
        self.im_comida.place(x=370, y=100)


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


app = Ventana()
app.mainloop()

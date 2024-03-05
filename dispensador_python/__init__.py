from tkinter import Tk, Frame, Button, Label, Entry, StringVar, IntVar, Scale, PhotoImage, messagebox, Toplevel, ttk,Scrollbar
from tkinter import Tk, Frame, Label, StringVar, Listbox, Scrollbar
import threading
import tkinter

miVentana = Tk()
miVentana.title("Gustavo Alexander Medina Cifuentes")
miVentana.resizable(0, 0)
miVentana.geometry("500x500")
miVentana.grid_propagate(0)

notebook = ttk.Notebook(miVentana)
notebook.pack(fill='both', expand=True)

inicio = Frame(notebook)
tiempo = Frame(notebook)
cont = Frame(notebook)
consulta =Frame(notebook)

inicio.grid()

notebook.add(inicio, text='Inicio') 
notebook.add(tiempo, text='Tiempo') 
notebook.add(cont, text='Contenedor')
notebook.add(consulta, text='Regristro')  

imagen_agua = PhotoImage(file="imagen/agua.png")
imagen_comida = PhotoImage(file="imagen/comida.png")


lbl_titulo = Label(inicio, text="..:: Encender Dispensador ::..")
lbl_titulo.grid(row=0, column=0,columnspan=4,padx=10,pady=5,sticky="we")


#imagen de agua
im_agua = Label(inicio, image=imagen_agua)
im_agua.grid(row=1, column=0)


#imagen de comida
im_comida = Label(inicio, image=imagen_comida)
im_comida.grid(row=1, column=1)


##botones para dispnsar el agua(servo)
btn_ON_Agua = Button(inicio, width=12, text="Dispensar Agua", fg="blue")
btn_ON_Agua.grid(row=2, column=0)

btn_OFF_Agua = Button(inicio, width=10, text="Detener", fg="red")
btn_OFF_Agua.grid(row=3, column=0)

##botones para dispnsar el comida(servo)
btn_ON_Comida = Button(inicio, width=14, text="Dispensar comida", fg="blue")
btn_ON_Comida.grid(row=2, column=1)

btn_OFF_Comida = Button(inicio, width=10, text="Detener", fg="red")
btn_OFF_Comida.grid(row=3, column=1)



##barra de estado(servo)
lbl_estado = Label(inicio, text="hola", fg="red", font=("Courier New", 14, "bold"))
lbl_estado.grid(row=10, column=0,columnspan=4,  padx=5, pady=5,sticky="we")


miVentana.mainloop()
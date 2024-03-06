from tkinter import Tk, Frame, Button, Label, Entry, StringVar, IntVar, Scale, PhotoImage, messagebox, Toplevel, ttk,Scrollbar,Tk, Frame, Label, Checkbutton, StringVar, IntVar
from tkinter import Tk, Frame, Label, StringVar, Listbox, Scrollbar
import threading
import tkinter

miVentana = Tk()
miVentana.title("Gustavo Alexander Medina Cifuentes")
miVentana.resizable(0, 0)
miVentana.geometry("700x600")
miVentana.grid_propagate(0)

notebook = ttk.Notebook(miVentana)
notebook.pack(fill='both', expand=True)

inicio = Frame(notebook)
tiempo = Frame(notebook)
consulta =Frame(notebook)

inicio.grid()

notebook.add(inicio, text='Inicio') 
notebook.add(tiempo, text='Tiempo') 
notebook.add(consulta, text='Regristro')  

imagen_agua = PhotoImage(file="imagen/agua.png")
imagen_comida = PhotoImage(file="imagen/comida.png")


###Inicio

lbl_titulo = Label(inicio, text="..:: Encender Dispensador ::..")
lbl_titulo.place(x=250,y=0)

##barra de estado(servo)
lbl_estado_agua = Label(inicio, text="Estado del agua", fg="red", font=("Courier New", 14, "bold"))
lbl_estado_agua.place(x=400,y=40)


lbl_estado_comida = Label(inicio, text="Estado decomida", fg="red", font=("Courier New", 14, "bold"))
lbl_estado_comida.place(x=100,y=40)

#imagen de agua
im_agua = Label(inicio,image=imagen_agua)
im_agua.place(x=70,y=100)


#imagen de comida
im_comida = Label(inicio, image=imagen_comida)
im_comida.place(x=370,y=100)


##botones para dispnsar el agua(servo)
Checkbutton(inicio, text="Dispensar agua", onvalue=1,offvalue=0, ).place(x=450,y=350)


##botones para dispnsar el comida(servo)
Checkbutton(inicio, text="Dispensar comida", onvalue=1,offvalue=0, ).place(x=150,y=350)



lbl_estado_comida = Label(inicio, text="si esta abierto o cerrado", fg="red", font=("Courier New", 14, "bold"))
lbl_estado_comida.place(x=200,y=400)


##recibir datos pel contenedor de agua
scroll_conte = Scrollbar(inicio, orient="vertical")
lstbox_conte = Listbox(inicio, height=5,width=43 ,yscrollcommand=scroll_conte.set)

scroll_conte.place(x=300, y=490)
lstbox_conte.place(x=15,y=470)
scroll_conte.configure(command=lstbox_conte.yview)


##recibir datos pel contenedor de agua
scroll_conte_come = Scrollbar(inicio, orient="vertical")
lstbox_conte_come = Listbox(inicio, height=5,width=43,  yscrollcommand=scroll_conte_come .set)

scroll_conte_come.place(x=674, y=490)
lstbox_conte_come.place(x=400,y=470)
scroll_conte_come.configure(command=lstbox_conte_come.yview)

##Timpo


lbl_titulo = Label(tiempo, text="..:: Tiempo para dispensar ::..")
lbl_titulo.grid(row=0, column=0,columnspan=6,padx=10,pady=5,sticky="we")

##barra de estado(servo)
lbl_estado_agua = Label(tiempo, text="Estado del agua", fg="red", font=("Courier New", 14, "bold"))
lbl_estado_agua.grid(row=1, column=2, columnspan=2, padx=5, pady=5)


lbl_estado_comida = Label(tiempo, text="Estado decomida", fg="red", font=("Courier New", 14, "bold"))
lbl_estado_comida.grid(row=1, column=4, columnspan=1, padx=5, pady=5)

Scale(tiempo,  from_=0, to=60, orient="vertical", tickinterval=30, length=200).grid(row=1, column=0, rowspan=4, padx=5, pady=5)
Scale(tiempo,  from_=0, to=60, orient="vertical", tickinterval=30, length=200).grid(row=1, column=5, rowspan=4, padx=5, pady=5)


#imagen de agua
im_agua = Label(tiempo, image=imagen_agua)
im_agua.grid(row=2, column=2)


#imagen de comida
im_comida = Label(tiempo, image=imagen_comida)
im_comida.grid(row=2, column=4)



    
selec_agua = ttk.Combobox(tiempo,values=["Minuto", "Segundo"])
selec_agua.bind("<<ComboboxSelected>>")
selec_agua.grid(row=4,column=2)

selec_comida = ttk.Combobox(tiempo,values=["Minuto", "Segundo"])
selec_comida.bind("<<ComboboxSelected>>")
selec_comida.grid(row=4,column=4)

Button(tiempo, width=8, text="Enviar").place(x=150,y=350)
Button(tiempo, width=8, text="Enviar").place(x=400,y=350)

lbl_estado_comida = Label(tiempo, text="si esta abierto o cerrado", fg="red", font=("Courier New", 14, "bold"))
lbl_estado_comida.place(x=200,y=450)



##Pestaña de registros en la base de datos
lbl_titulo = Label(consulta, text="..:: Tiempo para dispensar ::..")
lbl_titulo.place(x=250,y=0)

scroll_dato_agua = Scrollbar(consulta, orient="vertical")

agua = ttk.Treeview(consulta, height=10,yscrollcommand=scroll_dato_agua.set)

scroll_dato_agua.place(x=670,y=100)
scroll_dato_agua.configure(command=agua.yview)

agua.place(x=10,y=30)


agua["columns"] = ("Servo", "Valor", "Fecha", "Hora")
agua.column("#0", width=0, stretch="no")
agua.column("Servo", anchor="center", width=60)
agua.column("Fecha", anchor="center", width=50)
agua.column("Hora", anchor="center", width=450)
agua.column("Valor", anchor="center", width=80)

agua.heading("#0", text="", anchor="w")
agua.heading("Servo", text="Servo")
agua.heading("Valor", text="Valor")
agua.heading("Fecha", text="Fecha")
agua.heading("Hora", text="Hora")




scroll_dato_comida = Scrollbar(consulta, orient="vertical")

comida = ttk.Treeview(consulta, height=10, yscrollcommand=scroll_dato_comida.set)

scroll_dato_comida.place(x=670,y=450)
scroll_dato_comida.configure(command=comida.yview)

comida.place(x=10,y=340)


comida["columns"] = ("Servo", "Valor", "Fecha", "Hora")
comida.column("#0", width=0, stretch="no")
comida.column("Servo", anchor="center", width=60)
comida.column("Fecha", anchor="center", width=50)
comida.column("Hora", anchor="center", width=450)
comida.column("Valor", anchor="center", width=80)

comida.heading("#0", text="", anchor="w")
comida.heading("Servo", text="Servo")
comida.heading("Valor", text="Valor")
comida.heading("Fecha", text="Fecha")
comida.heading("Hora", text="Hora")


miVentana.mainloop()
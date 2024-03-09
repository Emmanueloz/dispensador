from tkinter import Tk, Frame, Button, Label, Entry, StringVar, IntVar, Scale, PhotoImage, messagebox, Toplevel, ttk,Scrollbar,Tk, Frame, Label, Checkbutton, StringVar, IntVar
from tkinter import Tk, Frame, Label, StringVar, Listbox, Scrollbar
import threading
import tkinter
from serial import SerialException
from .controlador import Controller
import time

controlador = Controller()

def conectar_todo():
    resultado_conexion = controlador.conectar_todo()
    messagebox.showinfo("Conexión", resultado_conexion)
    
    
    
def dispensar_comida_var():
    global dispensando
    estado_comida = var_dispensar_comida.get()

    if estado_comida == 1:
        resultado_dispensar_comida = controlador.abrir_dispensador_alimento()
        dispensando = True
    else:
        resultado_dispensar_comida = controlador.cerrar_dispensador_alimento()
        dispensando = False

    lbl_dispensando.config(text="Dispensando" if dispensando else "")
    return resultado_dispensar_comida
    
    
def dispensar_agua_var():
    global dispensandoA
    estado_agua = var_dispensar_agua.get()

    if estado_agua == 1:
        resultado_dispensar_agua = controlador.abrir_dispensador_agua()
        dispensandoA = True
    else:
        resultado_dispensar_agua = controlador.cerrar_dispensador_agua()
        dispensandoA = False
        
    lbl_dispensandoAgua.config(text="Dispensado" if dispensandoA else "")
    return("Dispensar agua", resultado_dispensar_agua)



def enviar_tiempo_comida():
    unidad = selec_comida.get()
    tiempo = tiempo_comida_var.get()

    if unidad and tiempo:
        unidad_visual = 'm' if unidad == 'Minuto' else 's'
        tiempo_visual = f"{tiempo} {unidad_visual}"
        
        lbl_estado_comida.config(text=f"Tiempo de comida: {tiempo_visual}")
        controlador.definir_intervalo_tiempo_comida(tiempo, unidad_visual)

        
    else:
        messagebox.showwarning("Advertencia", "Selecciona unidad y tiempo antes de enviar.")
        
        
        
def enviar_tiempo_agua():
    unidad = selec_agua.get()
    tiempo = tiempo_agua_var.get()

    if unidad and tiempo:
        unidad_visual = 'm' if unidad == 'Minuto' else 's'
        tiempo_visual = f"{tiempo} {unidad_visual}"
        
        lbl_estado_comida.config(text=f"Tiempo de agua: {tiempo_visual}")
        controlador.definir_intervalo_tiempo_agua(tiempo, unidad_visual)
        
    else:
        messagebox.showwarning("Advertencia", "Selecciona unidad y tiempo antes de enviar.")


def monitorear_estado_servo(etiqueta_estado):
    while True:
        try:
            posicion_servo = controlador.obtener_posicion_servo_alimento()

            mapa_posiciones = {"0": "Cerrado", "90": "Abierto"}

            estado_actual = mapa_posiciones.get(posicion_servo, "...Esperando..")

            etiqueta_estado.config(text=f"{estado_actual}")
            
            estado = 1 if posicion_servo == "90" else 0
            print(f"alimento {estado}")
            
            var_dispensar_comida.set(estado)
            

        except SerialException as serial_error:
            etiqueta_estado.config(text=f"Error de comunicación serial: {str(serial_error)}")
        except Exception as error:
            etiqueta_estado.config(text=f"Error inesperado al obtener la posición del servo de alimento: {str(error)}")

        time.sleep(8)


def monitorear_estado_servo_agua(etiqueta_estado):
    while True:
        try:

            posicion_servo_agua = controlador.obtener_posicion_servo_agua()

            mapa_posiciones_agua = {"0": "Cerrado", "90": "Abierto"}

            estado_actual_agua = mapa_posiciones_agua.get(posicion_servo_agua, "...Esperando..")

            etiqueta_estado.config(text=f"{estado_actual_agua}")
            
            estado = 1 if posicion_servo_agua == "90" else 0
            print(f"agua {estado}")
            var_dispensar_agua.set(estado)

        except SerialException as serial_error:
            etiqueta_estado.config(text=f"Error de comunicación serial: {str(serial_error)}")
        except Exception as error:
            etiqueta_estado.config(text=f"Error inesperado al obtener la posición del servo de agua: {str(error)}")

        time.sleep(11)


def monitorear_estado_contenedor_alimento( etiqueta_estado):
    while True:
        try:
            # Obtener el estado del contenedor de alimento
            estado_contenedor_alimento = controlador.obtener_estado_contenedor_alimento()

            # Actualizar la etiqueta con el estado actual
            etiqueta_estado.config(text=estado_contenedor_alimento)

        except SerialException as serial_error:
            etiqueta_estado.config(text=f"Error de comunicación serial: {str(serial_error)}")
        except Exception as error:
            etiqueta_estado.config(text=f"Error inesperado al obtener el estado del contenedor de alimento: {str(error)}")

        time.sleep(15) 
        
def monitorear_estado_contenedor_agua( etiqueta_estado):
    while True:
        try:
            # Obtener el estado del contenedor de alimento
            estado_contenedor_agua = controlador.obtener_distancia_ultrasonico_agua()

            # Actualizar la etiqueta con el estado actual
            etiqueta_estado.config(text=estado_contenedor_agua)

        except SerialException as serial_error:
            etiqueta_estado.config(text=f"Error de comunicación serial: {str(serial_error)}")
        except Exception as error:
            etiqueta_estado.config(text=f"Error inesperado al obtener el estado del contenedor de alimento: {str(error)}")

        time.sleep(14)  

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
lbl_estado_agua = Label(inicio, fg="red", font=("Courier New", 10, "bold"))
lbl_estado_agua.place(x=100,y=40)


lbl_estado_comidaIni = Label(inicio, fg="red", font=("Courier New", 10, "bold"))
lbl_estado_comidaIni.place(x=400,y=40)

#imagen de agua
im_agua = Label(inicio,image=imagen_agua)
im_agua.place(x=70,y=100)


#imagen de comida
im_comida = Label(inicio, image=imagen_comida)
im_comida.place(x=370,y=100)


##botones para dispnsar el agua(servo)
var_dispensar_agua = IntVar()
Checkbutton(inicio, text="Dispensar agua", onvalue=1,offvalue=0, variable=var_dispensar_agua, command=dispensar_agua_var ).place(x=150, y=350)


var_dispensar_comida = IntVar()
checkbutton_comida = Checkbutton(inicio,text="Dispensar Comida", onvalue=1, offvalue=0, variable=var_dispensar_comida, command=dispensar_comida_var)
checkbutton_comida.place(x=450, y=350)



lbl_dispensando = Label(inicio, text="", fg="green", font=("Courier New", 14, "bold"))
lbl_dispensando.place(x=450, y=390)

lbl_dispensandoAgua = Label(inicio, text="", fg="green", font=("Courier New", 14, "bold"))
lbl_dispensandoAgua.place(x=30, y=390)


lbl_contene_comida = Label(inicio,text="", fg="red", font=("Courier New", 14, "bold"))
lbl_contene_comida.place(x=30,y=470)



##recibir datos pel contenedor de agua
lbl_contene_agua = Label(inicio, fg="blue", font=("Courier New", 14, "bold"))
lbl_contene_agua.place(x=30,y=500)
##Timpo


lbl_titulo = Label(tiempo, text="..:: Tiempo para dispensar ::..")
lbl_titulo.grid(row=0, column=0,columnspan=6,padx=10,pady=5,sticky="we")

##barra de estado(servo)
lbl_estado_aguaT = Label(tiempo, fg="red", font=("Courier New", 14, "bold"))
lbl_estado_aguaT.grid(row=1, column=2, columnspan=2, padx=5, pady=5)


lbl_estado_comidaT = Label(tiempo, fg="red", font=("Courier New", 14, "bold"))
lbl_estado_comidaT.grid(row=1, column=4, columnspan=1, padx=5, pady=5)


tiempo_agua_var = IntVar()
tiempo_agua=Scale(tiempo,  from_=0, to=60, orient="vertical", tickinterval=30, length=400,variable=tiempo_agua_var).grid(row=1, column=0, rowspan=4, padx=5, pady=5)
tiempo_comida_var = IntVar()  # Variable para almacenar el valor de la escala
tiempo_comida = Scale(tiempo, from_=0, to=60, orient="vertical", tickinterval=30, length=400, variable=tiempo_comida_var).grid(row=1, column=5, rowspan=4, padx=5, pady=5)


#imagen de agua
im_agua = Label(tiempo, image=imagen_agua)
im_agua.grid(row=2, column=2)


#imagen de comida
im_comida = Label(tiempo, image=imagen_comida)
im_comida.grid(row=2, column=4)



    
selec_agua = ttk.Combobox(tiempo,values=["Minuto", "Segundo"])
selec_agua.grid(row=4,column=2)

selec_comida = ttk.Combobox(tiempo,values=["Minuto", "Segundo"])
selec_comida.grid(row=4,column=4)

enviar_agua=Button(tiempo, width=8, text="Enviar",command=enviar_tiempo_agua).place(x=150,y=350)

enviar_comida=Button(tiempo, width=8, text="Enviar",command=enviar_tiempo_comida).place(x=400,y=350)



lbl_estado_comida = Label(tiempo, fg="red", font=("Courier New", 14, "bold"))
lbl_estado_comida.place(x=200,y=450)



conectar_todo()
hilo_monitoreo = threading.Thread(target=monitorear_estado_servo, args=(lbl_estado_comidaIni,))
hilo_monitoreo.start()
hilo_monitoreo_agua = threading.Thread(target=monitorear_estado_servo_agua, args=(lbl_estado_agua,))
hilo_monitoreo_agua.start()
hilo_monitoreo_contenedor_alimento = threading.Thread(target=monitorear_estado_contenedor_alimento, args=(lbl_contene_comida,))
hilo_monitoreo_contenedor_alimento.start()
hilo_monitoreo_contenedor_alimento = threading.Thread(target=monitorear_estado_contenedor_agua, args=(lbl_contene_agua,))
hilo_monitoreo_contenedor_alimento.start()



##Pestaña de registros en la base de datos
lbl_titulo = Label(consulta, text="Registros")
lbl_titulo.place(x=250,y=0)

scroll_dato_agua = Scrollbar(consulta, orient="vertical")

agua = ttk.Treeview(consulta, height=10,yscrollcommand=scroll_dato_agua.set)

scroll_dato_agua.place(x=670,y=100)
scroll_dato_agua.configure(command=agua.yview)

agua.place(x=10,y=30)


agua["columns"] = ("Servo" ,"id","Estado", "Fecha", "Hora")
agua.column("#0", width=0, stretch="no")
agua.column("Servo", anchor="center", width=60)
agua.column("id", anchor="center", width=60)
agua.column("Estado", anchor="center", width=50)
agua.column("Fecha", anchor="center", width=200)
agua.column("Hora", anchor="center", width=200)

agua.heading("#0", text="", anchor="w")
agua.heading("Servo", text="Servo")
agua.heading("id", text="id")
agua.heading("Estado", text="Estado")
agua.heading("Fecha", text="Fecha")
agua.heading("Hora", text="Hora")




scroll_dato_comida = Scrollbar(consulta, orient="vertical")

comida = ttk.Treeview(consulta, height=10, yscrollcommand=scroll_dato_comida.set)

scroll_dato_comida.place(x=670,y=450)
scroll_dato_comida.configure(command=comida.yview)

comida.place(x=10,y=340)


##trecera pestaña 

comida["columns"] = ("Servo" ,"id","Estado", "Fecha", "Hora")
comida.column("#0", width=0, stretch="no")
comida.column("Servo", anchor="center", width=60)
comida.column("id", anchor="center", width=60)
comida.column("Estado", anchor="center", width=50)
comida.column("Fecha", anchor="center", width=200)
comida.column("Hora", anchor="center", width=200)

comida.heading("#0", text="", anchor="w")
comida.heading("Servo", text="Servo")
comida.heading("id", text="id")
comida.heading("Estado", text="Estado")
comida.heading("Fecha", text="Fecha")
comida.heading("Hora", text="Hora")


def actualizar_tablas():
    registros_agua = controlador.consultar_registro(idComponente=1)
    registros_comida = controlador.consultar_registro(idComponente=2)

    # Limpiar tablas
    agua.delete(*agua.get_children())
    comida.delete(*comida.get_children())

    # Actualizar tabla de agua
    for registro in registros_agua:
        # Modificar la columna "id" con "Servo1"
        registro = list(registro)
        registro[0] = "agua" if registro[0] == 1 else "agua"
        agua.insert("", "end", values=registro)

    # Actualizar tabla de comida
    for registro in registros_comida:
        # Modificar la columna "id" con "Servo1"
        registro = list(registro)
        registro[0] = "comida" if registro[0] == 1 else "comida"
        comida.insert("", "end", values=registro)
        
    agua.after(100000, actualizar_tablas)
    comida.after(10000,actualizar_tablas)

actualizar_tablas()

miVentana.mainloop()
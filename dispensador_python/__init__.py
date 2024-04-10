from .controlador import ControllerVista
from .vista import Ventana


app = Ventana()
controlador = ControllerVista(app, "dis3")
controlador.iniciar()
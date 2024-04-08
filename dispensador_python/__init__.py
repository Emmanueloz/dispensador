from .controlador import ControllerVista
from .vista import Ventana


app = Ventana()
controlador = ControllerVista(app, "dis1")
controlador.iniciar()

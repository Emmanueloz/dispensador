from .controlador import ControllerVista
from .vista import Ventana


app = Ventana()
controlador = ControllerVista(app)
controlador.iniciar()

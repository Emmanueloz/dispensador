from .controlador import ControllerVista
from .vista import Ventana


name_id = "dis5"

app = Ventana(name_id)
controlador = ControllerVista(app, name_id)
controlador.iniciar()

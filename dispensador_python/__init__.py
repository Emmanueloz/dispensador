from colorama import init, Fore, Back
from .controlador import Controller

# Inicializar Colorama
init(autoreset=True)

# Crear una instancia del controlador
controller = Controller()

result = controller.conectar_todo()
print(result)

menu = f'''
=========[Dispensadores]=============================
|| {Back.GREEN}1{Back.RESET} - {Fore.CYAN}Dispensar Agua o Comida{Fore.RESET}                      ||
|| {Back.GREEN}2{Back.RESET} - {Fore.CYAN}Cerrar dispensador{Fore.RESET}                      ||
|| {Back.GREEN}3{Back.RESET} - {Fore.MAGENTA}Consulta Registros{Fore.RESET}                        ||
|| {Back.GREEN}4{Back.RESET} - {Fore.BLUE}Dispensar automático{Fore.RESET}                      ||
|| {Back.GREEN}5{Back.RESET} - {Fore.MAGENTA}Consulta Dispensador{Fore.RESET}                        ||
|| {Back.GREEN}6{Back.RESET} - {Fore.MAGENTA}Consulta Contenedores{Fore.RESET}                        ||
|| {Back.GREEN}7{Back.RESET} - {Fore.MAGENTA}Consultar intervalo{Fore.RESET}                        ||
|| {Back.GREEN}s{Back.RESET} - {Fore.RED}Salir{Fore.RESET}                                        ||
======================================================
'''

subMenu = f'''
||      {Back.GREEN}A.{Back.RESET}{Fore.BLUE} Agua {Fore.RESET}                     ||
||      {Back.GREEN}B.{Back.RESET}{Fore.YELLOW} Comida {Fore.RESET}                   ||
||      {Back.GREEN}M.{Back.RESET}{Fore.RED} Volver al Menú Principal {Fore.RESET} ||
'''

tiempo = f'''
||      {Back.GREEN}A.{Back.RESET}{Fore.BLUE} Minuto {Fore.RESET}                     ||
||      {Back.GREEN}B.{Back.RESET}{Fore.YELLOW} Segundo {Fore.RESET}                   ||
||      {Back.GREEN}M.{Back.RESET}{Fore.RED} Volver al Menú Principal {Fore.RESET} ||
'''

while True:
    print(menu)
    opcion_principal = input(f"{Fore.GREEN}Seleccione una opción (1-3, s): ")

    if opcion_principal in ["1", "2", "3", "4", "5", "6", "7"]:
        print(subMenu)
        opcion_secundaria = input(
            f"{Fore.GREEN}Seleccione una opción (A-B-M):{Fore.RESET}")

        if opcion_secundaria.lower() == 'm':
            continue  # Regresar al menú principal

        elif opcion_secundaria.lower() == 'a' or opcion_secundaria.lower() == 'b':
            if opcion_principal == '1':
                if opcion_secundaria.lower() == 'a':
                    respuesta = controller.abrir_dispensador_agua()
                    print(respuesta)
                elif opcion_secundaria.lower() == 'b':
                    respuesta = controller.abrir_dispensador_alimento()
                    print(respuesta)
                elif opcion_secundaria.lower() == 'm':
                    continue
            elif opcion_principal == '2':
                if opcion_secundaria.lower() == 'a':
                    cerrar_dispensador = input(
                        "¿Desea cerrar el dispensador? (s/n): ").lower()
                    if cerrar_dispensador == 's':
                        respuesta_cerrar = controller.cerrar_dispensador_agua()
                        print(respuesta_cerrar)
                    else:
                        print("El dispensador ya esta cerrado")
                elif opcion_secundaria.lower() == 'b':
                    cerrar_dispensador = input(
                        "¿Desea cerrar el dispensador? (s/n): ").lower()
                    if cerrar_dispensador == 's':
                        respuesta_cerrar = controller.cerrar_dispensador_alimento()
                        print(respuesta_cerrar)
                    else:
                        print("El despensador de alimento esta cerrdo")
            elif opcion_principal == '3':
                if opcion_secundaria.lower() == 'a':
                    respuesta = controller.consultar_registro(idSensor="1")
                    print(respuesta)
                elif opcion_secundaria.lower() == 'b':
                    respuesta = controller.consultar_registro(idSensor="2")
                    print(respuesta)

            elif opcion_principal == '4':
                print(tiempo)
                option_tiempo = input(
                    f"{Fore.GREEN}Seleccione una opción (A-B-M):{Fore.RESET}")

                if option_tiempo.lower() == 'a' or option_tiempo.lower() == 'b':
                    valor_tiempo = input(
                        f"{Fore.GREEN}Inserte el valor para el dispensador en {option_tiempo.capitalize()}:{Fore.RESET}")

                    if valor_tiempo.isdigit():
                        # unidad_tiempo = 'm' if option_tiempo.lower() == 'a' else 's'

                        if opcion_secundaria.lower() == 'a':
                            # Llamar a la función correspondiente del controlador
                            respuesta = controller.definir_intervalo_tiempo_agua(
                                tiempo=valor_tiempo, unidad="m")
                            print(respuesta)
                        elif opcion_secundaria.lower() == 'b':
                            # Llamar a la función correspondiente del controlador
                            respuesta = controller.definir_intervalo_tiempo_comida(
                                tiempo=valor_tiempo, unidad="s")
                            print(respuesta)
                    else:
                        print(f"""{Back.RED}Error: El valor debe ser un número entero{
                              Back.RESET}""")
                        continue  # Regresar al menú principal

                elif option_tiempo.lower() == 'm':
                    continue

            elif opcion_principal == '5':
                if opcion_secundaria.lower() == 'a':
                    estado_agua = controller.obtener_posicion_servo_agua()
                    if estado_agua == "1":
                        print(f"El dispensador de agua está cerrado.")
                    elif estado_agua == "90":
                        print(f"El dispensador de agua está abierto.")
                elif opcion_secundaria.lower() == 'b':
                    estado_alimento = controller.obtener_posicion_servo_alimento()
                    if estado_alimento == "1":
                        print(f"El dispensador de alimento está cerrado.")
                    elif estado_alimento == "90":
                        print(f"El dispensador de alimento está abierto.")
                elif opcion_secundaria.lower() == 'm':
                    continue  # Regresar al menú principal

            elif opcion_principal == '6':
                if opcion_secundaria.lower() == 'a':
                    respuesta = controller.obtener_distancia_ultrasonico_agua()
                    print(respuesta)
                elif opcion_secundaria.lower() == 'b':
                    respuesta = controller.obtener_distancia_ultrasonico_alimento()
                    print(respuesta)

            elif opcion_principal == '7':
                if opcion_secundaria.lower() == 'a':
                    respuesta = controller.definir_intervalo_tiempo_agua()
                    print(respuesta)
                elif opcion_secundaria.lower() == 'b':
                    respuesta = controller.definir_intervalo_tiempo_comida()
                    print(respuesta)
    elif opcion_principal.lower() == 's':
        respuesta = controller.cerrar_todo()
        print(respuesta)
        print("Saliendo del programa. ¡Hasta luego!")
        break
    else:
        print(f"{Back.RED}Opción no válida. Intente de nuevo{Back.RESET}")

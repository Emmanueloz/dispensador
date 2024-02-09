from colorama import init, Fore, Back

# Inicializar Colorama
init(autoreset=True)

menu = f'''
=========[Dispensadores]=============================
|| {Back.GREEN}1{Back.RESET} - {Fore.CYAN}Dispensar Agua o Comida{Fore.RESET}                      ||
|| {Back.GREEN}2{Back.RESET} - {Fore.MAGENTA}Consulta Contenedores{Fore.RESET}                        ||
|| {Back.GREEN}3{Back.RESET} - {Fore.BLUE}Dispensar automatico{Fore.RESET}                      ||
|| {Back.GREEN}s{Back.RESET} - {Fore.RED}Salir{Fore.RESET}                                        ||
======================================================
'''

subMenu = f'''
||      {Back.GREEN}A.{Back.RESET}{Fore.BLUE} Agua {Fore.RESET}                     ||
||      {Back.GREEN}B.{Back.RESET}{Fore.YELLOW} Comida {Fore.RESET}                   ||
||      {Back.GREEN}M.{Back.RESET}{Fore.RED} Volver al Menú Principal {Fore.RESET} ||
'''

tiempo = f'''
{Back.RED}Advertencia: Solo se podrá insertar o enviar una petición mediante una de las siguientes opciones. No se podrá realizar todo al mismo tiempo (minuto, segundo){Back.RESET}
||      {Back.GREEN}A.{Back.RESET}{Fore.BLUE} Minuto {Fore.RESET}                     ||
||      {Back.GREEN}B.{Back.RESET}{Fore.YELLOW} Segundo {Fore.RESET}                   ||
||      {Back.GREEN}M.{Back.RESET}{Fore.RED} Volver al Menú Principal {Fore.RESET} ||
'''

while True:
    print(menu)
    opcion_principal = input(f"{Fore.GREEN}Seleccione una opción (1-3, s): ")

    if opcion_principal == '1' or opcion_principal == '2' or opcion_principal == '3':
        print(subMenu)
        opcion_secundaria = input(
            f"{Fore.GREEN}Seleccione una opción (A-B-M):{Fore.RESET}")

        if opcion_secundaria.lower() == 'm':
            continue  # Regresar al menú principal

        elif opcion_secundaria.lower() == 'a' or opcion_secundaria.lower() == 'b':
            print(tiempo)
            option_tiempo = input(
                f"{Fore.GREEN}Seleccione una opción (A-B-M):{Fore.RESET}")

            if option_tiempo.lower() == 'm':
                continue  # Regresar al menú principal

            if opcion_principal == '1':
                print(f'Abrir dispensador de {Fore.BLUE}{opcion_secundaria}{Fore.RESET} cada {Fore.BLUE}{Fore.RESET}')
            elif opcion_principal == '2':
                print(f'{Fore.MAGENTA}Consultar dispensador de {Fore.BLUE}{opcion_secundaria}{Fore.RESET} cada {Fore.BLUE}{Fore.RESET}')
            elif opcion_principal == '3':
                print(f'Consultar tiempo del dispensador de {Fore.BLUE}{opcion_secundaria}{Fore.RESET} cada {Fore.BLUE}{option_tiempo}{Fore.RESET}')

    elif opcion_principal.lower() == 's':
        print("Saliendo del programa. ¡Hasta luego!")
        break
    else:
        print(f"{Back.RED}Opción no válida. Intente de nuevo{Back.RESET}")

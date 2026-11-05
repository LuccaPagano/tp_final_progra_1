from paquete import *

tablas = []
usuarios = [[USUARIO_INICIAL, CONTRASENIA_INICIAL]]
otro_usuario = True

while otro_usuario == True:
    autenticar(usuarios)
    continuar = True

    while continuar:
        mostrar_menu()
        opcion = leer_opcion("Ingrese una opcion: ", OPCIONES_MENU)

        match opcion:
            case "a":
                print("Seleccionaste Proyectos.")
            case "b":
                opcion_tablas(tablas)
            case "c":
                print("Seleccionaste Variables.")
            case "d":
                opcion_mostrar(tablas)
            case "e":
                print("Seleccionaste Estadística.")
            case "f":
                print("Sesión finalizada.")
                continuar = False
            case _:
                print("Opción no válida.")

    otro_usuario = leer_si_no("¿Desea ingresar con otro usuario?")

print("Programa finalizado.")

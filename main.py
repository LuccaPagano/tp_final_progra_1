from paquete import *

proyectos = crear_proyectos()
usuarios = cargar_usuarios()
proyecto_seleccionado = None
otro_usuario = proyectos != None and usuarios != None

while otro_usuario == True:
    autenticar(usuarios)
    proyecto_seleccionado = None
    continuar = True

    while continuar:
        mostrar_menu()
        opcion = leer_opcion("Ingrese una opcion: ", OPCIONES_MENU)

        match opcion:
            case "a":
                proyecto_seleccionado = seleccionar_proyecto(proyectos)
                print(f"Proyecto seleccionado: {proyecto_seleccionado['nombre']}.")
            case "b":
                if proyecto_seleccionado == None:
                    print("Error: primero debe seleccionar un proyecto (opción A).")
                else:
                    opcion_tablas(proyecto_seleccionado, proyectos)
            case "c":
                if proyecto_seleccionado == None:
                    print("Error: primero debe seleccionar un proyecto (opción A).")
                else:
                    opcion_modificar(proyecto_seleccionado, proyectos)
            case "d":
                if proyecto_seleccionado == None:
                    print("Error: primero debe seleccionar un proyecto (opción A).")
                else:
                    opcion_mostrar(proyecto_seleccionado["tablas"])
            case "e":
                if proyecto_seleccionado == None:
                    print("Error: primero debe seleccionar un proyecto (opción A).")
                else:
                    opcion_estadistica(proyecto_seleccionado)
            case "f":
                print("Sesión finalizada.")
                continuar = False
            case _:
                print("Opción no válida.")

    otro_usuario = leer_si_no("¿Desea ingresar con otro usuario?")

print("Programa finalizado.")
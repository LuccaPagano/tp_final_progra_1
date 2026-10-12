from validaciones import *

continuar = "s" or "S"
usuario_registrado = "Pedro"
contrasenia_registrada = "1234"

nombre_usuario = input("Ingrese su nombre de usuario: ")

if nombre_usuario == usuario_registrado or nombre_usuario == "pedro":
    contrasenia_usuario = input("Ingrese su contraseña: ")

    while contrasenia_usuario != contrasenia_registrada:
        print("contrasenia incorrecta.")
        contrasenia_usuario = input("Ingrese su contraseña nuevamente: ")

    print(f"Bienvenido, {nombre_usuario}.")    

elif nombre_usuario != usuario_registrado:
    print("El usuario no existe. Registre sus datos.")
    usuario_registrado = input("Ingrese su nuevo nombre de usuario: ")
    contrasenia_registrada = input("Ingrese su nueva contraseña: ")

    
    print("Usuario registrado correctamente.")
    nombre_usuario = input("Inicie sesión. Nombre de usuario: ")
    contrasenia_usuario = input("Ingrese su contraseña: ")

    while nombre_usuario != usuario_registrado:
        print("Nombre de usuario incorrecto.")
        nombre_usuario = input("Inicie sesión. Nombre de usuario: ")
        contrasenia_usuario = input("Ingrese su contraseña nuevamente: ")
        
    while contrasenia_usuario != contrasenia_registrada:
        print("Contraseña incorrecta.")
        contrasenia_usuario = input("Ingrese su contraseña nuevamente: ")

    print(f"Bienvenido, {nombre_usuario}.")
    
while (continuar == "s" or continuar == "S") and ((nombre_usuario == usuario_registrado or nombre_usuario == "pedro") and contrasenia_usuario == contrasenia_registrada):

    print("=" * 75)

    print("    Menú de opciones. Ingrese la letra correspondiente a la opción deseada.")
    print("""\n                                                                                                  
    A. Proyectos: Generación y gestión de proyectos.                      
    B. Tablas: creación y modificación de tablas.                         
    C. Variables: Creación, carga y modificación de variables.           
    D. Mostrar: Mostrar por pantalla información disponible en una tabla.
    E. Estadística: Conteos o frecuencias. Máximos y mínimos.             
    Medidas de tendencia central: promedios aritméticos y geométricos.    
    Medidas de dispersión. Medidas de posición.                           
    F. Salir.                                                             
    """)
    print("=" * 75)
    opcion = input("Ingrese una opcion: ")

    match opcion:
        case "a" | "A":
            print("Seleccionaste Proyectos.")

        case "b" | "B":
            print("Seleccionaste Tablas.")
            
        case "c" | "C":
            print("Seleccionaste Variables.")

        case "d" | "D":
            print("Seleccionaste Mostrar.")

        case "e" | "E":
            print("Seleccionaste Estadística.")

        case "f" | "F":
            print("Programa finalizado.")
            continuar = "no"
        case _:
            print("Opción no válida.")


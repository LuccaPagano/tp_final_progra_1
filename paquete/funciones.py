from .validaciones import *

"""Punto b (parte 3): creación, carga secuencial/distribuida y modificación de tablas.

Solo listas y matrices:
    tabla = [nombre, columnas, denominaciones, filas]
        columnas  -> lista de nombres de columna
        denominaciones -> lista con el nombre opcional de cada fila
        filas     -> matriz con los datos
"""

COLUMNAS = ["Nombre", "Apellido", "Materia", "Nota PP", "Nota SP", "Nota final"]
IDX_NOTAS = 3
IDX_NOTA_PP = 3
IDX_NOTA_SP = 4
IDX_NOTA_FINAL = 5
NOTA_MIN = 0
NOTA_MAX = 10
MAX_LARGO = 50
MAX_FILAS = 1000

TABLA_NOMBRE = 0
TABLA_COLUMNAS = 1
TABLA_DENOMINACIONES = 2
TABLA_FILAS = 3

USUARIO_INICIAL = "Pedro"
CONTRASENIA_INICIAL = "1234"
OPCIONES_MENU = ["a", "b", "c", "d", "e", "f"]



def recortar(texto: str) -> str:
    """Quita espacios y tabulaciones al inicio y al final."""
    inicio = 0
    fin = len(texto)
    while inicio < fin and (texto[inicio] == " " or texto[inicio] == "\t"):
        inicio += 1
    while fin > inicio and (texto[fin - 1] == " " or texto[fin - 1] == "\t"):
        fin -= 1
    return texto[inicio:fin]


def pasar_minusculas(texto: str) -> str:
    '''
    Pasa a minúscula las letras A-Z de un texto (suma 32 a su código ASCII).
    recibe un string.
    retorna un string.
    '''
    i = 0
    resultado = ""

    while i < len(texto):
        if validar_mayusculas(texto[i]):
            resultado += chr(ord(texto[i]) + 32)
        else:
            resultado += texto[i]
        i += 1

    return resultado

def leer_texto(mensaje: str) -> str:
    """Pide un texto no vacío de hasta MAX_LARGO caracteres."""
    texto = recortar(input(mensaje))
    while texto == "" or len(texto) > MAX_LARGO:
        if texto == "":
            print(f"Error: el texto no puede estar vacío.")
        else:
            print(f"Error: el texto no puede superar los {MAX_LARGO} caracteres.")
        texto = recortar(input(mensaje))
    return texto


def leer_nombre(mensaje: str) -> str:
    """Pide un nombre propio (solo letras)."""
    texto = recortar(input(mensaje))
    while es_nombre_valido(texto) == False:
        print(f"Error: ingrese solo letras (sin números ni símbolos), hasta {MAX_LARGO} caracteres.")
        texto = recortar(input(mensaje))
    return texto


def sacar_ceros_izquierda(texto: str) -> str:
    '''
    Quita los ceros a la izquierda de una cadena numérica (deja al menos un carácter).
    recibe un string.
    retorna un string.
    '''
    i = 0

    while i < len(texto) - 1 and texto[i] == "0":
        i += 1

    return texto[i:]


def leer_entero_postivo(mensaje: str, minimo: int, maximo: int) -> int:
    """Pide un entero dentro de [minimo, maximo]."""
    valor = None
    while valor == None:
        texto = sacar_ceros_izquierda(recortar(input(mensaje)))
        if es_entero(texto) == False:
            print(f"Error: ingrese un número entero positivo (o 0).")
        elif len(texto) > len(str(maximo)) or int(texto) < minimo or int(texto) > maximo:
            print(f"Error: el valor debe estar entre {minimo} y {maximo}.")
        else:
            valor = int(texto)
    return valor


def leer_nota(mensaje: str) -> float:
    """Pide una nota entre NOTA_MIN y NOTA_MAX."""
    valor = None
    while valor == None:
        texto = recortar(input(mensaje))
        if es_nota(texto) == False:
            print(f"Error: ingrese un número válido (ej: 7.5).")
        elif float(texto) < NOTA_MIN or float(texto) > NOTA_MAX:
            print(f"Error: la nota debe estar entre {NOTA_MIN} y {NOTA_MAX}.")
        else:
            valor = float(texto)
    return valor


def leer_opcion(mensaje: str, opciones: list) -> str:
    """Pide una opción (en minúsculas) incluida en la lista."""
    opcion = pasar_minusculas(recortar(input(mensaje)))
    while esta_en_lista(opciones, opcion) == False:
        lista = ""
        for opcion_disponible in opciones:
            if lista == "":
                lista = opcion_disponible
            else:
                lista += ", " + opcion_disponible
        print(f"Error: opción no válida. Opciones posibles: {lista}.")
        opcion = pasar_minusculas(recortar(input(mensaje)))
    return opcion


def leer_si_no(mensaje: str) -> bool:
    """Pide s/n y devuelve True si la respuesta es s."""
    respuesta = pasar_minusculas(recortar(input(f"{mensaje} (s/n): ")))
    while respuesta != "s" and respuesta != "n":
        print(f"Error: responda 's' o 'n'.")
        respuesta = pasar_minusculas(recortar(input(f"{mensaje} (s/n): ")))
    return respuesta == "s"


def leer_dato(j: int, mensaje: str):
    """Pide el dato de la columna j: letras para Nombre/Apellido, texto para Materia, nota 0-10 para las notas."""
    if j >= IDX_NOTAS:
        valor = leer_nota(mensaje)
    elif j < 2:
        valor = leer_nombre(mensaje)
    else:
        valor = leer_texto(mensaje)
    return valor


def registrar_usuario(usuario: str, contrasenia: str) -> tuple:
    '''
    Devuelve el usuario y la contrasenia recibidos por parametro.

    Args:
    usuario(str): recibe el usuario a registrar
    contrasenia(str): recibe la contrasenia a registrar

    Returns:
    Devuelve el usuario y la contrasenia

    '''
    return usuario, contrasenia


def buscar_usuario(usuarios: list, nombre: str) -> int:
    """Devuelve la posición del usuario en la lista (sin distinguir mayúsculas) o -1 si no existe."""
    posicion = -1
    i = 0
    while i < len(usuarios) and posicion == -1:
        if validar_usuario(pasar_minusculas(nombre), pasar_minusculas(usuarios[i][0])):
            posicion = i
        i += 1
    return posicion


def registrar_nuevo_usuario(usuarios: list) -> list:
    """Pide los datos de una persona nueva, la agrega a la lista y devuelve [usuario, contraseña]."""
    print("--- REGISTRO ---")
    nuevo_usuario = recortar(input("Ingrese su nuevo nombre de usuario: "))
    while nuevo_usuario == "" or buscar_usuario(usuarios, nuevo_usuario) != -1:
        print("Nombre de usuario vacío o ya registrado.")
        nuevo_usuario = recortar(input("Ingrese otro nombre de usuario: "))
    nueva_contrasenia = input("Ingrese su nueva contraseña: ")

    datos = list(registrar_usuario(nuevo_usuario, nueva_contrasenia))
    usuarios += [datos]
    print("Usuario registrado correctamente.")
    return datos


def iniciar_sesion(usuario_registrado: str, contra_regis: str):
    '''
    Es el inicio de sesion del programa

    Args:
    usuario_registrado(str): Recibe el usuario registrado
    contra_regis(str): Recibe la contrasenia registrada

    Returns:
    No retorna nada

    '''

    nombre_usuario = input("Ingrese su nombre de usuario: ")

    while not validar_usuario(pasar_minusculas(nombre_usuario), pasar_minusculas(usuario_registrado)):
        print("Usuario incorrecto.")
        nombre_usuario = input("Ingrese nuevamente: ")

    contra_usu = input("Ingrese su contraseña: ")

    validar_contrasenia(contra_usu, contra_regis)

    print(f"Bienvenido, {nombre_usuario}.")


def autenticar(usuarios: list) -> None:
    """Una persona nueva se registra, inicia sesión y queda lista para entrar al menú."""
    datos = registrar_nuevo_usuario(usuarios)
    print("--- INICIO DE SESIÓN ---")
    iniciar_sesion(datos[0], datos[1])


def mostrar_lista_tablas(tablas: list) -> None:
    """Muestra las tablas disponibles."""
    if len(tablas) == 0:
        print(f"  (no hay tablas disponibles)")
    for i in range(len(tablas)):
        print(f"  {i + 1}. {tablas[i][TABLA_NOMBRE]} ({len(tablas[i][TABLA_FILAS])} filas)")


def rango_indices(inicio: int, fin: int) -> list:
    """Devuelve la lista de índices desde inicio hasta fin - 1."""

    indices = []
    for i in range(inicio, fin):
        indices += [i]
    return indices


def formatear_dato(dato, columna: int, es_encabezado: bool) -> str:
    """Pasa el dato a texto y, en las columnas de notas, quita el '.0' final."""

    texto = str(dato)
    if es_encabezado == False and columna >= IDX_NOTAS and len(texto) >= 2:
        if texto[len(texto) - 2] == "." and texto[len(texto) - 1] == "0":
            texto = texto[:len(texto) - 2]
    return texto


def elegir_seleccion(matriz: list) -> tuple[list, list]:
    """Muestra el menú y devuelve (filas, columnas) a mostrar como listas de índices."""

    cant_columnas = len(matriz[0])
    print("--- VISUALIZADOR DE TABLAS ---")
    print("1) Mostrar tabla COMPLETA")
    print("2) Mostrar una FILA específica")
    print("3) Mostrar una COLUMNA específica")

    opcion = leer_entero_postivo("Seleccione una opción (1, 2 o 3): ", 1, 3)

    if opcion == 1:
        filas = rango_indices(1, len(matriz))
        columnas = rango_indices(0, cant_columnas)
        print("--- TABLA COMPLETA ---")

    elif opcion == 2:
        cant_filas_datos = len(matriz) - 1
        fila_elegida = leer_entero_postivo(f"Número de fila (1-{cant_filas_datos}): ", 1, cant_filas_datos)
        filas = [fila_elegida]
        columnas = rango_indices(0, cant_columnas)
        print(f"--- FILA {fila_elegida} ---")

    else:
        for j in range(cant_columnas):
            print(f"{j + 1}) {matriz[0][j]}")
        columna_elegida = leer_entero_postivo(
            f"Número de columna (1-{cant_columnas}): ", 1, cant_columnas) - 1
        filas = rango_indices(1, len(matriz))
        columnas = [columna_elegida]
        print(f"--- COLUMNA {matriz[0][columna_elegida]} ---")

    return filas, columnas


def calcular_anchos(matriz: list, filas: list, columnas: list) -> list:
    """Calcula el ancho de cada columna visible según su texto más largo."""

    anchos = []
    for j in range(len(columnas)):
        columna = columnas[j]
        ancho = len(str(matriz[0][columna]))
        for i in range(len(filas)):
            dato = formatear_dato(matriz[filas[i]][columna], columna, False)
            if len(dato) > ancho:
                ancho = len(dato)
        anchos += [ancho]
    return anchos


def armar_borde(anchos: list) -> str:
    """Arma la línea separadora, por ejemplo +------+----+."""

    borde = "+"
    for j in range(len(anchos)):
        borde += "-" * (anchos[j] + 2) + "+"
    return borde


def armar_linea(matriz: list, fila: int, columnas: list, anchos: list) -> str:
    """Arma el texto de una fila de la matriz (la fila 0 son los encabezados)."""

    linea = "|"
    for j in range(len(columnas)):
        columna = columnas[j]
        dato = formatear_dato(matriz[fila][columna], columna, fila == 0)
        linea += " " + dato + " " * (anchos[j] - len(dato) + 1) + "|"
    return linea


def imprimir_tabla(matriz: list, filas: list, columnas: list) -> None:
    """Imprime los encabezados y las filas indicadas."""
    
    anchos = calcular_anchos(matriz, filas, columnas)
    borde = armar_borde(anchos)

    print(borde)
    print(armar_linea(matriz, 0, columnas, anchos))
    print(borde)
    for i in range(len(filas)):
        print(armar_linea(matriz, filas[i], columnas, anchos))
        print(borde)


def mostrar_tablas(matriz: list) -> None:
    """Permite mostrar una matriz completa, una fila o una columna."""
    if len(matriz) < 2:
        print("ERROR: La tabla no contiene datos suficientes para ser mostrada.")
    else:
        filas, columnas = elegir_seleccion(matriz)
        imprimir_tabla(matriz, filas, columnas)


def opcion_mostrar(tablas: list) -> None:
    """Muestra la tabla compartida si existe."""
    if len(tablas) == 0:
        print("Primero debe crear la tabla compartida.")
    else:
        matriz = [tablas[0][TABLA_COLUMNAS]] + tablas[0][TABLA_FILAS]
        mostrar_tablas(matriz)


def elegir_tabla(tablas: list) -> int:
    """Muestra las tablas y devuelve el índice elegido, o -1 si cancela/no hay."""
    elegida = -1
    mostrar_lista_tablas(tablas)
    if len(tablas) > 0:
        elegida = leer_entero_postivo("Número de tabla (0 para cancelar): ", 0, len(tablas)) - 1
    return elegida


def crear_tabla(tablas: list) -> None:
    """Crea la tabla compartida si todavía no existe."""
    if len(tablas) == 0:
        nombre = leer_texto("Nombre de la tabla compartida: ")
        tablas += [[nombre, COLUMNAS[:], [], []]]
        print(f"Tabla compartida creada con las columnas: Nombre, Apellido, Materia, Nota PP, Nota SP, Nota final.")
    else:
        print(f"Ya existe una tabla compartida. Todos los usuarios deben usarla.")


def pedir_etiqueta(usar_denominacion: bool, numero: int) -> str:
    """Pide la denominación de una fila si el usuario eligió usarla."""
    
    etiqueta = ""
    if usar_denominacion:
        etiqueta = leer_texto(f"Denominación de la fila {numero}: ")
    return etiqueta


def calcular_nota_final(nota_pp: float, nota_sp: float) -> float:
    """La nota final es el promedio de la Nota PP y la Nota SP."""
    return (nota_pp + nota_sp) / 2


def carga_secuencial(tabla: list, cantidad: int, usar_denominacion: bool) -> None:
    """Carga fila por fila: completa todas las columnas de una fila antes de pasar a la siguiente."""

    for numero in range(len(tabla[TABLA_FILAS]) + 1, len(tabla[TABLA_FILAS]) + cantidad + 1):
        print(f"--- Fila {numero} ---")

        tabla[TABLA_DENOMINACIONES] += [pedir_etiqueta(usar_denominacion, numero)]

        fila = []
        
        for j in range(IDX_NOTA_FINAL):
            fila += [leer_dato(j, f"  {tabla[TABLA_COLUMNAS][j]}: ")]
        fila += [calcular_nota_final(fila[IDX_NOTA_PP], fila[IDX_NOTA_SP])]
        tabla[TABLA_FILAS] += [fila]


def carga_distribuida(tabla: list, cantidad: int, usar_denominacion: bool) -> None:
    """Carga columna por columna: completa una columna para todas las filas nuevas antes de pasar a la siguiente."""

    inicio = len(tabla[TABLA_FILAS])

    for indice_fila in range(cantidad):
        tabla[TABLA_DENOMINACIONES] += [pedir_etiqueta(usar_denominacion, inicio + indice_fila + 1)]
        tabla[TABLA_FILAS] += [[]]

    for indice_columna in range(IDX_NOTA_FINAL):
        print(f"--- Columna {tabla[TABLA_COLUMNAS][indice_columna]} ---")

        for indice_fila in range(cantidad):
            tabla[TABLA_FILAS][inicio + indice_fila] += [leer_dato(indice_columna, f"  Fila {inicio + indice_fila + 1}: ")]

    for indice_fila in range(cantidad):
        fila = tabla[TABLA_FILAS][inicio + indice_fila]
        fila += [calcular_nota_final(fila[IDX_NOTA_PP], fila[IDX_NOTA_SP])]


def cargar_tabla(tabla: list) -> None:
    """Pide cantidad de filas y modo de carga, y carga la tabla."""
    disponibles = MAX_FILAS - len(tabla[TABLA_FILAS])

    if disponibles <= 0:
        print(f"La tabla alcanzó el máximo de filas.")
    else:
        cantidad = leer_entero_postivo(f"Cantidad de filas a cargar (1-{disponibles}): ", 1, disponibles)
        usar_denominacion = leer_si_no("¿Desea denominar las filas?")

        print(f"a) Carga secuencial (fila por fila)")
        print(f"b) Carga distribuida (columna por columna)")
        
        if leer_opcion("Modo de carga: ", ["a", "b"]) == "a":
            carga_secuencial(tabla, cantidad, usar_denominacion)
        else:
            carga_distribuida(tabla, cantidad, usar_denominacion)
        print(f"Carga finalizada.")


def modificar_dato(tabla: list) -> None:
    """Modifica un dato de la tabla."""
    if len(tabla[TABLA_FILAS]) == 0:
        print(f"La tabla no tiene filas.")
    else:
        i = leer_entero_postivo(f"Número de fila (1-{len(tabla[TABLA_FILAS])}, 0 para cancelar): ",
                        0, len(tabla[TABLA_FILAS])) - 1
        if i != -1:
            for j in range(len(tabla[TABLA_COLUMNAS])):
                print(f"  {j + 1}. {tabla[TABLA_COLUMNAS][j]}")
            j = leer_entero_postivo("Número de columna (0 para cancelar): ", 0, len(tabla[TABLA_COLUMNAS])) - 1

            if j == IDX_NOTA_FINAL:
                print(f"La Nota final se calcula automáticamente con la Nota PP y la Nota SP.")

            elif j != -1:
                print(f"Valor actual: {tabla[TABLA_FILAS][i][j]}")
                tabla[TABLA_FILAS][i][j] = leer_dato(j, f"Nuevo valor ({tabla[TABLA_COLUMNAS][j]}): ")

                if j == IDX_NOTA_PP or j == IDX_NOTA_SP:
                    fila = tabla[TABLA_FILAS][i]
                    fila[IDX_NOTA_FINAL] = calcular_nota_final(fila[IDX_NOTA_PP], fila[IDX_NOTA_SP])
                print(f"Dato modificado.")


def opcion_tablas(tablas: list) -> None:
    """Menú del punto b: gestiona una única tabla compartida entre los usuarios."""
    volver = False
    while volver == False:
        print(f"\n--- TABLA COMPARTIDA ---")
        mostrar_lista_tablas(tablas)
        print(f"a) Crear tabla compartida  b) Cargar filas  c) Modificar un dato  d) Volver")
        opcion = leer_opcion("Opción: ", ["a", "b", "c", "d"])
        if opcion == "a":
            crear_tabla(tablas)

        elif opcion == "d":
            volver = True

        elif len(tablas) == 0:
            print(f"Primero debe crear la tabla compartida.")
            
        else:
            if opcion == "b":
                cargar_tabla(tablas[0])
            else:
                modificar_dato(tablas[0])


def mostrar_menu() -> None:
    """Imprime el menú principal."""
    print("=" * 75)
    print("    Menú de opciones. Ingrese la letra correspondiente a la opción deseada.")
    print("""
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

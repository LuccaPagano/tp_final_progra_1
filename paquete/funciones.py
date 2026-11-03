"""Punto b (parte 3): creación, carga secuencial/distribuida y modificación de tablas.

Solo listas y matrices:
    tabla = [nombre, columnas, denominaciones, filas]
        columnas  -> lista de nombres de columna
        denominaciones -> lista con el nombre opcional de cada fila
        filas     -> matriz con los datos
"""

COLUMNAS = ["Nombre", "Apellido", "Materia", "Nota PP", "Nota SP", "Nota final"]
IDX_NOTAS = 3
NOTA_MIN = 0
NOTA_MAX = 10
MAX_LARGO = 50
MAX_FILAS = 1000

T_NOMBRE = 0
T_COLUMNAS = 1
T_DENOMINACIONES = 2
T_FILAS = 3


# ------------------------------------------------------------- validaciones
def recortar(texto: str) -> str:
    """Quita espacios y tabulaciones al inicio y al final."""
    inicio = 0
    fin = len(texto)
    while inicio < fin and (texto[inicio] == " " or texto[inicio] == "\t"):
        inicio += 1
    while fin > inicio and (texto[fin - 1] == " " or texto[fin - 1] == "\t"):
        fin -= 1
    return texto[inicio:fin]


def validar_numero(cadena: str) -> bool:
    '''
    Valida que una cadena de caracteres esté compuesta por números (ASCII 48-57).
    recibe un string.
    retorna un bool.
    '''
    i = 0
    es_numero = True

    while i < len(cadena) and es_numero:
        if ord(cadena[i]) < 48 or ord(cadena[i]) > 57:
            es_numero = False
        i += 1

    return es_numero


def validar_mayusculas(cadena: str) -> bool:
    '''
    Valida que una cadena de caracteres esté compuesta por letras mayúsculas A-Z (ASCII 65-90).
    recibe un string.
    retorna un bool.
    '''
    i = 0
    son_mayusculas = True

    while i < len(cadena) and son_mayusculas:
        if ord(cadena[i]) < 65 or ord(cadena[i]) > 90:
            son_mayusculas = False
        i += 1

    return son_mayusculas


def validar_minusculas(cadena: str) -> bool:
    '''
    Valida que una cadena de caracteres esté compuesta por letras minúsculas a-z (ASCII 97-122).
    recibe un string.
    retorna un bool.
    '''
    i = 0
    son_minusculas = True

    while i < len(cadena) and son_minusculas:
        if ord(cadena[i]) < 97 or ord(cadena[i]) > 122:
            son_minusculas = False
        i += 1

    return son_minusculas


def validar_acentuadas(cadena: str) -> bool:
    '''
    Valida que una cadena de caracteres esté compuesta por letras acentuadas, ñ o ü
    (códigos 192-255, excluyendo × (215) y ÷ (247)).
    recibe un string.
    retorna un bool.
    '''
    i = 0
    son_acentuadas = True

    while i < len(cadena) and son_acentuadas:
        if ord(cadena[i]) < 192 or ord(cadena[i]) > 255 or ord(cadena[i]) == 215 or ord(cadena[i]) == 247:
            son_acentuadas = False
        i += 1

    return son_acentuadas


def a_minusculas(texto: str) -> str:
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


def es_entero(texto: str) -> bool:
    """True si el texto es un entero sin signo."""
    return len(texto) > 0 and validar_numero(texto)


def es_nota(texto: str) -> bool:
    """True si el texto es un número no negativo con a lo sumo un punto decimal."""
    puntos = 0
    posicion = 0
    for i in range(len(texto)):
        if texto[i] == ".":
            puntos += 1
            posicion = i
    if puntos > 1:
        resultado = False
    elif puntos == 0:
        resultado = len(texto) > 0 and validar_numero(texto)
    else:
        entero = texto[:posicion] + texto[posicion + 1:]
        resultado = len(entero) > 0 and validar_numero(entero)
    return resultado


def es_nombre_valido(texto: str) -> bool:
    '''
    Valida que un texto no vacío esté compuesto solo por letras (mayúsculas, minúsculas o
    acentuadas), espacios, guiones o apóstrofes.
    recibe un string.
    retorna un bool.
    '''
    i = 0
    es_valido = len(texto) > 0 and len(texto) <= MAX_LARGO

    while i < len(texto) and es_valido:
        if (validar_mayusculas(texto[i]) or validar_minusculas(texto[i])
                or validar_acentuadas(texto[i]) or texto[i] == " " or texto[i] == "-"
                or texto[i] == "'"):
            i += 1
        else:
            es_valido = False

    return es_valido


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


def sin_ceros_izquierda(texto: str) -> str:
    '''
    Quita los ceros a la izquierda de una cadena numérica (deja al menos un carácter).
    recibe un string.
    retorna un string.
    '''
    i = 0

    while i < len(texto) - 1 and texto[i] == "0":
        i += 1

    return texto[i:]


def leer_entero(mensaje: str, minimo: int, maximo: int) -> int:
    """Pide un entero dentro de [minimo, maximo]."""
    valor = None
    while valor == None:
        texto = sin_ceros_izquierda(recortar(input(mensaje)))
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


def esta_en_lista(lista: list, elemento: str) -> bool:
    '''
    Indica si un elemento se encuentra en una lista.
    recibe una lista y un string.
    retorna un bool.
    '''
    i = 0
    encontrado = False

    while i < len(lista) and encontrado == False:
        if lista[i] == elemento:
            encontrado = True
        i += 1

    return encontrado


def leer_opcion(mensaje: str, opciones: list) -> str:
    """Pide una opción (en minúsculas) incluida en la lista."""
    opcion = a_minusculas(recortar(input(mensaje)))
    while esta_en_lista(opciones, opcion) == False:
        lista = ""
        for o in opciones:
            lista += (", " if lista != "" else "") + o
        print(f"Error: opción no válida. Opciones posibles: {lista}.")
        opcion = a_minusculas(recortar(input(mensaje)))
    return opcion


def leer_si_no(mensaje: str) -> bool:
    """Pide s/n y devuelve True si la respuesta es s."""
    respuesta = a_minusculas(recortar(input(f"{mensaje} (s/n): ")))
    while respuesta != "s" and respuesta != "n":
        print(f"Error: responda 's' o 'n'.")
        respuesta = a_minusculas(recortar(input(f"{mensaje} (s/n): ")))
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


# ------------------------------------------------------------------- tablas
def mostrar_tablas(tablas: list) -> None:
    """Muestra las tablas disponibles."""
    if len(tablas) == 0:
        print(f"  (no hay tablas disponibles)")
    for i in range(len(tablas)):
        print(f"  {i + 1}. {tablas[i][T_NOMBRE]} ({len(tablas[i][T_FILAS])} filas)")


def elegir_tabla(tablas: list) -> int:
    """Muestra las tablas y devuelve el índice elegido, o -1 si cancela/no hay."""
    elegida = -1
    mostrar_tablas(tablas)
    if len(tablas) > 0:
        elegida = leer_entero("Número de tabla (0 para cancelar): ", 0, len(tablas)) - 1
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


def carga_secuencial(tabla: list, cantidad: int, usar_denominacion: bool) -> None:
    """Carga fila por fila: completa todas las columnas de una fila antes de pasar a la siguiente."""
    for _ in range(cantidad):
        numero = len(tabla[T_FILAS]) + 1
        print(f"--- Fila {numero} ---")
        tabla[T_DENOMINACIONES] += [pedir_etiqueta(usar_denominacion, numero)]
        fila = []
        for j in range(len(tabla[T_COLUMNAS])):
            fila += [leer_dato(j, f"  {tabla[T_COLUMNAS][j]}: ")]
        tabla[T_FILAS] += [fila]


def carga_distribuida(tabla: list, cantidad: int, usar_denominacion: bool) -> None:
    """Carga columna por columna: completa una columna para todas las filas nuevas antes de pasar a la siguiente."""
    inicio = len(tabla[T_FILAS])
    for k in range(cantidad):
        tabla[T_DENOMINACIONES] += [pedir_etiqueta(usar_denominacion, inicio + k + 1)]
        tabla[T_FILAS] += [[]]
    for j in range(len(tabla[T_COLUMNAS])):
        print(f"--- Columna {tabla[T_COLUMNAS][j]} ---")
        for k in range(cantidad):
            tabla[T_FILAS][inicio + k] += [leer_dato(j, f"  Fila {inicio + k + 1}: ")]


def cargar_tabla(tabla: list) -> None:
    """Pide cantidad de filas y modo de carga, y carga la tabla."""
    disponibles = MAX_FILAS - len(tabla[T_FILAS])

    if disponibles <= 0:
        print(f"La tabla alcanzó el máximo de filas.")
    else:
        cantidad = leer_entero(f"Cantidad de filas a cargar (1-{disponibles}): ", 1, disponibles)
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
    if len(tabla[T_FILAS]) == 0:
        print(f"La tabla no tiene filas.")
    else:
        i = leer_entero(f"Número de fila (1-{len(tabla[T_FILAS])}, 0 para cancelar): ",
                        0, len(tabla[T_FILAS])) - 1
        if i != -1:
            for j in range(len(tabla[T_COLUMNAS])):
                print(f"  {j + 1}. {tabla[T_COLUMNAS][j]}")
            j = leer_entero("Número de columna (0 para cancelar): ", 0, len(tabla[T_COLUMNAS])) - 1
            if j != -1:
                print(f"Valor actual: {tabla[T_FILAS][i][j]}")
                tabla[T_FILAS][i][j] = leer_dato(j, f"Nuevo valor ({tabla[T_COLUMNAS][j]}): ")
                print(f"Dato modificado.")


def menu_tablas(tablas: list) -> None:
    """Menú del punto b: gestiona una única tabla compartida entre los usuarios."""
    volver = False
    while volver == False:
        print(f"\n--- TABLA COMPARTIDA ---")
        mostrar_tablas(tablas)
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


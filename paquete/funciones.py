from .validaciones import * 
from .archivos_csv import escribir_registro, leer_registros, ruta_archivo


COLUMNAS = ["Nombre", "Apellido", "Materia", "Nota PP", "Nota SP", "Nota final"]  
IDX_NOTAS = 3  

NOTA_MIN = 0  
NOTA_MAX = 10  
MAX_LARGO = 50  
MAX_FILAS = 1000  
OPCIONES_MENU = ["a", "b", "c", "d", "e", "f"]  




def recortar(texto: str) -> str:  
    """Elimina espacios/tabulaciones del inicio y final.

    Args:
        texto (str): Texto que se va a procesar.

    Returns:
        str: Texto sin espacios ni tabulaciones al principio o al final.
    """
    inicio = 0
    fin = len(texto)
    while inicio < fin and (texto[inicio] == " " or texto[inicio] == "\t"):
        inicio += 1
    while fin > inicio and (texto[fin - 1] == " " or texto[fin - 1] == "\t"):
        fin -= 1
    return texto[inicio:fin]


def pasar_minusculas(texto: str) -> str:  
    """Convierte A-Z a a-z (suma 32 a ASCII).

    Args:
        texto (str): Texto que se va a procesar.

    Returns:
        str: Texto con las letras mayúsculas ASCII convertidas a minúsculas.
    """
    i = 0
    resultado = ""
    while i < len(texto):
        if validar_mayusculas(texto[i]):
            resultado += chr(ord(texto[i]) + 32)

        else:
            resultado += texto[i]
        i += 1
    return resultado


def pasar_mayuscula_primera(texto: str) -> str:  
    """Convierte la primera letra a mayúscula (resta 32 de ASCII).

    Args:
        texto (str): Texto que se va a procesar.

    Returns:
        str: Texto con su primera letra convertida a mayúscula cuando corresponde.
    """
    
    resultado = ""
    if len(texto) > 0:
        primera_letra = texto[0]
        if validar_minusculas(primera_letra):
            primera_letra = chr(ord(primera_letra) - 32)
        resultado = primera_letra + texto[1:]
    return resultado


def reemplazar_caracteres(texto: str, caracteres_viejo: str, caracteres_nuevo: str) -> str:  
    """Reemplaza caracteres especificados por otros.

    Args:
        texto (str): Texto que se va a procesar.
        caracteres_viejo (str): Caracteres que se buscan para reemplazar.
        caracteres_nuevo (str): Caracteres que sustituyen a los anteriores.

    Returns:
        str: Texto resultante de reemplazar los caracteres indicados.
    """
    i = 0
    resultado = ""
    while i < len(texto):
        encontrado = False
        j = 0
        while j < len(caracteres_viejo):
            if texto[i] == caracteres_viejo[j]:
                resultado += caracteres_nuevo[j]
                encontrado = True
                break
            j = j + 1
        if encontrado == False:
            resultado += texto[i]
        i = i + 1
    return resultado


def leer_texto(mensaje: str) -> str:  
    """Lee texto no vacío de hasta MAX_LARGO caracteres.

    Args:
        mensaje (str): Mensaje que se muestra para solicitar el dato.

    Returns:
        str: Texto ingresado que cumple las validaciones.
    """
    texto = recortar(input(mensaje))
    while texto == "" or len(texto) > MAX_LARGO:
        if texto == "":
            print(f"Error: el texto no puede estar vacío.")
        else:
            print(f"Error: el texto no puede superar los {MAX_LARGO} caracteres.")
        texto = recortar(input(mensaje))
    return texto


def leer_nombre(mensaje: str) -> str:
    """Lee un nombre válido, admitiendo espacios, guiones y apóstrofos.

    Args:
        mensaje (str): Mensaje que se muestra para solicitar el dato.

    Returns:
        str: Nombre ingresado que cumple las validaciones.
    """
    nombre = leer_texto(mensaje)
    while es_nombre_valido(nombre) == False:
        print("Error: ingrese solo letras.")
        nombre = leer_texto(mensaje)
    return nombre


def leer_entero_postivo(mensaje: str, minimo: int, maximo: int) -> int:  
    """Lee entero entre minimo y maximo (inclusive).

    Args:
        mensaje (str): Mensaje que se muestra para solicitar el dato.
        minimo (int): Límite mínimo admitido.
        maximo (int): Límite máximo admitido.

    Returns:
        int: Entero ingresado dentro de los límites indicados.
    """
    entero = None
    while entero == None:
        entrada = input(mensaje)
        if es_entero(entrada):
            valor = int(entrada)
            if validar_rango(valor, minimo, maximo):
                entero = valor
            else:
                print(f"Error: ingrese un valor entre {minimo} y {maximo}.")
        else:
            print("Error: ingrese un número entero válido.")
    return entero


def leer_decimal(mensaje: str) -> float: 
    """Lee un número decimal no negativo.

    Args:
        mensaje (str): Mensaje que se muestra para solicitar el dato.

    Returns:
        float: Número decimal ingresado y validado.
    """
    decimal = None
    while decimal is None:
        entrada = input(mensaje)
        if es_nota(entrada):
            decimal = float(entrada)
        else:
            print("Error: ingrese un número válido.")
    return decimal


def leer_nota(mensaje: str) -> float:  
    """Lee nota entre NOTA_MIN y NOTA_MAX (0-10).

    Args:
        mensaje (str): Mensaje que se muestra para solicitar el dato.

    Returns:
        float: Nota ingresada y validada.
    """
    nota = None
    while nota is None:
        entrada = input(mensaje)
        if es_nota(entrada):
            valor = float(entrada)
            if validar_rango(valor, NOTA_MIN, NOTA_MAX):
                nota = valor
            else:
                print(f"Error: la nota debe estar entre {NOTA_MIN} y {NOTA_MAX}.")
        else:
            print("Error: ingrese una nota válida.")
    return nota


def leer_opcion(mensaje: str, opciones: list) -> str:  
    """Lee opción válida de una lista.

    Args:
        mensaje (str): Mensaje que se muestra para solicitar el dato.
        opciones (list): Opciones que se consideran válidas.

    Returns:
        str: Opción válida ingresada por el usuario.
    """
    
    opcion_valida = False
    
    while opcion_valida == False:
        
        opcion = pasar_minusculas(recortar(input(mensaje)))
        
        opcion_valida = esta_en_lista(opciones, opcion)
        if opcion_valida == False:
            print(f"Error: opciones válidas son {opciones}.")
    return opcion


def leer_dato_por_tipo(tipo: str, mensaje: str, rango: list = None):  
    """Lee dato según tipo (str, int, float) y rango opcional.

    Args:
        tipo (str): Tipo de dato que se solicita o procesa.
        mensaje (str): Mensaje que se muestra para solicitar el dato.
        rango (list): Límites permitidos para el dato, si están definidos. Por defecto: None.

    Returns:
        Valor ingresado convertido al tipo solicitado.
    """
    if tipo == "str":
        valor = leer_texto(mensaje)
    elif tipo == "int":
        if rango:
            valor = leer_entero_postivo(mensaje, int(rango[0]), int(rango[1]))
        else:
            valor = leer_entero_postivo(mensaje, 0, 999999)
    elif tipo == "float":
        valor = leer_decimal(mensaje)
        if rango:
            while not validar_rango(valor, rango[0], rango[1]):
                print(f"Error: ingrese un valor entre {rango[0]} y {rango[1]}.")
                valor = leer_decimal(mensaje)
    else:
        valor = leer_texto(mensaje)
    return valor


def leer_si_no(mensaje: str) -> bool:  
    """Lee respuesta sí/no (s/n) y retorna True/False.

    Args:
        mensaje (str): Mensaje que se muestra para solicitar el dato.

    Returns:
        bool: True si la respuesta es afirmativa; False si es negativa.
    """

    opcion = leer_opcion(mensaje + " (s/n): ", ["s", "n"])
    
    return opcion == "s"


def leer_dato(nombre_columna: str, mensaje: str):  
    """Lee dato según tipo esperado de la columna por su nombre.

    Args:
        nombre_columna (str): Nombre de la columna a la que corresponde el dato.
        mensaje (str): Mensaje que se muestra para solicitar el dato.

    Returns:
        Dato ingresado para la columna indicada.
    """

    columnas_nota = ["Nota PP", "Nota SP", "Nota final"]  
    es_columna_nota = esta_en_lista(columnas_nota, nombre_columna)
    
    if es_columna_nota:
        dato = leer_nota(mensaje)
    else:
        dato = leer_texto(mensaje)
    return dato


def guardar_tabla(tabla: dict, nombre_archivo: str) -> None:  
    """Guarda tabla a CSV con encabezados, datos y denominaciones.

    Args:
        tabla (dict): Tabla sobre la que se realiza la operación.
        nombre_archivo (str): Nombre del archivo CSV.

    Returns:
        No devuelve un valor.
    """

    archivo = open(ruta_archivo(nombre_archivo), "w", encoding="utf-8", newline="")

    escribir_registro(archivo, tabla["columnas"] + ["Denominación"])
    
    i = 0
    while i < len(tabla["filas"]):
        escribir_registro(archivo, tabla["filas"][i] + [tabla["denominaciones"][i]])
        i = i + 1
    
    archivo.close()


def leer_tabla(nombre: str, nombre_archivo: str) -> dict | None:  
    """Lee tabla de CSV. Convierte columnas de notas (3+) a float.

    Args:
        nombre (str): Nombre que se utiliza en la operación.
        nombre_archivo (str): Nombre del archivo CSV.

    Returns:
        dict | None: Tabla leída del CSV, o None si el CSV no es válido.
    """
    tabla = {"nombre": nombre, "columnas": COLUMNAS[:], "denominaciones": [], "filas": []}
    
    archivo = open(ruta_archivo(nombre_archivo), "r", encoding="utf-8", newline="")    
    registros = leer_registros(archivo)
    archivo.close()
    
    if registros == None:
        tabla = None
        registros = []
    for registro in registros[1:]:
        if len(registro) > len(COLUMNAS):
            fila = []
            denominacion = ""
            
            i = 0
            while i < len(COLUMNAS):
                if i >= 3:
                    fila += [float(registro[i])]
                else:
                    fila += [registro[i]]
                i = i + 1
            
            if len(registro) > len(COLUMNAS):
                denominacion = registro[len(COLUMNAS)]
            
            tabla["denominaciones"] += [denominacion]
            tabla["filas"] += [fila]
    
    return tabla


def pedir_etiqueta(usar_denominacion: bool, numero: int) -> str: 
    """Pide denominación (etiqueta) de fila si usuario lo desea.

    Args:
        usar_denominacion (bool): Indica si se debe solicitar una denominación para la fila.
        numero (int): Número que se utiliza en la operación.

    Returns:
        str: Denominación ingresada, o una cadena vacía si no se solicita.
    """
    etiqueta = ""
    if usar_denominacion:
        etiqueta = leer_texto(f"Denominación de la fila {numero}: ")
    return etiqueta


def calcular_nota_final(nota_pp: float, nota_sp: float) -> float:  
    """Calcula nota final como promedio: (PP + SP) / 2.

    Args:
        nota_pp (float): Nota del primer parcial.
        nota_sp (float): Nota del segundo parcial.

    Returns:
        float: Promedio de las dos notas de parcial.
    """

    return (nota_pp + nota_sp) / 2

def rango_indices(inicio: int, fin: int) -> list:  
    """Retorna lista de índices: [inicio, inicio+1, ..., fin-1].

    Args:
        inicio (int): Límite inicial del intervalo.
        fin (int): Límite final del intervalo.

    Returns:
        list: Lista de índices desde inicio hasta fin, sin incluir fin.
    """

    resultado = []
    i = inicio

    while i < fin:
        resultado += [i]
        i = i + 1

    return resultado

def mostrar_menu() -> None:  
    """Imprime menú principal con opciones A-F.

    Returns:
        No devuelve un valor.
    """

    print("=" * 75)
    print("    Menú de opciones. Ingrese la letra correspondiente a la opción deseada.")
    print("""
    A. Proyectos: Generación y gestión de proyectos.
    B. Tablas: Crear, cargar y modificar tablas.
    C. Variables: Crear, cargar y modificar filas o columnas.
    D. Mostrar: Mostrar por pantalla información disponible en una tabla.
    E. Estadística: Conteos o frecuencias. Máximos y mínimos.
    Medidas de tendencia central: promedios aritméticos y geométricos.
    Medidas de dispersión. Medidas de posición.
    F. Salir.
    """)
    print("=" * 75)

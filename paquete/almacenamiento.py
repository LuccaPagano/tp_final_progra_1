"""Lectura y guardado de proyectos y tablas en archivos CSV."""

from .archivos_csv import escribir_registro, leer_registros, ruta_archivo

from .funciones import guardar_tabla
from .validaciones import es_entero, es_nota, esta_en_lista

ARCHIVO_PROYECTOS = "proyectos_totales.csv"


def es_decimal_guardado(texto: str) -> bool:
    """Indica si el texto representa un decimal, incluso en notación científica.

    Args:
        texto (str): Texto que se va a procesar.

    Returns:
        bool: True si el texto representa un decimal válido; False en caso contrario.
    """
    posicion = 0
    while posicion < len(texto) and texto[posicion] != "e" and texto[posicion] != "E":
        posicion += 1
    if posicion == len(texto):
        resultado = es_nota(texto)
    else:
        mantisa = texto[:posicion]
        exponente = texto[posicion + 1:]
        if len(exponente) > 0 and (exponente[0] == "+" or exponente[0] == "-"):
            exponente = exponente[1:]
        resultado = es_nota(mantisa) and es_entero(exponente)
    return resultado


def guardar_catalogo(proyectos: dict) -> None:
    """Guarda los proyectos y las tablas que no usan un archivo propio.

    Args:
        proyectos (dict): Diccionario de proyectos disponibles.

    Returns:
        No devuelve un valor.
    """
    archivo = open(ruta_archivo(ARCHIVO_PROYECTOS), "w", encoding="utf-8", newline="")
    escribir_registro(archivo, ["Registro", "Proyecto", "Datos"])

    primero = True
    for clave in proyectos:
        if primero == False:
            escribir_registro(archivo, [])
        primero = False
        proyecto = proyectos[clave]
        escribir_registro(archivo, ["proyecto", clave, proyecto["nombre"], proyecto["archivo"]])
        i = 0
        while i < len(proyecto["tablas"]):
            tabla = proyecto["tablas"][i]
            escribir_registro(archivo, ["tabla", clave, i, tabla["nombre"], tabla["archivo"], tabla["es_notas"]])
            j = 0
            while j < len(tabla["columnas"]):
                rango = tabla["rangos"][j]
                minimo = ""
                maximo = ""
                if rango != None:
                    minimo = rango[0]
                    maximo = rango[1]
                escribir_registro(archivo, ["columna", clave, i, tabla["columnas"][j],
                                        tabla["tipos_datos"][j], minimo, maximo])
                j += 1
            if tabla["archivo"] == "":
                j = 0
                while j < len(tabla["filas"]):
                    registro = ["fila", clave, i, tabla["denominaciones"][j]]
                    registro += tabla["filas"][j]
                    escribir_registro(archivo, registro)
                    j += 1
            i += 1
    archivo.close()


def guardar_cambios_archivos(tabla: dict, proyectos: dict) -> None:
    """Guarda la tabla base en su CSV y las demás en el catálogo.

    Args:
        tabla (dict): Tabla sobre la que se realiza la operación.
        proyectos (dict): Diccionario de proyectos disponibles.

    Returns:
        No devuelve un valor.
    """
    if tabla["archivo"] != "":
        guardar_tabla(tabla, tabla["archivo"])
    guardar_catalogo(proyectos)


def convertir_fila(valores: list, tipos: list) -> list | None:
    """Convierte una fila según los tipos declarados, o devuelve None si es inválida.

    Args:
        valores (list): Valores que se van a procesar.
        tipos (list): Tipos de los valores, en el mismo orden que estos.

    Returns:
        list | None: Fila con los valores convertidos, o None si no son válidos.
    """
    fila = []
    valido = True
    if len(valores) != len(tipos):
        print("Error: la cantidad de valores no coincide con las columnas.")
        valido = False
    i = 0
    while i < len(tipos) and valido:
        valor = valores[i]
        if valor != "":
            if tipos[i] == "int":
                if es_entero(valor) == False:
                    print(f"Error: '{valor}' no es un número entero válido.")
                    valido = False
                else:
                    valor = int(valor)
            elif tipos[i] == "float":
                if es_decimal_guardado(valor) == False:
                    print(f"Error: '{valor}' no es un número decimal válido.")
                    valido = False
                else:
                    valor = float(valor)
            elif tipos[i] != "str":
                print(f"Error: tipo de dato desconocido: {tipos[i]}")
                valido = False
        if valido:
            fila += [valor]
        i += 1
    if valido == False:
        fila = None
    return fila


def leer_tabla_archivo(tabla: dict) -> bool:
    """Carga las filas del archivo de una tabla y valida su estructura.

    Args:
        tabla (dict): Tabla sobre la que se realiza la operación.

    Returns:
        bool: True si la tabla se cargó correctamente; False si contiene errores.
    """
    archivo = open(ruta_archivo(tabla["archivo"]), "a", encoding="utf-8")
    archivo.close()
    archivo = open(ruta_archivo(tabla["archivo"]), "r", encoding="utf-8", newline="")
    registros = leer_registros(archivo)
    archivo.close()
    valido = registros != None
    if valido:
        if len(registros) == 0 or registros[0] != tabla["columnas"] + ["Denominación"]:
            print(f"Error: las columnas de {tabla['archivo']} no coinciden con el catálogo.")
            valido = False
        i = 1
        while i < len(registros) and valido:
            registro = registros[i]
            if len(registro) != len(registros[0]):
                print(f"Error: una fila de {tabla['archivo']} tiene una cantidad incorrecta de valores.")
                valido = False
            else:
                fila = convertir_fila(registro[:-1], tabla["tipos_datos"])
                if fila == None:
                    valido = False
                else:
                    tabla["filas"] += [fila]
                    tabla["denominaciones"] += [registro[-1]]
            i += 1
    return valido


def procesar_registro_catalogo(registro: list, proyectos: dict) -> bool:
    """Incorpora un registro válido del catálogo a los proyectos.

    Args:
        registro (list): Campos del registro que se va a procesar.
        proyectos (dict): Diccionario de proyectos disponibles.

    Returns:
        bool: True si el registro es válido; False si no se pudo procesar.
    """
    valido = True
    if len(registro) < 2:
        print(f"Error: registro incompleto en {ARCHIVO_PROYECTOS}.")
        valido = False
    else:
        tipo_registro = registro[0]
        clave = registro[1]
        if tipo_registro == "proyecto":
            if len(registro) != 4 or clave in proyectos:
                print(f"Error: proyecto inválido o repetido en {ARCHIVO_PROYECTOS}.")
                valido = False
            else:
                proyectos[clave] = {
                    "nombre": registro[2], "archivo": registro[3], "tablas": []
                }
        elif clave not in proyectos or len(registro) < 3 or es_entero(registro[2]) == False:
            print(f"Error: proyecto o tabla inválidos en {ARCHIVO_PROYECTOS}.")
            valido = False
        elif tipo_registro == "tabla" and len(registro) == 6 and int(registro[2]) == len(proyectos[clave]["tablas"]):
            tabla = {
                "nombre": registro[3], "archivo": registro[4],
                "es_notas": registro[5] == "True", "columnas": [],
                "tipos_datos": [], "rangos": [], "filas": [], "denominaciones": []
            }
            proyectos[clave]["tablas"] += [tabla]
        elif (tipo_registro == "columna" and len(registro) == 7
            and int(registro[2]) < len(proyectos[clave]["tablas"])
            and esta_en_lista(["str", "int", "float"], registro[4])):
            tabla = proyectos[clave]["tablas"][int(registro[2])]
            rango = None
            if registro[5] != "":
                if registro[4] == "int":
                    if es_entero(registro[5]) == False or es_entero(registro[6]) == False:
                        print(f"Error: rango entero inválido en {ARCHIVO_PROYECTOS}.")
                        valido = False
                    else:
                        rango = [int(registro[5]), int(registro[6])]
                elif registro[4] == "float" and es_decimal_guardado(registro[5]) and es_decimal_guardado(registro[6]):
                    rango = [float(registro[5]), float(registro[6])]
                else:
                    print(f"Error: rango decimal inválido en {ARCHIVO_PROYECTOS}.")
                    valido = False
            if valido:
                tabla["columnas"] += [registro[3]]
                tabla["tipos_datos"] += [registro[4]]
                tabla["rangos"] += [rango]
        elif tipo_registro == "fila" and len(registro) >= 4 and int(registro[2]) < len(proyectos[clave]["tablas"]):
            tabla = proyectos[clave]["tablas"][int(registro[2])]
            fila = convertir_fila(registro[4:], tabla["tipos_datos"])
            if fila == None:
                valido = False
            else:
                tabla["denominaciones"] += [registro[3]]
                tabla["filas"] += [fila]
        else:
            print(f"Error: registro desconocido en {ARCHIVO_PROYECTOS}: {tipo_registro}")
            valido = False
    return valido


def cargar_catalogo() -> dict | None:
    """Recupera cada tabla dentro del proyecto al que pertenece.

    Returns:
        dict | None: Proyectos cargados, o None si el catálogo contiene errores.
    """
    archivo = open(ruta_archivo(ARCHIVO_PROYECTOS), "a", encoding="utf-8")
    archivo.close()
    archivo = open(ruta_archivo(ARCHIVO_PROYECTOS), "r", encoding="utf-8", newline="")
    registros = leer_registros(archivo)
    archivo.close()
    proyectos = {}
    valido = registros != None
    if registros != None and len(registros) > 0:
        if registros[0] != ["Registro", "Proyecto", "Datos"]:
            print(f"Error: encabezado incorrecto en {ARCHIVO_PROYECTOS}.")
            valido = False
        i = 1
        while i < len(registros) and valido:
            if len(registros[i]) > 0:
                valido = procesar_registro_catalogo(registros[i], proyectos)
            i += 1
        if valido and len(proyectos) == 0:
            print(f"Error: no hay proyectos en {ARCHIVO_PROYECTOS}.")
            valido = False
    if valido:
        for clave in proyectos:
            i = 0
            while i < len(proyectos[clave]["tablas"]) and valido:
                tabla = proyectos[clave]["tablas"][i]
                if tabla["archivo"] != "":
                    valido = leer_tabla_archivo(tabla)
                i += 1
    if valido == False:
        proyectos = None
    return proyectos

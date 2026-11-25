"""Lectura y escritura de registros CSV mediante archivos de texto."""


def ruta_archivo(nombre: str) -> str:
    """Construye la ruta relativa de un archivo de datos.

    Args:
        nombre (str): Nombre del archivo, incluida su extensión.

    Returns:
        str: Ruta dentro de la carpeta archivos.
    """
    return "archivos\\" + nombre


def escribir_registro(archivo, valores: list) -> None:
    """Escribe una fila CSV, escapando comillas y campos especiales.

    Args:
        archivo: Archivo de texto abierto para escritura.
        valores (list): Campos de la fila que se desea escribir.

    Returns:
        None: Escribe el registro directamente en el archivo.
    """
    linea = ""
    i = 0
    while i < len(valores):
        if i > 0:
            linea += ","
        texto = ""
        if valores[i] != None:
            texto = str(valores[i])
        campo = ""
        necesita_comillas = len(valores) == 1 and texto == ""
        j = 0
        while j < len(texto):
            caracter = texto[j]
            if caracter == '"':
                campo += '""'
                necesita_comillas = True
            else:
                campo += caracter
                if caracter == "," or caracter == "\r" or caracter == "\n":
                    necesita_comillas = True
            j += 1
        if necesita_comillas:
            linea += '"' + campo + '"'
        else:
            linea += campo
        i += 1
    archivo.write(linea + "\r\n")


def leer_registros(archivo) -> list | None:
    """Lee registros CSV respetando comillas y saltos de línea dentro de campos.

    Args:
        archivo: Archivo de texto abierto para lectura.

    Returns:
        list | None: Lista de registros, o None si una comilla queda sin cerrar.
    """
    texto = archivo.read()
    registros = []
    registro = []
    campo = ""
    entre_comillas = False
    inicio_campo = True
    hay_datos = False
    i = 0
    while i < len(texto):
        caracter = texto[i]
        if entre_comillas:
            if caracter == '"':
                if i + 1 < len(texto) and texto[i + 1] == '"':
                    campo += '"'
                    i += 1
                else:
                    entre_comillas = False
            else:
                campo += caracter
        elif caracter == '"' and inicio_campo:
            entre_comillas = True
            inicio_campo = False
            hay_datos = True
        elif caracter == ",":
            registro += [campo]
            campo = ""
            inicio_campo = True
            hay_datos = True
        elif caracter == "\r" or caracter == "\n":
            if hay_datos:
                registro += [campo]
            registros += [registro]
            registro = []
            campo = ""
            inicio_campo = True
            hay_datos = False
            if caracter == "\r" and i + 1 < len(texto) and texto[i + 1] == "\n":
                i += 1
        else:
            campo += caracter
            inicio_campo = False
            hay_datos = True
        i += 1
    if entre_comillas:
        print("Error: el archivo CSV contiene un campo con comillas sin cerrar.")
        registros = None
    elif hay_datos:
        registro += [campo]
        registros += [registro]
    return registros

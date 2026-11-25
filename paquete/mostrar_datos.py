from .funciones import leer_entero_postivo, rango_indices, IDX_NOTAS  # Importa leer_entero_postivo (leer entero), rango_indices (crear lista de índices), e IDX_NOTAS (índice donde comienzan notas)


def opcion_mostrar(tablas: list) -> None:  
    """Muestra la tabla del proyecto seleccionado.

    Args:
        tablas (list): Lista de tablas del proyecto.

    Returns:
        No devuelve un valor.
    """
    indice = 0
    if len(tablas) > 1:
        print("--- TABLAS DISPONIBLES ---")
        i = 0
        while i < len(tablas):
            print(f"{i + 1}) {tablas[i]['nombre']}")
            i += 1
        indice = leer_entero_postivo("Seleccione una tabla: ", 1, len(tablas)) - 1
    matriz = [tablas[indice]["columnas"]] + tablas[indice]["filas"]
    mostrar_tablas(matriz, tablas[indice]["denominaciones"])


def mostrar_filas_disponibles(columnas: list, filas: list, denominaciones: list | None = None) -> None:
    """Muestra el número, la denominación opcional y los datos de cada fila.

    Args:
        columnas (list): Columnas o índices de columnas que se van a procesar.
        filas (list): Filas o índices de filas que se van a procesar.
        denominaciones (list | None): Denominaciones opcionales de las filas. Por defecto: None.

    Returns:
        No devuelve un valor.
    """
    print("--- FILAS DISPONIBLES ---")
    i = 0
    while i < len(filas):
        texto = f"{i + 1})"
        if denominaciones != None and denominaciones[i] != "":
            texto += f" ({denominaciones[i]})"
        j = 0
        while j < len(columnas):
            valor = filas[i][j]
            if valor == "":
                valor = "(vacío)"
            texto += f"  {columnas[j]}: {valor}"
            j += 1
        print(texto)
        i += 1


def mostrar_columnas_disponibles(columnas: list) -> None:
    """Muestra las columnas numeradas para facilitar su selección.

    Args:
        columnas (list): Columnas o índices de columnas que se van a procesar.

    Returns:
        No devuelve un valor.
    """
    print("--- COLUMNAS DISPONIBLES ---")
    i = 0
    while i < len(columnas):
        print(f"{i + 1}) {columnas[i]}")
        i += 1


def mostrar_tablas(matriz: list, denominaciones: list | None = None) -> None:  
    """Permite mostrar una matriz completa, una fila o una columna.

    Args:
        matriz (list): Matriz que se va a mostrar.
        denominaciones (list | None): Denominaciones opcionales de las filas. Por defecto: None.

    Returns:
        No devuelve un valor.
    """
    if len(matriz) < 2:
        print("ERROR: La tabla no contiene datos suficientes para ser mostrada.")
    else:
        filas, columnas = elegir_seleccion(matriz, denominaciones)
        imprimir_tabla(matriz, filas, columnas)


def elegir_seleccion(matriz: list, denominaciones: list | None = None) -> tuple[list, list]:  
    """Muestra el menú y devuelve (filas, columnas) a mostrar como listas de índices.

    Args:
        matriz (list): Matriz que se va a mostrar.
        denominaciones (list | None): Denominaciones opcionales de las filas. Por defecto: None.

    Returns:
        tuple[list, list]: Tupla con los índices de filas y columnas seleccionadas.
    """

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
        mostrar_filas_disponibles(matriz[0], matriz[1:], denominaciones)
        cant_filas_datos = len(matriz) - 1
        fila_elegida = leer_entero_postivo(f"Número de fila (1-{cant_filas_datos}): ", 1, cant_filas_datos)
        filas = [fila_elegida]
        columnas = rango_indices(0, cant_columnas)
        print(f"--- FILA {fila_elegida} ---")

    else:
        mostrar_columnas_disponibles(matriz[0])
        columna_elegida = leer_entero_postivo(
            f"Número de columna (1-{cant_columnas}): ", 1, cant_columnas) - 1
        
        filas = rango_indices(1, len(matriz))
        columnas = [columna_elegida]
        print(f"--- COLUMNA {matriz[0][columna_elegida]} ---")

    return filas, columnas


def imprimir_tabla(matriz: list, filas: list, columnas: list) -> None:  
    """Imprime los encabezados y las filas indicadas.

    Args:
        matriz (list): Matriz que se va a mostrar.
        filas (list): Filas o índices de filas que se van a procesar.
        columnas (list): Columnas o índices de columnas que se van a procesar.

    Returns:
        No devuelve un valor.
    """
    
    anchos = calcular_anchos(matriz, filas, columnas)
    borde = armar_borde(anchos)

    print(borde)
    print(armar_linea(matriz, 0, columnas, anchos))
    print(borde)

    for i in range(len(filas)):
        print(armar_linea(matriz, filas[i], columnas, anchos))
        print(borde)


def calcular_anchos(matriz: list, filas: list, columnas: list) -> list:  
    """Calcula el ancho de cada columna visible según su texto más largo.

    Args:
        matriz (list): Matriz que se va a mostrar.
        filas (list): Filas o índices de filas que se van a procesar.
        columnas (list): Columnas o índices de columnas que se van a procesar.

    Returns:
        list: Lista con el ancho necesario para cada columna seleccionada.
    """

    
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
    """Arma la línea separadora, por ejemplo +------+----+.

    Args:
        anchos (list): Ancho de cada columna que se mostrará.

    Returns:
        str: Cadena que representa el borde de la tabla.
    """

    borde = "+"
    for j in range(len(anchos)):
        borde += "-" * (anchos[j] + 2) + "+"
    return borde


def armar_linea(matriz: list, fila: int, columnas: list, anchos: list) -> str:  
    """Arma el texto de una fila de la matriz (la fila 0 son los encabezados).

    Args:
        matriz (list): Matriz que se va a mostrar.
        fila (int): Índice de la fila.
        columnas (list): Columnas o índices de columnas que se van a procesar.
        anchos (list): Ancho de cada columna que se mostrará.

    Returns:
        str: Cadena formateada con los datos de la fila indicada.
    """

    linea = "|"

    for j in range(len(columnas)):
        columna = columnas[j]
        dato = formatear_dato(matriz[fila][columna], columna, fila == 0)
        linea += " " + dato + " " * (anchos[j] - len(dato) + 1) + "|"
    
    return linea


def formatear_dato(dato, columna: int, es_encabezado: bool) -> str: 
    """Pasa el dato a texto y, en las columnas de notas, quita el '.0' final.

    Args:
        dato: Dato que se va a procesar o mostrar.
        columna (int): Índice de la columna.
        es_encabezado (bool): Indica si el dato pertenece al encabezado.

    Returns:
        str: Dato convertido a texto para su visualización.
    """
    texto = str(dato)

    if es_encabezado == False and columna >= IDX_NOTAS and len(texto) >= 2:
        if texto[len(texto) - 2] == "." and texto[len(texto) - 1] == "0":
            texto = texto[:len(texto) - 2]
    return texto

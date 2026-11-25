"""Carga y modificación de tablas y variables."""

from .almacenamiento import guardar_catalogo, guardar_cambios_archivos
from .mostrar_datos import mostrar_columnas_disponibles, mostrar_filas_disponibles
from .validaciones import esta_en_lista
from .funciones import (
    MAX_FILAS, leer_dato_por_tipo, leer_entero_postivo, leer_opcion,
    leer_si_no, leer_texto, leer_nombre, pedir_etiqueta, calcular_nota_final,
)


def seleccionar_tabla(proyecto: dict) -> dict:
    """Muestra las tablas del proyecto y devuelve la seleccionada.

    Args:
        proyecto (dict): Proyecto seleccionado y sus datos.

    Returns:
        dict: Tabla seleccionada por el usuario.
    """
    print("--- TABLAS DISPONIBLES ---")
    i = 0
    while i < len(proyecto["tablas"]):
        print(f"{i + 1}) {proyecto['tablas'][i]['nombre']}")
        i += 1
    numero = leer_entero_postivo("Seleccione una tabla: ", 1, len(proyecto["tablas"]))
    return proyecto["tablas"][numero - 1]


def pedir_columna(tabla: dict) -> tuple:
    """Solicita un nombre único y un tipo de dato para una nueva columna.

    Args:
        tabla (dict): Tabla sobre la que se realiza la operación.

    Returns:
        tuple: Tupla con el nombre y el tipo de la columna.
    """
    nombre = leer_texto("Nombre de la columna: ")
    while esta_en_lista(tabla["columnas"], nombre) or nombre == "Denominación":
        print("Error: el nombre ya existe o está reservado.")
        nombre = leer_texto("Nombre de la columna: ")
    print("1) Texto  2) Entero  3) Decimal")
    opcion = leer_entero_postivo("Tipo de dato: ", 1, 3)
    if opcion == 1:
        tipo = "str"
    elif opcion == 2:
        tipo = "int"
    else:
        tipo = "float"
    return nombre, tipo


def crear_tabla(proyecto: dict, proyectos: dict) -> None:
    """Crea una tabla con columnas definidas por el usuario y la guarda.

    Args:
        proyecto (dict): Proyecto seleccionado y sus datos.
        proyectos (dict): Diccionario de proyectos disponibles.

    Returns:
        No devuelve un valor.
    """
    nombre = leer_texto("Nombre de la tabla: ")
    repetido = False
    i = 0
    while i < len(proyecto["tablas"]):
        if proyecto["tablas"][i]["nombre"] == nombre:
            repetido = True
        i += 1
    if repetido:
        print("Error: ya existe una tabla con ese nombre.")
    else:
        tabla = {
            "nombre": nombre, "archivo": "", "columnas": [],
            "tipos_datos": [], "rangos": [], "es_notas": False,
            "filas": [], "denominaciones": []
        }
        cantidad = leer_entero_postivo("Cantidad de columnas (1-50): ", 1, 50)
        i = 0
        while i < cantidad:
            nombre_columna, tipo = pedir_columna(tabla)
            tabla["columnas"] += [nombre_columna]
            tabla["tipos_datos"] += [tipo]
            tabla["rangos"] += [None]
            i += 1
        proyecto["tablas"] += [tabla]
        guardar_catalogo(proyectos)
        print("Tabla creada.")
    return


def copiar_tabla(tabla: dict) -> dict:
    """Copia los datos para completar la carga antes de guardarla.

    Args:
        tabla (dict): Tabla sobre la que se realiza la operación.

    Returns:
        dict: Copia de la tabla, con listas de datos independientes.
    """
    copia = {
        "nombre": tabla["nombre"], "archivo": tabla["archivo"],
        "es_notas": tabla["es_notas"], "columnas": tabla["columnas"][:],
        "tipos_datos": tabla["tipos_datos"][:], "rangos": tabla["rangos"][:],
        "denominaciones": tabla["denominaciones"][:], "filas": []
    }
    i = 0
    while i < len(tabla["filas"]):
        copia["filas"] += [tabla["filas"][i][:]]
        i += 1
    return copia


def guardar_cambios(tabla: dict, copia: dict, proyectos: dict) -> None:
    """Actualiza la tabla con la copia editada y persiste los cambios.

    Args:
        tabla (dict): Tabla sobre la que se realiza la operación.
        copia (dict): Copia de la tabla con los cambios realizados.
        proyectos (dict): Diccionario de proyectos disponibles.

    Returns:
        No devuelve un valor.
    """
    tabla["columnas"] = copia["columnas"]
    tabla["tipos_datos"] = copia["tipos_datos"]
    tabla["rangos"] = copia["rangos"]
    tabla["filas"] = copia["filas"]
    tabla["denominaciones"] = copia["denominaciones"]
    guardar_cambios_archivos(tabla, proyectos)
    print("Cambios guardados.")


def columna_calculada(tabla: dict, columna: int) -> bool:
    """Indica si la columna es la nota final calculada de una tabla de notas.

    Args:
        tabla (dict): Tabla sobre la que se realiza la operación.
        columna (int): Índice de la columna.

    Returns:
        bool: True si es la columna de nota final calculada; False en caso contrario.
    """
    return tabla["es_notas"] and tabla["columnas"][columna] == "Nota final"


def actualizar_nota(tabla: dict, fila: int) -> None:
    """Recalcula la nota final de una fila cuando sus dos notas están cargadas.

    Args:
        tabla (dict): Tabla sobre la que se realiza la operación.
        fila (int): Índice de la fila.

    Returns:
        No devuelve un valor.
    """
    if tabla["es_notas"]:
        pp = tabla["filas"][fila][3]
        sp = tabla["filas"][fila][4]
        if pp != "" and sp != "":
            tabla["filas"][fila][5] = calcular_nota_final(float(pp), float(sp))
        else:
            tabla["filas"][fila][5] = ""


def cargar_celda(tabla: dict, fila: int, columna: int) -> None:
    """Solicita un valor para una celda editable y actualiza la nota final.

    Args:
        tabla (dict): Tabla sobre la que se realiza la operación.
        fila (int): Índice de la fila.
        columna (int): Índice de la columna.

    Returns:
        No devuelve un valor.
    """
    if columna_calculada(tabla, columna):
        print("La nota final se calcula automáticamente.")
    else:
        nombre = tabla["columnas"][columna]
        actual = tabla["filas"][fila][columna]
        print(f"Fila {fila + 1}, {nombre}: {actual}")
        mensaje = f"Nuevo valor para {nombre}: "
        if tabla["tipos_datos"][columna] == "str" and nombre.lower() in ["nombre", "apellido"]:
            valor = leer_nombre(mensaje)
        else:
            valor = leer_dato_por_tipo(
                tabla["tipos_datos"][columna], mensaje, tabla["rangos"][columna]
            )
        tabla["filas"][fila][columna] = valor
        actualizar_nota(tabla, fila)


def elegir_columna(tabla: dict) -> int:
    """Muestra las columnas y devuelve el índice de la seleccionada.

    Args:
        tabla (dict): Tabla sobre la que se realiza la operación.

    Returns:
        int: Índice, desde cero, de la columna seleccionada.
    """
    mostrar_columnas_disponibles(tabla["columnas"])
    return leer_entero_postivo("Número de columna: ", 1, len(tabla["columnas"])) - 1


def elegir_fila(tabla: dict) -> int:
    """Muestra las filas y devuelve el índice de la seleccionada.

    Args:
        tabla (dict): Tabla sobre la que se realiza la operación.

    Returns:
        int: Índice, desde cero, de la fila seleccionada.
    """
    mostrar_filas_disponibles(tabla["columnas"], tabla["filas"], tabla["denominaciones"])
    return leer_entero_postivo("Número de fila: ", 1, len(tabla["filas"])) - 1


def recorrer_secuencial(tabla: dict, eje: str, indice: int, matriz: bool) -> None:
    """Solicita los valores de la fila o columna elegida.

    Args:
        tabla (dict): Tabla sobre la que se realiza la operación.
        eje (str): Indica si se trabaja con una fila o una columna.
        indice (int): Índice de la fila o columna elegida.
        matriz (bool): Indica si se recorre la tabla completa como matriz.

    Returns:
        No devuelve un valor.
    """
    if matriz:
        i = 0
        while i < len(tabla["filas"]):
            j = 0
            while j < len(tabla["columnas"]):
                if (eje == "a" and i == indice) or (eje == "b" and j == indice):
                    cargar_celda(tabla, i, j)
                j += 1
            i += 1
    elif eje == "a":
        j = 0
        while j < len(tabla["filas"][indice]):
            cargar_celda(tabla, indice, j)
            j += 1
    else:
        columna = []
        i = 0
        while i < len(tabla["filas"]):
            columna += [tabla["filas"][i][indice]]
            i += 1
        i = 0
        while i < len(columna):
            cargar_celda(tabla, i, indice)
            i += 1


def editar_secuencial(tabla: dict, proyectos: dict, matriz: bool,
                    eje: str = "", indice: int = -1) -> None:
    """Permite editar y guardar secuencialmente filas o columnas.

    Args:
        tabla (dict): Tabla sobre la que se realiza la operación.
        proyectos (dict): Diccionario de proyectos disponibles.
        matriz (bool): Indica si se recorre la tabla completa como matriz.
        eje (str): Indica si se trabaja con una fila o una columna. Por defecto: ''.
        indice (int): Índice de la fila o columna elegida. Por defecto: -1.

    Returns:
        No devuelve un valor.
    """
    continuar = True
    while continuar:
        if eje == "":
            print("a) Fila  b) Columna")
            eje = leer_opcion("¿Qué desea recorrer?: ", ["a", "b"])
            if eje == "a":
                indice = elegir_fila(tabla)
            else:
                indice = elegir_columna(tabla)
        copia = copiar_tabla(tabla)
        if eje == "b" and columna_calculada(copia, indice):
            print("La nota final se calcula automáticamente y no se puede modificar.")
        else:
            recorrer_secuencial(copia, eje, indice, matriz)
            guardar_cambios(tabla, copia, proyectos)
        continuar = leer_si_no("¿Desea elegir otra fila o columna?")
        eje = ""


def editar_distribuida(tabla: dict, proyectos: dict, matriz: bool) -> None:
    """Permite elegir, modificar y guardar celdas individualmente.

    Args:
        tabla (dict): Tabla sobre la que se realiza la operación.
        proyectos (dict): Diccionario de proyectos disponibles.
        matriz (bool): Indica si se recorre la tabla completa como matriz.

    Returns:
        No devuelve un valor.
    """
    continuar = True
    while continuar:
        fila = elegir_fila(tabla)
        columna = elegir_columna(tabla)
        if columna_calculada(tabla, columna):
            print("La nota final se calcula automáticamente y no se puede modificar.")
        else:
            copia = copiar_tabla(tabla)
            if matriz:
                i = 0
                while i < len(copia["filas"]):
                    j = 0
                    while j < len(copia["columnas"]):
                        if i == fila and j == columna:
                            cargar_celda(copia, i, j)
                        j += 1
                    i += 1
            else:
                cargar_celda(copia, fila, columna)
            guardar_cambios(tabla, copia, proyectos)
        continuar = leer_si_no("¿Desea elegir otra celda?")


def elegir_modo() -> str:
    """Solicita y devuelve el modo de carga: secuencial o distribuida.

    Returns:
        str: La opción elegida: 'a' para secuencial o 'b' para distribuida.
    """
    print("a) Carga secuencial  b) Carga distribuida")
    return leer_opcion("Modo de carga: ", ["a", "b"])


def editar_tabla(tabla: dict, proyectos: dict, matriz: bool) -> None:
    """Inicia la edición de una tabla con filas en el modo elegido.

    Args:
        tabla (dict): Tabla sobre la que se realiza la operación.
        proyectos (dict): Diccionario de proyectos disponibles.
        matriz (bool): Indica si se recorre la tabla completa como matriz.

    Returns:
        No devuelve un valor.
    """
    if len(tabla["filas"]) == 0:
        print("La tabla no tiene filas. Agregue una fila primero.")
    elif elegir_modo() == "a":
        editar_secuencial(tabla, proyectos, matriz)
    else:
        editar_distribuida(tabla, proyectos, matriz)


def agregar_fila(tabla: dict, proyectos: dict, matriz: bool) -> None:
    """Agrega una fila y permite cargarla de forma secuencial o distribuida.

    Args:
        tabla (dict): Tabla sobre la que se realiza la operación.
        proyectos (dict): Diccionario de proyectos disponibles.
        matriz (bool): Indica si se recorre la tabla completa como matriz.

    Returns:
        No devuelve un valor.
    """
    if len(tabla["filas"]) >= MAX_FILAS:
        print("La tabla alcanzó el máximo de filas.")
    else:
        modo = elegir_modo()
        copia = copiar_tabla(tabla)
        numero = len(copia["filas"]) + 1
        denominar = leer_si_no("¿Desea denominar la fila?")
        copia["denominaciones"] += [pedir_etiqueta(denominar, numero)]
        fila = []
        i = 0
        while i < len(copia["columnas"]):
            fila += [""]
            i += 1
        copia["filas"] += [fila]
        if modo == "a":
            recorrer_secuencial(copia, "a", numero - 1, matriz)
            guardar_cambios(tabla, copia, proyectos)
            if leer_si_no("¿Desea elegir otra fila o columna?"):
                editar_secuencial(tabla, proyectos, matriz)
        else:
            guardar_cambios(tabla, copia, proyectos)
            print(f"Se agregó la fila {numero}. Puede cargar sus celdas ahora.")
            editar_distribuida(tabla, proyectos, matriz)
    return


def agregar_columna(tabla: dict, proyectos: dict, matriz: bool) -> None:
    """Agrega una columna y permite cargar sus valores si hay filas.

    Args:
        tabla (dict): Tabla sobre la que se realiza la operación.
        proyectos (dict): Diccionario de proyectos disponibles.
        matriz (bool): Indica si se recorre la tabla completa como matriz.

    Returns:
        No devuelve un valor.
    """
    if len(tabla["columnas"]) >= 50:
        print("La tabla alcanzó el máximo de columnas.")
    else:
        copia = copiar_tabla(tabla)
        nombre, tipo = pedir_columna(copia)
        copia["columnas"] += [nombre]
        copia["tipos_datos"] += [tipo]
        copia["rangos"] += [None]
        i = 0
        while i < len(copia["filas"]):
            copia["filas"][i] += [""]
            i += 1
        if len(copia["filas"]) == 0:
            guardar_cambios(tabla, copia, proyectos)
        else:
            modo = elegir_modo()
            if modo == "a":
                columna = len(copia["columnas"]) - 1
                recorrer_secuencial(copia, "b", columna, matriz)
                guardar_cambios(tabla, copia, proyectos)
                if leer_si_no("¿Desea elegir otra fila o columna?"):
                    editar_secuencial(tabla, proyectos, matriz)
            else:
                guardar_cambios(tabla, copia, proyectos)
                print(f"Se agregó la columna {nombre}. Puede cargar sus celdas ahora.")
                editar_distribuida(tabla, proyectos, matriz)
    return


def opcion_tablas(proyecto: dict, proyectos: dict) -> None:
    """Gestiona el menú de creación y edición de tablas del proyecto.

    Args:
        proyecto (dict): Proyecto seleccionado y sus datos.
        proyectos (dict): Diccionario de proyectos disponibles.

    Returns:
        No devuelve un valor.
    """
    volver = False
    while volver == False:
        print("\na) Seleccionar tabla  b) Crear tabla  c) Volver")
        opcion = leer_opcion("Opción: ", ["a", "b", "c"])
        if opcion == "c":
            volver = True
        elif opcion == "b":
            crear_tabla(proyecto, proyectos)
        else:
            tabla = seleccionar_tabla(proyecto)
            volver_tabla = False
            while volver_tabla == False:
                print(f"\n--- {tabla['nombre']} ---")
                print("a) Cargar o modificar matriz  b) Agregar fila  c) Agregar columna  d) Volver")
                accion = leer_opcion("Opción: ", ["a", "b", "c", "d"])
                if accion == "a":
                    editar_tabla(tabla, proyectos, True)
                elif accion == "b":
                    agregar_fila(tabla, proyectos, True)
                elif accion == "c":
                    agregar_columna(tabla, proyectos, True)
                else:
                    volver_tabla = True


def opcion_modificar(proyecto: dict, proyectos: dict) -> None:
    """Gestiona el menú de edición de filas y columnas como variables.

    Args:
        proyecto (dict): Proyecto seleccionado y sus datos.
        proyectos (dict): Diccionario de proyectos disponibles.

    Returns:
        No devuelve un valor.
    """
    tabla = seleccionar_tabla(proyecto)
    volver = False
    while volver == False:
        print(f"\n--- Variables de {tabla['nombre']} ---")
        print("a) Cargar o modificar fila o columna  b) Crear columna  c) Volver")
        opcion = leer_opcion("Opción: ", ["a", "b", "c"])
        if opcion == "a":
            editar_tabla(tabla, proyectos, False)
        elif opcion == "b":
            agregar_columna(tabla, proyectos, False)
        else:
            volver = True

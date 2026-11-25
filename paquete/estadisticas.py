"""Cálculos y menú de estadísticas para los datos de una tabla."""

from .funciones import leer_opcion
from .operaciones_tablas import elegir_columna, elegir_fila, seleccionar_tabla
from .validaciones import es_multiplo, esta_en_lista


def ordenar(valores: list) -> list:
    """Ordena una copia de valores comparables mediante inserción.

    Args:
        valores (list): Valores que se van a procesar.

    Returns:
        list: Copia ordenada de los valores de entrada.
    """
    ordenados = valores[:]
    i = 1
    while i < len(ordenados):
        valor = ordenados[i]
        j = i - 1
        while j >= 0 and ordenados[j] > valor:
            ordenados[j + 1] = ordenados[j]
            j -= 1
        ordenados[j + 1] = valor
        i += 1
    return ordenados


def sumar(valores: list) -> float:
    """Devuelve la suma de los valores numéricos.

    Args:
        valores (list): Valores que se van a procesar.

    Returns:
        int | float: Suma de los valores; cero si la lista está vacía.
    """
    total = 0
    for valor in valores:
        total += valor
    return total


def contar_frecuencias(valores: list) -> dict:
    """Cuenta las apariciones de cada valor.

    Args:
        valores (list): Valores que se van a procesar.

    Returns:
        dict: Diccionario que relaciona cada valor con su cantidad de apariciones.
    """
    frecuencias = {}
    for valor in valores:
        if valor in frecuencias:
            frecuencias[valor] += 1
        else:
            frecuencias[valor] = 1
    return frecuencias


def mostrar_frecuencias(valores: list, tipos: list) -> None:
    """Muestra frecuencias de números y textos, ordenados por separado.

    Args:
        valores (list): Valores que se van a procesar.
        tipos (list): Tipos de los valores, en el mismo orden que estos.

    Returns:
        No devuelve un valor.
    """
    if len(valores) == 0:
        print("No hay valores cargados para calcular frecuencias.")
    else:
        frecuencias = contar_frecuencias(valores)
        numeros = []
        textos = []
        i = 0
        while i < len(valores):
            if tipos[i] == "str":
                if not esta_en_lista(textos, valores[i]):
                    textos += [valores[i]]
            else:
                if not esta_en_lista(numeros, valores[i]):
                    numeros += [valores[i]]
            i += 1
        numeros = ordenar(numeros)
        textos = ordenar(textos)

        print(f"{'Valor':<20}{'Tipo':<10}{'Frecuencia':>12}{'Porcentaje':>12}")
        print("-" * 54)
        for valor in numeros:
            porcentaje = frecuencias[valor] * 100 / len(valores)
            print(f"{str(valor):<20}{'Número':<10}{frecuencias[valor]:>12}{porcentaje:>11.2f}%")
        for valor in textos:
            porcentaje = frecuencias[valor] * 100 / len(valores)
            print(f"{str(valor):<20}{'Texto':<10}{frecuencias[valor]:>12}{porcentaje:>11.2f}%")
        print("-" * 54)
        print(f"Cantidad de valores: {len(valores)}")
        print(f"Valores distintos: {len(frecuencias)}")



es_mayor = lambda valor, actual: valor > actual
es_menor = lambda valor, actual: valor < actual


def extremo(valores: list, comparar) -> int | float | None:
    """Devuelve el valor extremo según la lambda de comparación recibida.

    Args:
        valores (list): Valores que se van a procesar.
        comparar: Lambda que indica si el primer valor supera al segundo.

    Returns:
        int | float | None: Valor extremo de la lista, o None si está vacía.
    """
    resultado = None
    if len(valores) > 0:
        resultado = valores[0]
        for valor in valores:
            if comparar(valor, resultado):
                resultado = valor
    return resultado


def media_aritmetica(valores: list) -> float | None:
    """Calcula el promedio aritmético, o devuelve None si no hay valores.

    Args:
        valores (list): Valores que se van a procesar.

    Returns:
        float | None: Media aritmética, o None si la lista está vacía.
    """
    resultado = None
    if len(valores) > 0:
        resultado = sumar(valores) / len(valores)
    return resultado


def media_geometrica(valores: list) -> float | None:
    """Calcula la media geométrica de valores positivos, o devuelve None.

    Args:
        valores (list): Valores que se van a procesar.

    Returns:
        float | None: Media geométrica, o None si no hay valores o alguno no es positivo.
    """
    todos_positivos = len(valores) > 0
    for valor in valores:
        if valor <= 0:
            todos_positivos = False
    resultado = None
    if todos_positivos:
        exponente = 1 / len(valores)
        resultado = 1.0
        for valor in valores:
            resultado = resultado * valor ** exponente
    return resultado


def varianza(valores: list) -> float | None:
    """Calcula la varianza poblacional, o devuelve None si no hay valores.

    Args:
        valores (list): Valores que se van a procesar.

    Returns:
        float | None: Varianza poblacional, o None si la lista está vacía.
    """
    resultado = None
    if len(valores) > 0:
        media = media_aritmetica(valores)
        suma_cuadrados = 0.0
        for valor in valores:
            suma_cuadrados += (valor - media) ** 2
        resultado = suma_cuadrados / len(valores)
    return resultado


def desvio_estandar(valores: list) -> float | None:
    """Calcula el desvío estándar poblacional, o None si no hay valores.

    Args:
        valores (list): Valores que se van a procesar.

    Returns:
        float | None: Desvío estándar poblacional, o None si la lista está vacía.
    """
    resultado = None
    if len(valores) > 0:
        resultado = varianza(valores) ** 0.5
    return resultado


def mediana(valores: list) -> int | float | None:
    """Devuelve la mediana de los valores, o None si la lista está vacía.

    Args:
        valores (list): Valores que se van a procesar.

    Returns:
        int | float | None: Mediana, o None si la lista está vacía.
    """
    resultado = None
    if len(valores) > 0:
        ordenados = ordenar(valores)
        medio = len(ordenados) // 2
        if es_multiplo(len(ordenados), 2):
            resultado = (ordenados[medio - 1] + ordenados[medio]) / 2
        else:
            resultado = ordenados[medio]
    return resultado


def cuartiles(valores: list) -> tuple | None:
    """Calcula cuartiles por el método de las mitades.

    Args:
        valores (list): Valores que se van a procesar.

    Returns:
        tuple | None: Tupla con Q1, Q2 y Q3, o None si la lista está vacía.
    """
    ordenados = ordenar(valores)
    cantidad = len(ordenados)
    mitad = cantidad // 2
    if cantidad == 0:
        resultado = None
    elif cantidad == 1:
        resultado = (ordenados[0], ordenados[0], ordenados[0])
    else:
        inferior = []
        for i in range(mitad):
            inferior += [ordenados[i]]
        superior = []
        for i in range(cantidad - mitad, cantidad):
            superior += [ordenados[i]]
        resultado = (mediana(inferior), mediana(ordenados), mediana(superior))
    return resultado


def seleccionar_valores(tabla: dict) -> tuple:
    """Recoge los datos y tipos de una fila, columna o tabla completa.

    Args:
        tabla (dict): Tabla sobre la que se realiza la operación.

    Returns:
        tuple: Tupla con valores no vacíos, sus tipos y la cantidad de celdas vacías.
    """
    print("a) Una fila  b) Una columna  c) Toda la tabla")
    opcion = leer_opcion("Datos a analizar: ", ["a", "b", "c"])
    fila_elegida = -1
    columna_elegida = -1
    if opcion == "a":
        fila_elegida = elegir_fila(tabla)
    elif opcion == "b":
        columna_elegida = elegir_columna(tabla)

    valores = []
    tipos = []
    vacios = 0
    i = 0
    while i < len(tabla["filas"]):
        j = 0
        while j < len(tabla["columnas"]):
            if opcion == "c" or (opcion == "a" and i == fila_elegida) or (opcion == "b" and j == columna_elegida):
                valor = tabla["filas"][i][j]
                if valor == "":
                    vacios += 1
                else:
                    valores += [valor]
                    tipos += [tabla["tipos_datos"][j]]
            j += 1
        i += 1
    return valores, tipos, vacios


def mostrar_medidas_numericas(opcion: str, valores: list, tipos: list) -> None:
    """Muestra la medida elegida utilizando únicamente los valores numéricos.

    Args:
        opcion (str): Opción elegida por el usuario.
        valores (list): Valores que se van a procesar.
        tipos (list): Tipos de los valores, en el mismo orden que estos.

    Returns:
        No devuelve un valor.
    """
    numeros = []
    textos = 0
    i = 0
    while i < len(valores):
        if tipos[i] == "int" or tipos[i] == "float":
            numeros += [valores[i]]
        elif tipos[i] == "str":
            textos += 1
        else:
            print(f"Error: tipo de dato desconocido: {tipos[i]}")
            numeros = []
            i = len(valores)
        i += 1
    if textos > 0:
        print(f"Valores de texto omitidos: {textos}.")
    if len(numeros) == 0:
        print("No hay valores numéricos para calcular esta medida.")
    elif opcion == "b":
        print(f"Máximo: {extremo(numeros, es_mayor)}")
        print(f"Mínimo: {extremo(numeros, es_menor)}")
    elif opcion == "c":
        print(f"Media aritmética: {media_aritmetica(numeros)}")
        geometrica = media_geometrica(numeros)
        if geometrica == None:
            print("La media geométrica requiere valores mayores que cero.")
        else:
            print(f"Media geométrica: {geometrica}")
    elif opcion == "d":
        print(f"Varianza poblacional: {varianza(numeros)}")
        print(f"Desvío estándar: {desvio_estandar(numeros)}")
    elif opcion == "e":
        print(f"Mediana: {mediana(numeros)}")
        q1, q2, q3 = cuartiles(numeros)
        print(f"Cuartiles: Q1 = {q1}, Q2 = {q2}, Q3 = {q3}")


def opcion_estadistica(proyecto: dict) -> None:
    """Permite elegir datos de una tabla y consultar sus estadísticas.

    Args:
        proyecto (dict): Proyecto seleccionado y sus datos.

    Returns:
        No devuelve un valor.
    """
    tabla = seleccionar_tabla(proyecto)
    if len(tabla["filas"]) == 0:
        print("La tabla no tiene filas para analizar.")
    else:
        volver = False
        while volver == False:
            valores, tipos, vacios = seleccionar_valores(tabla)
            print(f"Celdas vacías omitidas: {vacios}.")
            cambiar_datos = False
            while cambiar_datos == False and volver == False:
                print("\na) Frecuencias  b) Máximo y mínimo  c) Tendencia central")
                print("d) Dispersión  e) Posición  f) Elegir otros datos  g) Volver")
                opcion = leer_opcion("Opción: ", ["a", "b", "c", "d", "e", "f", "g"])
                if opcion == "a":
                    mostrar_frecuencias(valores, tipos)
                elif opcion == "f":
                    cambiar_datos = True
                elif opcion == "g":
                    volver = True
                else:
                    mostrar_medidas_numericas(opcion, valores, tipos)

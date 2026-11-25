MAX_LARGO = 50

def par_impar(numero: int) -> bool:
    """Determina si un número es par o impar.

    Args:
        numero (int): Número a evaluar.

    Returns:
        bool: True si el número es par, False si es impar.
    """

    if numero == 0:
        resultado = True
    elif numero == 1:
        resultado = False
    else:
        resultado = par_impar(numero - 2)
    return resultado


def es_primo(numero: int) -> bool:
    """Determina si un número es primo.

    Args:
        numero (int): Número a evaluar.

    Returns:
        bool: True si el número es primo, False en caso contrario.
    """
    if numero < 2:
        resultado = False
    else:
        resultado = True
        #usar while en vez del for

        for i in range(2, int(numero ** 0.5) + 1):
            if es_multiplo(numero, i):
                resultado = False
                break
    return resultado


def es_multiplo(numero: int, multiplo: int) -> bool:
    """Determina si un número es múltiplo de otro.

    Args:
        numero (int): Número a evaluar.
        multiplo (int): Número del cual se quiere verificar si es múltiplo.

    Returns:
        bool: True si el número es múltiplo del otro, False en caso contrario.
    """
    if multiplo == 0:
        resultado = False
    elif numero % multiplo == 0:
        resultado = True
    else:
        resultado = False
    return resultado

def validar_rango(valor: int | float, minimo: int | float, maximo: int | float) -> bool:
    """Indica si un número se encuentra dentro de un rango inclusivo.

    Args:
        valor (int | float): Valor que se desea validar.
        minimo (int | float): Límite inferior del rango.
        maximo (int | float): Límite superior del rango.

    Returns:
        bool: True si el valor está dentro del rango, False en caso contrario.
    """
    resultado = minimo <= valor and valor <= maximo
    return resultado


def validar_numero(cadena: str) -> bool:
    """Valida que una cadena de caracteres esté compuesta por números (ASCII 48-57).

    Args:
        cadena (str): Cadena que se va a validar.

    Returns:
        bool: True si se cumple la condición indicada; False en caso contrario.
    """
    i = 0
    es_numero = True

    while i < len(cadena) and es_numero:
        if ord(cadena[i]) < 48 or ord(cadena[i]) > 57:
            es_numero = False
        i += 1

    return es_numero


def validar_mayusculas(cadena: str) -> bool:
    """Valida que una cadena de caracteres esté compuesta por letras mayúsculas A-Z (ASCII 65-90).

    Args:
        cadena (str): Cadena que se va a validar.

    Returns:
        bool: True si se cumple la condición indicada; False en caso contrario.
    """
    i = 0
    son_mayusculas = True

    while i < len(cadena) and son_mayusculas:
        if ord(cadena[i]) < 65 or ord(cadena[i]) > 90:
            son_mayusculas = False
        i += 1

    return son_mayusculas


def validar_minusculas(cadena: str) -> bool:
    """Valida que una cadena de caracteres esté compuesta por letras minúsculas a-z (ASCII 97-122).

    Args:
        cadena (str): Cadena que se va a validar.

    Returns:
        bool: True si se cumple la condición indicada; False en caso contrario.
    """
    i = 0
    son_minusculas = True

    while i < len(cadena) and son_minusculas:
        if ord(cadena[i]) < 97 or ord(cadena[i]) > 122:
            son_minusculas = False
        i += 1

    return son_minusculas


def validar_acentuadas(cadena: str) -> bool:
    """Valida que una cadena de caracteres esté compuesta por letras acentuadas, ñ o ü

    Args:
        cadena (str): Cadena que se va a validar.

    Returns:
        bool: True si se cumple la condición indicada; False en caso contrario.
    """
    i = 0
    son_acentuadas = True

    while i < len(cadena) and son_acentuadas:
        if ord(cadena[i]) < 192 or ord(cadena[i]) > 255 or ord(cadena[i]) == 215 or ord(cadena[i]) == 247:
            son_acentuadas = False
        i += 1

    return son_acentuadas

def es_entero(texto: str) -> bool:
    """True si el texto es un entero sin signo.

    Args:
        texto (str): Texto que se va a procesar.

    Returns:
        bool: True si se cumple la condición indicada; False en caso contrario.
    """
    return len(texto) > 0 and validar_numero(texto)


def es_nota(texto: str) -> bool:
    """True si el texto es un número no negativo con a lo sumo un punto decimal.

    Args:
        texto (str): Texto que se va a procesar.

    Returns:
        bool: True si se cumple la condición indicada; False en caso contrario.
    """
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
    """Valida un nombre con letras, espacios, guiones o apóstrofos.

    Args:
        texto (str): Texto que se va a procesar.

    Returns:
        bool: True si se cumple la condición indicada; False en caso contrario.
    """
    i = 0
    tiene_letra = False
    es_valido = len(texto) > 0 and len(texto) <= MAX_LARGO

    while i < len(texto) and es_valido:
        es_letra = (validar_mayusculas(texto[i]) or validar_minusculas(texto[i])
                    or validar_acentuadas(texto[i]))
        if (es_letra or texto[i] == " " or texto[i] == "-" or texto[i] == "'"):
            if es_letra:
                tiene_letra = True
            i += 1
        else:
            es_valido = False

    return es_valido and tiene_letra


def esta_en_lista(lista: list, elemento: str | int | float) -> bool:  # Función que verifica si un elemento está en una lista
    """Verifica si un elemento se encuentra en una lista.
    
    Args:
        lista (list): Lista donde buscar
        elemento (str | int | float): Elemento a buscar
    
    Returns:
        bool: True si el elemento está en la lista, False en caso contrario
    """
    i = 0
    encontrado = False

    while i < len(lista) and encontrado == False:
        if lista[i] == elemento:
            encontrado = True
            
        i += 1

    return encontrado
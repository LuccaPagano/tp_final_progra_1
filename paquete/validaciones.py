MAX_LARGO = 50

def validar_contrasenia(contra_usu: str, contra_regis: str) -> str:

    '''
    Valida si la contrasenia de usuario es igual a la registrada
    
    Args: 
    contra_usu (str): Recibe la contrania de usuario
    contra_regis (str): Recibe la contrasenia a comparar

    Returns:
    contra_usu (str): Devuelve la contrasenia
    '''
    while contra_usu != contra_regis:
        print("Contraseña incorrecta.")
        contra_usu = input("Ingrese su contraseña nuevamente: ")

    return contra_usu

def validar_usuario(nombre_usuario: str, usuario_registrado: str) -> bool:

    '''
    Valida si el nombre de usuario es igual al usuario registrado

    Args:
    nombre_usuario (str): recibe el nombre usuario ingresado
    usuario_registrado(str): almacena el nombre de usuario guardado

    Return:
    Cambia el nombre de usuario registrado por el nuevo
    '''

    return (nombre_usuario) == (usuario_registrado)

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
            if numero % i == 0:
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

def validar_rango(valor: int, minimo: int, maximo: int) -> bool:
    """Indica si un entero se encuentra dentro de un rango inclusivo.

    La búsqueda recursiva divide el rango de enteros a la mitad en cada
    llamada.

    Args:
        valor (int): Valor que se desea validar.
        minimo (int): Límite inferior del rango.
        maximo (int): Límite superior del rango.

    Returns:
        bool: True si el valor está dentro del rango, False en caso contrario.
    """


    if minimo > maximo or valor < minimo or valor > maximo:
        return False

    medio = (minimo + maximo) // 2

    if valor == medio:
        resultado = True
    elif valor < medio:
        resultado = validar_rango(valor, minimo, medio - 1)
    else:
        resultado = validar_rango(valor, medio + 1, maximo)

    return resultado


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

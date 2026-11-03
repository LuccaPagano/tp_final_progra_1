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
        resultado = False

    medio = (minimo + maximo) // 2
    
    if valor == medio:
        resultado= True
    elif valor < medio:
        resultado = validar_rango(valor, minimo, medio - 1)
    else:
        resultado = validar_rango(valor, medio + 1, maximo)

    return resultado


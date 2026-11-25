from .funciones import (  
    leer_texto, 
    leer_entero_postivo,
    leer_decimal,  
    leer_opcion, 
    guardar_tabla,
    leer_tabla,
    COLUMNAS  
)
from .almacenamiento import cargar_catalogo, guardar_catalogo
from .archivos_csv import ruta_archivo
from .validaciones import esta_en_lista


def seleccionar_proyecto(proyectos: dict) -> dict:
    """Permite crear un proyecto nuevo o elegir uno existente.

    Args:
        proyectos (dict): Diccionario de proyectos disponibles.

    Returns:
        dict | None: Proyecto creado o seleccionado, o None si no hay proyectos disponibles.
    """
    print("--- GESTIÓN DE PROYECTOS ---")
    print("a) Crear proyecto nuevo")
    print("b) Elegir proyecto existente")
    opcion = leer_opcion("Seleccione una opción: ", ["a", "b"])
    
    if opcion == "a":
        proyecto = crear_proyecto_nuevo(proyectos)
    else:
        proyecto = elegir_proyecto_existente(proyectos)
    
    return proyecto


def crear_proyecto_nuevo(proyectos: dict) -> dict:  
    """Crea un proyecto nuevo con columnas personalizadas y sus tipos de dato.

    Args:
        proyectos (dict): Diccionario de proyectos disponibles.

    Returns:
        dict: Proyecto creado y agregado al diccionario de proyectos.
    """
    print("--- CREAR PROYECTO NUEVO ---")
    nombre_proyecto = leer_texto("Nombre del proyecto: ")
    nombre_repetido = True
    while nombre_repetido:
        nombre_repetido = False

        for clave in proyectos:
            if proyectos[clave]["nombre"] == nombre_proyecto:
                nombre_repetido = True

        if nombre_repetido:
            print("Error: ya existe un proyecto con ese nombre.")
            nombre_proyecto = leer_texto("Nombre del proyecto: ")
    cantidad_columnas = leer_entero_postivo("Cantidad de columnas: ", 1, 50)
    
    columnas = []
    tipos_datos = []
    rangos = []
    i = 0
    while i < cantidad_columnas:
        nombre_columna = leer_texto(f"Nombre de columna {i + 1}: ")
        while esta_en_lista(columnas, nombre_columna) or nombre_columna == "Denominación":
            print("Error: el nombre ya existe o está reservado.")
            nombre_columna = leer_texto(f"Nombre de columna {i + 1}: ")
        columnas += [nombre_columna]
        
        print("Tipos de dato disponibles:")
        print("  1) Texto (str)")
        print("  2) Número entero (int)")
        print("  3) Número decimal (float)")
        tipo_opcion = leer_entero_postivo("Seleccione el tipo de dato: ", 1, 3)
        
        if tipo_opcion == 1:
            tipo = "str"
            rango = None
        elif tipo_opcion == 2:
            tipo = "int"
            minimo = leer_entero_postivo("Valor mínimo: ", 0, 999999)
            maximo = leer_entero_postivo("Valor máximo: ", minimo, 999999)
            rango = [minimo, maximo]
        else:
            tipo = "float"
            minimo = leer_decimal("Valor mínimo: ")
            maximo = leer_decimal("Valor máximo: ")
            rango = [minimo, maximo]
        
        tipos_datos += [tipo]
        rangos += [rango]
        i = i + 1
    
    id_proyecto = str(len(proyectos) + 1)
    nombre_archivo = ""
    
    proyecto = {
        "nombre": nombre_proyecto,  
        "archivo": nombre_archivo, 
        "tipos_datos": tipos_datos,  
        "rangos": rangos, 
        "es_notas": False,  
        "tablas": [  
            {
                "nombre": nombre_proyecto,  
                "archivo": nombre_archivo,
                "tipos_datos": tipos_datos[:],
                "rangos": rangos[:],
                "es_notas": False,
                "columnas": columnas,  
                "denominaciones": [],  
                "filas": []  
            }
        ]
    }
    
    proyectos[id_proyecto] = proyecto
    
    guardar_catalogo(proyectos)
    
    print(f"Proyecto '{nombre_proyecto}' creado correctamente.")
    return proyecto


def elegir_proyecto_existente(proyectos: dict) -> dict | None:  
    """Muestra los proyectos existentes y permite elegir uno.

    Args:
        proyectos (dict): Diccionario de proyectos disponibles.

    Returns:
        dict | None: Proyecto elegido, o None si no hay proyectos disponibles.
    """
    print("--- PROYECTOS DISPONIBLES ---")
    claves = []
    i = 0
    for clave in proyectos:
        print(f"  {i + 1}. {proyectos[clave]['nombre']}")
        claves += [clave]
        i = i + 1
    
    if len(claves) == 0:
        print("No hay proyectos disponibles.")
        proyecto = None
    else:
        numero = leer_entero_postivo("Seleccione un proyecto: ", 1, len(claves))
        clave_elegida = claves[numero - 1]
        proyecto = proyectos[clave_elegida]

    return proyecto


def crear_proyectos_base() -> dict | None:
    """Carga los proyectos de ambos años o crea sus archivos de ejemplo si no existen.

    Returns:
        dict | None: Proyectos base cargados, o None si no se pueden leer.
    """
    proyectos = {
        "1": {  
            "nombre": "Notas primer año",  
            "archivo": "notas_primer_anio.csv",  
            "ejemplo": ["Ana", "Pérez", "Programación", 8.0, 6.0, 7.0],  
            "tipos_datos": ["str", "str", "str", "float", "float"],  
            "rangos": [None, None, None, [1.0, 10.0], [1.0, 10.0]],  
            "es_notas": True  
        },
        "2": {  
            "nombre": "Notas segundo año",  
            "archivo": "notas_segundo_anio.csv",  
            "ejemplo": ["Juan", "García", "Matemática", 7.0, 9.0, 8.0],  
            "tipos_datos": ["str", "str", "str", "float", "float"],  
            "rangos": [None, None, None, [1.0, 10.0], [1.0, 10.0]], 
            "es_notas": True  
        }
    }
    i = 0
    while i < 2 and proyectos != None:
        clave = "1" if i == 0 else "2"
        proyecto = proyectos[clave]
        archivo = proyecto["archivo"]
        
        archivo_obj = open(ruta_archivo(archivo), "a")
        archivo_obj.close()
        tabla = leer_tabla(proyecto["nombre"], archivo)
        if tabla == None:
            proyectos = None
        else:
            if len(tabla["filas"]) == 0:
                tabla = {
                    "nombre": proyecto["nombre"],
                    "columnas": COLUMNAS[:],
                    "denominaciones": [""],
                    "filas": [proyecto["ejemplo"][:]]
                }
                guardar_tabla(tabla, archivo)
            tabla["archivo"] = archivo
            tabla["tipos_datos"] = proyecto["tipos_datos"] + ["float"]
            tabla["rangos"] = proyecto["rangos"] + [None]
            tabla["es_notas"] = True
            proyecto["tablas"] = [tabla]
        
        i = i + 1
    
    return proyectos


def crear_proyectos() -> dict | None:
    """Carga el catálogo o crea los proyectos base si todavía está vacío.

    Returns:
        dict | None: Proyectos cargados o creados, o None si hay errores de lectura.
    """
    catalogo = cargar_catalogo()
    if catalogo == None:
        proyectos = None
    elif len(catalogo) > 0:
        proyectos = catalogo
    else:
        proyectos = crear_proyectos_base()
    return proyectos

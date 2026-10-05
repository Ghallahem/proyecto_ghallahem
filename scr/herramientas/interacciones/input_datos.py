from typing import Any, List, Dict, Optional
from ..utilidades import log_error
from .menus import menu_seleccion


def ingresar_dato_individual(mensaje_pregunta: str, es_requerido: bool = True) -> Any:
    """
    Pide un valor al usuario, intenta convertirlo a número si es posible.

    Si el usuario no escribe nada (presiona Enter):
    - Si 'es_requerido' es True: Muestra advertencia y vuelve a preguntar.
    - Si 'es_requerido' es False: Devuelve None.

    Args:
        mensaje_pregunta (str): El texto que se muestra al usuario para pedir el dato.
        es_requerido (bool): Determina si se permite una entrada vacía.

    Returns:
        Any: El valor: str o None.
    """
    while True:
        try:
            entrada_texto = input(f"{mensaje_pregunta}: ").strip()

            # Caso 1: Entrada vacía
            if not entrada_texto:
                if es_requerido:
                    log_error(
                        "El campo es obligatorio. No puede estar vacío.", "WARNING"
                    )
                    continue  # Vuelve a pedir el dato
                else:
                    return None
            else:
                # Caso 3: Es texto
                return entrada_texto

        except KeyboardInterrupt:
            log_error("Operación cancelada por el usuario.", "INFO")
            raise KeyboardInterrupt


def ingresar_fila_completa(
    nombres_columnas: List[str], columnas_requeridas: Optional[List[str]] = None
) -> Dict[str, Any]:
    """
    Pide al usuario los datos para una fila completa según las columnas definidas.

    Usa 'columnas_requeridas' para determinar qué campos son obligatorios.
    Si no se pasan requeridos, usa una lista por defecto basada en nombres comunes.

    Args:
        nombres_columnas (List[str]): Lista de nombres de las columnas.
        columnas_requeridas (List[str], opcional): Lista de columnas que deben tener valor.

    Returns:
        Dict[str, Any]: Diccionario con los datos ingresados.
    """
    datos_fila = {}

    # Determinar lista de requeridos
    if columnas_requeridas is None:
        # Lista por defecto si el usuario no especifica nada
        columnas_requeridas = ["id", "DNI"]

    # Estandarizar a minúsculas para comparación
    requeridos_normales = [col.strip().lower() for col in columnas_requeridas]

    print("\n--- Ingreso de Datos para Nueva Fila ---")

    for nombre_columna in nombres_columnas:
        # Verificar si la columna actual está en la lista de requeridos
        es_requerido = nombre_columna.strip().lower() in requeridos_normales

        valor_ingresado = ingresar_dato_individual(
            f"Ingrese el valor para '{nombre_columna}'", es_requerido=es_requerido
        )

        datos_fila[nombre_columna] = valor_ingresado

    return datos_fila


def cargar_datos_interactivos(
    nombres_columnas: List[str],
    columnas_requeridas: Optional[List[str]] = None,
    cantidad_minima_filas: int = 1,
    cantidad_maxima_filas: int = 100,
) -> List[Dict[str, Any]]:
    """
    Interfaz completa para cargar múltiples filas de datos.

    Permite al usuario ingresar datos repetidamente hasta que decida terminar.
    Las reglas de campos requeridos se aplican a todas las filas.

    Args:
        nombres_columnas (List[str]): Lista de nombres de columnas.
        columnas_requeridas (List[str], opcional): Lista de columnas que deben tener valor.
        cantidad_minima_filas (int): Mínimo de filas requeridas.
        cantidad_maxima_filas (int): Máximo de filas permitidas.

    Returns:
        List[Dict[str, Any]]: Lista completa de diccionarios con los datos.
    """
    lista_completa_de_datos = []
    contador_filas_ingresadas = 0

    print(f"\n=== Sistema de Carga de Datos ===")
    print(f"Columnas: {', '.join(nombres_columnas)}")

    # Mostrar qué columnas son requeridas (si se especificaron o si hay por defecto)
    if columnas_requeridas:
        print(f"Campos obligatorios: {', '.join(columnas_requeridas)}")
    else:
        print("Usando reglas por defecto para campos obligatorios.")

    print(f"Mínimo de filas: {cantidad_minima_filas}")

    while True:
        if contador_filas_ingresadas >= cantidad_maxima_filas:
            log_error(
                f"Límite máximo de {cantidad_maxima_filas} filas alcanzado.", "INFO"
            )
            break

        print(f"\n[ Fila {contador_filas_ingresadas + 1} ]")

        # PASAR columnas_requeridas a la función de fila
        nueva_fila = ingresar_fila_completa(nombres_columnas, columnas_requeridas)
        lista_completa_de_datos.append(nueva_fila)
        contador_filas_ingresadas += 1

        if contador_filas_ingresadas >= cantidad_minima_filas:
            opciones = ["Sí, guardar y finalizar", "No, agregar otra fila"]
            eleccion_usuario = menu_seleccion(
                "¿Deseas agregar otra fila de datos?", opciones
            )

            if eleccion_usuario == "Sí, guardar y finalizar":
                break
        else:
            log_error(
                f"Debes ingresar al menos {cantidad_minima_filas} fila(s) antes de finalizar.",
                "WARNING",
            )
    return lista_completa_de_datos


if __name__ == "__main__":
    pass

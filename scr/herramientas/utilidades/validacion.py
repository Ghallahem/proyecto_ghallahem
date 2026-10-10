from .registro import log_error
from typing import Any


def validar_numero(valor):
    """
    Valida si un valor puede ser convertido a un número (int o float).
    Devuelve True si es válido, False si no lo es.
    """
    try:
        float(valor)
        return True
    except (ValueError, TypeError):
        return False


def convertir_a_float(valor: str, default: float = 0.0) -> float:
    """
    Convierte un string a float de forma segura.

    Si la conversión falla, devuelve un valor por defecto

    Args:
        valor (str): El string a convertir.
        default (float, opcional): Valor a devolver si falla la conversión.

    Returns:
        valor (float): El valor numérico o el valor por defecto.

    Ejemplo:
        >>> convertir_a_float("10.50")
        10.5
        >>> convertir_a_float("no es numero", default=-1.0)
        -1.0

    """
    if not isinstance(valor, str):
        return float(valor) if isinstance(valor, (int, float)) else default
    try:
        return float(valor)
    except ValueError:
        log_error(
            f"No se pudo convertir '{valor}' a número. Usando valor por defecto: {default}",
            "WARNING",
        )
        return default


def convertir_campo_a_tipo(
    lista_datos: list,
    campo: str,
    tipo_destino: type,
    default: Any = None,
    manejar_errores: bool = True,
) -> list:
    """
    Convierte un campo específico en todos los diccionarios de una lista a un tipo de dato dado.

    Es segura: si un valor no puede convertirse, usa un valor por defecto o mantiene el original.
    No modifica la lista original, devuelve una nueva.

    Args:
        lista_datos (list): Lista de diccionarios.
        campo (str): Nombre del campo a convertir.
        tipo_destino (type): Tipo al que convertir (ej: int, float, str).
        default (any): Valor a usar si la conversión falla. Por defecto None.
        manejar_errores (bool): Si True, usa default en errores. Si False, lanza la excepción.

    Returns:
        list: Una nueva lista con los campos convertidos.
    """
    resultado = []

    for i, item in enumerate(lista_datos):

        # Hacemos una copia profunda para no mutar el original accidentalmente
        nuevo_item = item.copy()

        if campo in nuevo_item:
            valor_actual = nuevo_item[campo]

            # Caso especial: si ya es el tipo deseado, no hace nada
            if not isinstance(valor_actual, tipo_destino) and valor_actual is not None:
                try:
                    nuevo_item[campo] = tipo_destino(valor_actual)
                except (ValueError, TypeError) as e:
                    if manejar_errores:
                        mensaje = (
                            f"Línea {i}: Celda vacía o inválida en columna '{campo}'."
                            f"Se rellenó con {default}."
                        )
                        log_error(mensaje, "WARNING")
                        nuevo_item[campo] = default

                    else:
                        raise e from e

        resultado.append(nuevo_item)

    return resultado


if __name__ == "__main__":
    pass

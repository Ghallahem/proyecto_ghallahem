from pathlib import Path
from typing import List, Dict, Any, Union
from ..utilidades import log_error


def leer_csv_simple(
    ruta: Union[str, Path], headers: List[str], separador: str = ","
) -> List[Dict[str, Any]]:
    """
    Lee un archivo .txt con formato CSV y devuelve una lista de diccionarios.

    Reglas de validación:
    - Si una fila tiene MÁS datos que headers: Lanza ValueError (Error Crítico).
    - Si una fila tiene celdas vacías ("") o MENOS datos que headers: Rellena con None y lanza WARNING.
    - Intenta convertir columnas a int/float automáticamente si es posible.
    - Atencion: La funcion no puede manejar correctamente "," dentro de palabras o celdas de texto.

    Args:
        ruta (str | Path): Ruta al archivo.
                           - Opción recomendada: Usa obtener_ruta_segura("archivo.txt")
                             para asegurar que se encuentra en la carpeta del script.
                           - Opción simple: Pasa "archivo.txt" si el archivo está
                             en la misma carpeta donde ejecutaste el programa
        headers (List[str]): Lista de nombres de las columnas (Obligatorio).
        separador (str): Carácter qué separa los datos en cada fila.
                         Por defecto es ","
    Returns:
        List[Dict[str, Any]]: Lista de diccionarios con los datos leídos.

    Raises:
        FileNotFoundError: Si el archivo no existe.
        ValueError: Si una fila tiene más columnas de las esperadas.
    """
    path_obj = Path(ruta)
    if not path_obj.exists():
        mensaje_error = f"Archivo no encontrado: {ruta}"
        log_error(mensaje_error, "ERROR")
        raise FileNotFoundError(mensaje_error)

    datos = []
    expected_columns = len(headers)

    with open(path_obj, "r", encoding="utf-8") as f:
        lineas = f.readlines()

    if not lineas:
        return []

    for i, linea in enumerate(lineas, start=1):
        linea = linea.strip()
        if not linea:
            continue  # Saltar líneas vacías

        valores = linea.split(separador)
        num_valores = len(valores)

        # --- CASO 1: Demasiados datos (Error Crítico) ---
        if num_valores > expected_columns:

            # Detenemos el programa inmediatamente
            mensaje_error = (
                f"Error de formato en la línea {i}: "
                f"La fila tiene {num_valores} datos, pero solo se esperan {expected_columns}. "
                f"Datos extra: {valores}"
                f"Verifica que el archivo no tenga columnas adicionales o comas mal colocadas."
            )
            log_error(mensaje_error, "ERROR")
            raise ValueError(mensaje_error)

        # --- CASO 2: Datos faltantes (Advertencia y relleno) ---
        fila_dict = {}
        for j, header in enumerate(headers):
            if j < num_valores:
                valor_str = valores[j].strip()

                # --- Detectar celda vacía ---
                if valor_str == "":

                    fila_dict[header] = None
                    log_error(
                        f"Línea {i}: Celda vacía en columna '{header}'. "
                        f"Se rellenó con None.",
                        "WARNING",
                    )
                    continue
                # Conversión (int -> float -> str)
                try:
                    valor_final = int(valor_str)
                except ValueError:
                    try:
                        valor_final = round(float(valor_str), 2)
                    except ValueError:
                        valor_final = valor_str

                fila_dict[header] = valor_final
            else:
                # --- Falta dato para esta columna ---
                fila_dict[header] = None
                log_error(
                    f"Línea {i}: Dato faltante para la columna '{header}'. "
                    f"Se encontró {num_valores} datos, se esperaban {expected_columns}. "
                    f"Se rellenó con None.",
                    "WARNING",
                )

        datos.append(fila_dict)

    return datos


if __name__ == "__main__":
    pass

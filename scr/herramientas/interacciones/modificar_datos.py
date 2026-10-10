from typing import List, Dict, Any, Optional
from .menus import menu_seleccion
from .input_datos import ingresar_dato_individual
from ..utilidades import log_error


def generar_id_unico(cliente_data: List[Dict[str, Any]]) -> int:
    """
    Genera un id unico basado en una lista de diccionarios.

    Si la lista esta basia retornara 1
    """
    # 1. Chequeo de tipo: ¿Es una lista?
    if not isinstance(cliente_data, list):
        raise TypeError(
            f"¡Alerta! Se espera una lista de clientes, pero recibiste: {type(cliente_data)}"
        )

    # Si es lista, procedemos normal
    if not cliente_data:
        return 1

    ids_existentes = [c["id"] for c in cliente_data if "id" in c]

    if not ids_existentes:
        return 1

    return max(ids_existentes) + 1


def buscar_fila_por_id(
    lista_datos: List[Dict[str, Any]], columna_id: str
) -> Optional[Dict[str, Any]]:
    """
    Busca una fila en la lista de datos por su valor de ID.

    Intenta convertir el ID ingresado para comparar correctamente
    (si el ID en la lista es int y el usuario escribe str).

    Args:
        lista_datos (List[Dict]): La lista de diccionarios a buscar.
        columna_id (str): Nombre de la columna que contiene el identificador único.

    Returns:
        Dict | None: El diccionario encontrado o None si no existe.
    """

    while True:
        try:
            id_ingresado = input(f"Ingrese el ID del registro: ").strip()

            if not id_ingresado:
                log_error("El ID no puede estar vacío.", "WARNING")
                continue

            # Intentar convertir para comparar
            # Si el usuario escribe "1" y el ID en la lista es 1 (int), debe coincidir
            valor_buscado: Any = None
            try:
                valor_buscado = int(id_ingresado)
            except ValueError:
                try:
                    valor_buscado = float(id_ingresado)
                except ValueError:
                    valor_buscado = id_ingresado  # Es texto

            # Buscar en la lista
            for fila in lista_datos:

                valor_fila = fila.get(columna_id)

                # Comparación segura: intentamos igualar tipos o usar str
                if str(valor_fila) == str(valor_buscado):
                    return fila

            log_error(
                f"No se encontró ningún registro con ID '{id_ingresado}'.", "WARNING"
            )

            opciones = ["Seguir buscando", "Cancelar búsqueda"]
            eleccion = menu_seleccion("¿Qué desea hacer?", opciones)
            if eleccion == "Cancelar búsqueda":
                return None

        except KeyboardInterrupt:
            log_error("Operación cancelada.", "INFO")
            return None


def modificar_fila(
    fila_a_modificar: Dict[str, Any], nombres_columnas: List[str]
) -> Dict[str, Any]:
    """
    Permite al usuario modificar los valores de una fila existente.

    Muestra los valores actuales e invita al usuario a escribir nuevos.
    Si el usuario presiona Enter sin escribir nada, se mantiene el valor antiguo.

    Args:
        fila_a_modificar (Dict): El diccionario con los datos actuales.
        nombres_columnas (List[str]): Lista de columnas para iterar.

    Returns:
        Dict[str, Any]: El diccionario actualizado con los nuevos valores.
    """
    print("\n--- Modificar Registro ---")
    print(
        "Escriba un nuevo valor para actualizar. No escriba nada y presione ENTER para mantener el actual."
    )
    print("-" * 40)

    for nombre_columna in nombres_columnas:
        valor_actual = fila_a_modificar.get(nombre_columna)

        # Formatear el valor actual para mostrarlo (None se muestra como "N/A")
        texto_actual = str(valor_actual) if valor_actual is not None else "N/A"

        mensaje_pregunta = f"Valor actual de '{nombre_columna}' [{texto_actual}]: "

        # Pedir nuevo valor (no requerido, porque si está vacío usamos el actual)
        nuevo_valor = ingresar_dato_individual(mensaje_pregunta, es_requerido=False)

        # Si el usuario escribió algo, actualizamos. Si no, dejamos el antiguo.
        if nuevo_valor is not None:
            fila_a_modificar[nombre_columna] = nuevo_valor
            print(f"  ✅ Actualizado a: {nuevo_valor}")
        else:
            print(f"  ➡️  Mantenido: {valor_actual}")

    return fila_a_modificar


def editar_datos(
    lista_datos: List[Dict[str, Any]],
    nombres_columnas: List[str],
    columna_id: str = "id",
) -> List[Dict[str, Any]]:
    """
    Flujo completo para buscar y editar registros en una lista existente.

    Permite editar múltiples registros antes de devolver la lista actualizada.

    Args:
        lista_datos (List[Dict]): Lista de datos leídos previamente.
        nombres_columnas (List[str]): Nombres de las columnas.
        columna_id (str): Nombre de la columna que sirve como identificador único.

    Returns:
        List[Dict[str, Any]]: La misma lista (modificada en memoria).
    """
    if not lista_datos:
        log_error("No hay registros para editar.", "WARNING")
        return lista_datos

    print(f"\n=== Editor de Registros ===")
    print(f"Total de registros: {len(lista_datos)}")

    while True:
        # 1. Buscar
        fila_encontrada = buscar_fila_por_id(lista_datos, columna_id)

        if fila_encontrada is None:
            # Si no encontró o canceló, preguntamos si quiere salir
            opciones_salir = ["Salir del editor", "Buscar otro registro"]
            eleccion = menu_seleccion("¿Desea salir?", opciones_salir)
            if eleccion == "Salir del editor":
                break
            continue  # Vuelve al inicio del while para buscar de nuevo

        # 2. Modificar
        modificar_fila(fila_encontrada, nombres_columnas)

        # 3. Preguntar si sigue editando
        opciones_continuar = ["Editar otro registro", "Finalizar y guardar"]
        eleccion = menu_seleccion("¿Qué desea hacer ahora?", opciones_continuar)

        if eleccion == "Finalizar y guardar":
            break

    return lista_datos


if __name__ == "__main__":
    pass

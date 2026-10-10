from typing import List
from ..utilidades import log_error


def menu_seleccion(
    mensaje: str, opciones: List[str], mostrar_numeros: bool = True
) -> str:
    """
    Muestra un menú de opciones al usuario y valida que la entrada sea correcta.

    El usuario puede ingresar el texto completo de la opción o su índice (si
    se muestran números). La función repite la solicitud hasta recibir una
    opción válida.

    Args:
        mensaje (str): El texto principal que se muestra antes de las opciones.
        opciones (list): Lista de strings con las opciones disponibles (ej. ["Salir", "Jugar"]).
        mostrar_numeros (bool): Si es True, muestra las opciones numeradas (1. Opción).
                                Si es False, muestra solo el texto.

    Returns:
        seleccion_valida (str): La opción seleccionada por el usuario (el texto exacto de la lista).

    Ejemplo:
        >>> eleccion = menu_seleccion("Elige una acción", ["Iniciar", "Pausar", "Salir"])
        [MENU] Elige una acción:
        1. Iniciar
        2. Pausar
        3. Salir
        > Iniciar
        # Retorna "Iniciar"
    """
    if not opciones:
        raise ValueError(
            log_error("La lista de opciones no puede estar vacía.", "ERROR")
        )

    # Normalizar opciones para búsqueda (mayúsculas/minúsculas)
    opciones_lower = [opt.lower() for opt in opciones]

    while True:
        print(f"\n{mensaje}")

        # Mostrar opciones
        for i, opcion in enumerate(opciones, start=1):
            prefijo = f"{i}. " if mostrar_numeros else "   "
            print(f"{prefijo}{opcion}")

        try:
            entrada = input("\n> ").strip()
            if not entrada:
                log_error("Entrada vacía. Intenta de nuevo.", "WARNING")
                continue

            # Lógica de validación flexible
            seleccion_valida = None

            # 1. Intentar como texto exacto (case-insensitive)
            if entrada.lower() in opciones_lower:
                idx = opciones_lower.index(entrada.lower())
                seleccion_valida = opciones[idx]

            # 2. Intentar como número (índice)
            elif mostrar_numeros:
                try:
                    indice = int(entrada)
                    if 1 <= indice <= len(opciones):
                        seleccion_valida = opciones[indice - 1]
                except ValueError:
                    pass  # No es un número válido o está fuera de rango

            if seleccion_valida:
                return seleccion_valida
            else:
                log_error(
                    f"Opción inválida. Elige una de: {', '.join(opciones)}", "WARNING"
                )
                continue
        except KeyboardInterrupt:
            log_error("Operación cancelada por el usuario.", "INFO")
            raise KeyboardInterrupt


if __name__ == "__main__":
    pass

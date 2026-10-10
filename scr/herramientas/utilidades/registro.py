def log_error(mensaje: str, tipo: str = "ERROR") -> None:
    """
    Centraliza la impresión de mensajes de error o advertencias.

    En lugar de usar print() suelto, usamos esta función para tener un
    formato consistente y fácil de filtrar o redirigir en el futuro.

    Args:
        mensaje (str): El mensaje de error o advertencia.
        tipo (str, opcional): El tipo de mensaje ("ERROR", "WARNING", "INFO").
                              Por defecto es "ERROR".
    Ejemplo:
        >>> log_error("El archivo no se encontró", "WARNING")
        [WARNING] El archivo no se encontró
        >>> log_error("Cálculo inválido", "ERROR")
        [ERROR] Cálculo inválido
        >>> log_error("Proceso iniciado correctamente", "INFO")
        [INFO] Proceso iniciado correctamente
    """

    print(f"[{tipo.upper()}] {mensaje}")  # Mensaje con formato

if __name__ == "__main__":
    pass
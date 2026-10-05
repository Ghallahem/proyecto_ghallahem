from pathlib import Path
from typing import Union
from typing import Optional

def obtener_ruta_segura(nombre_archivo: str, carpeta_base: Optional[Path] = None) -> Path:
    """
    Construye una ruta absoluta a un archivo.

    Por defecto busca relativo al directorio donde se ejecuta el script (tu proyecto).
    Si se pasa 'carpeta_base', busca relativo a esa carpeta (útil para archivos embebidos).

    Args:
        nombre_archivo (str): Nombre del archivo (ej. "datos.csv")
        carpeta_base (Path, opcional): Carpeta base para la búsqueda. Si es None, usa el cwd.

    Returns:
        Path: El objeto Path con la ruta completa.

    Raises:
        FileNotFoundError: Si el archivo no se encuentra en la ruta calculada.
    """
    # Este bloque calcula la ruta en base al script de ejecucion (main)
    if carpeta_base is None:
        carpeta_base = Path.cwd()
    
    ruta_completa = carpeta_base / nombre_archivo
    return ruta_completa

def asegurar_carpeta(ruta: Union[str, Path]):
    """
    Crea la carpeta si no existe.
    - Si existe no hace nada.
    - Si la ruta recibida incluye un archivo, usa solo la carpeta padre.
    - Si falla (permisos, ruta inválida), lanza una excepción clara.
    - Si tiene éxito, no devuelve nada (None).

    Args:
        ruta (Union[str, Paht]): La ruta de la carpeta a verificar o crear.
                                 Puede ser un string o un objeto Path.

    """
    ruta_path = Path(ruta)
    
    if ruta_path.is_file() or (not ruta_path.exists() and ruta_path.suffix):
        # Si ruta contiene un archivo
        ruta_carpeta = ruta_path.parent
    else:
        # Si ruta ya es carpeta
        ruta_carpeta = ruta_path

    if ruta_carpeta.exists():
        if not ruta_carpeta.is_dir():
            raise ValueError(f"La ruta existe pero no es una carpeta: {ruta_carpeta}")
        return  # Ya existe, todo bien.

    try:
        ruta_carpeta.mkdir(parents=True, exist_ok=True)
    except PermissionError:
        raise PermissionError(f"No tienes permiso para crear la carpeta: {ruta_carpeta}")
    except OSError as e:
        raise OSError(f"Error al crear carpeta {ruta_carpeta}: {e}")

if __name__ == "__main__":
    pass
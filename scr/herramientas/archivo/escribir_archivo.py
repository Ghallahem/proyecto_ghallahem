from pathlib import Path
from typing import List, Dict, Any, Union
from ..utilidades import log_error
from ..utilidades import asegurar_carpeta

def guardar_csv_simple(
    ruta: Union[str, Path], 
    datos: List[Dict[str, Any]], 
    headers: List[str], 
    separador: str = ",",
    escribir_encabezados: bool = False,
    crear_backup: bool = False
) -> None:
    """
    Guarda una lista de diccionarios en un archivo .txt con formato CSV.

    Args:
        ruta (str | Path): Ruta de destino.
        datos (List[Dict]): Lista de diccionarios con los datos.
        headers (List[str]): Lista de nombres de columnas (define el orden).
        separador (str): Carácter separador (por defecto ",").
        escribir_encabezados (bool): Si es True, escribe la primera fila con los nombres de las columnas.
                                     Por defecto es False (formato sin títulos).
        crear_backup (bool): Si True, crea una copia de seguridad (.bak) antes de sobrescribir. Por defecto es False

    Raises:
        ValueError: Si 'headers' está vacío.
        PermissionError: Si no hay permisos para escribir.
        OSError: Si ocurre un error general de sistema de archivos.
    """
    if not datos:
        log_error("No hay datos para guardar. Archivo no creado.", "WARNING")
        return

    if not headers:
        mensaje_error = "La lista de 'headers' no puede estar vacía."
        log_error(mensaje_error,"ERROR")
        raise ValueError(mensaje_error)

    path_obj = Path(ruta)
    asegurar_carpeta(path_obj.parent)

    if crear_backup and path_obj.exists():
        backup_path = Path(str(path_obj) + ".bak")
        try:
            # replace() mueve el archivo original a .bak y sobrescribe si ya existía el .bak
            path_obj.replace(backup_path)
            log_error(f"Copia de seguridad creada: {backup_path}", "INFO")
        except OSError as e:
            log_error(f"No se pudo crear la copia de seguridad", "WARNING")
    
    try:
        with open(path_obj, "w", encoding="utf-8") as f:
            
            # 1. Opcional: Escribir encabezados
            if escribir_encabezados:
                f.write(separador.join(headers) + "\n")
            
            # 2. Escribir los datos
            for fila in datos:
                linea_datos = []
                for header in headers:
                    valor = fila.get(header)
                    
                    # Manejo de None: Escribir cadena vacía
                    if valor is None:
                        linea_datos.append("")
                    else:
                        linea_datos.append(str(valor))
                
                f.write(separador.join(linea_datos) + "\n")
        
        log_error(f"Archivo guardado correctamente: {path_obj}", "INFO")

    except PermissionError:
        raise PermissionError(f"No tienes permiso para escribir en: {ruta}")
    except OSError as e:
        raise OSError(f"Error al escribir el archivo: {e}")

if __name__ == "__main__":
    pass
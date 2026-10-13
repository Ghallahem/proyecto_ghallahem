def imprimir_lista_registros(lista_registros: list[dict], etiquetas_cabecera: list[str], titulo_seccion: str) -> None:
    """
    Imprime una lista de diccionarios en la consola con un formato de tabla alineado.
    
    Args:
        lista_registros: La lista de diccionarios a mostrar (ej: clientes, productos).
        etiquetas_cabecera: Lista de strings con los nombres de las columnas a mostrar (ej: ['id', 'Nombre']).
        titulo_seccion: El título que se mostrará antes de la tabla.
    """
    if not lista_registros:
        ancho_titulo = max(60, len(titulo_seccion) + 4)
        print("\n" + "=" * ancho_titulo)
        print(f" {titulo_seccion.upper()} ".center(ancho_titulo, "="))
        print("=" * ancho_titulo)
        print("No hay registros disponibles para mostrar.")
        print("=" * ancho_titulo)
        return

    # 1. Calcular el ancho máximo necesario para cada columna
    anchos_columnas = []
    for indice, etiqueta in enumerate(etiquetas_cabecera):
        # Buscar el string más largo entre el encabezado y los valores de la columna
        max_longitud = len(etiqueta)
        for registro in lista_registros:
            valor = str(registro.get(etiqueta, ""))
            if len(valor) > max_longitud:
                max_longitud = len(valor)
        
        # Espacio extra (2 espacios) para que el texto no pegue
        anchos_columnas.append(max_longitud + 2)

    # El título y sus separadores usan el ancho de la tabla, con un mínimo
    # de 60 caracteres para conservar el formato de secciones cortas.
    ancho_tabla = sum(anchos_columnas)
    ancho_titulo = max(60, ancho_tabla, len(titulo_seccion) + 4)
    print("\n" + "=" * ancho_titulo)
    print(f" {titulo_seccion.upper()} ".center(ancho_titulo, "="))
    print("=" * ancho_titulo)

    # 2. Imprimir el encabezado (Cabeceras)
    linea_encabezado = ""
    for indice, etiqueta in enumerate(etiquetas_cabecera):
        linea_encabezado += f"{etiqueta:<{anchos_columnas[indice]}}" # < para alineación a la izquierda
    print(linea_encabezado)
    
    # Imprimir la línea separadora
    print("-" * sum(anchos_columnas))

    # 3. Imprimir cada registro
    for registro in lista_registros:
        linea_registro = ""
        for indice, etiqueta in enumerate(etiquetas_cabecera):
            valor = str(registro.get(etiqueta, "N/A")) # "N/A" si el dato no existe
            linea_registro += f"{valor:<{anchos_columnas[indice]}}"
        print(linea_registro)

    print("=" * ancho_titulo)

if __name__ == "__main__":
    pass

import pandas as pd
from src.Settings import *
import os

class GestorArchivos:
    def leer_archivo(self, ruta_archivo, palabra_clave, unico_dato, dict_archivos_extra):
        """
        Lee un archivo Excel y filtra las filas que contienen una palabra clave en la columna 'PROGRAMA ACADÉMICO'.
        También selecciona columnas predeterminadas y opcionalmente incluye solo la última columna.

        Args:
            ruta_archivo (str): Ruta del archivo Excel.
            palabra_clave (str): Palabra clave a buscar.

        Returns:
            pd.DataFrame: DataFrame filtrado y procesado.
        """
        try:
            #Miramos si la ruta pertenece a los archivos extra
            if ruta_archivo in dict_archivos_extra:
                archivo_temporal = dict_archivos_extra[ruta_archivo]
                df = pd.read_excel(archivo_temporal)
            else :
                #De lo contrario, tratamos de leer el archivo en los archivos originales
                df = pd.read_excel(ruta_archivo)  # Cambia si las columnas relevantes están en un rango específico.

            if not unico_dato:
                # Leer el archivo Excel con solo las columnas necesarias al inicio
                df_palabra_clave = df[df[STR_PROGRAMA_ACADEMICO].str.contains(palabra_clave, case=False, na=False)]
                columnas_predeterminadas = [STR_CODIGO_SNIES, STR_METODOLOGIA, STR_PROGRAMA_ACADEMICO, STR_NOMBRE_IES,
                                            STR_TIPO_IES, STR_DEPARTAMENTO, STR_MUNICIPIO, STR_NIVEL_FORMACION, STR_SEMESTRE]
                ultima_columna_nombre = df.columns[-1]
                ultima_columna = df_palabra_clave[ultima_columna_nombre]
                df_filtrado = df_palabra_clave[columnas_predeterminadas]
                df_filtrado = pd.concat([df_filtrado, ultima_columna], axis=1)
                df_consolidado = df_filtrado.groupby(columnas_predeterminadas).sum(numeric_only=True).reset_index()
            else:
                df_palabra_clave = df[df[STR_PROGRAMA_ACADEMICO].str.contains(palabra_clave, case=False, na=False)]
                columnas_predeterminadas = [STR_CODIGO_SNIES, STR_SEMESTRE]
                ultima_columna_nombre = df.columns[-1]
                ultima_columna = df_palabra_clave[ultima_columna_nombre]
                df_filtrado = df_palabra_clave[columnas_predeterminadas]
                df_filtrado = pd.concat([df_filtrado, ultima_columna], axis=1)
                df_consolidado = df_filtrado.groupby(columnas_predeterminadas).sum(numeric_only=True).reset_index()


            return df_consolidado
        except FileNotFoundError:
            raise FileNotFoundError
        except Exception as e:
            print(f"Error al procesar el archivo: {e}")
            return pd.DataFrame()
import streamlit as st
import os
from src.Settings import *

def gestion_archivos(dict_archivos_extra):
    # Sección 1: Carga de Archivos
    st.title("Gestion de archivos")

    input_folder = BASE_PATH  # Asegúrate de que la carpeta existe

    # Utilizamos esta lista para imprimir los archivos cargados al SNIES EXTRACTOR
    default_files = []

    # Recorrer cada archivo en la carpeta
    for f in os.listdir(input_folder):
        # Comprobar si el archivo tiene la extensión .xlsx
        if f.endswith('.xlsx'):
            # Si es así, agregarlo a la lista default_files
            default_files.append(f)

    #Recorrer cada archivo en los adicionales
    for key in dict_archivos_extra:
        archivo_temporal = dict_archivos_extra[key]
        ruta_extra = archivo_temporal.name
        # Comprobar si el archivo tiene la extensión .xlsx
        if ruta_extra.endswith('.xlsx'):
            # Si es así, agregarlo a la lista default_files
            default_files.append(ruta_extra)

    default_files.sort()

    # Mostrar los archivos disponibles en un selectbox o multiselect
    st.title("Archivos Disponibles en 'inputs'")
    st.info(
        "Este es un listado de los archivos de Excel disponibles en la carpeta 'inputs'.")
    st.selectbox("Archivos disponibles", options=default_files)


    st.subheader("Carga de Archivos")
    uploaded_file = st.file_uploader("Subir archivos", type="xlsx")
    if uploaded_file is not None:
        ruta_archivo = BASE_PATH + "/" + uploaded_file.name
        dict_archivos_extra[ruta_archivo] = uploaded_file

gestion_archivos(st.session_state.dict_archivos_extra)


import streamlit as st
import pandas as pd
import plotly.express as px

from src.Settings import STR_CODIGO_SNIES, STR_METODOLOGIA, STR_PROGRAMA_ACADEMICO, STR_NOMBRE_IES, STR_TIPO_IES, \
    STR_DEPARTAMENTO, STR_MUNICIPIO, STR_NIVEL_FORMACION, STR_ADMITIDOS, STR_GRADUADOS, STR_INSCRITOS, STR_MATRICULADOS, \
    STR_PRIMER_CURSO


def graficas_comparacion(controlador):
    df_original = controlador.get_df_junto()

    if df_original is not None:

        keyword = st.selectbox("Seleccione la métrica para analizar:",
                               options=[STR_ADMITIDOS, STR_GRADUADOS, STR_INSCRITOS, STR_MATRICULADOS,
                                        STR_PRIMER_CURSO])

        if keyword:
            # Identificar dinámicamente las columnas relevantes para la palabra clave seleccionada
            columnas_relevantes = [col for col in df_original.columns if keyword in col]

            if not columnas_relevantes:
                st.warning(f"No se encontraron datos para '{keyword}'.")
            else:
                # Incluir las columnas clave adicionales
                columnas_relevantes = [STR_CODIGO_SNIES, STR_PROGRAMA_ACADEMICO, STR_NIVEL_FORMACION] + columnas_relevantes
                df_filtrado = df_original[columnas_relevantes]

                # Reorganizar el DataFrame en formato largo
                df_long = pd.melt(
                    df_filtrado,
                    id_vars=[STR_CODIGO_SNIES, STR_PROGRAMA_ACADEMICO, STR_NIVEL_FORMACION],
                    value_vars=columnas_relevantes[3:],
                    var_name=f"AÑO_{keyword}",
                    value_name=keyword
                )

                # Extraer el año del nombre de la columna
                df_long["AÑO"] = df_long[f"AÑO_{keyword}"].str.extract("(\d{4})").astype(int)

                # Eliminar la columna temporal "AÑO_{keyword}"
                df_long.drop(columns=[f"AÑO_{keyword}"], inplace=True)

                # Título de la página
                st.title(f"Comparación de {keyword} entre Años y Tipos de Formación")

                # Selección de tipos de formación
                tipos_formacion = df_long[STR_NIVEL_FORMACION].unique()
                tipos_seleccionados = st.multiselect(
                    "Seleccione los tipos de formación que desea incluir:",
                    options=tipos_formacion,
                    default=tipos_formacion
                )

                # Filtrar el DataFrame según la selección del usuario
                if tipos_seleccionados:
                    df_filtered = df_long[df_long[STR_NIVEL_FORMACION].isin(tipos_seleccionados)]

                    # Crear el gráfico de barras agrupadas
                    fig = px.bar(
                        df_filtered,
                        x="AÑO",
                        y=keyword,
                        color=STR_NIVEL_FORMACION,
                        barmode="group",  # Alternativa: "stack" para barras apiladas
                        labels={
                            "AÑO": "Año",
                            keyword: f"Número de {keyword}",
                            STR_NIVEL_FORMACION: "Tipo de Formación"
                        },
                        title=f"Comparación de {keyword} entre Años por Tipo de Formación"
                    )

                    # Mostrar el gráfico en Streamlit
                    st.plotly_chart(fig, use_container_width=True)
                else:
                    st.warning("Seleccione al menos un tipo de formación para visualizar el gráfico.")
        else:
            st.warning("Seleccione algo.")
    else:
        st.warning("Realiza la búsqueda de los programas que deseas analizar.")


graficas_comparacion(st.session_state.controlador)
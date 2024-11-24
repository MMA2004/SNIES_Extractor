@echo off

REM Activar el entorno virtual si tienes uno
call venv\Scripts\activate.bat
call .venv\Scripts\activate.bat

REM Ejecutar el programa en streamlit
streamlit run app.py
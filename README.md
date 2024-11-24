[![Review Assignment Due Date](https://classroom.github.com/assets/deadline-readme-button-22041afd0340ce965d47ae6ef1cefeee28c7c493a6346c4f15d667ab976d596c.svg)](https://classroom.github.com/a/9bKkctvo)
# snies_proyecto_3
Proyecto_3

```mermaid
classDiagram
direction TB
    sniesController ..> gestorArchivos
    sniesController ..> Utilidad

    class gestorArchivos {
        leer_archivo()
    }
    
    class sniesController {
        DataFrame df
        procesar_datos()
        set_df()
        get_df()
        generar_anios_busqueda()
    }
    
    class Utilidad {
        minusculas_sin_espacio()
        string_to_int()
    }
```
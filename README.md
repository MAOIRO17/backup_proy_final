# backup_proy_final

## Estructura de Datos (HDFS)
Los datos se organizan siguiendo la jerarquía del sistema de archivos distribuido:

* **`smart/`**: Datasets de smartphones extraídos de **PcBox** y **PcComponentes**.
* **`port/`**: Datasets de portátiles procedentes de **Coolmod** y **PcComponentes**.
* **`comp/`**: Datasets de componentes de hardware de **PcComponentes**.
* **`comparaciones/`**: Resultados finales tras aplicar algoritmos de *fuzzy matching*.
* **`dt_kaggle/`**: Datasets de referencia externos (**Kaggle**).

---

## Flujo de trabajo

Los datos almacenados en este repositorio son el resultado de un flujo de trabajo dividido en tres fases principales:

1. **Extracción (Scraping):** Desarrollo de scripts en **Python** (Selenium) encargados de recolectar precios y especificaciones en tiempo real de las distintas tiendas.
2. **Limpieza y Matching:** Implementación de la librería **thefuzz** para realizar un emparejamiento inteligente de cadenas, permitiendo vincular productos idénticos entre tiendas a pesar de variaciones en el nombre.
3. **Procesamiento:** Análisis avanzado de datos mediante **Spark SQL** para la generación de KPIs estratégicos, cálculo de medias por fabricante y algoritmos de detección de anomalías en los precios.

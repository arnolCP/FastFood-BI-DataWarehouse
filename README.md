# Análisis BI de Preferencias del Consumidor de Fast Food

Solución integral de Inteligencia de Negocios (BI) diseñada para analizar la cuota de mercado (Market Share), los índices de satisfacción (CSAT) y los patrones de consumo de franquicias de comida rápida.

## Arquitectura y Tecnologías
*   **Procesamiento de Datos (ELT):** Python (Pandas, Numpy)
*   **Modelado de Datos:** Metodología Hefesto, Esquema Estrella (Star Schema)
*   **Visualización:** Power BI
*   **Fuentes de Datos:** Encuestas de mercado y evaluación de consumidores

## Estructura del Repositorio

### 1. Extracción, Carga y Transformación (ELT)
Se desarrollaron scripts en Python para la limpieza, conversión y estandarización de los datos crudos extraídos de las encuestas.
*   **LIMPIEZA.py:** Script principal para la depuración de datos, tratamiento de valores nulos y normalización de variables.
*   **division.py:** Script para la segmentación de datos y estructuración preliminar de las dimensiones.

### 2. Modelado de Datos (Data Warehouse)
Diseño del modelo multidimensional para optimizar el análisis OLAP, definiendo la tabla de hechos a nivel atómico y sus dimensiones correspondientes.
*   **Modelo_Estrella_BI.xlsx:** Matriz de configuración y diseño lógico del esquema estrella bajo la Metodología Hefesto.
*   **BD_Encuesta_Limpia.xlsx:** Base de datos consolidada, estructurada y lista para la conexión con Power BI.

## Resultados e Insights
El modelo de datos sustenta un dashboard interactivo que permite descubrir insights estratégicos, facilitando el análisis de:
*   Variación de factores decisivos de compra segmentados por perfil demográfico y zona geográfica.
*   Niveles de satisfacción del cliente frente a la competencia directa.
*   Identificación de patrones para recomendaciones accionables de negocio.

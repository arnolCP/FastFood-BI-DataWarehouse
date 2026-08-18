import pandas as pd
import re

# 1. Cargar datos originales
df = pd.read_excel('Test de autoevaluación en blanco (respuestas).xlsx')
df.columns = df.columns.str.strip()

# Renombrar columnas para facilitar el trabajo
col_map = {
    'La presente encuesta tiene fines académicos y es anónima.\n¿Acepta participar?': 'Consentimiento',
    '¿Qué edad tienes?': 'Edad',
    '¿Cuál es tu género?': 'Genero',
    '¿En qué distrito de Lima resides?': 'Distrito',
    '¿Con qué frecuencia consumes comida rápida?': 'Frecuencia',
    '¿Cuál es tu cadena de comida rápida preferida?': 'Marca',
    'Basado en tu experiencia, ¿Cómo calificas los siguientes aspectos de la franquicia que elegiste arriba?   [Precio]': 'Calif_Precio',
    'Basado en tu experiencia, ¿Cómo calificas los siguientes aspectos de la franquicia que elegiste arriba?   [Sabor]': 'Calif_Sabor',
    'Basado en tu experiencia, ¿Cómo calificas los siguientes aspectos de la franquicia que elegiste arriba?   [Rapidez ]': 'Calif_Rapidez',
    'Basado en tu experiencia, ¿Cómo calificas los siguientes aspectos de la franquicia que elegiste arriba?   [Promociones ]': 'Calif_Promociones',
    'Al momento de elegir dónde comer, ¿Cuál de estos factores influye más en tu decisión final?': 'Factor_Decisivo'
}
df = df.rename(columns=col_map)

# 2. Limpieza de datos (ELT)
df = df[df['Consentimiento'] == 'Sí'].copy()
df = df.dropna(subset=['Edad', 'Genero', 'Marca'])

def extract_num(val):
    if pd.isna(val): return None
    match = re.search(r'\d+', str(val))
    return int(match.group()) if match else None

for col in ['Calif_Precio', 'Calif_Sabor', 'Calif_Rapidez', 'Calif_Promociones']:
    df[col] = df[col].apply(extract_num)

df.insert(0, 'id_encuesta', range(1, len(df) + 1))
df['cantidad_respuestas'] = 1

# 3. CREACIÓN DE DIMENSIONES (Asignando un ID único a cada una)
dim_marca = df[['Marca']].drop_duplicates().reset_index(drop=True)
dim_marca.insert(0, 'id_marca', range(1, len(dim_marca) + 1))

dim_zona = df[['Distrito']].drop_duplicates().reset_index(drop=True)
dim_zona.insert(0, 'id_zona', range(1, len(dim_zona) + 1))

dim_cliente = df[['Edad', 'Genero']].drop_duplicates().reset_index(drop=True)
dim_cliente.insert(0, 'id_cliente', range(1, len(dim_cliente) + 1))

dim_factor = df[['Factor_Decisivo']].drop_duplicates().reset_index(drop=True)
dim_factor.insert(0, 'id_factor', range(1, len(dim_factor) + 1))

dim_frecuencia = df[['Frecuencia']].drop_duplicates().reset_index(drop=True)
dim_frecuencia.insert(0, 'id_frecuencia', range(1, len(dim_frecuencia) + 1))

# 4. CREACIÓN DE LA TABLA DE HECHOS (Cruzando los IDs)
fact_df = df.copy()
fact_df = fact_df.merge(dim_marca, on='Marca', how='left')
fact_df = fact_df.merge(dim_zona, on='Distrito', how='left')
fact_df = fact_df.merge(dim_cliente, on=['Edad', 'Genero'], how='left')
fact_df = fact_df.merge(dim_factor, on='Factor_Decisivo', how='left')
fact_df = fact_df.merge(dim_frecuencia, on='Frecuencia', how='left')

# Seleccionar solo las llaves (IDs) y las métricas
fact_encuesta = fact_df[['id_encuesta', 'id_cliente', 'id_zona', 'id_marca', 'id_factor', 'id_frecuencia', 
                         'Calif_Precio', 'Calif_Sabor', 'Calif_Rapidez', 'Calif_Promociones', 'cantidad_respuestas']]

# 5. EXPORTAR A EXCEL (Cada tabla en una pestaña separada)
with pd.ExcelWriter('Modelo_Estrella_BI.xlsx') as writer:
    fact_encuesta.to_excel(writer, sheet_name='FACT_ENCUESTA', index=False)
    dim_cliente.to_excel(writer, sheet_name='DIM_CLIENTE', index=False)
    dim_marca.to_excel(writer, sheet_name='DIM_MARCA', index=False)
    dim_zona.to_excel(writer, sheet_name='DIM_ZONA', index=False)
    dim_factor.to_excel(writer, sheet_name='DIM_FACTOR', index=False)
    dim_frecuencia.to_excel(writer, sheet_name='DIM_FRECUENCIA', index=False)

print("¡Éxito! El archivo Modelo_Estrella_BI.xlsx está listo para descargar.")
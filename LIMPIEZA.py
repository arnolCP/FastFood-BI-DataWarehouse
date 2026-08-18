import pandas as pd
import re

# 1. Cargar el Excel original (Asegúrate de que el nombre coincida con el archivo que subas a Colab)
df = pd.read_excel('Test de autoevaluación en blanco (respuestas).xlsx')

# 2. Limpiar nombres de columnas eliminando espacios en blanco extra
df.columns = df.columns.str.strip()

# Renombrar las columnas para que sean fáciles de usar en Power BI
col_map = {
    'La presente encuesta tiene fines académicos y es anónima.\n¿Acepta participar?': 'Consentimiento',
    '¿Qué edad tienes?': 'Edad',
    '¿Cuál es tu género?': 'Genero',
    '¿En qué distrito de Lima resides?': 'Distrito',
    '¿Con qué frecuencia consumes comida rápida?': 'Frecuencia',
    '¿Cuál es tu cadena de comida rápida preferida?': 'Marca_Preferida',
    'Basado en tu experiencia, ¿Cómo calificas los siguientes aspectos de la franquicia que elegiste arriba?   [Precio]': 'Calif_Precio',
    'Basado en tu experiencia, ¿Cómo calificas los siguientes aspectos de la franquicia que elegiste arriba?   [Sabor]': 'Calif_Sabor',
    'Basado en tu experiencia, ¿Cómo calificas los siguientes aspectos de la franquicia que elegiste arriba?   [Rapidez ]': 'Calif_Rapidez',
    'Basado en tu experiencia, ¿Cómo calificas los siguientes aspectos de la franquicia que elegiste arriba?   [Promociones ]': 'Calif_Promociones',
    'Al momento de elegir dónde comer, ¿Cuál de estos factores influye más en tu decisión final?': 'Factor_Decisivo'
}
df = df.rename(columns=col_map)

# 3. Filtrar encuestados válidos (Consentimiento = Sí) y eliminar nulos críticos
df = df[df['Consentimiento'] == 'Sí'].copy()
df = df.dropna(subset=['Edad', 'Genero', 'Marca_Preferida'])

# 4. Crear una columna 'ID_Encuesta' como Llave Primaria (PK) y limpiar columnas innecesarias
df.insert(0, 'ID_Encuesta', range(1, len(df) + 1))
df = df.drop(columns=['Marca temporal', 'Consentimiento', 'Puntuación'], errors='ignore')

# 5. Transformar calificaciones de texto a números enteros puros
def extraer_numero(val):
    if pd.isna(val): return None
    match = re.search(r'\d+', str(val))
    return int(match.group()) if match else None

columnas_calificacion = ['Calif_Precio', 'Calif_Sabor', 'Calif_Rapidez', 'Calif_Promociones']
for col in columnas_calificacion:
    df[col] = df[col].apply(extraer_numero)

# 6. Exportar el nuevo archivo limpio
df.to_excel('BD_Encuesta_Limpia.xlsx', index=False)
print(f"¡Limpieza completada! Se ha generado un archivo con {len(df)} registros válidos.")
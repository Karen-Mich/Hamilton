import pandas as pd
import numpy as np
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
import pyodbc
from connection import conectar_sql_server
import matplotlib.pyplot as plt

def ejecutar_consulta(query):
    conn = conectar_sql_server()
    df = pd.read_sql(query, conn)
    conn.close()
    return df

query_rentabilidad = """
SELECT p.peliculaID, p.pelicula, p.duracion, p.anioLanzamiento,
       SUM(f.montoTotal) as ingresos_totales,
       COUNT(f.finanzaID) as num_alquileres
FROM dimPeliculas p
JOIN factFinanzas f ON p.peliculaID = f.peliculaID
GROUP BY p.peliculaID, p.pelicula, p.duracion, p.anioLanzamiento
"""
df_rentabilidad = ejecutar_consulta(query_rentabilidad)

# Limpieza y conversión de datos
df_rentabilidad['ingresos_totales'] = pd.to_numeric(df_rentabilidad['ingresos_totales'], errors='coerce')
df_rentabilidad['num_alquileres'] = pd.to_numeric(df_rentabilidad['num_alquileres'], errors='coerce')
df_rentabilidad['duracion'] = pd.to_numeric(df_rentabilidad['duracion'], errors='coerce')
df_rentabilidad['anioLanzamiento'] = pd.to_numeric(df_rentabilidad['anioLanzamiento'], errors='coerce')

# Eliminar filas con valores nulos
df_rentabilidad = df_rentabilidad.dropna(subset=['ingresos_totales', 'num_alquileres', 'duracion', 'anioLanzamiento'])

# Verificar los tipos de datos
print(df_rentabilidad.dtypes)

# Aplicar K-means a rentabilidad
features_rentabilidad = ['ingresos_totales', 'num_alquileres', 'duracion', 'anioLanzamiento']
X_rentabilidad = df_rentabilidad[features_rentabilidad]
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X_rentabilidad)
kmeans = KMeans(n_clusters=3, random_state=42)
df_rentabilidad['cluster'] = kmeans.fit_predict(X_scaled)

print("Análisis de rentabilidad de películas:")
print(df_rentabilidad.groupby('cluster')[features_rentabilidad].mean())

def visualizar_rentabilidad_peliculas(df):
    plt.figure(figsize=(12, 8))
    scatter = plt.scatter(df['ingresos_totales'], df['num_alquileres'], 
                          c=df['cluster'], cmap='viridis', alpha=0.6)
    plt.xlabel('Ingresos Totales')
    plt.ylabel('Número de Alquileres')
    plt.title('Clústeres de Rentabilidad de Películas')
    plt.colorbar(scatter)
    plt.show()

visualizar_rentabilidad_peliculas(df_rentabilidad)
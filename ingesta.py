import pymysql
import pandas as pd
import boto3

# --- Configuración de la base de datos MySQL ---
db_config = {
    'host': '172.31.28.118',
    'user': 'root',
    'password': 'utec',
    'database': 'peliculas_db',
    'port':'8005'
}

# --- Parámetros ---
tabla = 'peliculas'
archivo_csv = 'data.csv'
bucket_s3 = 'peliculas-bucket'

# --- Conectar a MySQL y leer datos ---
try:
    conexion = pymysql.connect(**db_config)
    consulta = f"SELECT * FROM {tabla}"
    df = pd.read_sql(consulta, conexion)
    conexion.close()

    # Guardar como CSV
    df.to_csv(archivo_csv, index=False)
    print(f"Datos exportados a {archivo_csv}")
except Exception as e:
    print("Error al consultar la base de datos:", e)
    exit(1)

# --- Subir a S3 ---
try:
    s3 = boto3.client('s3')
    s3.upload_file(archivo_csv, bucket_s3, archivo_csv)
    print("Archivo subido a S3 exitosamente.")
except Exception as e:
    print("Error al subir a S3:", e)

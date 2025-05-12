import mysql.connector
import pandas as pd
import boto3

# --- Configuración de la base de datos MySQL ---
db_config = {
    'host': '172.31.28.118',  # IP privada de la base de datos
    'user': 'root',
    'password': 'utec',
    'database': 'peliculas_db',
    'port': 8005  # El puerto que estás usando para la conexión
}

# --- Parámetros ---
tabla = 'peliculas'
archivo_csv = 'data.csv'
bucket_s3 = 'peliculas-bucket'

# --- Conectar a MySQL y leer datos ---
try:
    conexion = mysql.connector.connect(**db_config)
    cursor = conexion.cursor()

    # Realizar la consulta SQL para obtener los datos
    consulta = f"SELECT * FROM {tabla}"
    cursor.execute(consulta)

    # Obtener los resultados y los nombres de las columnas
    columnas = [desc[0] for desc in cursor.description]
    resultados = cursor.fetchall()

    # Convertir los resultados a un DataFrame de pandas
    df = pd.DataFrame(resultados, columns=columnas)
    
    # Cerrar el cursor y la conexión
    cursor.close()
    conexion.close()

    # Guardar los datos en un archivo CSV
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


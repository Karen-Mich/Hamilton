import pyodbc

def conectar_sql_server():
    """
    Establece una conexión a SQL Server y retorna el objeto de conexión.
    
    :return: Objeto de conexión de pyodbc o None si falla la conexión.
    """
    # Parámetros de la conexión
    server = 'localhost'
    database = 'pelipickDW22'

    # Cadena de conexión
    connection_string = f'DRIVER={{ODBC Driver 17 for SQL Server}};SERVER={server};DATABASE={database};Trusted_Connection=yes'

    try:
        # Establecer la conexión
        conn = pyodbc.connect(connection_string)
        print("Conexión exitosa a SQL Server")
        return conn

    except Exception as e:
        print(f"Error al conectar a SQL Server: {e}")
        return None

conectar_sql_server()
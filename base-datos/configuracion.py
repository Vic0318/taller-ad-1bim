import os
from dotenv import load_dotenv
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker

# Cargar variables de entorno desde .env si existe
load_dotenv()

# Tipo de base de datos a usar: 'postgres' o 'mariadb'
# Se puede configurar mediante la variable de entorno DB_TIPO (por defecto 'postgres')
DB_TIPO = os.getenv("DB_TIPO", "postgres").lower()

# Configuración de URLs de conexión
POSTGRES_BASE_URL = "postgresql+psycopg2://user:password@127.0.0.1:5434"
POSTGRES_DB_URL = f"{POSTGRES_BASE_URL}/db_universidad"

MARIADB_BASE_URL = "mysql+mysqlconnector://root:rootpassword@127.0.0.1:3308"
MARIADB_DB_URL = f"{MARIADB_BASE_URL}/db_universidad"

def inicializar_base_datos():
    """Crea la base de datos db_universidad si no existe en el motor configurado."""
    if DB_TIPO == "postgres":
        # Conectar a la base de datos default 'postgres' para poder crear db_universidad
        temp_engine = create_engine(f"{POSTGRES_BASE_URL}/postgres", isolation_level="AUTOCOMMIT")
        with temp_engine.connect() as conn:
            # Verificar si existe la base de datos
            result = conn.execute(text("SELECT 1 FROM pg_database WHERE datname='db_universidad'"))
            exists = result.scalar()
            if not exists:
                print("Creando base de datos 'db_universidad' en PostgreSQL...")
                conn.execute(text("CREATE DATABASE db_universidad"))
            else:
                print("La base de datos 'db_universidad' ya existe en PostgreSQL.")
        temp_engine.dispose()
        
    elif DB_TIPO == "mariadb":
        # Conectar al servidor de MariaDB sin especificar base de datos
        temp_engine = create_engine(MARIADB_BASE_URL)
        with temp_engine.connect() as conn:
            print("Creando base de datos 'db_universidad' en MariaDB si no existe...")
            conn.execute(text("CREATE DATABASE IF NOT EXISTS db_universidad"))
        temp_engine.dispose()
    else:
        raise ValueError(f"Motor de base de datos no soportado: {DB_TIPO}")

# Obtener URL correspondiente
if DB_TIPO == "postgres":
    DATABASE_URL = POSTGRES_DB_URL
elif DB_TIPO == "mariadb":
    DATABASE_URL = MARIADB_DB_URL
else:
    raise ValueError(f"Motor de base de datos no soportado: {DB_TIPO}")

# Crear el motor de base de datos definitivo
engine = create_engine(DATABASE_URL)

# Crear fábrica de sesiones
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def obtener_sesion():
    """Retorna una nueva sesión de base de datos."""
    return SessionLocal()

# crear_db.py
from database import engine
from models import Base

print("Conectando con el motor de base de datos...")
# Esta línea obliga a crear las tablas basadas en tus modelos
Base.metadata.create_all(bind=engine)
print("¡Éxito! Base de datos 'nexus_gestion.db' debería existir ahora.")
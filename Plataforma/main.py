from fastapi import FastAPI
from pydantic import BaseModel
from typing import Optional

# 1. Creamos la aplicación
app = FastAPI()

# 2. Definimos cómo es un "Usuario" en nuestra red
class Usuario(BaseModel):
    nombre: str
    especialidad: str  # Ejemplo: "Barbero", "Programador"
    puntos_reputacion: int = 0
    biografia: Optional[str] = None

# 3. Nuestra primera "Ruta" (lo que pasa cuando alguien entra a la app)
@app.get("/")
def inicio():
    return {"mensaje": "Bienvenido a Nexus, la red social del futuro"}

# 4. Ruta para crear un usuario
@app.post("/crear-usuario/")
def crear_usuario(usuario: Usuario):
    return {"status": "Usuario creado con éxito", "datos": usuario}
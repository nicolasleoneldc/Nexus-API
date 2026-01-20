# schemas.py (COMPLETO Y ORDENADO)
from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime

# --- ESQUEMAS DE VISITAS (Primero, porque el cliente las usa) ---
class VisitaCreate(BaseModel):
    tipo_servicio: str
    precio_cobrado: float
    notas_tecnicas: Optional[str] = None

class VisitaResponse(BaseModel):
    id: int
    fecha: datetime
    tipo_servicio: str
    precio_cobrado: float
    notas_tecnicas: Optional[str]
    cliente_id: int
    
    class Config:
        from_attributes = True

# --- ESQUEMAS DE CLIENTES ---
class ClienteCreate(BaseModel):
    nombre: str
    telefono: str
    alias: Optional[str] = None

class ClienteResponse(BaseModel):
    id: int
    nombre: str
    telefono: str
    alias: Optional[str]
    deuda: float
    # AQUÍ ESTÁ LA MAGIA: Incluimos la lista de visitas en la respuesta
    visitas: List[VisitaResponse] = []
    
    class Config:
        from_attributes = True
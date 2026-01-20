# models.py
from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey, Boolean, Text
from sqlalchemy.orm import relationship
from datetime import datetime
from database import Base

class Cliente(Base):
    __tablename__ = "clientes"

    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String, index=True)  # Ej: "Juan Perez"
    telefono = Column(String, unique=True, index=True) # Clave para el Marketing por WhatsApp
    alias = Column(String, nullable=True) # Ej: "El Ruso", "Colo" (Importante para el barrio)
    
    # Datos de negocio
    deuda = Column(Float, default=0.0) # Aquí guardamos si debe plata del fiado
    fecha_creacion = Column(DateTime, default=datetime.utcnow)
    
    # Relación: Un cliente tiene muchas visitas
    visitas = relationship("Visita", back_populates="cliente")

class Visita(Base):
    __tablename__ = "visitas"

    id = Column(Integer, primary_key=True, index=True)
    fecha = Column(DateTime, default=datetime.utcnow) # Cuándo vino
    
    # Relación con Cliente
    cliente_id = Column(Integer, ForeignKey("clientes.id"))
    cliente = relationship("Cliente", back_populates="visitas")
    
    # Detalles del trabajo (La Ficha Técnica)
    tipo_servicio = Column(String) # Ej: "Corte + Barba", "Tinte"
    notas_tecnicas = Column(Text, nullable=True) # Ej: "Usé la 2 al costado, tijera arriba, tiene un remolino atrás"
    precio_cobrado = Column(Float)
    
    # Futuro: Aquí guardaremos la URL de la foto del corte
    foto_url = Column(String, nullable=True)
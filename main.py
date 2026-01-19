from fastapi.responses import RedirectResponse # <--- Importar esto arriba del todo

from fastapi import FastAPI, HTTPException, Depends
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from sqlmodel import SQLModel, Field, Session, create_engine, select
from typing import List, Optional
from passlib.context import CryptContext

# --- 1. CONFIGURACIÓN DE BASE DE DATOS ---
sqlite_file_name = "nexus.db"
sqlite_url = f"sqlite:///{sqlite_file_name}"
connect_args = {"check_same_thread": False}
engine = create_engine(sqlite_url, connect_args=connect_args)

# --- 2. CONFIGURACIÓN DE SEGURIDAD ---
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

app = FastAPI() # (0 con la config de docs_url=None)

# --- 3. MODELOS (TABLAS) ---
class Usuario(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    nombre: str
    especialidad: str
    biografia: str
    password: str

class Publicacion(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    titulo: str
    contenido: str
    usuario_id: int

class Comentario(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    contenido: str
    usuario_id: int
    publicacion_id: int

# --- 4. FUNCIONES AUXILIARES Y DE SEGURIDAD ---

@app.on_event("startup")
def on_startup():
    SQLModel.metadata.create_all(engine)

def get_session():
    with Session(engine) as session:
        yield session

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password):
    return pwd_context.hash(password)

# --- ¡AQUÍ ESTÁ LA FUNCIÓN QUE FALTABA! (Debe ir antes de las rutas) ---
def get_current_user(token: str = Depends(oauth2_scheme), session: Session = Depends(get_session)):
    statement = select(Usuario).where(Usuario.nombre == token)
    user = session.exec(statement).first()
    if not user:
        raise HTTPException(status_code=401, detail="Token inválido o usuario no existe")
    return user

# --- 5. RUTAS (ENDPOINTS) ---

# RUTA DE LOGIN
@app.post("/token")
def login_para_access_token(form_data: OAuth2PasswordRequestForm = Depends(), session: Session = Depends(get_session)):
    statement = select(Usuario).where(Usuario.nombre == form_data.username)
    user = session.exec(statement).first()
    
    if not user or not verify_password(form_data.password, user.password):
        raise HTTPException(status_code=400, detail="Usuario o contraseña incorrectos")
    
    return {"access_token": user.nombre, "token_type": "bearer"}

# CREAR USUARIO
@app.post("/crear-usuario/", response_model=Usuario)
def crear_usuario(usuario: Usuario, session: Session = Depends(get_session)):
    usuario.password = get_password_hash(usuario.password)
    session.add(usuario)
    session.commit()
    session.refresh(usuario)
    return usuario

# PUBLICAR (PROTEGIDO - USA get_current_user)
@app.post("/publicar/", response_model=Publicacion)
def crear_publicacion(
    publicacion: Publicacion, 
    session: Session = Depends(get_session),
    usuario_actual: Usuario = Depends(get_current_user) 
):
    # Asignamos automáticamente el ID del usuario logueado
    publicacion.usuario_id = usuario_actual.id
    session.add(publicacion)
    session.commit()
    session.refresh(publicacion)
    return publicacion

# VER PUBLICACIONES
# --- RUTA RAÍZ (LA PUERTA DE ENTRADA) ---
@app.get("/")
def home():
    # Opción A: Un mensaje JSON simple
    #return {"mensaje": "¡Bienvenido a la API de Nexus! Ve a /docs para usarla."}

    # Opción B (Más pro): Que te redirija directo a la documentación
    return RedirectResponse(url="/docs")

@app.get("/publicaciones/", response_model=List[Publicacion])
def ver_publicaciones(session: Session = Depends(get_session)):
    return session.exec(select(Publicacion)).all()

# COMENTAR
@app.post("/comentar/", response_model=Comentario)
def crear_comentario(comentario: Comentario, session: Session = Depends(get_session)):
    if not session.get(Usuario, comentario.usuario_id):
        raise HTTPException(status_code=404, detail="Usuario autor no encontrado")
    if not session.get(Publicacion, comentario.publicacion_id):
        raise HTTPException(status_code=404, detail="Publicación destino no encontrada")
    
    session.add(comentario)
    session.commit()
    session.refresh(comentario)
    return comentario

# VER COMENTARIOS
@app.get("/publicaciones/{publicacion_id}/comentarios")
def ver_comentarios(publicacion_id: int, session: Session = Depends(get_session)):
    statement = select(Comentario).where(Comentario.publicacion_id == publicacion_id)
    return session.exec(statement).all()

# PERFIL
@app.get("/usuarios/{usuario_id}/publicaciones")
def perfil_usuario(usuario_id: int, session: Session = Depends(get_session)):
    usuario = session.get(Usuario, usuario_id)
    if not usuario:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    
    statement = select(Publicacion).where(Publicacion.usuario_id == usuario_id)
    publicaciones = session.exec(statement).all()
    
    return {
        "usuario": usuario.nombre,
        "total_publicaciones": len(publicaciones),
        "publicaciones": publicaciones
    }


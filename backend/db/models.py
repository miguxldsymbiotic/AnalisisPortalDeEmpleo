from sqlalchemy import Column, Integer, String, Boolean, Text, DateTime, SmallInteger, JSON, func
from sqlalchemy.dialects.postgresql import TSVECTOR
from sqlalchemy.orm import declarative_base

Base = declarative_base()

class ScrapingSession(Base):
    __tablename__ = "scrape_sessions"
    
    id = Column(Integer, primary_key=True, index=True)
    fecha_inicio = Column(DateTime(timezone=True), server_default=func.now())
    pagina_actual = Column(Integer, default=1)
    total_registros = Column(Integer, default=0)
    registros_nuevos = Column(Integer, default=0)
    estado = Column(String(20), default='en_progreso') # 'en_progreso', 'completado', 'error', 'cancelado'

class Vacante(Base):
    __tablename__ = "vacantes"

    id = Column(Integer, primary_key=True, autoincrement=True)
    codigo_vacante = Column(String(50), nullable=False, unique=True, index=True)
    titulo_vacante = Column(String(500))
    descripcion_vacante = Column(Text)
    cargo = Column(String(300))
    nivel_estudios = Column(String(100))
    rango_salarial = Column(String(100))
    tipo_contrato = Column(String(100))
    cantidad_vacantes = Column(SmallInteger, default=1)
    meses_experiencia_cargo = Column(Integer, default=0)
    sector_economico = Column(String(200), index=True)
    departamento = Column(String(100), index=True)
    municipio = Column(String(150))
    fecha_publicacion = Column(DateTime(timezone=True), index=True)
    fecha_vencimiento = Column(DateTime(timezone=True))
    teletrabajo = Column(Boolean, default=False)
    discapacidad = Column(Boolean, default=False)
    hidrocarburos = Column(Boolean, default=False)
    plaza_practica = Column(Boolean, default=False)
    detalles_prestador = Column(JSON, default=list) # Indexing is done manually or using specific operators
    fecha_scraping = Column(DateTime(timezone=True), server_default=func.now())
    search_vector = Column(TSVECTOR) # For full text search

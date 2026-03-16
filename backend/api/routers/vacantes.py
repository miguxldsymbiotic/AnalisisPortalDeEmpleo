from fastapi import APIRouter, Depends, Query, HTTPException, BackgroundTasks
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func, cast, Date
from typing import Optional, List
from datetime import date
from db.session import get_db
from db.models import Vacante

router = APIRouter(prefix="/vacantes", tags=["vacantes"])

@router.get("")
async def list_vacantes(
    pagina: int = Query(1, ge=1),
    por_pagina: int = Query(50, ge=1, le=100),
    departamento: Optional[str] = None,
    sector: Optional[str] = None,
    tipo_contrato: Optional[str] = None,
    nivel_estudios: Optional[str] = None,
    teletrabajo: Optional[bool] = None,
    fecha_desde: Optional[date] = None,
    fecha_hasta: Optional[date] = None,
    db: AsyncSession = Depends(get_db)
):
    stmt = select(Vacante)
    
    if departamento:
        stmt = stmt.where(Vacante.departamento == departamento)
    if sector:
        stmt = stmt.where(Vacante.sector_economico == sector)
    if tipo_contrato:
        stmt = stmt.where(Vacante.tipo_contrato == tipo_contrato)
    if nivel_estudios:
        stmt = stmt.where(Vacante.nivel_estudios == nivel_estudios)
    if teletrabajo is not None:
        stmt = stmt.where(Vacante.teletrabajo == teletrabajo)
    if fecha_desde:
        stmt = stmt.where(cast(Vacante.fecha_publicacion, Date) >= fecha_desde)
    if fecha_hasta:
        stmt = stmt.where(cast(Vacante.fecha_publicacion, Date) <= fecha_hasta)
        
    # Count total
    count_stmt = select(func.count()).select_from(stmt.subquery())
    total_result = await db.execute(count_stmt)
    total = total_result.scalar()
    
    # Pagination
    stmt = stmt.order_by(Vacante.fecha_publicacion.desc())
    stmt = stmt.offset((pagina - 1) * por_pagina).limit(por_pagina)
    
    result = await db.execute(stmt)
    vacantes = result.scalars().all()
    
    return {
        "total": total,
        "pagina": pagina,
        "por_pagina": por_pagina,
        "resultados": vacantes
    }

@router.get("/{codigo}")
async def get_vacante(codigo: str, db: AsyncSession = Depends(get_db)):
    stmt = select(Vacante).where(Vacante.codigo_vacante == codigo)
    result = await db.execute(stmt)
    vacante = result.scalar_one_or_none()
    
    if not vacante:
        raise HTTPException(status_code=404, detail="Vacante no encontrada")
    return vacante

@router.get("/buscar")
async def search_vacantes(q: str = Query(..., min_length=3), db: AsyncSession = Depends(get_db)):
    # Basic ILIKE search since plainto_tsquery needs special raw SQL logic in async SQLAlchemy
    stmt = select(Vacante).where(Vacante.titulo_vacante.ilike(f"%{q}%")).limit(20)
    result = await db.execute(stmt)
    return result.scalars().all()

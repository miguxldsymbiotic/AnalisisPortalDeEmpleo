from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func, case, literal_column
from typing import Optional
from db.session import get_db
from db.models import Vacante

router = APIRouter(prefix="/estadisticas", tags=["estadisticas"])

# ─── ENDPOINTS EXISTENTES ───────────────────────────────────────────────

@router.get("/resumen")
async def get_resumen(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(func.count(Vacante.id), func.sum(Vacante.cantidad_vacantes)))
    total_vacantes, total_plazas = result.one()
    
    # Teletrabajo
    tele_res = await db.execute(select(func.count(Vacante.id)).where(Vacante.teletrabajo == True))
    tele_count = tele_res.scalar()
    
    # Discapacidad
    disc_res = await db.execute(select(func.count(Vacante.id)).where(Vacante.discapacidad == True))
    disc_count = disc_res.scalar()

    # Plaza práctica (jóvenes)
    plaza_res = await db.execute(select(func.count(Vacante.id)).where(Vacante.plaza_practica == True))
    plaza_count = plaza_res.scalar()
    
    return {
        "total_vacantes": total_vacantes or 0,
        "total_plazas": total_plazas or 0,
        "teletrabajo_pct": round((tele_count / total_vacantes) * 100, 1) if total_vacantes else 0,
        "discapacidad_pct": round((disc_count / total_vacantes) * 100, 1) if total_vacantes else 0,
        "plaza_practica_pct": round((plaza_count / total_vacantes) * 100, 1) if total_vacantes else 0,
    }

@router.get("/por-departamento")
async def get_por_departamento(db: AsyncSession = Depends(get_db)):
    stmt = select(Vacante.departamento, func.count(Vacante.id).label("total")).group_by(Vacante.departamento).order_by(func.count(Vacante.id).desc()).limit(10)
    result = await db.execute(stmt)
    return [{"departamento": r.departamento, "total": r.total} for r in result]

@router.get("/por-sector")
async def get_por_sector(db: AsyncSession = Depends(get_db)):
    stmt = select(Vacante.sector_economico, func.count(Vacante.id).label("total")).group_by(Vacante.sector_economico).order_by(func.count(Vacante.id).desc()).limit(10)
    result = await db.execute(stmt)
    return [{"sector": r.sector_economico, "total": r.total} for r in result]
    
@router.get("/por-contrato")
async def get_por_contrato(db: AsyncSession = Depends(get_db)):
    stmt = select(Vacante.tipo_contrato, func.count(Vacante.id).label("total")).group_by(Vacante.tipo_contrato).order_by(func.count(Vacante.id).desc())
    result = await db.execute(stmt)
    return [{"tipo_contrato": r.tipo_contrato, "total": r.total} for r in result]

@router.get("/por-estudios")
async def get_por_estudios(db: AsyncSession = Depends(get_db)):
    stmt = select(Vacante.nivel_estudios, func.count(Vacante.id).label("total")).group_by(Vacante.nivel_estudios).order_by(func.count(Vacante.id).desc())
    result = await db.execute(stmt)
    return [{"nivel_estudios": r.nivel_estudios, "total": r.total} for r in result]
    
@router.get("/salarios")
async def get_salarios(db: AsyncSession = Depends(get_db)):
    stmt = select(Vacante.rango_salarial, func.count(Vacante.id).label("total")).group_by(Vacante.rango_salarial).order_by(func.count(Vacante.id).desc())
    result = await db.execute(stmt)
    return [{"rango": r.rango_salarial, "total": r.total} for r in result]


# ─── NUEVOS ENDPOINTS BID ───────────────────────────────────────────────

@router.get("/territorial")
async def get_territorial(db: AsyncSession = Depends(get_db)):
    """
    Datos por departamento para mapa coroplético del BID.
    Incluye: total vacantes, total plazas, salario predominante, sector top,
    % teletrabajo y % discapacidad por departamento.
    """
    # Total vacantes y plazas por departamento
    base_stmt = (
        select(
            Vacante.departamento,
            func.count(Vacante.id).label("total_vacantes"),
            func.sum(Vacante.cantidad_vacantes).label("total_plazas"),
            func.sum(case((Vacante.teletrabajo == True, 1), else_=0)).label("teletrabajo_count"),
            func.sum(case((Vacante.discapacidad == True, 1), else_=0)).label("discapacidad_count"),
            func.sum(case((Vacante.plaza_practica == True, 1), else_=0)).label("plaza_practica_count"),
        )
        .where(Vacante.departamento.isnot(None))
        .group_by(Vacante.departamento)
        .order_by(func.count(Vacante.id).desc())
    )
    result = await db.execute(base_stmt)
    dept_data = result.all()

    # Salario predominante por departamento
    salary_stmt = (
        select(
            Vacante.departamento,
            Vacante.rango_salarial,
            func.count(Vacante.id).label("cnt"),
        )
        .where(Vacante.departamento.isnot(None))
        .where(Vacante.rango_salarial.isnot(None))
        .group_by(Vacante.departamento, Vacante.rango_salarial)
        .order_by(Vacante.departamento, func.count(Vacante.id).desc())
    )
    sal_result = await db.execute(salary_stmt)
    # Keep only top salary per department
    salary_by_dept = {}
    for r in sal_result:
        if r.departamento not in salary_by_dept:
            salary_by_dept[r.departamento] = r.rango_salarial

    # Sector top por departamento
    sector_stmt = (
        select(
            Vacante.departamento,
            Vacante.sector_economico,
            func.count(Vacante.id).label("cnt"),
        )
        .where(Vacante.departamento.isnot(None))
        .where(Vacante.sector_economico.isnot(None))
        .group_by(Vacante.departamento, Vacante.sector_economico)
        .order_by(Vacante.departamento, func.count(Vacante.id).desc())
    )
    sec_result = await db.execute(sector_stmt)
    sector_by_dept = {}
    for r in sec_result:
        if r.departamento not in sector_by_dept:
            sector_by_dept[r.departamento] = r.sector_economico

    return [
        {
            "departamento": r.departamento,
            "total_vacantes": r.total_vacantes,
            "total_plazas": r.total_plazas or 0,
            "salario_predominante": salary_by_dept.get(r.departamento, "N/A"),
            "sector_top": sector_by_dept.get(r.departamento, "N/A"),
            "teletrabajo_pct": round((r.teletrabajo_count / r.total_vacantes) * 100, 1) if r.total_vacantes else 0,
            "discapacidad_pct": round((r.discapacidad_count / r.total_vacantes) * 100, 1) if r.total_vacantes else 0,
            "plaza_practica_pct": round((r.plaza_practica_count / r.total_vacantes) * 100, 1) if r.total_vacantes else 0,
        }
        for r in dept_data
    ]


@router.get("/inclusion")
async def get_inclusion(db: AsyncSession = Depends(get_db)):
    """
    KPIs de poblaciones vulnerables para el BID.
    Discapacidad, plaza de práctica (jóvenes), desglose territorial y sectorial.
    """
    # Totales generales
    total_res = await db.execute(select(func.count(Vacante.id)))
    total = total_res.scalar() or 0

    disc_res = await db.execute(select(func.count(Vacante.id)).where(Vacante.discapacidad == True))
    disc_total = disc_res.scalar() or 0

    plaza_res = await db.execute(select(func.count(Vacante.id)).where(Vacante.plaza_practica == True))
    plaza_total = plaza_res.scalar() or 0

    # Discapacidad por departamento (top 10)
    disc_dept_stmt = (
        select(
            Vacante.departamento,
            func.count(Vacante.id).label("total"),
        )
        .where(Vacante.discapacidad == True)
        .where(Vacante.departamento.isnot(None))
        .group_by(Vacante.departamento)
        .order_by(func.count(Vacante.id).desc())
        .limit(10)
    )
    disc_dept = await db.execute(disc_dept_stmt)
    disc_por_depto = [{"departamento": r.departamento, "total": r.total} for r in disc_dept]

    # Plaza práctica por departamento (top 10)
    plaza_dept_stmt = (
        select(
            Vacante.departamento,
            func.count(Vacante.id).label("total"),
        )
        .where(Vacante.plaza_practica == True)
        .where(Vacante.departamento.isnot(None))
        .group_by(Vacante.departamento)
        .order_by(func.count(Vacante.id).desc())
        .limit(10)
    )
    plaza_dept = await db.execute(plaza_dept_stmt)
    plaza_por_depto = [{"departamento": r.departamento, "total": r.total} for r in plaza_dept]

    # Discapacidad por sector (top 10)
    disc_sector_stmt = (
        select(
            Vacante.sector_economico,
            func.count(Vacante.id).label("total"),
        )
        .where(Vacante.discapacidad == True)
        .where(Vacante.sector_economico.isnot(None))
        .group_by(Vacante.sector_economico)
        .order_by(func.count(Vacante.id).desc())
        .limit(10)
    )
    disc_sector = await db.execute(disc_sector_stmt)
    disc_por_sector = [{"sector": r.sector_economico, "total": r.total} for r in disc_sector]

    # Plaza práctica por sector (top 10)
    plaza_sector_stmt = (
        select(
            Vacante.sector_economico,
            func.count(Vacante.id).label("total"),
        )
        .where(Vacante.plaza_practica == True)
        .where(Vacante.sector_economico.isnot(None))
        .group_by(Vacante.sector_economico)
        .order_by(func.count(Vacante.id).desc())
        .limit(10)
    )
    plaza_sector = await db.execute(plaza_sector_stmt)
    plaza_por_sector = [{"sector": r.sector_economico, "total": r.total} for r in plaza_sector]

    return {
        "total_vacantes": total,
        "discapacidad": {
            "total": disc_total,
            "porcentaje": round((disc_total / total) * 100, 2) if total else 0,
            "por_departamento": disc_por_depto,
            "por_sector": disc_por_sector,
        },
        "plaza_practica": {
            "total": plaza_total,
            "porcentaje": round((plaza_total / total) * 100, 2) if total else 0,
            "por_departamento": plaza_por_depto,
            "por_sector": plaza_por_sector,
        },
    }


@router.get("/brechas")
async def get_brechas(
    sector: Optional[str] = None,
    db: AsyncSession = Depends(get_db),
):
    """
    Análisis de brechas oferta-demanda para el BID.
    Cruce: nivel_estudios × rango_salarial × experiencia promedio, por sector.
    Identifica vacantes desalineadas.
    """
    stmt = (
        select(
            Vacante.sector_economico,
            Vacante.nivel_estudios,
            Vacante.rango_salarial,
            func.avg(Vacante.meses_experiencia_cargo).label("experiencia_promedio"),
            func.count(Vacante.id).label("total_vacantes"),
            func.sum(Vacante.cantidad_vacantes).label("total_plazas"),
        )
        .where(Vacante.sector_economico.isnot(None))
        .where(Vacante.nivel_estudios.isnot(None))
        .where(Vacante.rango_salarial.isnot(None))
    )

    if sector:
        stmt = stmt.where(Vacante.sector_economico == sector)

    stmt = (
        stmt.group_by(
            Vacante.sector_economico,
            Vacante.nivel_estudios,
            Vacante.rango_salarial,
        )
        .order_by(func.count(Vacante.id).desc())
        .limit(100)
    )

    result = await db.execute(stmt)

    brechas = []
    for r in result:
        brechas.append({
            "sector": r.sector_economico,
            "nivel_estudios": r.nivel_estudios,
            "rango_salarial": r.rango_salarial,
            "experiencia_promedio_meses": round(float(r.experiencia_promedio or 0), 1),
            "total_vacantes": r.total_vacantes,
            "total_plazas": r.total_plazas or 0,
        })

    # Sectores disponibles para filtro
    sectores_stmt = (
        select(Vacante.sector_economico)
        .where(Vacante.sector_economico.isnot(None))
        .group_by(Vacante.sector_economico)
        .order_by(func.count(Vacante.id).desc())
        .limit(20)
    )
    sec_res = await db.execute(sectores_stmt)
    sectores_disponibles = [r[0] for r in sec_res]

    return {
        "brechas": brechas,
        "sectores_disponibles": sectores_disponibles,
        "filtro_sector": sector,
    }

@router.get("/tendencias")
async def get_tendencias(db: AsyncSession = Depends(get_db)):
    """
    Análisis de series de tiempo para el BID.
    Evolución semanal de nuevas vacantes en los últimos 6 meses.
    """
    # Group by week of publication date
    # In PostgreSQL we use date_trunc
    stmt = (
        select(
            func.date_trunc('week', Vacante.fecha_publicacion).label("semana"),
            func.count(Vacante.id).label("total"),
            func.sum(case((Vacante.teletrabajo == True, 1), else_=0)).label("teletrabajo"),
        )
        .where(Vacante.fecha_publicacion.isnot(None))
        .group_by(literal_column("semana"))
        .order_by(literal_column("semana").asc())
    )
    
    result = await db.execute(stmt)
    
    tendencias = []
    for r in result:
        tendencias.append({
            "fecha": r.semana.strftime("%Y-%W"), # Año-Semana
            "total": r.total,
            "teletrabajo": int(r.teletrabajo or 0),
        })
        
    return tendencias


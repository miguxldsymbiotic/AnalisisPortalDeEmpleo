from datetime import datetime

def parse_vacante(data: dict) -> dict:
    try:
        fecha_pub = datetime.fromisoformat(data.get("FECHA_PUBLICACION", "").replace("Z", "+00:00")) if data.get("FECHA_PUBLICACION") else None
    except Exception:
        fecha_pub = None

    try:
        fecha_ven = datetime.fromisoformat(data.get("FECHA_VENCIMIENTO", "").replace("Z", "+00:00")) if data.get("FECHA_VENCIMIENTO") else None
    except Exception:
        fecha_ven = None

    # Handle weird key MESOS_EXPERIENCIA_CARGO instead of MESES_EXPERIENCIA_CARGO (from README)
    meses_exp = data.get("MESOS_EXPERIENCIA_CARGO", 0)
    if meses_exp is None:
         meses_exp = 0

    return {
        "codigo_vacante": str(data.get("CODIGO_VACANTE")),
        "titulo_vacante": data.get("TITULO_VACANTE"),
        "descripcion_vacante": data.get("DESCRIPCION_VACANTE"),
        "cargo": data.get("CARGO"),
        "nivel_estudios": data.get("NIVEL_ESTUDIOS"),
        "rango_salarial": data.get("RANGO_SALARIAL"),
        "tipo_contrato": data.get("TIPO_CONTRATO"),
        "cantidad_vacantes": data.get("CANTIDAD_VACANTES", 1),
        "meses_experiencia_cargo": int(meses_exp),
        "sector_economico": data.get("SECTOR_ECONOMICO"),
        "departamento": data.get("DEPARTAMENTO"),
        "municipio": data.get("MUNICIPIO"),
        "fecha_publicacion": fecha_pub,
        "fecha_vencimiento": fecha_ven,
        "teletrabajo": bool(data.get("TELETRABAJO", 0)),
        "discapacidad": bool(data.get("DISCAPACIDAD", 0)),
        "hidrocarburos": bool(data.get("HIDROCARBUROS", 0)),
        "plaza_practica": bool(data.get("PLAZA_PRACTICA", 0)),
        "detalles_prestador": data.get("DETALLES_PRESTADOR", [])
    }

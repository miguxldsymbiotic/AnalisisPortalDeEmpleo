import os
import datetime
import decimal
import json
import psycopg2
from psycopg2 import extras
from dotenv import load_dotenv

# Configuración de adaptación de tipos para Aiven/Postgres
def adapt_value(v):
    if v is None: return None
    if isinstance(v, (datetime.date, datetime.datetime)):
        return v.isoformat()
    if isinstance(v, decimal.Decimal):
        return float(v)
    if isinstance(v, (dict, list)):
        return json.dumps(v)
    return v

def migrate_definitive():
    load_dotenv('../.env')
    
    # URL Local
    local_url = "postgresql://vacantes_user:cambiame@localhost:5432/vacantes_colombia"
    # URL Aiven (Sincrónico para psycopg2)
    aiven_env = os.getenv("DATABASE_URL", "")
    aiven_url = aiven_env.replace("postgresql+asyncpg://", "postgresql://")
    if "sslmode=" not in aiven_url:
        aiven_url += "?sslmode=require"
    
    print("🚀 Iniciando migración definitiva a Aiven Cloud...")
    
    try:
        conn_l = psycopg2.connect(local_url)
        conn_a = psycopg2.connect(aiven_url)
        cur_l = conn_l.cursor()
        cur_a = conn_a.cursor()
        
        # 1. Obtener columnas (ignorando search_vector por ahora para estabilidad)
        cur_l.execute("SELECT column_name FROM information_schema.columns WHERE table_name = 'vacantes' AND column_name != 'search_vector' ORDER BY ordinal_position")
        cols = [r[0] for r in cur_l.fetchall()]
        col_str = ", ".join(cols)
        
        # 2. Identificar IDs faltantes
        print("🔍 Comparando registros entre Local y Nube...")
        cur_l.execute("SELECT id FROM vacantes")
        local_ids = {r[0] for r in cur_l.fetchall()}
        cur_a.execute("SELECT id FROM vacantes")
        aiven_ids = {r[0] for r in cur_a.fetchall()}
        
        missing = list(local_ids - aiven_ids)
        missing.sort()
        total_missing = len(missing)
        
        print(f"📊 Encontrados {len(local_ids)} locales y {len(aiven_ids)} en la nube.")
        print(f"📥 Registros por subir: {total_missing}")
        
        if total_missing == 0:
            print("✅ ¡La base de datos ya está 100% sincronizada!")
            return

        # 3. Migración en Chunks para evitar saturar la conexión
        batch_size = 500
        for i in range(0, total_missing, batch_size):
            chunk_ids = tuple(missing[i:i+batch_size])
            
            # Obtener datos locales
            if len(chunk_ids) == 1:
                cur_l.execute(f"SELECT {col_str} FROM vacantes WHERE id = %s", (chunk_ids[0],))
            else:
                cur_l.execute(f"SELECT {col_str} FROM vacantes WHERE id IN %s", (chunk_ids,))
            
            rows = cur_l.fetchall()
            adapted_rows = []
            for row in rows:
                adapted_rows.append(tuple(adapt_value(v) for v in row))
            
            # Insertar en Aiven
            try:
                placeholders = ",".join(["%s"] * len(cols))
                # Insertar en Aiven
                extras.execute_values(cur_a, f"INSERT INTO vacantes ({col_str}) VALUES %s ON CONFLICT (codigo_vacante) DO NOTHING", adapted_rows)
                conn_a.commit()
                print(f"✅ Progreso: {min(i + batch_size, total_missing)}/{total_missing} registros procesados.")
            except Exception as e:
                conn_a.rollback()
                print(f"❌ Error en lote {i}: {e}")
                # Si falla el lote, intentar uno por uno en este pequeño grupo
                for row_data in adapted_rows:
                    try:
                        cur_a.execute(f"INSERT INTO vacantes ({col_str}) VALUES ({placeholders}) ON CONFLICT (codigo_vacante) DO NOTHING", row_data)
                        conn_a.commit()
                    except:
                        conn_a.rollback()
        
        print("🏁 Migración DEFINITIVA completada con éxito.")
        
    except Exception as e:
        print(f"💥 ERROR CRÍTICO: {e}")
    finally:
        if 'conn_l' in locals(): conn_l.close()
        if 'conn_a' in locals(): conn_a.close()

if __name__ == "__main__":
    migrate_definitive()

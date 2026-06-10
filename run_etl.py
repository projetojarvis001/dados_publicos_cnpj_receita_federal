import os, sys
from pathlib import Path

sys.path.insert(0, "/mnt/storage/home/wagner/repos/receita_cnpj_etl")

# Carrega .env local sem sobrescrever variaveis ja exportadas pelo ambiente.
try:
    from dotenv import load_dotenv
    load_dotenv(Path(__file__).resolve().parent / ".env", override=False)
except Exception:
    pass

# Defaults nao sensiveis para compatibilidade com execucao manual.
os.environ.setdefault("POSTGRES_HOST", "localhost")
os.environ.setdefault("POSTGRES_PORT", "5432")
os.environ.setdefault("POSTGRES_DB", "cnpj_rf")
os.environ.setdefault("DB_MODEL_COMPANY", "estabelecimentos")
os.environ.setdefault("N_ROWS_CHUNKSIZE", "100000")

# Monkey-patch get_last_ref_date
import src.io.get_last_ref_date as grd
grd.main = lambda: "2026-04-12"
import src.engine.core as core
orig_get_ref = core.get_last_ref_date
core.get_last_ref_date = lambda: "2026-04-12"

print("Iniciando unzip...")
from src.io.unzip import main as unzip
unzip()
print("Unzip completo! Iniciando engine-company...")
from src.engine.company import Company
c = Company(ref_date="2026-04-12")
c.execute()
print("ETL COMPLETO!")

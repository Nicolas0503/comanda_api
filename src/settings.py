import os

from dotenv import load_dotenv


load_dotenv()

# Configuracoes da API
HOST = os.getenv("HOST", "127.0.0.1")
PORT = int(os.getenv("PORT", "8000"))
RELOAD = os.getenv("RELOAD", "true").lower() == "true"

# Configuracoes do banco
DB_DIALECT = os.getenv("DB_DIALECT", "sqlite")
DB_NAME = os.getenv("DB_NAME", "comanda.db")

if DB_DIALECT == "sqlite":
	STR_DATABASE = f"sqlite:///./{DB_NAME}"
else:
	DB_USER = os.getenv("DB_USER", "")
	DB_PASSWORD = os.getenv("DB_PASSWORD", "")
	DB_HOST = os.getenv("DB_HOST", "")
	DB_PORT = os.getenv("DB_PORT", "")
	STR_DATABASE = (
		f"{DB_DIALECT}://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
	)